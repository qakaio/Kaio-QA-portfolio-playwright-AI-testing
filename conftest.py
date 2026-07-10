import pytest
import os
from helpers.failure_analyzer import FailureAnalyzer


def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "requires_groq: mark test as requiring GROQ_API_KEY")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and analyze failures"""
    outcome = yield
    report = outcome.get_result()

    # Only analyze failures in the call phase (not setup/teardown)
    if report.when == 'call' and report.failed:
        analyzer = FailureAnalyzer()

        failure_data = {
            'title': item.nodeid,
            'status': 'failed',
            'error': {
                'message': str(report.longrepr),
                'stack': str(report.longrepr)
            }
        }

        try:
            analysis = analyzer.analyze_failure(failure_data)
            print('\n🤖 AI Failure Analysis:')
            print(f"Root Cause: {analysis['analysis']['rootCause']}")
            print(f"Solutions: {', '.join(analysis['analysis']['solutions'])}")
        except Exception as e:
            print(f'Failed to analyze test failure: {str(e)}')


def pytest_collection_modifyitems(config, items):
    """Skip Groq-requiring tests if API key not available"""
    if not os.getenv('GROQ_API_KEY'):
        skip_groq = pytest.mark.skip(reason="GROQ_API_KEY not set")
        for item in items:
            if "requires_groq" in item.keywords:
                item.add_marker(skip_groq)