"""Offline checks for this repository's deliberately small authoring format.

Not a general YAML parser, model evaluator, or complete privacy detector.
"""
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    'README.md', 'SKILL.md', 'LICENSE', '.gitignore',
    'references/strict-aggregate-selection.md',
    'eval/golden_cases.json', 'eval/results/historical-summary.json',
    'eval/EVIDENCE.md', 'eval/check.py', 'tests/test_check.py',
    'docs/assets/readme/illustration-brief.md',
    'docs/assets/readme/align-me.png',
}
IMAGE_FILES = {'docs/assets/readme/align-me.png'}
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
TAGS = {
    'ordinary-two', 'earned-third', 'exceptional-six', 'high-consequence',
    'premise', 'defer', 'stop', 'correction', 'human-choice', 'read-only',
    'prototype-boundary', 'aggregate-valid', 'aggregate-reject', 'no-authority',
}
# Broad indicators only; human inspection remains mandatory.
PRIVATE = re.compile(
    r'(?:/(?:home|Users)/[^\s/]+|[A-Za-z]:\\Users\\|'
    r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|'
    r'(?:ghp_|github_pat_|sk_live_)[A-Za-z0-9_]{12,}|'
    r'\b[0-9]{17,20}\b|\.hermes/|workspace-config|harness-eval/)',
    re.IGNORECASE,
)


def strings(value):
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, str) and item.strip() for item in value
    )


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('duplicate JSON key')
        value[key] = item
    return value


def reject_constant(value):
    raise ValueError('non-JSON numeric constant')


def exact_json(value, expected):
    return json.dumps(value, sort_keys=True) == json.dumps(expected, sort_keys=True)


def decoded_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from decoded_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from decoded_strings(item)


def png_dimensions(path):
    with path.open('rb') as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != PNG_SIGNATURE or header[12:16] != b'IHDR':
        raise ValueError('invalid PNG header')
    if struct.unpack('>I', header[8:12])[0] != 13:
        raise ValueError('invalid PNG IHDR')
    width, height = struct.unpack('>II', header[16:24])
    if not width or not height:
        raise ValueError('invalid PNG dimensions')
    return width, height


def check(root=ROOT):
    root = Path(root)
    errors = []
    texts = {}
    present = set()
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if relative.parts[0] == '.git':
            continue
        name = relative.as_posix()
        if path.is_symlink():
            errors.append(f'{name}: symlink is not public content')
            continue
        if path.is_dir():
            continue
        if name not in FILES:
            errors.append(f'{name}: unexpected file; review before adding to public set')
            continue
        present.add(name)
        if name in IMAGE_FILES:
            try:
                width, height = png_dimensions(path)
            except (OSError, ValueError) as exc:
                errors.append(f'{name}: invalid PNG ({exc})')
            else:
                if width * 9 != height * 16:
                    errors.append(f'{name}: expected true 16:9 dimensions, got {width}x{height}')
            continue
        try:
            texts[name] = path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            errors.append(f'{name}: unreadable text ({type(exc).__name__})')
    for name in sorted(FILES - present):
        errors.append(f'{name}: missing required file')
    for name, text in texts.items():
        # Checker/test source contains detection patterns, not publication evidence.
        if not name.endswith('.py') and PRIVATE.search(text):
            errors.append(f'{name}: potential private path, identity, or secret')
        if name.endswith('.md'):
            for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^\s)]+)\)', text):
                if target.startswith(('https://', 'http://', '#')):
                    continue
                destination = (root / name).parent / target.split('#')[0]
                if not destination.resolve().is_relative_to(root.resolve()) or not destination.is_file():
                    errors.append(f'{name}: invalid local link {target}')
    skill = texts.get('SKILL.md', '')
    parts = skill.split('---\n', 2)
    fields = {}
    if len(parts) != 3 or parts[0]:
        errors.append('SKILL.md: missing YAML frontmatter delimiters')
    else:
        for line in parts[1].splitlines():
            match = re.fullmatch(r'(name|description|license): ([^\n]+)', line)
            if not match or match[1] in fields:
                errors.append('SKILL.md: use unique plain name/description/license fields')
            else:
                fields[match[1]] = match[2]
        name = fields.get('name', '')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64 or name != root.name:
            errors.append('SKILL.md: invalid name or directory mismatch')
        description = fields.get('description', '')
        if not 1 <= len(description) <= 1024 or ': ' in description or ' #' in description:
            errors.append('SKILL.md: invalid plain description')
        if fields.get('license') != 'MIT':
            errors.append('SKILL.md: expected MIT license')
        if not parts[2].strip():
            errors.append('SKILL.md: missing instructions')
    if len(skill.splitlines()) >= 500:
        errors.append('SKILL.md: exceeds recommended progressive-disclosure size')
    data = {}
    for name in ('eval/golden_cases.json', 'eval/results/historical-summary.json'):
        try:
            data[name] = json.loads(texts.get(name, ''), object_pairs_hook=unique_object, parse_constant=reject_constant)
            if any(PRIVATE.search(s) for s in decoded_strings(data[name])):
                errors.append(f'{name}: potential private decoded JSON content')
        except (ValueError, TypeError):
            errors.append(f'{name}: invalid JSON')
    fixtures = data.get('eval/golden_cases.json', {})
    if not isinstance(fixtures, dict) or fixtures.get('schema_version') != 1 or not isinstance(fixtures.get('cases'), list) or not fixtures['cases']:
        errors.append('golden cases: invalid document')
    else:
        seen, covered = set(), set()
        for case in fixtures['cases']:
            if not isinstance(case, dict):
                errors.append('golden cases: case must be an object')
                continue
            ident = case.get('id')
            if not isinstance(ident, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', ident):
                errors.append('golden cases: invalid id')
            elif ident in seen:
                errors.append('golden cases: duplicate id')
            else:
                seen.add(ident)
            if case.get('provenance') != 'synthetic':
                errors.append('golden cases: only synthetic provenance allowed')
            if not isinstance(case.get('prompt'), str) or not case['prompt'].strip():
                errors.append('golden cases: missing prompt')
            for field in ('expected', 'forbidden', 'tags'):
                if not strings(case.get(field)):
                    errors.append(f'golden cases: invalid {field}')
            if strings(case.get('tags')):
                covered.update(case['tags'])
        if not TAGS <= covered:
            errors.append('golden cases: missing coverage tags ' + ', '.join(sorted(TAGS - covered)))
    history = data.get('eval/results/historical-summary.json', {})
    if isinstance(history, dict) and set(history) != {'schema_version', 'evidence_status', 'current_package_evaluated', 'reports'}:
        errors.append('historical summary: unexpected or missing document fields')
    if not isinstance(history, dict) or history.get('schema_version') != 1 or history.get('evidence_status') != 'historical-only' or history.get('current_package_evaluated') is not False:
        errors.append('historical summary: invalid evidence boundary')
    elif not isinstance(history.get('reports'), list) or len(history['reports']) != 4:
        errors.append('historical summary: expected four accepted reports')
    else:
        ids = set()
        for report in history['reports']:
            if isinstance(report, dict) and set(report) != {'id', 'status', 'scope', 'limitations', 'verified_results'}:
                errors.append('historical summary: unexpected or missing report fields')
            if not isinstance(report, dict) or any(not isinstance(report.get(key), str) or not report[key].strip() for key in ('id', 'status', 'scope', 'limitations')):
                errors.append('historical summary: incomplete report')
            elif not isinstance(report['id'], str) or report['id'] in ids:
                errors.append('historical summary: invalid or duplicate id')
            else:
                ids.add(report['id'])
        indexed = {r['id']: r for r in history['reports'] if isinstance(r, dict) and isinstance(r.get('id'), str)}
        baseline = indexed.get('baseline-comparison', {}).get('verified_results')
        expected_baseline = {
            'candidate_mean': 4.625, 'canonical_mean': 4.133,
            'mapped_outcome_units': {'candidate': 9, 'canonical': 1, 'ties': 2},
        }
        if not exact_json(baseline, expected_baseline):
            errors.append('historical summary: baseline results differ from inspected report')
        rerun = indexed.get('text-first-rerun', {}).get('verified_results', {})
        if not exact_json(rerun, {
            'reviewer_total': 3, 'reviewer_pass': 3, 'reviewer_needs_patch': 0,
            'focus': 'Alignment content remains in assistant text and the clarify tool is out of scope.',
        }):
            errors.append('historical summary: reviewer results differ from inspected report')
        if ids != {'baseline-comparison', 'current-source-archive', 'gen12-14-refinement', 'text-first-rerun'}:
            errors.append('historical summary: report outside accepted set')
        for ident, status in {
            'baseline-comparison': 'complete', 'current-source-archive': 'archive-only',
            'gen12-14-refinement': 'pass', 'text-first-rerun': 'pass',
        }.items():
            if indexed.get(ident, {}).get('status') != status:
                errors.append('historical summary: status differs from inspected report')
        archive = indexed.get('current-source-archive', {}).get('verified_results', {})
        if not exact_json(archive, {
            'evaluation_performed': False,
            'archived_materials': [
                'candidate source snapshot', 'evaluation fixture snapshot',
                'historical generation record', 'canonical comparison snapshot',
            ],
        }):
            errors.append('historical summary: archive is not evaluation evidence')
        refinement = indexed.get('gen12-14-refinement', {}).get('verified_results')
        if not exact_json(refinement, {'generation_outcomes': {'gen12': 'needs-patch', 'gen13': 'pass', 'gen14': 'pass'}, 'final_regression': 'pass'}):
            errors.append('historical summary: refinement results differ from inspected report')
    return errors


if __name__ == '__main__':
    failures = check()
    for failure in failures:
        print('FAIL:', failure)
    if not failures:
        print('PASS: repository structure, synthetic fixture coverage, historical boundaries, and privacy indicators')
        print('LIMIT: no model evaluation or complete semantic/privacy guarantee; manual review required')
    raise SystemExit(bool(failures))
