import tempfile
from pathlib import Path
import unittest
from unittest.mock import Mock, patch
import dns.exception
import dns.resolver
import py3dns


class DNSRegressionTests(unittest.TestCase):
    def test_txt_chunks_and_timeout(self):
        resolver = Mock()
        resolver.resolve.return_value = [Mock(strings=[b'v=spf1 ', b'-all'])]
        self.assertEqual(py3dns.lookup_txt('example.org', resolver), (['v=spf1 -all'], None))
        resolver.resolve.side_effect = dns.exception.Timeout()
        records, error = py3dns.lookup_txt('example.org', resolver)
        self.assertEqual(records, [])
        self.assertIn('unknown', error)

    def test_missing_dmarc_does_not_drop_domain_or_repeat_queries(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'domains.txt'
            output = Path(directory) / 'results.txt'
            source.write_text('# comment\nexample.org\n\nexample.org\n')
            with patch.object(py3dns, 'lookup_txt', return_value=([], None)) as lookup:
                py3dns.main([str(source), '--output', str(output)])
            self.assertIn('example.org\nDMARC:', output.read_text())
            self.assertEqual(lookup.call_count, 8)

    def test_invalid_input_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'domains.txt'
            source.write_text('--help\n')
            with self.assertRaises(ValueError):
                py3dns.read_domains(source)

    def test_spf_substring_is_not_matching_policy(self):
        with patch.object(py3dns, 'lookup_txt', return_value=(['unrelated v=spf1', 'v=spf1 -all'], None)):
            self.assertEqual(py3dns.collect_records('example.org', selectors=())["SPF"][0], ['v=spf1 -all'])
