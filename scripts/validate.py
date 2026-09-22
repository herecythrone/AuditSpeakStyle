#!/usr/bin/env python3
"""Validate this package, not model behavior. Python standard library only."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path('skills/audit-speak-style/SKILL.md')
IGNORED_DIRS = {'.git', '.venv', 'venv', '__pycache__', '.agents', '.codex',
                '.claude', 'private', 'local-runs'}
IGNORED_NAMES = {'.DS_Store', 'Thumbs.db'}
REQUIRED = {
    'README.md', 'VERSION', '.gitignore', '.gitattributes', 'HANDOFF.md',
    'docs/source-research.md', 'docs/migration.md', 'docs/license-decision.md',
    'docs/validation-report.md', SKILL.as_posix(),
    'skills/audit-speak-style/references/style-principles.md',
    'skills/audit-speak-style/references/auditor-boundaries.md',
    'skills/audit-speak-style/references/scenarios.md',
    'skills/audit-speak-style/references/examples.md',
    'tests/README.md', 'tests/cases.json', 'tests/cases.md',
    'tests/author-review.md', 'tests/test_validate.py', 'scripts/validate.py',
}
REQUIRED.update({
    'ATTRIBUTION.md', 'CHANGELOG.md', 'docs/upstream-review.md',
    'docs/upstream-sources.json', 'docs/adaptation-map.md', 'docs/adaptation-map.json',
    'skills/audit-speak-style/PROVENANCE.md',
    'skills/audit-speak-style/LICENSES/A-market-ecm-lawyer-plugin.txt',
    'skills/audit-speak-style/references/review-method.md',
    'scripts/prepare_eval.py', 'tests/test_traceability.py', 'tests/test_prepare_eval.py',
})
UPSTREAM_COMMIT = '42b295ffbd9a8d7b07eef11ec653c1d375862d13'
UPSTREAM_LICENSE_BLOB = 'fdb09f36c442491f6c69832c67ff09260ecde213'
CORE_CATEGORIES = {
    'minimal-edit', 'no-fabrication', 'sample-scope', 'small-amount',
    'management-attribution', 'legal-no-relabel', 'natural-internal',
    'supported-directness', 'adversarial-drift',
}
# This is a narrow leak screen, not a guarantee that all private content is absent.
LEAK_PATTERN = re.compile(
    r'[A-Za-z]:\\|' + r'/mnt/' + r'data/|' +
    r'ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{24,}'
)


def package_files(root: Path) -> list[Path]:
    """Return release-relevant paths; reject symlinks before reading their bytes."""
    result = []
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue
        if path.name in IGNORED_NAMES or path.suffix in {'.pyc', '.zip'}:
            continue
        if path.is_symlink():
            raise ValueError(f'symlink not allowed: {rel.as_posix()}')
        if path.is_file():
            result.append(path)
    return sorted(result, key=lambda p: p.relative_to(root).as_posix())


def parse_frontmatter(text: str, expected_name: str = 'audit-speak-style') -> dict:
    """Validate the two-key YAML subset used here, not arbitrary YAML syntax."""
    lines = text.splitlines()
    if not lines or lines[0] != '---':
        raise ValueError('frontmatter must start with --- without BOM')
    try:
        end = lines.index('---', 1)
    except ValueError as exc:
        raise ValueError('frontmatter closing delimiter missing') from exc
    data = {}
    for line in lines[1:end]:
        if ': ' not in line:
            raise ValueError('expected key: value in the supported YAML subset')
        key, value = line.split(': ', 1)
        if key not in {'name', 'description'} or key in data:
            raise ValueError(f'unknown or duplicate key: {key}')
        if key == 'description':
            try:
                value = json.loads(value)  # JSON double-quoted scalar is valid YAML.
            except (json.JSONDecodeError, TypeError) as exc:
                raise ValueError('description must be a JSON-quoted YAML string') from exc
        data[key] = value
    if set(data) != {'name', 'description'}:
        raise ValueError('name and description are both required')
    name = data['name']
    if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('invalid lowercase-hyphen name')
    if len(name) > 64 or name != expected_name:
        raise ValueError('name length or directory match is invalid')
    desc = data['description']
    if not isinstance(desc, str) or not 1 <= len(desc) <= 1024:
        raise ValueError('description must contain 1 to 1024 characters')
    return data


def link_errors(root: Path, path: Path, text: str) -> list[str]:
    """Check local Markdown file targets; headings and remote availability are excluded."""
    errors = []
    text = re.sub(r'^```.*?^```\s*$', '', text, flags=re.MULTILINE | re.DOTALL)
    for target in re.findall(r'\[[^\]\n]+\]\(([^)\s]+)\)', text):
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith('#'):
            continue
        raw = unquote(parsed.path)
        if not raw:
            continue
        dest = (path.parent / raw).resolve()
        if not dest.is_relative_to(root.resolve()):
            errors.append(f'local link escapes package: {target}')
        elif not dest.exists():
            errors.append(f'broken local link: {target}')
        elif path.is_relative_to(root / 'skills') and not dest.is_relative_to(root / SKILL.parent):
            errors.append(f'installed skill depends on a file outside its own directory: {target}')
    return errors


def case_schema_errors(data: dict) -> list[str]:
    """Check fixture completeness and coverage labels, never grade answer meaning."""
    errors = []
    cases = data.get('cases', []) if isinstance(data, dict) else []
    if not isinstance(cases, list) or len(cases) < 8:
        return ['at least eight structured cases required']
    ids, categories, excluded = set(), set(), 0
    for item in cases:
        if not isinstance(item, dict):
            errors.append('case must be an object')
            continue
        cid = item.get('id', '')
        if not isinstance(cid, str) or not re.fullmatch(r'T\d{2,}', cid) or cid in ids:
            errors.append(f'invalid or duplicate case id: {cid}')
        ids.add(str(cid))
        for key in ('title', 'category', 'input', 'reference_answer', 'author_review'):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f'{cid}: missing nonempty string {key}')
        for key in ('must_preserve', 'hard_failures'):
            value = item.get(key)
            if not isinstance(value, list) or not value or not all(isinstance(x, str) and x for x in value):
                errors.append(f'{cid}: missing acceptance list {key}')
        if item.get('fictional') is not True:
            errors.append(f'{cid}: fictional label required')
        if item.get('trigger') not in {'yes', 'no', 'partial'}:
            errors.append(f'{cid}: invalid trigger label')
        excluded += item.get('trigger') == 'no'
        category = item.get('category')
        if isinstance(category, str):
            categories.add(category)
    missing = CORE_CATEGORIES - categories
    if missing:
        errors.append('missing required coverage labels: ' + ', '.join(sorted(missing)))
    if excluded < 3:
        errors.append('at least three no-trigger cases required')
    return errors


def privacy_errors(text: str) -> list[str]:
    return ['possible private path or credential-shaped text'] if LEAK_PATTERN.search(text) else []


def write_manifest(root: Path) -> int:
    records = []
    for path in package_files(root):
        rel = path.relative_to(root).as_posix()
        if rel != 'MANIFEST.sha256':
            records.append(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {rel}')
    (root / 'MANIFEST.sha256').write_text('\n'.join(records) + '\n', encoding='utf-8', newline='\n')
    return len(records)


def manifest_errors(root: Path) -> list[str]:
    path = root / 'MANIFEST.sha256'
    if not path.exists():
        return ['MANIFEST.sha256 missing']
    records, errors = {}, []
    for line in path.read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        if not match:
            errors.append('malformed manifest record')
            continue
        digest, name = match.groups()
        rel = Path(name)
        if rel.is_absolute() or '..' in rel.parts or name in records or name == 'MANIFEST.sha256':
            errors.append(f'invalid or duplicate manifest path: {name}')
            continue
        records[name] = digest
    actual = {p.relative_to(root).as_posix(): p for p in package_files(root)
              if p.name != 'MANIFEST.sha256'}
    for name in sorted(set(records) - set(actual)):
        errors.append(f'manifest file missing: {name}')
    for name in sorted(set(actual) - set(records)):
        errors.append(f'file not listed in manifest: {name}')
    for name in sorted(set(actual) & set(records)):
        if hashlib.sha256(actual[name].read_bytes()).hexdigest() != records[name]:
            errors.append(f'hash mismatch: {name}')
    return errors



def git_blob_sha(raw: bytes) -> str:
    """Compute Git's blob identifier for comparison with the retrieved upstream value."""
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def traceability_errors(root: Path) -> tuple[list[str], dict]:
    """Check local source/rule/case links and LICENSE bytes, not source truth or semantics."""
    errors, stats = [], {}
    refs = root / SKILL.parent / 'references'
    rules = set()
    for p in refs.glob('*.md'):
        rules.update(re.findall(r'^#{2,3} ([SBR]\d{2})｜', p.read_text(encoding='utf-8'), re.MULTILINE))
    try:
        ledger = json.loads((root / 'docs/upstream-sources.json').read_text(encoding='utf-8'))
        mapping = json.loads((root / 'docs/adaptation-map.json').read_text(encoding='utf-8'))
        cases = json.loads((root / 'tests/cases.json').read_text(encoding='utf-8'))['cases']
        sources = ledger['sources']
        adaptations = mapping['adaptations']
        if not isinstance(sources, list) or not isinstance(adaptations, list):
            raise ValueError('sources and adaptations must be lists')
        if ledger.get('commit') != UPSTREAM_COMMIT:
            errors.append('upstream commit does not match reviewed snapshot')
        ids, paths = set(), set()
        for source in sources:
            sid, path = source['id'], source['path']
            if not re.fullmatch(r'U\d{2}', sid) or sid in ids:
                errors.append('invalid or duplicate upstream source id: ' + str(sid))
            if path in paths or Path(path).is_absolute() or '..' in Path(path).parts:
                errors.append('duplicate or unsafe upstream source path: ' + str(path))
            ids.add(sid); paths.add(path)
            if not re.fullmatch(r'[0-9a-f]{40}', source.get('blob_sha', '')):
                errors.append('invalid upstream blob sha: ' + sid)
            expected = 'https://github.com/' + ledger['repository'] + '/blob/' + UPSTREAM_COMMIT + '/' + path
            if source.get('url') != expected:
                errors.append('source URL is not pinned to reviewed path: ' + sid)
            for key in ('read_scope', 'observed', 'decision'):
                if not isinstance(source.get(key), str) or not source[key].strip():
                    errors.append('missing source review field: ' + sid + ' ' + key)
        by_case = {c['id']: c for c in cases}
        covered_rules, covered_sources, adaptation_ids = set(), set(), set()
        for a in adaptations:
            if a['id'] in adaptation_ids:
                errors.append('duplicate adaptation id: ' + a['id'])
            adaptation_ids.add(a['id'])
            for key in ('decision', 'upstream', 'adapted'):
                if not isinstance(a.get(key), str) or not a[key].strip():
                    errors.append('missing adaptation text: ' + a['id'] + ' ' + key)
            for sid in a['sources']:
                if sid not in ids:
                    errors.append('unknown source in adaptation: ' + str(sid))
                covered_sources.add(sid)
            for rid in a['rules']:
                if rid not in rules:
                    errors.append('unknown rule in adaptation: ' + str(rid))
                covered_rules.add(rid)
            for cid in a['cases']:
                if cid not in by_case:
                    errors.append('unknown case in adaptation: ' + str(cid))
            if a['rules'] and not a['cases']:
                errors.append('runtime adaptation lacks a behavior fixture: ' + a['id'])
        if ids - covered_sources:
            errors.append('sources without an adaptation disposition: ' + ', '.join(sorted(ids - covered_sources)))
        if rules - covered_rules:
            errors.append('core rules absent from adaptation map: ' + ', '.join(sorted(rules - covered_rules)))
        tested_rules = set()
        for case in cases:
            if not isinstance(case.get('rules'), list) or not case['rules']:
                errors.append('case has no rule links: ' + case['id'])
                continue
            for rid in case['rules']:
                if rid not in rules:
                    errors.append('unknown rule in fixture: ' + str(rid))
                tested_rules.add(rid)
        if rules - tested_rules:
            errors.append('core rules without a fixture: ' + ', '.join(sorted(rules - tested_rules)))
        stats.update(upstream_files_reviewed=len(sources), adaptation_decisions=len(adaptations),
                     core_rule_ids=len(rules))
    except (OSError, KeyError, ValueError, TypeError, AttributeError) as exc:
        errors.append('traceability data invalid: ' + str(exc))
    license_path = root / SKILL.parent / 'LICENSES/A-market-ecm-lawyer-plugin.txt'
    try:
        if git_blob_sha(license_path.read_bytes()) != UPSTREAM_LICENSE_BLOB:
            errors.append('upstream LICENSE bytes differ from reviewed source')
    except OSError:
        errors.append('upstream LICENSE file missing')
    provenance = root / SKILL.parent / 'PROVENANCE.md'
    if not provenance.exists():
        errors.append('installed skill lacks PROVENANCE.md')
    else:
        text = provenance.read_text(encoding='utf-8')
        if UPSTREAM_COMMIT not in text or 'zeweihan and A-market-ecm-lawyer-plugin contributors' not in text:
            errors.append('installed provenance lacks pinned source or copyright')
    # Do not adjudicate or remove a user's pre-existing root project license.
    # This delivery itself omits a root LICENSE; upstream notices are checked above.
    return errors, stats


def validate(root: Path, check_manifest: bool = False) -> tuple[list[str], dict]:
    errors, stats = [], {}
    paths = package_files(root)
    found = {p.relative_to(root).as_posix() for p in paths}
    errors.extend('required file missing: ' + x for x in sorted(REQUIRED - found))
    texts = {}
    for path in paths:
        name = path.relative_to(root).as_posix()
        raw = path.read_bytes()
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            errors.append(f'{name}: not UTF-8 text')
            continue
        texts[name] = text
        if raw.startswith(b'\xef\xbb\xbf') or b'\r' in raw:
            errors.append(f'{name}: expected UTF-8 without BOM and LF line endings')
        errors.extend(f'{name}: {x}' for x in privacy_errors(text))
        if path.suffix == '.md':
            errors.extend(f'{name}: {x}' for x in link_errors(root, path, text))
    if SKILL.as_posix() in texts:
        try:
            metadata = parse_frontmatter(texts[SKILL.as_posix()], SKILL.parent.name)
            stats['description_characters'] = len(metadata['description'])
        except ValueError as exc:
            errors.append(f'{SKILL}: {exc}')
    if 'tests/cases.json' in texts:
        try:
            data = json.loads(texts['tests/cases.json'])
            errors.extend(case_schema_errors(data))
            cases = data.get('cases', [])
            stats['behavior_cases_defined'] = len(cases)
            for c in cases:
                if isinstance(c, dict) and f"## {c.get('id')}｜" not in texts.get('tests/cases.md', ''):
                    errors.append(f"case missing from human-readable cases: {c.get('id')}")
        except (json.JSONDecodeError, AttributeError, TypeError) as exc:
            errors.append(f'cases JSON invalid: {exc}')
    examples = texts.get('skills/audit-speak-style/references/examples.md', '')
    stats['examples_defined'] = len(re.findall(r'^## E\d{2}｜', examples, re.MULTILINE))
    if stats['examples_defined'] < 8 or '虚构教学案例' not in examples:
        errors.append('insufficient examples or missing fictional label')
    for path in (root / SKILL.parent / 'references').rglob('*.md'):
        if '虚构教学案例' not in path.read_text(encoding='utf-8'):
            errors.append(f'{path.relative_to(root)}: fictional-example notice missing')
    trace_errors, trace_stats = traceability_errors(root)
    errors.extend(trace_errors)
    stats.update(trace_stats)
    if check_manifest:
        errors.extend(manifest_errors(root))
    stats['files_checked'] = len(paths)
    stats['markdown_files_checked'] = sum(p.suffix == '.md' for p in paths)
    return errors, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--check-manifest', action='store_true')
    group.add_argument('--write-manifest', action='store_true')
    args = parser.parse_args()
    try:
        # Permit the initial manifest to be created while checking links to it.
        pending_manifest = not (ROOT / 'MANIFEST.sha256').exists()
        errors, stats = validate(ROOT, check_manifest=args.check_manifest)
        if args.write_manifest and pending_manifest:
            errors = [x for x in errors if not x.endswith('broken local link: MANIFEST.sha256')
                      and not x.endswith('broken local link: ../MANIFEST.sha256')]
        if errors:
            print('STATIC VALIDATION FAILED')
            for error in errors:
                print('- ' + error)
            return 1
        if args.write_manifest:
            count = write_manifest(ROOT)
            print(f'Manifest written: {count} file hashes')
        print('STATIC VALIDATION PASSED')
        print(json.dumps(stats, ensure_ascii=False, sort_keys=True))
        print('Scope: package structure and fixtures only; no host or model behavior was tested.')
        return 0
    except (OSError, ValueError) as exc:
        print(f'VALIDATION ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
