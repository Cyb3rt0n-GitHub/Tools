import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'ssl_scan_domains.sh'


class ShellRegressionTests(unittest.TestCase):
    def test_failed_scan_retained_and_later_domain_runs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bin_dir = root / 'bin'
            bin_dir.mkdir()
            for name, body in {
                'sslscan': '#!/bin/sh\necho "evidence:$2"\n[ "$2" != "bad.example" ]\n',
                'aha': '#!/bin/sh\ncat "$2"\n',
            }.items():
                tool = bin_dir / name
                tool.write_text(body)
                tool.chmod(0o755)
            source = root / 'domains.txt'
            source.write_text('# comment\n  bad.example\r\n\nok.example')
            output = root / 'results'
            env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ['PATH'])
            result = subprocess.run(['bash', str(SCRIPT), str(source), str(output)], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            text = (output / 'sslscan_results.txt').read_text()
            self.assertIn('SCAN FAILED', text)
            self.assertIn('evidence:ok.example', text)
            self.assertTrue((output / 'sslscan_results.html').exists())
            # Existing runs are refused, never appended or deleted.
            again = subprocess.run(['bash', str(SCRIPT), str(source), str(output)], env=env, capture_output=True)
            self.assertNotEqual(again.returncode, 0)
            self.assertEqual((output / 'sslscan_results.txt').read_text(), text)
