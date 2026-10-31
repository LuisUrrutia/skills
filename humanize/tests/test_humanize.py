import contextlib
import http.server
import importlib.machinery
import importlib.util
import io
import os
from pathlib import Path
import stat
import sys
import tempfile
import textwrap
import threading
import unittest
from unittest import mock
import urllib.error


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "humanize"
loader = importlib.machinery.SourceFileLoader("humanize", str(SCRIPT))
spec = importlib.util.spec_from_loader("humanize", loader)
humanize = importlib.util.module_from_spec(spec)
loader.exec_module(humanize)

# Answers like llama-server: /health once loaded, /completion with a fixed rewrite.
FAKE_LLAMA_SERVER = textwrap.dedent(f"""\
    #!{sys.executable}
    import http.server, json, sys
    port = int(sys.argv[sys.argv.index("--port") + 1])

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, body):
            data = json.dumps(body).encode()
            self.send_response(200)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            self.reply({{"status": "ok"}})

        def do_POST(self):
            self.rfile.read(int(self.headers["Content-Length"]))
            self.reply({{"content": "local rewrite of 12 engineers", "stop_type": "eos"}})

    http.server.HTTPServer(("127.0.0.1", port), Handler).serve_forever()
""")

BROKEN_LLAMA_SERVER = "#!/bin/sh\necho \"error loading model architecture: unknown model architecture 'gemma4'\"\nexit 1\n"


class RunpodStub:
    """A Runpod /completion endpoint that records the Authorization headers it gets."""

    def __enter__(self):
        auth = self.auth = []

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                self.rfile.read(int(self.headers["Content-Length"]))
                auth.append(self.headers.get("Authorization"))
                data = b'{"content": "runpod rewrite of 12 engineers", "stop_type": "eos"}'
                self.send_response(200)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

        self.server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_port}/completion"
        return self

    def __exit__(self, *exc):
        self.server.shutdown()
        self.server.server_close()


class HumanizeBackendTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.bin = self.tmp / "bin"
        self.bin.mkdir()
        cache = self.tmp / "cache" / "humanize"
        cache.mkdir(parents=True)
        for name, *_ in humanize.LOCAL_QUANTS:
            (cache / name).write_bytes(b"GGUF")
        self.enterContext(mock.patch.dict(os.environ, {
            "PATH": str(self.bin),
            "XDG_CACHE_HOME": str(self.tmp / "cache"),
        }))
        for name in ("RUNPOD_API_KEY", "HUMANIZER_URL"):
            os.environ.pop(name, None)
        # Keeps the developer's fish universal variables and PATH out of the tests.
        self.enterContext(mock.patch.object(humanize, "fish", return_value=""))

    def install(self, name, source):
        path = self.bin / name
        path.write_text(source)
        path.chmod(path.stat().st_mode | stat.S_IEXEC)

    def install_llama_server(self, source):
        self.install("llama-server", source)

    def run_script(self, memory, *args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with (
            mock.patch.object(humanize, "memory_gib", return_value=memory),
            mock.patch.object(sys, "argv", ["humanize", *args]),
            mock.patch.object(sys, "stdin", io.StringIO("Our team of 12 engineers shipped it.")),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            self.assertRaises(SystemExit) as exit,
        ):
            humanize.main()
        return exit.exception.code, stdout.getvalue(), stderr.getvalue()

    def test_runs_the_best_fitting_quantization_locally(self):
        self.install_llama_server(FAKE_LLAMA_SERVER)

        code, out, err = self.run_script((64.0, 0.0))

        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "local rewrite of 12 engineers")
        self.assertIn("running humanizer-12b-Q8_0.gguf locally", err)

    def test_picks_q6_k_when_vram_fits_only_q6_k(self):
        self.install_llama_server(FAKE_LLAMA_SERVER)

        code, _, err = self.run_script((0.0, 12.0))

        self.assertEqual(code, 0)
        self.assertIn("running humanizer-12b-Q6_K.gguf locally", err)

    def test_uses_runpod_when_memory_is_too_small(self):
        self.install_llama_server(FAKE_LLAMA_SERVER)
        with RunpodStub() as runpod:
            os.environ.update(RUNPOD_API_KEY="test-key", HUMANIZER_URL=runpod.url)

            code, out, err = self.run_script((8.0, 0.0))

        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "runpod rewrite of 12 engineers")
        self.assertEqual(runpod.auth, ["Bearer test-key"])
        self.assertIn("too little memory", err)

    def test_falls_back_to_runpod_when_llama_server_cannot_load_the_model(self):
        self.install_llama_server(BROKEN_LLAMA_SERVER)
        with RunpodStub() as runpod:
            os.environ.update(RUNPOD_API_KEY="test-key", HUMANIZER_URL=runpod.url)

            code, out, err = self.run_script((64.0, 0.0))

        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "runpod rewrite of 12 engineers")
        self.assertIn("unknown model architecture 'gemma4'", err)

    def test_falls_back_to_runpod_without_llama_server(self):
        with RunpodStub() as runpod:
            os.environ.update(RUNPOD_API_KEY="test-key", HUMANIZER_URL=runpod.url)

            code, out, err = self.run_script((64.0, 0.0))

        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "runpod rewrite of 12 engineers")
        self.assertIn("llama-server is not installed", err)

    def resume_refused(self, remote_size):
        refused = urllib.error.HTTPError("https://huggingface.co/x", 416, "Range Not Satisfiable", None, None)
        head = mock.MagicMock()
        head.__enter__.return_value.headers = {"Content-Length": str(remote_size)}
        return mock.patch.object(humanize.urllib.request, "urlopen", side_effect=[refused, head])

    def test_keeps_a_complete_download_that_was_never_renamed(self):
        cache = self.tmp / "cache" / "humanize"
        (cache / "humanizer-12b-Q8_0.gguf").rename(cache / "humanizer-12b-Q8_0.gguf.part")

        with self.resume_refused(remote_size=4):
            path = humanize.model_path("humanizer-12b-Q8_0.gguf")

        self.assertEqual(path, cache / "humanizer-12b-Q8_0.gguf")
        self.assertEqual(path.read_bytes(), b"GGUF")

    def test_discards_a_partial_file_larger_than_the_remote_file(self):
        cache = self.tmp / "cache" / "humanize"
        part = cache / "humanizer-12b-Q8_0.gguf.part"
        (cache / "humanizer-12b-Q8_0.gguf").unlink()
        part.write_bytes(b"GGUF stale bytes")

        with self.resume_refused(remote_size=4), self.assertRaises(OSError):
            humanize.model_path("humanizer-12b-Q8_0.gguf")

        self.assertFalse(part.exists())

    def test_ignores_gpus_that_report_no_memory(self):
        self.install("nvidia-smi", "#!/bin/sh\nprintf '[N/A]\\n24576\\n'\n")

        _, vram = humanize.memory_gib()

        self.assertEqual(vram, 24.0)

    def test_treats_a_hanging_probe_as_unavailable(self):
        self.install("slow", "#!/bin/sh\nsleep 5\n")

        self.assertEqual(humanize.probe([str(self.bin / "slow")], timeout=1), "")

    def test_forced_local_backend_fails_instead_of_billing_runpod(self):
        code, out, _ = self.run_script((8.0, 0.0), "--backend", "local")

        self.assertIn("cannot run locally", code)
        self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()
