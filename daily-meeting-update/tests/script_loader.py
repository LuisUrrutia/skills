from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT_DIR / "scripts"


def load_script_module(filename: str):
    script_path = SCRIPTS_DIR / filename
    spec = spec_from_file_location(f"tests_{script_path.stem}", script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load script module: {filename}")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
