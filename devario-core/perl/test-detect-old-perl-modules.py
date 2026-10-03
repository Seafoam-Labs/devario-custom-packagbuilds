#!/usr/bin/env python3
"""Exercise the installed helper against disposable RLPM records and modules."""
import pathlib
import subprocess
import tempfile
import unittest


class OldModulesTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.base = self.root / "usr/lib/perl5"
        self.db = self.root / "var/lib/shelly/local"
        self.base.mkdir(parents=True)
        self.db.mkdir(parents=True)
        source = pathlib.Path(__file__).with_name("detect-old-perl-modules.sh").read_text()
        self.script = self.root / "hook.sh"
        self.script.write_text(source.replace("'/usr/lib/perl5'", repr(str(self.base)))
                               .replace("'/var/lib/shelly/local'", repr(str(self.db))))

    def module(self, relative):
        path = self.base / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("module fixture\n")
        return path

    def record(self, name, paths, backup=""):
        record = self.db / (name + "-1-1")
        record.mkdir()
        (record / "desc").write_text(f"%NAME%\n{name}\n\n%VERSION%\n1-1\n\n")
        (record / "files").write_text("%FILES%\n" + "\n".join(str(p).lstrip('/') for p in paths)
                                     + "\n\n%BACKUP%\n" + backup + "\n")

    def run_hook(self):
        return subprocess.run(["sh", str(self.script)], text=True, capture_output=True)

    def test_owned_unowned_symlinks_and_current_version(self):
        owned = self.module("5.0/vendor_perl/Owned.pm")
        unowned = self.module("5.0/site_perl/Local module.pm")
        link = self.base / "5.0/site_perl/Broken.pm"
        link.symlink_to("missing.pm")
        current = subprocess.check_output(
            ["perl", "-e", 'printf "%vd", $^V'], text=True).rsplit('.', 1)[0]
        self.module(current + "/Current.pm")
        self.record("perl-owned", [owned.parent, owned])
        self.record("perl-shared", [owned.parent])
        self.record("unrelated", [], backup=str(unowned).lstrip('/'))
        result = self.run_hook()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Rebuild the affected packages: perl-owned perl-shared", result.stdout)
        self.assertIn(str(unowned), result.stdout)
        self.assertIn(str(link), result.stdout)
        self.assertNotIn(str(owned) + "\n", result.stdout)
        self.assertNotIn("Current.pm", result.stdout)
        self.assertNotIn("unrelated", result.stdout)

    def test_missing_database_does_not_mislabel_files_as_unowned(self):
        self.module("5.0/Old.pm")
        self.db.rmdir()
        result = self.run_hook()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ownership could not be checked", result.stdout)
        self.assertNotIn("Files not tracked", result.stdout)

    def test_empty_old_directory_is_quiet(self):
        (self.base / "5.0/empty").mkdir(parents=True)
        result = self.run_hook()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_incomplete_database_is_reported(self):
        self.module("5.0/Old.pm")
        self.record("incomplete", [])
        (self.db / "incomplete-1-1/files").unlink()
        result = self.run_hook()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Cannot read incomplete-1-1/files", result.stderr)


if __name__ == "__main__":
    unittest.main()
