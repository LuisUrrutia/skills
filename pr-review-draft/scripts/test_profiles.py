from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from resolve_profile import ProfileError, resolve_profile

BODY = '# Fixture\n\n## Matches\n\n| Repository | Status |\n| --- | --- |\n| `example-org/api` | current |\n'


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.profiles = Path(self.temp.name)

    def test_exact_target_only_and_case_insensitive(self):
        (self.profiles / 'profile.md').write_text(BODY)

        match = resolve_profile('EXAMPLE-ORG/API', self.profiles)
        other = resolve_profile('example-org/api-fork', self.profiles)

        self.assertEqual(match['status'], 'matched')
        self.assertEqual(other['status'], 'none')

    def test_duplicate_match_is_ambiguous(self):
        for name in ('one.md', 'two.md'):
            (self.profiles / name).write_text(BODY)

        result = resolve_profile('example-org/api', self.profiles)

        self.assertEqual(result['status'], 'ambiguous')
        self.assertEqual(len(result['profiles']), 2)

    def test_missing_default_allows_generic_review(self):
        with patch.dict(os.environ, {'XDG_CONFIG_HOME': str(self.profiles)}):
            self.assertEqual(resolve_profile('example-org/api')['status'], 'none')

    def test_missing_explicit_directory_is_an_error(self):
        with self.assertRaises(ProfileError):
            resolve_profile('example-org/api', self.profiles / 'missing')

    def test_malformed_or_unreadable_profile_is_not_none(self):
        candidate = self.profiles / 'broken.md'
        for content in ('# No matches\n', BODY + '| `example-org/other` | current |\n'):
            candidate.write_text(content)
            with self.assertRaises(ProfileError):
                resolve_profile('example-org/api', self.profiles)
        candidate.unlink()
        candidate.symlink_to(self.profiles / 'missing.md')
        with self.assertRaises(OSError):
            resolve_profile('example-org/api', self.profiles)


if __name__ == '__main__':
    unittest.main()
