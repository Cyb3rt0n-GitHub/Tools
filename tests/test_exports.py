import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('exports',Path(__file__).resolve().parents[1]/'scripts/cross-platform/security/compare_exports.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ExportTests(unittest.TestCase):
    def parse(self,text,kind='listeners'):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'export.csv';p.write_text(text,encoding='utf-8')
            return m.read_export(p,kind)
    def test_binding_change_not_hidden(self):
        a,_=self.parse('asset_id,protocol,address,port\nhost,tcp,127.0.0.1,443\n')
        b,_=self.parse('asset_id,protocol,address,port\nhost,tcp,0.0.0.0,443\n')
        r=m.compare(a,b)
        self.assertEqual(len(r['newly_observed']),1);self.assertEqual(len(r['no_longer_observed']),1)
    def test_metadata_change_and_stable_id(self):
        a,_=self.parse('asset_id,finding_id,protocol,port,severity\nhost,scanner:123,host,-,high\n','vulnerabilities')
        b,_=self.parse('asset_id,finding_id,protocol,port,severity\nhost,scanner:123,host,-,critical\n','vulnerabilities')
        r=m.compare(a,b)
        self.assertEqual(r['newly_observed'],[])
        self.assertEqual(r['changed_metadata'][0]['fields']['severity']['after'],'critical')
    def test_ipv6_and_duplicate_normalisation(self):
        a,meta=self.parse('asset_id,protocol,address,port\nhost,TCP,0:0:0:0:0:0:0:1,0443\nhost,tcp,::1,443\n')
        self.assertEqual(meta['exact_duplicates'],1);self.assertEqual(len(a),1)
    def test_conflicting_duplicates_fail(self):
        with self.assertRaises(ValueError):self.parse('asset_id,protocol,address,port,process\nhost,tcp,::1,443,a\nhost,tcp,::1,443,b\n')
    def test_invalid_input_not_empty_baseline(self):
        for text in ['asset_id,port\nhost,443\n','asset_id,protocol,address,port\nhost,tcp,::1,70000\n','asset_id,protocol,address,port\nhost,tcp,::1\n']:
            with self.assertRaises(ValueError):self.parse(text)
    def test_empty_valid_export_keeps_absence_unconfirmed(self):
        a,_=self.parse('asset_id,protocol,address,port\nhost,tcp,::1,443\n')
        b,_=self.parse('asset_id,protocol,address,port\n')
        self.assertEqual(len(m.compare(a,b)['no_longer_observed']),1)
    def test_naive_times_rejected(self):
        with self.assertRaises(SystemExit) as e:
            m.main(['listeners','a','b','--scope-id','lab','--before-at','2026-01-01','--after-at','2026-01-02'])
        self.assertEqual(e.exception.code,2)
