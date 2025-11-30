import pytest
from helpers.failure_analyzer import FailureAnalyzer


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
