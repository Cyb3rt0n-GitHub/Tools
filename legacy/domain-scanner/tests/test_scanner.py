import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch, Mock
import subprocess
import dns.exception
import legacy_domain_scanner as scan


class ScannerRegressionTests(unittest.TestCase):
    def test_domain_evidence_stays_separate_and_html_is_escaped(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'domains.txt'
            output = Path(directory) / 'report'
            source.write_text('one.example\ntwo.example\n')
            with patch.object(scan.shutil, 'which', return_value='/fake'), \
                 patch.object(scan, 'perform_ssl_scan', side_effect=lambda d: {'output': d + '<script>bad()</script>', 'error': None}), \
                 patch.object(scan, 'fetch_dns_and_mta_sts_records', return_value={}):
                self.assertEqual(scan.main([str(source), '--output-dir', str(output)]), 0)
            import json
            data = json.loads((output / 'results.json').read_text())
            self.assertEqual([r['tls']['output'] for r in data], ['one.example<script>bad()</script>', 'two.example<script>bad()</script>'])
            html = (output / 'domain_results.html').read_text()
            self.assertNotIn('<script>', html)
            self.assertIn('&lt;script&gt;', html)

    def test_failure_keeps_dns_and_continues(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'domains.txt'
            output = Path(directory) / 'report'
            source.write_text('one.example\ntwo.example\n')
            with patch.object(scan.shutil, 'which', return_value='/fake'), \
                 patch.object(scan, 'perform_ssl_scan', return_value={'output': 'partial', 'error': 'failed'}), \
                 patch.object(scan, 'fetch_dns_and_mta_sts_records', return_value={'SPF': {'records': ['v=spf1 -all'], 'error': None}}) as dns:
                self.assertEqual(scan.main([str(source), '--output-dir', str(output)]), 1)
            self.assertEqual(dns.call_count, 2)
            self.assertIn('v=spf1 -all', (output / 'results.json').read_text())

    def test_timeout_is_failure_with_partial_evidence(self):
        with patch.object(subprocess, 'run', side_effect=subprocess.TimeoutExpired('sslscan', 120, output=b'partial')):
            result = scan.perform_ssl_scan('example.org')
        self.assertEqual(result['output'], 'partial')
        self.assertIn('timed out', result['error'])

    def test_dns_timeout_is_unknown(self):
        with patch.object(scan.dns.resolver, 'Resolver') as factory:
            factory.return_value.resolve.side_effect = dns.exception.Timeout()
            result = scan.fetch_dns_and_mta_sts_records('example.org')
        self.assertTrue(all('unknown' in v['error'] for v in result.values()))
