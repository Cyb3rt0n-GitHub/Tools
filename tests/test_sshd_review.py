import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('sshd_review',Path(__file__).resolve().parents[1]/'scripts/cross-platform/security/review_sshd.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
BASE=b'port 22\npermitrootlogin prohibit-password\npasswordauthentication no\n'
class SSHReviewTests(unittest.TestCase):
    def test_unknown_and_context_are_preserved(self):
        r=m.review(BASE+b'authenticationmethods publickey,keyboard-interactive\nlistenaddress [::]:22\nlistenaddress 0.0.0.0:22\n')
        prompts={x['setting']:x for x in r['review_prompts']}
        self.assertEqual(prompts['permitrootlogin']['state'],'review')
        self.assertEqual(prompts['passwordauthentication']['state'],'matches_reference')
        self.assertEqual(prompts['kbdinteractiveauthentication']['state'],'unknown')
        self.assertEqual(len(r['effective_values']['listenaddress']),2)
        self.assertEqual(r['authentication_and_access_context']['authenticationmethods'],['publickey,keyboard-interactive'])
    def test_raw_config_and_empty_input_rejected(self):
        for data in (b'',b'PermitRootLogin no\n',BASE+b'Match User admin\n'):
            with self.assertRaises(ValueError):m.review(data)
    def test_conflicting_values_require_review(self):
        r=m.review(BASE+b'passwordauthentication yes\n')
        self.assertEqual(next(x for x in r['review_prompts'] if x['setting']=='passwordauthentication')['state'],'review')
