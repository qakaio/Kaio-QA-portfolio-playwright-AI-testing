# 🤖 AI-Powered Playwright Test Automation Framework

![AI Tests](https://github.com/qakaio/Kaio-QA-portfolio-playwright-AI-testing/actions/workflows/ai-tests.yml/badge.svg)

# 🤖 AI-Powered Playwright Test Automation Framework

> **Next-generation test automation** leveraging **Groq AI (llama-3.3-70b-versatile)** for intelligent testing capabilities.

Built by [Kaio Garcia](https://github.com/qakaio) — QA Engineer

---

## 📊 Project Status

| Metric | Value |
|--------|-------|
| **Tests** | 19 passing |
| **AI Features** | 5 core capabilities |
| **Language** | Python 3.11+ |
| **Framework** | Playwright 1.48 + Pytest 9.0 |
| **AI Provider** | Groq (llama-3.3-70b-versatile) |

---

## 🎯 AI Capabilities (5 Core Features)

| # | Capability | Description | Use Case |
|---|------------|-------------|----------|
| **1** | **AI Selector Generation** | Generate resilient selectors from natural language | Eliminate brittle XPath/CSS |
| **2** | **AI Test Data Generation** | Create realistic, unique test data automatically | Infinite unique test data |
| **3** | **AI Failure Analysis** | Automatic root cause + suggested fixes on failure | Instant debugging |
| **4** | **AI Visual Validation** | AI-powered visual regression & accessibility | UI consistency checks |
| **5** | **Self-Healing Tests** | Automatic selector recovery on failure | Zero-maintenance tests |

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| **Language** | Python 3.11+ |
| **Browser Automation** | Playwright 1.48 |
| **Test Framework** | Pytest 9.0 |
| **AI Provider** | Groq (llama-3.3-70b-versatile) |
| **AI Features** | Selector Gen, Data Gen, Failure Analysis, Visual Validation, Self-Healing |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Groq API Key (free at [console.groq.com](https://console.groq.com))

### Installation
```bash
# 1. Clone repository
git clone https://github.com/qakaio/Kaio-QA-portfolio-playwright-AI-testing.git
cd Kaio-QA-portfolio-playwright-AI-testing

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install chromium

# 5. Configure AI
cp .env.example .env
# Edit .env and add your Groq API key
```

### Configuration (`.env`)
```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### Running Tests
```bash
# Run all tests (19 tests, ~2 minutes)
pytest -v

# Run with verbose output
pytest -v -s

# Run specific AI feature demo
pytest tests/test_ai_features_showcase.py -v -s

# Run login tests with AI selectors
pytest tests/test_saucedemo_login.py::TestSauceDemoLogin::test_ai_generated_login_selectors -v -s

# Run shopping flow with AI-generated data
pytest tests/test_saucedemo_shopping.py::TestSauceDemoShopping::test_complete_checkout_with_ai_generated_data -v -s

# Run headed (visible browser)
pytest --headed

# Run in specific browser
pytest --browser=firefox
```

---

## 🎬 Demo Commands

| Feature | Command |
|---------|---------|
| **AI Selector Generation** | `pytest tests/test_saucedemo_login.py::TestSauceDemoLogin::test_ai_generated_login_selectors -v -s` |
| **AI Test Data Generation** | `pytest tests/test_saucedemo_shopping.py::TestSauceDemoShopping::test_complete_checkout_with_ai_generated_data -v -s` |
| **All AI Features Showcase** | `pytest tests/test_ai_features_showcase.py -v -s` |
| **AI Failure Analysis** | `pytest tests/test_example.py::TestExampleSuite::test_intentional_failure_for_ai_analysis -v -s` |

---

## 🏗 Architecture Overview

```
Kaio-QA-portfolio-playwright-AI-testing/
├── helpers/                    # AI-powered helper modules
│   ├── ai_client.py           # Groq AI integration & prompt engineering
│   ├── selector_generator.py  # AI selector generation from natural language
│   ├── test_data_generator.py # AI test data creation (realistic, unique)
│   ├── failure_analyzer.py    # AI failure analysis & fix suggestions
│   ├── visual_validator.py    # AI visual validation & accessibility
│   └── smart_waits.py         # AI-powered wait strategies
├── tests/                      # Test suites (19 tests total)
│   ├── test_ai_features_showcase.py  # AI capabilities demonstration (5 tests)
│   ├── test_saucedemo_login.py       # Login scenarios with AI (6 tests)
│   ├── test_saucedemo_shopping.py    # E2E shopping flow with AI data (5 tests)
│   └── test_example.py               # Basic examples + failure demo (4 tests)
├── conftest.py                 # Pytest hooks (auto AI analysis on failure)
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Dependencies
├── .env.example                # Environment template
└── README.md
```

---

## 🧠 AI Capabilities Deep Dive

### 1. AI Selector Generation
```python
from helpers.selector_generator import SelectorGenerator

selector_gen = SelectorGenerator()
selector = selector_gen.generate_selector(
    element_description='Login button',
    page_context='Login page with email/password fields'
)
# Returns: '[data-test="login-button"]' or '#login-btn' or 'button:has-text("Login")'
```

**Why it works:** AI understands context, generates resilient selectors (data-testid > role > text > CSS > XPath)

### 2. AI Test Data Generation
```python
from helpers.test_data_generator import TestDataGenerator

data_gen = TestDataGenerator()
checkout_data = data_gen.generate_checkout_data()
# Returns: {'firstName': 'Emma', 'lastName': 'Wilson', 'postalCode': '94102', ...}

user_data = data_gen.generate_user_data()
# Returns: {'email': 'unique@domain.com', 'password': 'SecurePass123!', ...}
```

**Benefits:** Infinite unique data, zero hardcoding, realistic values

### 3. Automatic Failure Analysis
```python
# Configured automatically in conftest.py
# Runs on ANY test failure:

🤖 AI Failure Analysis:
Root Cause: Element not found - selector may be outdated
Solutions: 
  1. Update selector to match current DOM
  2. Add explicit wait for element visibility
  3. Check if element is inside iframe
Prevention: Use AI selector generation for resilient locators
```

### 4. Self-Healing Tests
```python
from helpers.selector_generator import SelectorGenerator

try:
    page.click(ai_selector)
except Exception as error:
    alternatives = selector_gen.suggest_alternatives(ai_selector, str(error))
    page.click(alternatives[0])  # Automatic recovery with alternative
```

### 5. Visual Validation
```python
from helpers.visual_validator import VisualValidator

validator = VisualValidator()
result = validator.compare_screenshots(
    baseline='baseline/login-page.png',
    current='current/login-page.png',
    threshold=0.1  # 10% difference threshold
)
# Returns: {match: true, diff_percentage: 0.02, diff_image: 'diff.png'}
```

---

## 📁 Project Structure

```
Kaio-QA-portfolio-playwright-AI-testing/
├── helpers/                    # AI-powered helper modules
│   ├── ai_client.py           # Groq AI integration & prompt engineering
│   ├── selector_generator.py  # AI selector generation
│   ├── test_data_generator.py # AI test data creation
│   ├── failure_analyzer.py    # AI failure analysis
│   ├── visual_validator.py    # AI visual validation & a11y
│   └── smart_waits.py         # AI wait strategies
├── tests/                      # Test suites (19 tests)
│   ├── test_ai_features_showcase.py  # AI capabilities demo (5 tests)
│   ├── test_saucedemo_login.py       # Login with AI selectors (6 tests)
│   ├── test_saucedemo_shopping.py    # E2E shopping with AI data (5 tests)
│   └── test_example.py               # Basic examples + failure demo (4 tests)
├── conftest.py                 # Pytest hooks (auto AI analysis)
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Dependencies
├── .env.example                # Environment template
└── README.md
```

---

## 📊 Test Coverage

| Suite | Tests | Coverage |
|-------|-------|----------|
| **AI Features Showcase** | 5 | Selector gen, data gen, visual validation, smart waits, failure recovery |
| **Login Tests** | 6 | Standard login, AI selectors, locked user, invalid credentials |
| **Shopping Tests** | 5 | Add to cart, checkout with AI data, remove items, sorting, navigation |
| **Example Tests** | 4 | Basic navigation, AI selectors, search, failure demo |
| **Total** | **19** | **100% passing** |

---

## 🔧 Configuration

### Environment Variables (`.env`)
```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### Pytest Options
```bash
pytest -v                    # Verbose output
pytest -s                    # Show print statements (AI output)
pytest -k "login"            # Run tests matching "login"
pytest --headed              # Run in headed mode
pytest --browser=firefox     # Use different browser
pytest --browser=webkit      # Use WebKit
```

### Groq API Key (Free)
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up / log in
3. Create API key
4. Add to `.env` file

---

## 🎯 Real-World Usage Example

```python
# tests/test_my_feature.py
from playwright.sync_api import Page, expect
from helpers.selector_generator import SelectorGenerator
from helpers.test_data_generator import TestDataGenerator

def test_checkout_flow(page: Page):
    selector_gen = SelectorGenerator()
    data_gen = TestDataGenerator()
    
    # Navigate
    page.goto('https://example.com/checkout')
    
    # AI finds elements (resilient selectors)
    submit_btn = selector_gen.generate_selector('Submit button', 'Checkout form')
    first_name = selector_gen.generate_selector('First name field', 'Checkout form')
    
    # AI generates realistic test data
    form_data = data_gen.generate_checkout_data()
    
    # Fill and submit
    page.fill(first_name, form_data['firstName'])
    page.fill('#lastName', form_data['lastName'])
    page.fill('#postalCode', form_data['postalCode'])
    page.click(submit_btn)
    
    # Verify
    expect(page.locator('.success')).to_be_visible()
```

---

## 🛡 Automatic Failure Analysis (conftest.py)

```python
# Automatic AI analysis on ANY test failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call' and report.failed:
        analyzer = FailureAnalyzer()
        failure_data = {
            'test_name': item.name,
            'error': str(report.longrepr),
            'traceback': report.longreprtext,
        }
        analysis = analyzer.analyze_failure(failure_data)
        
        print(f'\n🤖 AI Failure Analysis:')
        print(f"Root Cause: {analysis['analysis']['rootCause']}")
        print(f"Solutions: {', '.join(analysis['analysis']['solutions'])}")
        print(f"Prevention: {analysis['analysis']['prevention']}")
```

---

## 🛡 Extending the Framework

### Add New AI Helper
```python
# helpers/my_ai_helper.py
from helpers.ai_client import AIClient

class MyAIHelper:
    def __init__(self):
        self.ai_client = AIClient()
    
    def my_ai_feature(self, input_data: str) -> dict:
        prompt = f"Analyze this QA scenario: {input_data}. Provide structured response."
        return self.ai_client.query_structured(prompt)
```

### Add New Test Suite
```python
# tests/test_my_feature.py
import pytest
from playwright.sync_api import Page
from helpers.my_ai_helper import MyAIHelper

class TestMyFeature:
    def test_something(self, page: Page):
        helper = MyAIHelper()
        result = helper.my_ai_feature("test input")
        assert result['success'] is True
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Tests failing** | Check `.env` has valid Groq API key |
| **Slow AI responses** | Groq typically <2s; check internet/API key |
| **Import errors** | Activate venv: `source .venv/bin/activate` |
| **Browser not found** | Run `playwright install chromium` |
| **Permission errors** | Check file permissions, run as user (not root) |

---

## 📦 Requirements

| Dependency | Version |
|------------|---------|
| Python | 3.11+ |
| Playwright | 1.48+ |
| Pytest | 9.0+ |
| Groq API | Free tier available |
| Groq Model | llama-3.3-70b-versatile |

Install: `pip install -r requirements.txt && playwright install chromium`

---

## 📄 License

MIT License — Educational and portfolio purposes.

---

## 👤 Author

**Kaio Garcia** — QA Engineer
🔗 [GitHub](https://github.com/qakaio) • [LinkedIn](https://linkedin.com/in/kaioqa) • [Portfolio](https://qakaio.github.io)

---

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for fast, free LLM inference
- [Playwright](https://playwright.dev/) for modern browser automation
- [Pytest](https://docs.pytest.org/) for the best testing framework
- [SauceDemo](https://www.saucedemo.com/) for the demo e-commerce site
