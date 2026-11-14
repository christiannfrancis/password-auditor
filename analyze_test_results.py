import csv
from pathlib import Path


def analyze_results(filename):
    with open(filename, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError('The CSV file is empty.')

        if 'result' in reader.fieldnames:
            tests = [(row.get('test', 'Unnamed test'), row['result'].strip().upper() == 'PASS') for row in reader]
        elif {'expected_passes', 'actual_passes'}.issubset(reader.fieldnames):
            tests = [(row.get('sample_password', 'Unnamed test'), row['expected_passes'].strip() == row['actual_passes'].strip()) for row in reader]
        else:
            raise ValueError('CSV must contain result or expected_passes and actual_passes columns.')

    total = len(tests)
    passed = sum(passed for _, passed in tests)
    failed = total - passed
    percentage = passed / total * 100 if total else 0

    lines = [
        'Password Auditor - Test Summary',
        f'File: {Path(filename).name}',
        f'Total tests: {total}',
        f'Passed: {passed}',
        f'Failed: {failed}',
        f'Pass rate: {percentage:.1f}%',
        '',
        'Failed tests:',
    ]
    failures = [name for name, success in tests if not success]
    lines.extend(f'- {name}' for name in failures) if failures else lines.append('None')
    return '\n'.join(lines)


if __name__ == '__main__':
    for filename in ('test_results.csv', 'week2_test_results.csv'):
        if Path(filename).exists():
            print(analyze_results(filename))
            print()
    filename = 'week2_test_results.csv' if Path('week2_test_results.csv').exists() else 'test_results.csv'
    if Path(filename).exists():
        Path('test_summary.txt').write_text(analyze_results(filename) + '\n', encoding='utf-8')
        print('Saved test_summary.txt')
    else:
        print('No test results CSV found in this folder.')
