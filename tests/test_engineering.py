import importlib.util
import json
from pathlib import Path
import ssl
import tempfile
import unittest
from unittest.mock import patch, MagicMock
ROOT=Path(__file__).resolve().parents[1]/'scripts/cross-platform/security'
def load(name):
    spec=importlib.util.spec_from_file_location(name, ROOT/(name+'.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
manifest,tls=load('evidence_manifest'),load('tls_expiry')
class EngineeringTests(unittest.TestCase):
    def test_manifest_changes_and_incomplete(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'a').write_text('before');a=manifest.snapshot(root)
            (root/'a').write_text('after');(root/'b').write_text('new');b=manifest.snapshot(root)
            self.assertEqual(manifest.compare(a,b)['changed'],['a'])
            self.assertEqual(manifest.compare(a,b)['added'],['b'])
            (root/'a').unlink();c=manifest.snapshot(root)
            self.assertEqual(manifest.compare(b,c)['removed'],['a'])
            c['errors']=[{'path':'a','error':'denied'}]
            self.assertEqual(manifest.compare(b,c)['removed'],[])
            self.assertEqual(manifest.compare(b,c)['missing_unconfirmed'],['a'])
    def test_symlink_and_output_protection(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'source';root.mkdir();(root/'a').write_text('x')
            try:(root/'link').symlink_to(root/'a')
            except OSError:pass
            else:self.assertIn('link',manifest.snapshot(root)['skipped'])
            out=Path(folder)/'manifest.json'
            self.assertEqual(manifest.main(['snapshot',str(root),str(out)]),0)
            with self.assertRaises(SystemExit):manifest.main(['snapshot',str(root),str(out)])
            with self.assertRaises(SystemExit):manifest.main(['snapshot',str(root),str(root/'inside.json')])
    def test_verified_context_sni_and_expiry(self):
        ctx=MagicMock();conn=ctx.wrap_socket.return_value.__enter__.return_value
        conn.getpeercert.side_effect=[{'notAfter':'Jan 01 00:00:00 2099 GMT'},b'leaf']
        conn.version.return_value='TLSv1.3';conn.cipher.return_value=('cipher','TLSv1.3',256);conn.getpeername.return_value=('192.0.2.1',443)
        with patch.object(tls.ssl,'create_default_context',return_value=ctx) as factory,patch.object(tls.socket,'create_connection'):
            r=tls.collect('example.org')
        factory.assert_called_once_with(cafile=None)
        self.assertEqual(ctx.wrap_socket.call_args.kwargs['server_hostname'],'example.org')
        self.assertEqual(r['status'],'ok');self.assertEqual(len(r['leaf_sha256']),64)
    def test_invalid_certificate_unknown(self):
        with patch.object(tls,'collect',side_effect=ssl.SSLCertVerificationError('untrusted')),patch('builtins.print') as output:
            self.assertEqual(tls.main(['example.org']),2)
        self.assertEqual(json.loads(output.call_args.args[0])['status'],'unknown')
