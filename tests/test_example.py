import pytest
from helpers.selector_generator import SelectorGenerator
from playwright.sync_api import Page, expect

PLAYWRIGHT_DOCS_URL = 'https://playwright.dev'
AI_TIMEOUT_MS = 3000
FALLBACK_GET_STARTED_SELECTOR = 'a:has-text("Get started")'
FALLBACK_SEARCH_SELECTOR = 'button[aria-label*="Search"], .DocSearch'


class TestExampleSuite:
    """Example test suite with AI features"""

    @pytest.mark.functional
    def test_basic_navigation(self, page: Page):
        """Basic navigation test"""
        page.goto(PLAYWRIGHT_DOCS_URL)

        title = page.title()
        assert 'Playwright' in title

    @pytest.mark.exploratory
    @pytest.mark.requires_groq
    def test_ai_powered_selector_generation(self, page: Page):
        """AI-powered selector generation example"""
        selector_gen = SelectorGenerator()

        page.goto(PLAYWRIGHT_DOCS_URL)

        selector = selector_gen.generate_selector(
            'Get Started link in the navigation or hero section',
            'Playwright documentation homepage'
        )

        print(f'Generated selector: {selector}')

        try:
            element = page.locator(selector).first
            expect(element).to_be_visible(timeout=AI_TIMEOUT_MS)
            print('✅ AI-generated selector worked!')
        except (AssertionError, TimeoutError, ValueError) as exc:
            print(f'⚠️ AI selector failed: {exc}')
            element = page.locator(FALLBACK_GET_STARTED_SELECTOR).first
            expect(element).to_be_visible()
            print(f'✅ Fallback selector worked: {FALLBACK_GET_STARTED_SELECTOR}')

    @pytest.mark.exploratory
    @pytest.mark.skip(reason='Intentional failure - remove skip to see AI analysis')
    def test_intentional_failure_for_ai_analysis(self, page: Page):
        """Test with intentional failure to demonstrate AI analysis"""
        page.goto(PLAYWRIGHT_DOCS_URL)

        expect(page.locator('[data-testid="non-existent"]')).to_be_visible()

    @pytest.mark.exploratory
    @pytest.mark.requires_groq
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
        except (AssertionError, TimeoutError, ValueError):
            # Fallback to known selector
            search_btn = page.locator('button[aria-label*="Search"], .DocSearch').first
            expect(search_btn).to_be_visible()
            print('✅ Used fallback search selector')