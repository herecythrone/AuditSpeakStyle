"""Regression tests of source mapping and license integrity, not model behavior."""
from __future__ import annotations
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('trace_validator',ROOT/'scripts/validate.py')
v=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(v)

class TraceabilityTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)/'package'
        shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('__pycache__','local-runs'))

    def tearDown(self):
        self.tmp.cleanup()

    def mutate(self,name,fn):
        p=self.root/name
        data=json.loads(p.read_text(encoding='utf-8'))
        fn(data)
        p.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')

    def test_complete_graph(self):
        errors,stats=v.traceability_errors(self.root)
        self.assertEqual(errors,[])
        self.assertEqual(stats['upstream_files_reviewed'],12)
        self.assertEqual(stats['adaptation_decisions'],26)
        self.assertEqual(stats['core_rule_ids'],26)

    def test_unknown_source_rejected(self):
        self.mutate('docs/adaptation-map.json',lambda d:d['adaptations'][0]['sources'].append('U99'))
        self.assertTrue(v.traceability_errors(self.root)[0])

    def test_unknown_rule_rejected(self):
        self.mutate('tests/cases.json',lambda d:d['cases'][0]['rules'].append('S99'))
        self.assertTrue(v.traceability_errors(self.root)[0])

    def test_unknown_case_rejected(self):
        self.mutate('docs/adaptation-map.json',lambda d:d['adaptations'][0]['cases'].append('T99'))
        self.assertTrue(v.traceability_errors(self.root)[0])

    def test_unpinned_source_rejected(self):
        self.mutate('docs/upstream-sources.json',lambda d:d['sources'][0].update(url='https://example.invalid/main'))
        self.assertTrue(v.traceability_errors(self.root)[0])

    def test_review_scope_required(self):
        self.mutate('docs/upstream-sources.json',lambda d:d['sources'][0].update(read_scope=''))
        self.assertTrue(v.traceability_errors(self.root)[0])

    def test_license_exact_blob(self):
        b=(self.root/v.SKILL.parent/'LICENSES/A-market-ecm-lawyer-plugin.txt').read_bytes()
        self.assertEqual(v.git_blob_sha(b),v.UPSTREAM_LICENSE_BLOB)

    def test_modified_license_rejected(self):
        p=self.root/v.SKILL.parent/'LICENSES/A-market-ecm-lawyer-plugin.txt'
        p.write_text(p.read_text(encoding='utf-8')+'changed',encoding='utf-8')
        self.assertTrue(v.traceability_errors(self.root)[0])

    def test_missing_installed_provenance_rejected(self):
        (self.root/v.SKILL.parent/'PROVENANCE.md').unlink()
        self.assertTrue(v.traceability_errors(self.root)[0])

    def test_preexisting_root_license_is_preserved(self):
        path=self.root/'LICENSE'
        path.write_text('User-managed license; not adjudicated by this checker.',encoding='utf-8')
        self.assertEqual(v.traceability_errors(self.root)[0],[])
        self.assertIn('User-managed',path.read_text(encoding='utf-8'))

    def test_rule_without_fixture_rejected(self):
        p=self.root/v.SKILL.parent/'references/style-principles.md'
        p.write_text(p.read_text(encoding='utf-8')+'\n### S99｜Uncovered\n',encoding='utf-8')
        self.assertTrue(v.traceability_errors(self.root)[0])

    def test_duplicate_adaptation_rejected(self):
        self.mutate('docs/adaptation-map.json',lambda d:d['adaptations'].append(d['adaptations'][0]))
        self.assertTrue(v.traceability_errors(self.root)[0])

    def test_malformed_ledger_reported(self):
        (self.root/'docs/upstream-sources.json').write_text('[]',encoding='utf-8')
        self.assertTrue(v.traceability_errors(self.root)[0])

if __name__=='__main__':
    unittest.main()
