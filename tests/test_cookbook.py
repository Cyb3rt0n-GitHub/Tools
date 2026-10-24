"""Check published recipe syntax and navigation without executing target commands."""
from pathlib import Path
import re
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]
class CookbookChecks(unittest.TestCase):
    def test_recipes_have_sections_and_valid_shell_syntax(self):
        pages=list((ROOT/'docs/cookbook').glob('[0-9]*.md'))
        self.assertEqual(len(pages),21)
        for page in pages:
            text=page.read_text(encoding='utf-8')
            for heading in ['Who','What','Where','When','How','Why','Output and interpretation','Next decision','Limits and recovery','Validation']:
                self.assertIn('## '+heading+'\n',text,page.name)
            for code in re.findall(r'```bash\n(.*?)```',text,re.S):
                result=subprocess.run(['bash','-n'],input=code,text=True,capture_output=True)
                self.assertEqual(result.returncode,0,page.name+': '+result.stderr)
    def test_relative_navigation_resolves(self):
        for page in (ROOT/'docs/cookbook').glob('*.md'):
            for link in re.findall(r'\]\(([^)]+)\)',page.read_text(encoding='utf-8')):
                if '://' not in link:
                    self.assertTrue((page.parent/link.split('#')[0]).exists(),str(page)+': '+link)
