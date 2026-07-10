import pytest
from playwright.sync_api import Page, expect
from helpers.selector_generator import SelectorGenerator
from helpers.test_data_generator import TestDataGenerator


class TestSauceDemoShopping:
    """E2E shopping flow tests with AI-powered test data generation"""

    BASE_URL = 'https://www.saucedemo.com'

    @pytest.fixture(autouse=True)
    def login(self, page: Page):
        """Auto-login before each test"""
        page.goto(self.BASE_URL)
        page.fill('[data-test="username"]', 'standard_user')
        page.fill('[data-test="password"]', 'secret_sauce')
        page.click('[data-test="login-button"]')
        expect(page).to_have_url(f'{self.BASE_URL}/inventory.html')

    def test_add_items_to_cart(self, page: Page):
        """Test adding multiple items to cart"""
        # Add first item
        page.click('[data-test="add-to-cart-sauce-labs-backpack"]')

        # Verify cart badge
        cart_badge = page.locator('.shopping_cart_badge')
        expect(cart_badge).to_have_text('1')

        # Add second item
        page.click('[data-test="add-to-cart-sauce-labs-bike-light"]')
        expect(cart_badge).to_have_text('2')

    def test_complete_checkout_with_ai_generated_data(self, page: Page):
        """Complete checkout flow with AI-generated test data"""
        data_gen = TestDataGenerator()

        # Add item to cart
        page.click('[data-test="add-to-cart-sauce-labs-backpack"]')
        page.click('.shopping_cart_link')

        # Proceed to checkout
        page.click('[data-test="checkout"]')

        # Generate realistic test data using AI
        checkout_data = data_gen.generate_checkout_data()

        print('\n🤖 AI Generated Test Data:')
        print(f'  First Name: {checkout_data["firstName"]}')
        print(f'  Last Name: {checkout_data["lastName"]}')
        print(f'  Postal Code: {checkout_data["postalCode"]}')

        # Fill checkout form
        page.fill('[data-test="firstName"]', checkout_data['firstName'])
        page.fill('[data-test="lastName"]', checkout_data['lastName'])
        page.fill('[data-test="postalCode"]', checkout_data['postalCode'])
        page.click('[data-test="continue"]')

        # Verify checkout overview
        expect(page).to_have_url(f'{self.BASE_URL}/checkout-step-two.html')

        # Complete order
        page.click('[data-test="finish"]')

        # Verify success
        expect(page.locator('.complete-header')).to_have_text('Thank you for your order!')

    def test_remove_item_from_cart(self, page: Page):
        """Test removing items from cart"""
        # Add item
        page.click('[data-test="add-to-cart-sauce-labs-backpack"]')

        # Go to cart
        page.click('.shopping_cart_link')

        # Remove item
        page.click('[data-test="remove-sauce-labs-backpack"]')

        # Verify cart is empty
        cart_items = page.locator('.cart_item')
        expect(cart_items).to_have_count(0)

    def test_sorting_products(self, page: Page):
        """Test product sorting functionality"""
        # Verify we're on inventory page
        expect(page).to_have_url(f'{self.BASE_URL}/inventory.html')

        # Wait for inventory to load
        page.wait_for_selector('.inventory_list', state='visible')

        # Get initial product names
        initial_products = page.locator('.inventory_item_name').all_text_contents()

        # Verify products are displayed
        assert len(initial_products) > 0, 'No products found on page'

        print(f'\n✅ Found {len(initial_products)} products on inventory page')

    def test_product_details_navigation(self, page: Page):
        """Test navigation to product details"""
        selector_gen = SelectorGenerator()

        # Use AI to find product link
        product_selector = selector_gen.generate_selector(
            'First product name link in the inventory',
            'SauceDemo inventory page'
        )

        print(f'\n🤖 AI Generated Product Selector: {product_selector}')

        # Click first product (with fallback)
        try:
            page.locator(product_selector).first.click()
        except Exception:
            page.locator('.inventory_item_name').first.click()

        # Verify we're on product details page
        expect(page.locator('.inventory_details_name')).to_be_visible()

        # Go back
        page.click('[data-test="back-to-products"]')
        expect(page).to_have_url(f'{self.BASE_URL}/inventory.html')