"""Count listing fields against supplied rules; no platform limits are assumed."""
import argparse
import json
import re
import sys
from pathlib import Path


def check_fields(data):
    if not isinstance(data, dict) or not isinstance(data.get('fields'), list) or not data['fields']:
        raise ValueError('fields must be a non-empty list')
    results, seen = [], set()
    for field in data['fields']:
        if not isinstance(field, dict):
            raise ValueError('each field must be an object')
        name, text, unit = field.get('name'), field.get('text'), field.get('unit', 'chars')
        if not isinstance(name, str) or not name.strip() or name in seen:
            raise ValueError('field names must be non-empty and unique')
        seen.add(name)
        if not isinstance(text, str) or unit not in ('chars', 'utf8_bytes', 'words'):
            raise ValueError(f'{name}: text must be a string and unit must be chars, utf8_bytes or words')
        limits = {key: field[key] for key in ('min', 'max') if key in field}
        for key, value in limits.items():
            if type(value) is not int or value < 0:
                raise ValueError(f'{name}: {key} must be a non-negative integer')
        if 'min' in limits and 'max' in limits and limits['min'] > limits['max']:
            raise ValueError(f'{name}: min exceeds max')
        if limits and (not isinstance(field.get('rule_source'), str) or not field['rule_source'].strip()):
            raise ValueError(f'{name}: limits require rule_source')
        count = len(text) if unit == 'chars' else len(text.encode('utf-8')) if unit == 'utf8_bytes' else len(re.findall(r'\S+', text))
        passed = count >= limits.get('min', 0) and ('max' not in limits or count <= limits['max'])
        results.append(dict(name=name, unit=unit, count=count, limits=limits, rule_source=field.get('rule_source'), status=('pass' if passed else 'fail') if limits else 'counted_only'))
    return {'fields': results, 'limits_passed': all(r['status'] != 'fail' for r in results), 'scope': 'Length checks only; facts and platform acceptance are not validated.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        report = check_fields(json.loads(args.input.read_text(encoding='utf-8-sig')))
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['limits_passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
