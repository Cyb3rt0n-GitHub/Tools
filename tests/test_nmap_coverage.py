import importlib.util
from pathlib import Path
import tempfile
import unittest
spec=importlib.util.spec_from_file_location('coverage_check',Path(__file__).resolve().parents[1]/'scripts/cross-platform/security/check_nmap_coverage.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
XML='''<?xml version="1.0"?><!DOCTYPE nmaprun><nmaprun scanner="nmap" version="synthetic"><scaninfo protocol="tcp" numservices="3" services="22,80,443"/><host><status state="up" reason="user-set"/><address addr="192.0.2.1" addrtype="ipv4"/><ports><extraports state="closed" count="2"/><port protocol="tcp" portid="443"><state state="open"/></port></ports></host><runstats><finished exit="success"/><hosts up="1" down="0" total="1"/></runstats></nmaprun>'''
class CoverageTests(unittest.TestCase):
    def check(self,xml=XML,scope=None,extra=False):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'scan.xml';p.write_text(xml)
            return m.check(scope or {'192.0.2.1'},{22,80,443},[p,p] if extra else [p])
    def test_aggregate_counts_and_user_set_reason(self):
        r=self.check();self.assertEqual(r['status'],'consistent')
        h=r['reports'][0]['hosts'][0]
        self.assertEqual(h['state_counts'],{'closed':2,'open':1});self.assertEqual(h['host_up_reason'],'user-set')
    def test_timeout_and_incomplete_counts(self):
        for xml in (XML.replace('<host>','<host timedout="true">'),XML.replace('count="2"','count="1"'),XML.replace('exit="success"','exit="error"')):
            self.assertEqual(self.check(xml)['status'],'incomplete_or_inconsistent')
    def test_wrong_scope_and_duplicate_batches(self):
        r=self.check(scope={'192.0.2.2'})
        self.assertEqual(r['missing_targets'],['192.0.2.2']);self.assertEqual(r['unexpected_targets'],['192.0.2.1'])
        self.assertEqual(self.check(extra=True)['duplicate_targets'],['192.0.2.1'])
    def test_port_set_and_protocol_mismatch(self):
        for xml in (XML.replace('services="22,80,443"','services="22,80,444"'),XML.replace('protocol="tcp"','protocol="udp"')):
            self.assertEqual(self.check(xml)['status'],'incomplete_or_inconsistent')
    def test_malformed_or_entity_xml_rejected(self):
        for xml in ('<nmaprun>',XML.replace('<!DOCTYPE nmaprun>','<!DOCTYPE nmaprun SYSTEM "file:///etc/passwd">'),XML.replace('<!DOCTYPE nmaprun>','<!DOCTYPE nmaprun [<!ENTITY x "x">]>')):
            with self.assertRaises((ValueError,m.ET.ParseError)):self.check(xml)
    def test_invalid_ports_and_duplicate_targets(self):
        for value in ('0','65536','80-22','tcp:443'):
            with self.assertRaises(ValueError):m.ports(value)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'targets';p.write_text('192.0.2.1\n192.0.2.1\n')
            with self.assertRaises(ValueError):m.targets(p)
    def test_missing_state_and_summary_are_not_success(self):
        for xml in (XML.replace('<state state="open"/>',''),XML.replace('total="1"','total="2"')):
            self.assertEqual(self.check(xml)['status'],'incomplete_or_inconsistent')
