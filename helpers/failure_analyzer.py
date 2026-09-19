import json
from datetime import datetime, timezone
from pathlib import Path

from helpers.ai_client import AIClient


class FailureAnalyzer:
    """AI-powered test failure analyzer"""

    def __init__(self):
        self.ai_client: AIClient | None
        try:
            self.ai_client = AIClient()
        except RuntimeError:
            self.ai_client = None

    def analyze_failure(self, test_result: dict) -> dict:
        """
        Analyze test failure and generate insights

        Args:
            test_result: Test result dictionary with title, error, status

        Returns:
            Analysis report dictionary
        """
        title = test_result.get('title', 'Unknown test')
        error = test_result.get('error', {})
        status = test_result.get('status', 'unknown')

        error_message = str(error.get('message', 'Unknown error'))
        stack_trace = str(error.get('stack', 'No stack trace'))

        prompt = f"""
Analyze this test failure:

Test: {title}
Status: {status}
Error: {error_message}
Stack: {stack_trace}

Provide:
1. Root cause analysis
2. Possible solutions
3. Prevention strategies

Format as JSON:
{{
  "rootCause": "...",
  "solutions": ["...", "..."],
  "prevention": ["...", "..."]
}}"""

        system_prompt = 'You are an expert QA engineer analyzing test failures. Provide actionable insights.'

        if self.ai_client is None:
            return {
                'test': title,
                'status': status,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'analysis': {
                    'rootCause': 'Analysis unavailable because GROQ_API_KEY is not configured.',
                    'solutions': ['Set GROQ_API_KEY and rerun the test to enable AI failure analysis.'],
                    'prevention': ['Keep the credential in a local .env file and do not commit it.'],
                },
                'error': error_message,
            }

        try:
            response = self.ai_client.query(
                prompt,
                system_prompt=system_prompt,
                temperature=0.6,
                max_tokens=800
            )

            # Try to parse JSON, handle markdown code blocks
            response_clean = response.strip()
            response_clean = response_clean.removeprefix('```json')
            response_clean = response_clean.removeprefix('```')
            response_clean = response_clean.removesuffix('```')
            response_clean = response_clean.strip()

            try:
                analysis = json.loads(response_clean)
            except json.JSONDecodeError:
                # If JSON parsing fails, create structured response from text
                analysis = {
                    'rootCause': response_clean.split('\n')[0] if response_clean else 'Unable to parse analysis',
                    'solutions': ['Review the test selector', 'Check if element exists on page'],
                    'prevention': ['Use more robust selectors', 'Add proper waits']
                }

            return {
                'test': title,
                'status': status,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'analysis': analysis,
                'error': error_message,
            }
        except (AttributeError, KeyError, TypeError, ValueError, RuntimeError) as err:
            print(f'Analysis failed: {err!s}')
            return {
                'test': title,
                'status': status,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'analysis': {
                    'rootCause': 'Analysis unavailable',
                    'solutions': [],
                    'prevention': [],
                },
                'error': error_message,
            }

    def generate_report(self, failures: list) -> str:
        """
        Generate a comprehensive failure report

        Args:
            failures: List of test failure dictionaries

        Returns:
            Path to generated report
        """
        analyses = [self.analyze_failure(failure) for failure in failures]

        report = {
            'generatedAt': datetime.now(timezone.utc).isoformat(),
            'totalFailures': len(failures),
            'failures': analyses,
        }

        # Create test-results directory
        results_dir = Path('test-results')
        results_dir.mkdir(exist_ok=True)

        # Save JSON report
        timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
        report_path = results_dir / f'ai-failure-report-{timestamp}.json'

        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        # Generate markdown report
        md_report = self._generate_markdown_report(report)
        md_path = report_path.with_suffix('.md')

        with open(md_path, 'w') as f:
            f.write(md_report)

        return str(md_path)

    def _generate_markdown_report(self, report: dict) -> str:
        """
        Generate markdown report from analysis

        Args:
            report: Analysis report dictionary

        Returns:
            Markdown formatted report string
        """
        md = '# AI Test Failure Analysis Report\n\n'
        md += f"**Generated:** {datetime.fromisoformat(report['generatedAt']).strftime('%Y-%m-%d %H:%M:%S')}\n"
        md += f"**Total Failures:** {report['totalFailures']}\n\n"
        md += '---\n\n'

        for index, failure in enumerate(report['failures'], 1):
            md += f"## {index}. {failure['test']}\n\n"
            md += f"**Status:** {failure['status']}\n"
            md += f"**Timestamp:** {datetime.fromisoformat(failure['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}\n\n"

            if failure.get('error'):
                md += f"**Error:** `{failure['error']}`\n\n"

            md += f"### Root Cause\n{failure['analysis']['rootCause']}\n\n"

            md += '### Possible Solutions\n'
            for sol in failure['analysis']['solutions']:
                md += f'- {sol}\n'
            md += '\n'

            md += '### Prevention Strategies\n'
            for prev in failure['analysis']['prevention']:
                md += f'- {prev}\n'
            md += '\n---\n\n'

        return md