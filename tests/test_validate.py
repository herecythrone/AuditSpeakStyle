"""Regression tests for the static checker, not behavioral tests of the Skill."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('package_validator', ROOT / 'scripts/validate.py')
v = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(v)


def header(name='audit-speak-style', description='审计写作', extra=''):
    return ('---\nname: ' + name + '\ndescription: ' + json.dumps(description, ensure_ascii=False)
            + '\n' + extra + '---\n# Body\n')


class FrontmatterTests(unittest.TestCase):
    def test_valid_subset(self):
        self.assertEqual(v.parse_frontmatter(header())['name'], 'audit-speak-style')

    def test_name_uppercase_rejected(self):
        with self.assertRaises(ValueError):
            v.parse_frontmatter(header(name='AuditSpeakStyle'))

    def test_double_hyphen_rejected(self):
        with self.assertRaises(ValueError):
            v.parse_frontmatter(header(name='audit--speak-style'))

    def test_directory_mismatch_rejected(self):
        with self.assertRaises(ValueError):
            v.parse_frontmatter(header(), expected_name='different-name')

    def test_description_limit(self):
        self.assertEqual(len(v.parse_frontmatter(header(description='字' * 1024))['description']), 1024)
        with self.assertRaises(ValueError):
            v.parse_frontmatter(header(description='字' * 1025))

    def test_description_must_be_nonempty_string(self):
        for value in ['', None, 5, ['not a string']]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                v.parse_frontmatter(header(description=value))

    def test_duplicate_key_rejected(self):
        with self.assertRaises(ValueError):
            v.parse_frontmatter(header(extra='name: audit-speak-style\n'))

    def test_unknown_key_rejected(self):
        with self.assertRaises(ValueError):
            v.parse_frontmatter(header(extra='license: invented\n'))

    def test_unquoted_description_rejected_by_subset(self):
        with self.assertRaises(ValueError):
            v.parse_frontmatter('---\nname: audit-speak-style\ndescription: plain\n---\n')

    def test_bom_and_missing_delimiter_rejected(self):
        for value in ['\ufeff' + header(), '---\nname: audit-speak-style\n']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                v.parse_frontmatter(value)


class LinkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.file = self.root / 'README.md'
        self.file.write_text('# test\n', encoding='utf-8')

    def tearDown(self):
        self.temp.cleanup()

    def test_existing_link(self):
        self.assertEqual(v.link_errors(self.root, self.file, '[self](README.md)'), [])

    def test_broken_link(self):
        self.assertTrue(v.link_errors(self.root, self.file, '[bad](missing.md)'))

    def test_external_and_fragment_links_skipped(self):
        self.assertEqual(v.link_errors(self.root, self.file, '[web](https://example.invalid) [a](#a)'), [])

    def test_escape_rejected(self):
        self.assertTrue(v.link_errors(self.root, self.file, '[bad](../outside.md)'))

    def test_fenced_example_not_treated_as_link(self):
        self.assertEqual(v.link_errors(self.root, self.file, '```text\n[x](missing.md)\n```\n'), [])

    def test_skill_cannot_depend_on_repo_docs(self):
        core = self.root / 'skills/audit-speak-style'
        core.mkdir(parents=True)
        self.assertTrue(v.link_errors(self.root, core / 'SKILL.md', '[bad](../../README.md)'))


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'tests/cases.json').read_text(encoding='utf-8'))

    def test_fixture_schema_and_coverage(self):
        self.assertEqual(v.case_schema_errors(self.data), [])

    def test_duplicate_case_rejected(self):
        self.data['cases'][1]['id'] = self.data['cases'][0]['id']
        self.assertTrue(v.case_schema_errors(self.data))

    def test_missing_acceptance_rejected(self):
        del self.data['cases'][0]['hard_failures']
        self.assertTrue(v.case_schema_errors(self.data))

    def test_missing_required_coverage_rejected(self):
        self.data['cases'] = [c for c in self.data['cases'] if c['category'] != 'adversarial-drift']
        self.assertTrue(v.case_schema_errors(self.data))

    def test_no_trigger_coverage_required(self):
        self.data['cases'] = [c for c in self.data['cases'] if c['trigger'] != 'no']
        self.assertTrue(v.case_schema_errors(self.data))

    def test_fictional_label_required(self):
        self.data['cases'][0]['fictional'] = False
        self.assertTrue(v.case_schema_errors(self.data))

    def test_example_arithmetic_constants(self):
        # Checks these fixture constants, not any generated answer or audit assertion.
        self.assertEqual((Decimal('1200') / Decimal('1000') - 1) * 100, Decimal('20'))
        self.assertEqual(Decimal('25') - Decimal('20'), Decimal('5'))
        self.assertEqual(sum(map(Decimal, ['100', '200', '350'])), Decimal('650'))
        self.assertEqual(Decimal('120') + Decimal('80'), Decimal('200'))


    def test_new_fixture_arithmetic_constants(self):
        # These arithmetic identities mirror the fictional examples; they do not verify business facts.
        self.assertEqual(Decimal('1240') - Decimal('1200'), Decimal('40'))
        self.assertEqual(Decimal('30') + Decimal('10'), Decimal('40'))
        self.assertEqual(Decimal('120') / Decimal('200') * 100, Decimal('60'))
        self.assertEqual(Decimal('20') - Decimal('-100'), Decimal('120'))
        self.assertEqual(14 + 1, 15)


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'README.md').write_text('test\n', encoding='utf-8')
        v.write_manifest(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_roundtrip(self):
        self.assertEqual(v.manifest_errors(self.root), [])

    def test_modified_file_rejected(self):
        (self.root / 'README.md').write_text('changed\n', encoding='utf-8')
        self.assertTrue(v.manifest_errors(self.root))

    def test_extra_file_rejected(self):
        (self.root / 'extra.md').write_text('extra\n', encoding='utf-8')
        self.assertTrue(v.manifest_errors(self.root))

    def test_missing_file_rejected(self):
        (self.root / 'README.md').unlink()
        self.assertTrue(v.manifest_errors(self.root))

    def test_ignored_runtime_directory(self):
        local = self.root / 'local-runs'
        local.mkdir()
        (local / 'output.txt').write_text('local only\n', encoding='utf-8')
        self.assertEqual(v.manifest_errors(self.root), [])

    def test_unsafe_manifest_path_rejected(self):
        (self.root / 'MANIFEST.sha256').write_text('0' * 64 + '  ../outside.md\n', encoding='utf-8')
        self.assertTrue(v.manifest_errors(self.root))


class PrivacyScreenTests(unittest.TestCase):
    def test_credential_shaped_value_rejected(self):
        # Synthetic text only; splitting the prefix avoids embedding a token-shaped literal.
        self.assertTrue(v.privacy_errors('gh' + 'p_' + 'x' * 25))

    def test_checker_source_not_self_flagged(self):
        self.assertEqual(v.privacy_errors((ROOT / 'scripts/validate.py').read_text(encoding='utf-8')), [])

    def test_generic_home_variable_allowed(self):
        self.assertEqual(v.privacy_errors('$HOME/.agents/skills/audit-speak-style'), [])


if __name__ == '__main__':
    unittest.main()
