import pytest
import os
from playwright.sync_api import Page
from helpers.selector_generator import SelectorGenerator
from helpers.test_data_generator import TestDataGenerator
from helpers.visual_validator import VisualValidator
from helpers.smart_waits import SmartWaits


class TestAIFeaturesShowcase:
    """Showcase all AI-powered testing features"""

    BASE_URL = 'https://www.saucedemo.com'

    def _skip_if_no_groq(self):
        """Skip test if GROQ_API_KEY is not set"""
        if not os.getenv("GROQ_API_KEY"):
            pytest.skip("GROQ_API_KEY not set - skipping AI-powered test")

    def test_ai_selector_generation_showcase(self, page: Page):
        """Demonstrate AI selector generation capabilities"""
        self._skip_if_no_groq()
        selector_gen = SelectorGenerator()
        page.goto(self.BASE_URL)

        print('\n' + '='*60)
        print('🤖 AI SELECTOR GENERATION SHOWCASE')
        print('='*60)

        # Generate multiple selectors
        selectors = {
            'Username Field': selector_gen.generate_selector('Username input field', 'Login page'),
            'Password Field': selector_gen.generate_selector('Password input field', 'Login page'),
            'Login Button': selector_gen.generate_selector('Login submit button', 'Login page'),
            'Logo': selector_gen.generate_selector('Company logo image', 'Login page')
        }

        for name, selector in selectors.items():
            print(f'  {name}: {selector}')

        print('='*60 + '\n')

    def test_ai_test_data_generation_showcase(self, page: Page):
        """Demonstrate AI test data generation"""
        self._skip_if_no_groq()
        data_gen = TestDataGenerator()

        print('\n' + '='*60)
        print('🤖 AI TEST DATA GENERATION SHOWCASE')
        print('='*60)

        # Generate multiple sets of data
        for i in range(3):
            checkout_data = data_gen.generate_checkout_data()
            print(f'\n  Dataset {i+1}:')
            print(f'    Name: {checkout_data["firstName"]} {checkout_data["lastName"]}')
            print(f'    ZIP: {checkout_data["postalCode"]}')

        # Generate user credentials
        user_creds = data_gen.generate_user_credentials('premium')
        print('\n  Premium User Credentials:')
        print(f'    Username: {user_creds["username"]}')
        print(f'    Password: {user_creds["password"]}')
        print(f'    Email: {user_creds["email"]}')

        print('='*60 + '\n')

    def test_ai_visual_validation_showcase(self, page: Page):
        """Demonstrate AI visual validation"""
        self._skip_if_no_groq()
        validator = VisualValidator()
        page.goto(self.BASE_URL)

        print('\n' + '='*60)
        print('🤖 AI VISUAL VALIDATION SHOWCASE')
        print('='*60)

        # Validate page layout
        expected_elements = [
            'Username input field',
            'Password input field',
            'Login button',
            'Logo image'
        ]

        validation_result = validator.validate_page_layout(page, expected_elements)
        print(f'\n  Page Title: {validation_result["title"]}')
        print(f'  Validation Passed: {validation_result["validation_passed"]}')
        print(f'  Found Elements: {len(validation_result["found_elements"])}')

        # Analyze accessibility
        accessibility = validator.analyze_page_accessibility(page)
        print(f'\n  Accessibility Score: {accessibility["accessibility_score"]}/100')
        print(f'  Issues Found: {accessibility["total_issues"]}')
        for issue in accessibility['issues']:
            print(f'    - {issue}')

        print('='*60 + '\n')

    def test_ai_smart_waits_showcase(self, page: Page):
        """Demonstrate AI-powered smart wait strategies"""
        self._skip_if_no_groq()
        smart_waits = SmartWaits()

        print('\n' + '='*60)
        print('🤖 AI SMART WAITS SHOWCASE')
        print('='*60)

        page.goto(self.BASE_URL)

        # Demonstrate intelligent waiting
        smart_waits.wait_for_element_intelligently(
            page,
            'Login form to be fully loaded',
            timeout=10000
        )

        # Show optimal timeout suggestions
        actions = ['click', 'navigation', 'api_call', 'form_submission']
        print('\n  Optimal Timeout Suggestions:')
        for action in actions:
            timeout = smart_waits.suggest_optimal_timeout(action)
            print(f'    {action}: {timeout}ms')

        print('='*60 + '\n')

    def test_ai_failure_recovery_showcase(self, page: Page):
        """Demonstrate AI-powered failure recovery"""
        self._skip_if_no_groq()
        selector_gen = SelectorGenerator()
        page.goto(self.BASE_URL)

        print('\n' + '='*60)
        print('🤖 AI FAILURE RECOVERY SHOWCASE')
        print('='*60)

        # Intentionally use a selector that might fail
        ai_selector = selector_gen.generate_selector('Login button', 'Login page')

        print(f'\n  Attempting with AI selector: {ai_selector}')

        try:
            page.click(ai_selector, timeout=2000)
            print('  ✅ AI selector worked!')
        except Exception as e:
            print(f'  ⚠️ AI selector failed: {str(e)[:50]}...')

            # Use AI to suggest alternatives
            alternatives = selector_gen.suggest_alternatives(ai_selector, str(e))
            print('\n  🤖 AI Suggested Alternatives:')
            for i, alt in enumerate(alternatives, 1):
                print(f'    {i}. {alt}')

            # Try fallback
            fallback = '[data-test="login-button"]'
            print(f'\n  Using fallback: {fallback}')
            page.click(fallback)
            print('  ✅ Fallback worked!')

        print('='*60 + '\n')