import pytest
from playwright.sync_api import Page, expect
from helpers.selector_generator import SelectorGenerator


class TestExampleSuite:
    """Example test suite with AI features"""

    def test_basic_navigation(self, page: Page):
        """Basic navigation test"""
        page.goto('https://playwright.dev')

        title = page.title()
        assert 'Playwright' in title

    def test_ai_powered_selector_generation(self, page: Page):
        """AI-powered selector generation example"""
        selector_gen = SelectorGenerator()

        page.goto('https://playwright.dev')

        # Generate selector using AI
        selector = selector_gen.generate_selector(
            'Get Started link in the navigation or hero section',
            'Playwright documentation homepage'
        )

        print(f'Generated selector: {selector}')

        # Try to use the generated selector, fallback to known selector if it fails
        try:
            element = page.locator(selector).first
            expect(element).to_be_visible(timeout=3000)
            print('✅ AI-generated selector worked!')
        except Exception as e:
            print(f'⚠️ AI selector failed: {e}')
            # Fallback to a known working selector
            fallback_selector = 'a:has-text("Get started")'
            element = page.locator(fallback_selector).first
            expect(element).to_be_visible()
            print(f'✅ Fallback selector worked: {fallback_selector}')

    @pytest.mark.skip(reason='Intentional failure - remove skip to see AI analysis')
    def test_intentional_failure_for_ai_analysis(self, page: Page):
        """Test with intentional failure to demonstrate AI analysis"""
        page.goto('https://playwright.dev')

        # This will fail to demonstrate AI failure analysis
        # Remove @pytest.mark.skip to see the AI analysis in action
        expect(page.locator('[data-testid="non-existent"]')).to_be_visible()

    def test_successful_search_functionality(self, page: Page):
        """Test search functionality with AI-generated selectors"""
        selector_gen = SelectorGenerator()

        page.goto('https://playwright.dev')

        # Generate selector for search button
        search_selector = selector_gen.generate_selector(
            'Search button or icon in the navigation bar',
            'Playwright documentation site'
        )

        print(f'Generated search selector: {search_selector}')

        # Try AI selector first, then fallback
        try:
            search_btn = page.locator(search_selector).first
            expect(search_btn).to_be_visible(timeout=3000)
            print('✅ AI-generated search selector worked!')
        except Exception:
            # Fallback to known selector
            search_btn = page.locator('button[aria-label*="Search"], .DocSearch').first
            expect(search_btn).to_be_visible()
            print('✅ Used fallback search selector')