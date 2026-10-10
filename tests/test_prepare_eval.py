"""Test answer-free export and no-overwrite behavior; no models are invoked."""
from __future__ import annotations
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('eval_export',ROOT/'scripts/prepare_eval.py')
p=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(p)

class ExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.out=Path(self.tmp.name)/'export'
        self.stats=p.prepare_eval(ROOT,self.out)

    def tearDown(self):
        self.tmp.cleanup()

    def rows(self,name):
        return [json.loads(x) for x in (self.out/name).read_text(encoding='utf-8').splitlines()]

    def test_counts_and_no_model_calls(self):
        self.assertEqual(self.stats,{'explicit_inputs':53,'implicit_inputs':56,'model_calls':0})

    def test_only_id_and_input_exported(self):
        for name in ('explicit-inputs.jsonl','implicit-routing-inputs.jsonl'):
            for row in self.rows(name):
                self.assertEqual(set(row),{'id','input'})

    def test_no_trigger_cases_excluded_from_explicit_set(self):
        ids={r['id'] for r in self.rows('explicit-inputs.jsonl')}
        self.assertFalse(ids & {'T23','T24','T25'})
        self.assertIn('T26',ids)

    def test_installed_skill_carries_license_and_provenance(self):
        skill=self.out/'skill/audit-speak-style'
        for name in ('SKILL.md','PROVENANCE.md','LICENSES/A-market-ecm-lawyer-plugin.txt'):
            self.assertEqual((skill/name).read_bytes(),(ROOT/'skills/audit-speak-style'/name).read_bytes())

    def test_run_logs_are_unrun_and_empty(self):
        for row in self.rows('run-log-template.jsonl'):
            self.assertEqual(row['status'],'not_run')
            self.assertEqual(row['actual_output'],'')

    def test_existing_destination_preserved(self):
        sentinel=self.out/'sentinel.txt'
        sentinel.write_text('keep',encoding='utf-8')
        with self.assertRaises(FileExistsError):
            p.prepare_eval(ROOT,self.out)
        self.assertEqual(sentinel.read_text(encoding='utf-8'),'keep')

    def test_fixture_answers_absent_from_jsonl_fields(self):
        for name in ('explicit-inputs.jsonl','implicit-routing-inputs.jsonl','run-log-template.jsonl'):
            for row in self.rows(name):
                self.assertFalse(set(row)&{'reference_answer','must_preserve','hard_failures','author_review','trigger'})

    def test_inputs_unchanged(self):
        original=json.loads((ROOT/'tests/cases.json').read_text(encoding='utf-8'))['cases']
        self.assertEqual(self.rows('implicit-routing-inputs.jsonl'),[{'id':c['id'],'input':c['input']} for c in original])

if __name__=='__main__':
    unittest.main()
