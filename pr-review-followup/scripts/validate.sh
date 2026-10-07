#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd -- "$script_dir/.." && pwd)"
export PYTHONDONTWRITEBYTECODE=1

python3 - "$skill_dir" <<'PY'
import pathlib
import re
import sys
import tomllib

skill = pathlib.Path(sys.argv[1]).resolve()
frontmatter = (skill / 'SKILL.md').read_text().split('---', 2)
assert len(frontmatter) == 3 and not frontmatter[0].strip()
assert re.search(r'^name: pr-review-followup$', frontmatter[1], re.M)
assert re.search(r'^description: \S.+$', frontmatter[1], re.M)
assert 'allow_implicit_invocation: false' in (skill / 'agents/openai.yaml').read_text()
with (skill / 'origin.txt').open('rb') as source:
    dependencies = tomllib.load(source)['dependencies']
assert {d['name'] for d in dependencies if d['required']} == {'pr-review', 'comment-style'}
for path in skill.rglob('*'):
    if path.is_symlink():
        assert path.resolve().is_relative_to(skill), f'escaping package symlink: {path}'
    if not path.is_file():
        continue
    if path.suffix == '.py':
        compile(path.read_text(), str(path), 'exec')
    if path.suffix == '.md':
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' in link or link.startswith('#'):
                continue
            destination = (path.parent / link.split('#')[0]).resolve()
            assert destination.is_relative_to(skill), f'escaping reference: {path}: {link}'
            assert destination.exists(), f'broken reference: {path}: {link}'
print('Package references, explicit-only metadata, provenance and Python syntax passed')
PY
python3 -m unittest discover -s "$script_dir" -p 'test_*.py' -v
printf 'pr-review-followup validation passed\n'
