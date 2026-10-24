"""Validate public mapping examples/navigation, never query a corporate environment."""
import json
from pathlib import Path
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]/'docs/enterprise-mapping'
class MappingDocsTests(unittest.TestCase):
    def test_relative_links(self):
        for page in ROOT.glob('*.md'):
            for link in re.findall(r'\]\(([^)]+)\)',page.read_text(encoding='utf-8')):
                if '://' not in link:
                    self.assertTrue((page.parent/link.split('#')[0]).exists(),str(page)+': '+link)
    def test_example_ids_and_references(self):
        e=json.loads((ROOT/'templates/example-estate.json').read_text())
        self.assertTrue(e['example_only'])
        kinds={'scopes':'scope_id','owners':'owner_id','services':'service_id','assets':'asset_id','interfaces':'interface_id','networks':'network_id','zones':'zone_id','boundaries':'boundary_id','identities':'identity_id','flows':'flow_id','relationships':'relation_id','suppliers':'supplier_id','collections':'collection_id','evidence':'evidence_id','assessments':'assessment_id','issues':'issue_id'}
        ids=[r[key] for collection,key in kinds.items() for r in e[collection]]
        self.assertEqual(len(ids),len(set(ids)))
        refs={'owner_id','asset_id','provider_asset_id','service_id','network_id','zone_id','source_zone_id','destination_zone_id','source_asset_id','destination_asset_id','identity_id','subject_id','from_id','to_id'}
        for collection in kinds:
            for row in e[collection]:
                for key,value in row.items():
                    if key in refs and value is not None:self.assertIn(value,ids,(collection,key,value))
                    if key in ('evidence_ids','boundary_ids'):
                        for ref in value:self.assertIn(ref,ids)
        self.assertEqual(e['assessments'][0]['assessment_status'],'unknown')
        self.assertFalse(e['scopes'][0]['active_tests_authorised'])
    def test_empty_template_has_no_corporate_records(self):
        e=json.loads((ROOT/'templates/estate-register.json').read_text())
        for value in e.values():
            if isinstance(value,list):self.assertEqual(value,[])
