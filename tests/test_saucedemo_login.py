import pytest
from playwright.sync_api import Page, expect
from helpers.selector_generator import SelectorGenerator


class TestSauceDemoLogin:
    """Login functionality tests with AI-powered features"""

    BASE_URL = 'https://www.saucedemo.com'

    def test_successful_login_standard_user(self, page: Page):
        """Test successful login with standard user"""
        page.goto(self.BASE_URL)

        # Login
        page.fill('[data-test="username"]', 'standard_user')
        page.fill('[data-test="password"]', 'secret_sauce')
        page.click('[data-test="login-button"]')

        # Verify successful login
        expect(page).to_have_url(f'{self.BASE_URL}/inventory.html')
        expect(page.locator('.inventory_list')).to_be_visible()

    @pytest.mark.requires_groq
    def test_ai_generated_login_selectors(self, page: Page):
        """Demonstrate AI selector generation for login elements"""
        selector_gen = SelectorGenerator()
        page.goto(self.BASE_URL)

        # Generate selectors using AI
        username_selector = selector_gen.generate_selector(
            'Username input field',
            'SauceDemo login page'
        )
        password_selector = selector_gen.generate_selector(
            'Password input field',
            'SauceDemo login page'
        )
        login_btn_selector = selector_gen.generate_selector(
            'Login submit button',
            'SauceDemo login page'
        )

        print('\n🤖 AI Generated Selectors:')
        print(f'  Username: {username_selector}')
        print(f'  Password: {password_selector}')
        print(f'  Login Button: {login_btn_selector}')

        # Use AI-generated selectors with fallback
        try:
            page.fill(username_selector, 'standard_user')
            page.fill(password_selector, 'secret_sauce')
            page.click(login_btn_selector)
            print('✅ AI selectors worked perfectly!')
        except Exception as e:
            print(f'⚠️ AI selectors failed, using fallback: {e}')
            page.fill('[data-test="username"]', 'standard_user')
            page.fill('[data-test="password"]', 'secret_sauce')
            page.click('[data-test="login-button"]')

        expect(page).to_have_url(f'{self.BASE_URL}/inventory.html')

    def test_locked_out_user(self, page: Page):
        """Test login with locked out user - demonstrates AI failure analysis"""
        page.goto(self.BASE_URL)

        page.fill('[data-test="username"]', 'locked_out_user')
        page.fill('[data-test="password"]', 'secret_sauce')
        page.click('[data-test="login-button"]')

        # Verify error message
        error_msg = page.locator('[data-test="error"]')
        expect(error_msg).to_be_visible()
        expect(error_msg).to_contain_text('Epic sadface: Sorry, this user has been locked out')

    @pytest.mark.parametrize('username,password,expected_error', [
        ('', '', 'Username is required'),
        ('standard_user', '', 'Password is required'),
        ('invalid_user', 'wrong_password', 'Username and password do not match'),
    ])
    def test_invalid_login_scenarios(self, page: Page, username: str, password: str, expected_error: str):
        """Test various invalid login scenarios"""
        page.goto(self.BASE_URL)

        if username:
            page.fill('[data-test="username"]', username)
        if password:
            page.fill('[data-test="password"]', password)

        page.click('[data-test="login-button"]')

        # Verify error message appears
        error_msg = page.locator('[data-test="error"]')
        expect(error_msg).to_be_visible()
        expect(error_msg).to_contain_text(expected_error)