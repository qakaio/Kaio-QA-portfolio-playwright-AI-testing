#!/usr/bin/env python3
"""
AI Testing Showcase Runner
Runs all tests and generates a comprehensive report
"""

from datetime import datetime
import subprocess


def print_banner(text):
    """Print a formatted banner"""
    print('\n' + '='*70)
    print(f'  {text}')
    print('='*70 + '\n')


def run_tests():
    """Run all test suites"""
    print_banner('🚀 PLAYWRIGHT AI TESTING FRAMEWORK SHOWCASE')

    print(f'Started at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')

    test_suites = [
        ('AI Features Showcase', 'tests/test_ai_features_showcase.py'),
        ('Login Tests', 'tests/test_saucedemo_login.py'),
        ('Shopping Flow Tests', 'tests/test_saucedemo_shopping.py'),
    ]

    results = []

    for suite_name, test_path in test_suites:
        print_banner(f'Running: {suite_name}')

        try:
            result = subprocess.run(
                ['pytest', test_path, '-v', '-s'],
                capture_output=False,
                text=True
            )

            status = '✅ PASSED' if result.returncode == 0 else '❌ FAILED'
            results.append((suite_name, status))

        except Exception as e:
            print(f'Error running {suite_name}: {e}')
            results.append((suite_name, '❌ ERROR'))

    # Print summary
    print_banner('📊 TEST EXECUTION SUMMARY')

    for suite_name, status in results:
        print(f'  {status} - {suite_name}')

    print(f'\nCompleted at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('\n' + '='*70 + '\n')


if __name__ == '__main__':
    run_tests()