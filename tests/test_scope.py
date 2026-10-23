"""Unit tests for full-repository and diff-highlight scan scopes."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from zeromdash.scope import materialize_scan_scope, parse_unified_diff


_DIFF = """\
diff --git a/src/parser.c b/src/parser.c
index 1111111..2222222 100644
--- a/src/parser.c
+++ b/src/parser.c
@@ -10,2 +10,4 @@ static int parse_header(Input *input)
     validate(input);
+    state->enabled = true;
+    parse_payload(input);
     return 0;
diff --git a/src/old.c b/src/new.c
similarity index 90%
rename from src/old.c
rename to src/new.c
@@ -1 +1 @@
-old();
+new();
"""


class ScopeParserTest(unittest.TestCase):
    @staticmethod
    def _git(repo: Path, *args: str) -> str:
        proc = subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise AssertionError(proc.stderr or proc.stdout)
        return proc.stdout.strip()

    def test_parse_unified_diff_extracts_files_hunks_and_symbol_hints(self):
        parsed = parse_unified_diff(_DIFF)

        self.assertEqual(parsed["changed_files"], ["src/parser.c", "src/new.c"])
        self.assertEqual(parsed["totals"]["files"], 2)
        self.assertEqual(parsed["totals"]["hunks"], 2)
        self.assertEqual(parsed["totals"]["added_lines"], 3)
        self.assertEqual(parsed["totals"]["deleted_lines"], 1)
        self.assertEqual(parsed["files"][1]["status"], "renamed")
        self.assertIn("parse_header", parsed["changed_symbols"][0]["symbol_hint"])

    def test_full_scope_preserves_repository_wide_analysis(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            scope_dir = root / "scope"
            repo.mkdir()
            (repo / "README.md").write_text("source")

            scope = materialize_scan_scope(
                scope_dir=scope_dir,
                repo_path=repo,
                mode="full",
            )

            self.assertEqual(scope["mode"], "full")
            self.assertFalse(scope["policy"]["finding_must_intersect_diff"])
            self.assertEqual(scope["changed_files"], [])
            self.assertTrue((scope_dir / "scope.json").is_file())
            self.assertEqual(json.loads((scope_dir / "scope.json").read_text())["mode"], "full")

    def test_diff_scope_validates_against_already_patched_repository(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            scope_dir = root / "scope"
            diff = root / "change.patch"
            (repo / "src").mkdir(parents=True)
            (repo / "src" / "parser.c").write_text("patched parser")
            (repo / "src" / "new.c").write_text("renamed")
            diff.write_text(_DIFF)

            scope = materialize_scan_scope(
                scope_dir=scope_dir,
                repo_path=repo,
                mode="diff",
                diff_file=str(diff),
            )

            self.assertEqual(scope["mode"], "diff")
            self.assertTrue(scope["policy"]["finding_must_intersect_diff"])
            self.assertTrue(scope["patched_repo_validation"]["ok"])
            self.assertEqual(scope["changed_files"], ["src/parser.c", "src/new.c"])
            self.assertEqual((scope_dir / "changes.diff").read_text(), _DIFF)

    def test_diff_scope_reports_missing_non_deleted_patched_path(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            scope_dir = root / "scope"
            diff = root / "change.patch"
            repo.mkdir()
            diff.write_text(_DIFF)

            scope = materialize_scan_scope(
                scope_dir=scope_dir,
                repo_path=repo,
                mode="diff",
                diff_file=str(diff),
            )

            self.assertFalse(scope["patched_repo_validation"]["ok"])
            self.assertEqual(
                scope["patched_repo_validation"]["missing_non_deleted_paths"],
                ["src/parser.c", "src/new.c"],
            )

    def test_diff_git_resolves_refs_checks_out_after_and_materializes_diff(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            scope_dir = root / "scope"
            repo.mkdir()
            self._git(repo, "init")
            self._git(repo, "config", "user.email", "test@example.com")
            self._git(repo, "config", "user.name", "Test User")
            (repo / "parser.c").write_text("int parse(void) { return 0; }\n")
            self._git(repo, "add", "parser.c")
            self._git(repo, "commit", "-m", "before")
            self._git(repo, "tag", "before-tag")
            (repo / "parser.c").write_text("int parse(void) { return unsafe(); }\n")
            self._git(repo, "add", "parser.c")
            self._git(repo, "commit", "-m", "after")
            self._git(repo, "branch", "after-branch")
            after_commit = self._git(repo, "rev-parse", "after-branch")

            scope = materialize_scan_scope(
                scope_dir=scope_dir,
                repo_path=repo,
                mode="diff",
                diff_git="before-tag..after-branch",
            )

            self.assertEqual(scope["git_range"], "before-tag..after-branch")
            self.assertEqual(scope["after_commit"], after_commit)
            self.assertEqual(self._git(repo, "rev-parse", "HEAD"), after_commit)
            self.assertEqual(scope["changed_files"], ["parser.c"])
            self.assertIn("diff --git a/parser.c b/parser.c", (scope_dir / "changes.diff").read_text())
            self.assertTrue(scope["patched_repo_validation"]["ok"])


if __name__ == "__main__":
    unittest.main()
