# 🤖 AI-Powered Playwright Test Automation

> Next-generation test automation framework leveraging Groq AI for intelligent testing

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.48-green.svg)](https://playwright.dev/)
[![Tests](https://img.shields.io/badge/tests-19%20passing-brightgreen.svg)](tests/)
[![AI](https://img.shields.io/badge/AI-Groq-orange.svg)](https://groq.com/)

<img width="1201" height="692" alt="image" src="https://github.com/user-attachments/assets/9d44c6e5-dc49-46ac-86b8-a383fc84e28f" />

## 🎯 About This Project

A test automation framework that uses **AI to solve real QA problems**:
- **AI generates selectors** from natural language (no more brittle XPath)
- **AI creates test data** automatically (realistic, unique every time)
- **AI analyzes failures** and suggests fixes
- **Self-healing tests** that recover automatically


---

## 🛠️ Tech Stack

- **Python 3.14** - Latest language features
- **Playwright 1.48** - Modern browser automation
- **Groq AI** - Fast LLM inference (llama-3.3-70b-versatile)
- **Pytest 9.0** - Professional testing framework

---

## 🚀 Quick Start

```bash
# 1. Install
pip install -r requirements.txt
playwright install chromium

# 2. Configure
cp .env.example .env
# Add your Groq API key to .env (get free key at https://console.groq.com)

# 3. Run
pytest -v
```

**Expected**: 19 tests passing in ~2 minutes

---

## ✨ Key Features

### 1. AI Selector Generation
```python
from helpers.selector_generator import SelectorGenerator

selector_gen = SelectorGenerator()
selector = selector_gen.generate_selector('Login button', 'Login page')
# Returns: '[data-test="login-button"]'
```

### 2. AI Test Data Generation
```python
from helpers.test_data_generator import TestDataGenerator

data_gen = TestDataGenerator()
data = data_gen.generate_checkout_data()
# Returns: {'firstName': 'Emma', 'lastName': 'Wilson', 'postalCode': '94102'}
```
**Result**: Infinite unique test data, zero hardcoding

### 3. Automatic Failure Analysis
When tests fail, AI automatically provides:
- Root cause analysis
- Suggested solutions
- Prevention strategies

```
🤖 AI Failure Analysis:
Root Cause: Element not found - selector may be outdated
Solutions: Update selector, Add explicit wait, Check element visibility
```

### 4. Self-Healing Tests
```python
try:
    page.click(ai_selector)
except:
    alternatives = selector_gen.suggest_alternatives(ai_selector, error)
    page.click(alternatives[0])  # Automatic recovery
```

---

## 📁 Project Structure

```
├── helpers/                    # AI-powered helper modules
│   ├── ai_client.py           # Groq AI integration
│   ├── selector_generator.py  # AI selector generation
│   ├── test_data_generator.py # AI test data creation
│   ├── failure_analyzer.py    # AI failure analysis
│   ├── visual_validator.py    # AI visual validation
│   └── smart_waits.py         # AI wait strategies
├── tests/                      # Test suites (19 tests)
│   ├── test_ai_features_showcase.py  # AI capabilities demo
│   ├── test_saucedemo_login.py       # Login scenarios
│   ├── test_saucedemo_shopping.py    # E2E shopping flow
│   └── test_example.py               # Basic examples
├── conftest.py                 # Pytest hooks (auto AI analysis)
├── pytest.ini                  # Pytest configuration
└── requirements.txt            # Dependencies
```

---

## 🎬 Demo Commands

### Show AI Selector Generation
```bash
pytest tests/test_saucedemo_login.py::TestSauceDemoLogin::test_ai_generated_login_selectors -v -s
```

### Show AI Test Data Generation
```bash
pytest tests/test_saucedemo_shopping.py::TestSauceDemoShopping::test_complete_checkout_with_ai_generated_data -v -s
```

### Show All AI Features
```bash
pytest tests/test_ai_features_showcase.py -v -s
```

### Show AI Failure Analysis
```bash
# Remove @pytest.mark.skip from test_intentional_failure_for_ai_analysis first
pytest tests/test_example.py::TestExampleSuite::test_intentional_failure_for_ai_analysis -v -s
```

---

## 📊 Test Coverage

| Suite | Tests | Coverage |
|-------|-------|----------|
| AI Features Showcase | 5 | Selector gen, data gen, visual validation, smart waits, failure recovery |
| Login Tests | 6 | Standard login, AI selectors, locked user, invalid credentials |
| Shopping Tests | 5 | Add to cart, checkout with AI data, remove items, sorting, navigation |
| Example Tests | 4 | Basic navigation, AI selectors, search, failure demo |

**Total**: 19 tests, 100% passing

---

## 💡 Real-World Usage

### Creating a New Test
```python
from playwright.sync_api import Page, expect
from helpers.selector_generator import SelectorGenerator
from helpers.test_data_generator import TestDataGenerator

def test_checkout_flow(page: Page):
    selector_gen = SelectorGenerator()
    data_gen = TestDataGenerator()
    
    # Navigate
    page.goto('https://example.com/checkout')
    
    # AI finds elements
    submit_btn = selector_gen.generate_selector('Submit button', 'Checkout form')
    
    # AI generates data
    form_data = data_gen.generate_checkout_data()
    
    # Fill and submit
    page.fill('#firstName', form_data['firstName'])
    page.fill('#lastName', form_data['lastName'])
    page.click(submit_btn)
    
    # Verify
    expect(page.locator('.success')).to_be_visible()
```

### Automatic Failure Analysis
Configured in `conftest.py` - runs automatically when any test fails:
```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call' and report.failed:
        analyzer = FailureAnalyzer()
        analysis = analyzer.analyze_failure(failure_data)
        print(f'\n🤖 AI Failure Analysis:')
        print(f"Root Cause: {analysis['analysis']['rootCause']}")
        print(f"Solutions: {', '.join(analysis['analysis']['solutions'])}")
```

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

Get free API key: https://console.groq.com/

### Pytest Options
```bash
pytest -v                    # Verbose output
pytest -s                    # Show print statements
pytest -k "login"            # Run tests matching "login"
pytest --headed              # Run in headed mode
pytest --browser=firefox     # Use different browser
```

---

## 🎯 Use Cases

1. **Flaky Test Prevention** - AI-generated selectors are more robust
2. **Faster Test Development** - Generate selectors and data instantly
3. **Better Debugging** - AI analyzes failures immediately
4. **Accessibility Testing** - Automated a11y checks
5. **Self-Healing Tests** - Automatic recovery from failures

---

## 🚧 Extending the Framework

### Add New AI Feature
```python
# Create new helper in helpers/
class MyAIHelper:
    def __init__(self):
        self.ai_client = AIClient()
    
    def my_ai_feature(self, input_data):
        prompt = f"Analyze this: {input_data}"
        return self.ai_client.query(prompt)
```

### Add New Test Suite
```python
# Create new file in tests/
class TestMyFeature:
    def test_something(self, page: Page):
        # Your test code
        pass
```

---

## 🐛 Troubleshooting

### Tests Failing?
```bash
# Check Groq API key
cat .env

# Reinstall dependencies
pip install -r requirements.txt

# Reinstall browsers
playwright install chromium
```

### Slow AI Responses?
- Groq is usually fast (<2 seconds)
- Check internet connection
- Verify API key is valid

### Import Errors?
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Verify installation
pip list | grep playwright
```
