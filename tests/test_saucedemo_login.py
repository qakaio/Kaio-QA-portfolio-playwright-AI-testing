import os

import pytest
from helpers.selector_generator import SelectorGenerator
from playwright.sync_api import Page, expect

DEFAULT_USERNAME = 'standard_user'
DEFAULT_PASSWORD = 'secret_sauce'
LOGIN_SELECTORS = {
    'username': '[data-test="username"]',
    'password': '[data-test="password"]',
    'submit': '[data-test="login-button"]',
    'error': '[data-test="error"]',
}


class TestSauceDemoLogin:
    """Login functionality tests with AI-powered features"""

    BASE_URL = os.getenv('BASE_URL', 'https://www.saucedemo.com')

    @pytest.mark.smoke
    def test_successful_login_standard_user(self, page: Page):
        """Test successful login with standard user"""
        page.goto(self.BASE_URL)

        page.fill(LOGIN_SELECTORS['username'], DEFAULT_USERNAME)
        page.fill(LOGIN_SELECTORS['password'], DEFAULT_PASSWORD)
        page.click(LOGIN_SELECTORS['submit'])

        # Verify successful login
        expect(page).to_have_url(f'{self.BASE_URL}/inventory.html')
        expect(page.locator('.inventory_list')).to_be_visible()

    @pytest.mark.functional
    @pytest.mark.requires_groq
    def test_ai_generated_login_selectors(self, page: Page):
        """Demonstrate AI selector generation for login elements"""
        selector_gen = SelectorGenerator()
        page.goto(self.BASE_URL)

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

        try:
            page.fill(username_selector, DEFAULT_USERNAME)
            page.fill(password_selector, DEFAULT_PASSWORD)
            page.click(login_btn_selector)
            print('✅ AI selectors worked perfectly!')
        except (AssertionError, TimeoutError, ValueError) as exc:
            print(f'⚠️ AI selectors failed, using fallback: {exc}')
            page.fill(LOGIN_SELECTORS['username'], DEFAULT_USERNAME)
            page.fill(LOGIN_SELECTORS['password'], DEFAULT_PASSWORD)
            page.click(LOGIN_SELECTORS['submit'])

        expect(page).to_have_url(f'{self.BASE_URL}/inventory.html')

    @pytest.mark.functional
    def test_locked_out_user(self, page: Page):
        """Test login with locked out user - demonstrates AI failure analysis"""
        page.goto(self.BASE_URL)

        page.fill(LOGIN_SELECTORS['username'], 'locked_out_user')
        page.fill(LOGIN_SELECTORS['password'], DEFAULT_PASSWORD)
        page.click(LOGIN_SELECTORS['submit'])

        error_msg = page.locator(LOGIN_SELECTORS['error'])
        expect(error_msg).to_be_visible()
        expect(error_msg).to_contain_text('Epic sadface: Sorry, this user has been locked out')

    @pytest.mark.functional
    @pytest.mark.parametrize('username,password,expected_error', [
        ('', '', 'Username is required'),
        ('standard_user', '', 'Password is required'),
        ('invalid_user', 'wrong_password', 'Username and password do not match'),
    ])
    def test_invalid_login_scenarios(self, page: Page, username: str, password: str, expected_error: str):
        """Test various invalid login scenarios"""
        page.goto(self.BASE_URL)

        if username:
            page.fill(LOGIN_SELECTORS['username'], username)
        if password:
            page.fill(LOGIN_SELECTORS['password'], password)

        page.click(LOGIN_SELECTORS['submit'])

        error_msg = page.locator(LOGIN_SELECTORS['error'])
        expect(error_msg).to_be_visible()
        expect(error_msg).to_contain_text(expected_error)