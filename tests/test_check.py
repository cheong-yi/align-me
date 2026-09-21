import importlib.util
import json
import struct
import shutil
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('checker', ROOT / 'eval/check.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def png_bytes(width, height):
    def chunk(kind, data):
        return (
            struct.pack('>I', len(data)) + kind + data
            + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
        )

    header = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    pixels = b'\x00' + (b'\x00\x00\x00' * width)
    return (
        b'\x89PNG\r\n\x1a\n'
        + chunk(b'IHDR', header)
        + chunk(b'IDAT', zlib.compress(pixels * height))
        + chunk(b'IEND', b'')
    )


class CheckerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'align-me'
        for name in checker.FILES:
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, destination)

    def mutate_json(self, name, change):
        path = self.root / name
        value = json.loads(path.read_text())
        change(value)
        path.write_text(json.dumps(value))

    def test_clean_tree(self):
        self.assertEqual(checker.check(self.root), [])

    def test_readme_image_requires_png_and_true_ratio(self):
        path = self.root / 'docs/assets/readme/align-me.png'
        path.write_bytes(b'not a png')
        self.assertTrue(any('invalid PNG' in e for e in checker.check(self.root)))
        path.write_bytes(png_bytes(4, 3))
        self.assertTrue(any('true 16:9' in e for e in checker.check(self.root)))
        path.write_bytes(png_bytes(16, 9))
        self.assertEqual(checker.check(self.root), [])

    def test_missing_file(self):
        (self.root / 'LICENSE').unlink()
        self.assertTrue(any('missing required' in e for e in checker.check(self.root)))

    def test_invalid_frontmatter(self):
        path = self.root / 'SKILL.md'
        for old, new in [('name: align-me', 'name: Wrong--Name'), ('license: MIT', 'license: MIT\nlicense: MIT'), ('description: ', 'unknown: ')]:
            with self.subTest(new=new):
                original = path.read_text()
                path.write_text(original.replace(old, new))
                self.assertTrue(checker.check(self.root))
                path.write_text(original)

    def test_directory_mismatch(self):
        renamed = self.root.with_name('different')
        self.root.rename(renamed)
        self.assertTrue(any('directory mismatch' in e for e in checker.check(renamed)))

    def test_broken_and_escaping_links(self):
        path = self.root / 'README.md'
        for target in ('missing.md', '../../outside.md'):
            with self.subTest(target=target):
                path.write_text(f'[link]({target})')
                self.assertTrue(any('invalid local link' in e for e in checker.check(self.root)))

    def test_private_indicators(self):
        path = self.root / 'eval/EVIDENCE.md'
        examples = ['/home/example/private', 'reader@example.invalid', 'ghp_' + 'x' * 30, '1234567890123456789']
        for value in examples:
            with self.subTest(value=value):
                path.write_text(value)
                self.assertTrue(any('potential private' in e for e in checker.check(self.root)))

    def test_unexpected_file_and_symlink(self):
        path = self.root / 'private.log'
        path.write_text('unexpected')
        self.assertTrue(any('unexpected file' in e for e in checker.check(self.root)))
        path.unlink()
        path.symlink_to(self.root / 'README.md')
        self.assertTrue(any('symlink' in e for e in checker.check(self.root)))

    def test_malformed_fixtures(self):
        path = self.root / 'eval/golden_cases.json'
        for value in ('{', '[]', '{"schema_version":1,"cases":[null]}'):
            with self.subTest(value=value):
                path.write_text(value)
                self.assertTrue(checker.check(self.root))

    def test_missing_coverage(self):
        self.mutate_json('eval/golden_cases.json', lambda d: [c.update(tags=['stop']) for c in d['cases']])
        self.assertTrue(any('missing coverage' in e for e in checker.check(self.root)))

    def test_duplicate_id_and_transcript_provenance(self):
        self.mutate_json('eval/golden_cases.json', lambda d: d['cases'].append(dict(d['cases'][0], provenance='transcript')))
        errors = checker.check(self.root)
        self.assertTrue(any('duplicate id' in e for e in errors))
        self.assertTrue(any('synthetic provenance' in e for e in errors))

    def test_no_current_evaluation_claim(self):
        self.mutate_json('eval/results/historical-summary.json', lambda d: d.update(current_package_evaluated=True))
        self.assertTrue(any('evidence boundary' in e for e in checker.check(self.root)))

    def test_missing_historical_limitations(self):
        self.mutate_json('eval/results/historical-summary.json', lambda d: d['reports'][0].pop('limitations'))
        self.assertTrue(any('incomplete report' in e for e in checker.check(self.root)))

    def test_changed_historical_numbers(self):
        self.mutate_json('eval/results/historical-summary.json', lambda d: d['reports'][0]['verified_results'].update(candidate_mean=5))
        self.assertTrue(any('baseline results differ' in e for e in checker.check(self.root)))

    def test_strict_json(self):
        for name in ('eval/golden_cases.json', 'eval/results/historical-summary.json'):
            path = self.root / name
            original = path.read_text()
            for value in ('{"x":NaN}', '{"x":Infinity}', '{"x":1,"x":2}'):
                with self.subTest(name=name, value=value):
                    path.write_text(value)
                    self.assertTrue(any('invalid JSON' in e for e in checker.check(self.root)))
            path.write_text(original)

    def test_encoded_private_data(self):
        path = self.root / 'eval/golden_cases.json'
        value = json.loads(path.read_text())
        value['cases'][0]['prompt'] = r'C:\Users\example\private'
        path.write_text(json.dumps(value))
        self.assertTrue(any('private decoded' in e for e in checker.check(self.root)))
        value['cases'][0]['prompt'] = 'reader@example.invalid'
        encoded = json.dumps(value).replace('@', r'\u0040')
        path.write_text(encoded)
        self.assertTrue(any('private decoded' in e for e in checker.check(self.root)))

    def test_all_historical_result_fields_are_closed(self):
        path = self.root / 'eval/results/historical-summary.json'
        original = json.loads(path.read_text())

        def leaves(value, prefix=()):
            if isinstance(value, dict):
                for key, item in value.items():
                    yield from leaves(item, prefix + (key,))
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    yield from leaves(item, prefix + (index,))
            else:
                yield prefix

        for index, report in enumerate(original['reports']):
            for keys in leaves(report['verified_results']):
                with self.subTest(report=report['id'], field=keys):
                    changed = json.loads(json.dumps(original))
                    cursor = changed['reports'][index]['verified_results']
                    for key in keys[:-1]:
                        cursor = cursor[key]
                    cursor[keys[-1]] = 'unsupported change'
                    path.write_text(json.dumps(changed))
                    self.assertTrue(checker.check(self.root))
            for mode in ('extra', 'missing'):
                with self.subTest(report=report['id'], mode=mode):
                    changed = json.loads(json.dumps(original))
                    results = changed['reports'][index]['verified_results']
                    if mode == 'extra':
                        results['unverified_claim'] = True
                    else:
                        results.pop(next(iter(results)))
                    path.write_text(json.dumps(changed))
                    self.assertTrue(checker.check(self.root))

    def test_archive_and_refinement_claims(self):
        name = 'eval/results/historical-summary.json'
        path = self.root / name
        original = path.read_text()
        mutations = [
            lambda d: d['reports'][1]['verified_results'].update(evaluation_performed=True),
            lambda d: d['reports'][2]['verified_results']['generation_outcomes'].update(gen12='pass'),
            lambda d: d['reports'][2].update(scope=['not a string']),
            lambda d: d['reports'][3].update(status='production-ready'),
        ]
        for change in mutations:
            path.write_text(original)
            self.mutate_json(name, change)
            self.assertTrue(checker.check(self.root))


if __name__ == '__main__':
    unittest.main()
