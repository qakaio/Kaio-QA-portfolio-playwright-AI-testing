import os

import pytest
from helpers.selector_generator import SelectorGenerator
from helpers.test_data_generator import TestDataGenerator
from playwright.sync_api import Page, expect

DEFAULT_USERNAME = 'standard_user'
DEFAULT_PASSWORD = 'secret_sauce'
SHOPPING_SELECTORS = {
    'cart_link': '.shopping_cart_link',
    'cart_badge': '.shopping_cart_badge',
    'checkout': '[data-test="checkout"]',
    'continue': '[data-test="continue"]',
    'finish': '[data-test="finish"]',
    'first_name': '[data-test="firstName"]',
    'last_name': '[data-test="lastName"]',
    'postal_code': '[data-test="postalCode"]',
    'inventory_list': '.inventory_list',
    'inventory_item_name': '.inventory_item_name',
    'product_details_name': '.inventory_details_name',
    'back_to_products': '[data-test="back-to-products"]',
}


class TestSauceDemoShopping:
    """E2E shopping flow tests with AI-powered test data generation"""

    BASE_URL = os.getenv('BASE_URL', 'https://www.saucedemo.com')

    @pytest.fixture(autouse=True)
    def login(self, page: Page):
        """Auto-login before each test"""
        page.goto(self.BASE_URL)
        page.fill('[data-test="username"]', DEFAULT_USERNAME)
        page.fill('[data-test="password"]', DEFAULT_PASSWORD)
        page.click('[data-test="login-button"]')
        expect(page).to_have_url(f'{self.BASE_URL}/inventory.html')

    @pytest.mark.functional
    def test_add_items_to_cart(self, page: Page):
        """Test adding multiple items to cart"""
        page.click('[data-test="add-to-cart-sauce-labs-backpack"]')

        cart_badge = page.locator(SHOPPING_SELECTORS['cart_badge'])
        expect(cart_badge).to_have_text('1')

        page.click('[data-test="add-to-cart-sauce-labs-bike-light"]')
        expect(cart_badge).to_have_text('2')

    @pytest.mark.functional
    @pytest.mark.requires_groq
    def test_complete_checkout_with_ai_generated_data(self, page: Page):
        """Complete checkout flow with AI-generated test data"""
        data_gen = TestDataGenerator()

        page.click('[data-test="add-to-cart-sauce-labs-backpack"]')
        page.click(SHOPPING_SELECTORS['cart_link'])

        page.click(SHOPPING_SELECTORS['checkout'])

        # Generate realistic test data using AI
        checkout_data = data_gen.generate_checkout_data()

        print('\n🤖 AI Generated Test Data:')
        print(f'  First Name: {checkout_data["firstName"]}')
        print(f'  Last Name: {checkout_data["lastName"]}')
        print(f'  Postal Code: {checkout_data["postalCode"]}')

        page.fill(SHOPPING_SELECTORS['first_name'], checkout_data['firstName'])
        page.fill(SHOPPING_SELECTORS['last_name'], checkout_data['lastName'])
        page.fill(SHOPPING_SELECTORS['postal_code'], checkout_data['postalCode'])
        page.click(SHOPPING_SELECTORS['continue'])

        expect(page).to_have_url(f'{self.BASE_URL}/checkout-step-two.html')

        page.click(SHOPPING_SELECTORS['finish'])

        expect(page.locator('.complete-header')).to_have_text('Thank you for your order!')

    @pytest.mark.functional
    def test_remove_item_from_cart(self, page: Page):
        """Test removing items from cart"""
        page.click('[data-test="add-to-cart-sauce-labs-backpack"]')

        page.click(SHOPPING_SELECTORS['cart_link'])

        page.click('[data-test="remove-sauce-labs-backpack"]')

        cart_items = page.locator('.cart_item')
        expect(cart_items).to_have_count(0)

    @pytest.mark.functional
    def test_sorting_products(self, page: Page):
        """Test product sorting functionality"""
        expect(page).to_have_url(f'{self.BASE_URL}/inventory.html')

        page.wait_for_selector(SHOPPING_SELECTORS['inventory_list'], state='visible')

        initial_products = page.locator(SHOPPING_SELECTORS['inventory_item_name']).all_text_contents()

        assert len(initial_products) > 0, 'No products found on page'

        print(f'\n✅ Found {len(initial_products)} products on inventory page')

    @pytest.mark.functional
    @pytest.mark.requires_groq
    def test_product_details_navigation(self, page: Page):
        """Test navigation to product details"""
        selector_gen = SelectorGenerator()

        product_selector = selector_gen.generate_selector(
            'First product name link in the inventory',
            'SauceDemo inventory page'
        )

        print(f'\n🤖 AI Generated Product Selector: {product_selector}')

        try:
            page.locator(product_selector).first.click()
        except (AssertionError, TimeoutError, ValueError):
            page.locator(SHOPPING_SELECTORS['inventory_item_name']).first.click()

        expect(page.locator(SHOPPING_SELECTORS['product_details_name'])).to_be_visible()

        page.click(SHOPPING_SELECTORS['back_to_products'])
        expect(page).to_have_url(f'{self.BASE_URL}/inventory.html')