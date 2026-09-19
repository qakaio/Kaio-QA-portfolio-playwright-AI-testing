import httpx
import pytest
from groq import RateLimitError
from helpers.ai_client import AIClient
from helpers.selector_generator import SelectorGenerator
from helpers.test_data_generator import TestDataGenerator


class _FakeChoice:
    def __init__(self, content):
        self.message = type('Message', (), {'content': content})()


class _FakeResponse:
    def __init__(self, content):
        self.choices = [_FakeChoice(content)]


def test_ai_client_returns_empty_string_for_empty_model_response():
    client = AIClient.__new__(AIClient)
    client.model = 'test-model'
    client.client = type(
        'DummyClient',
        (),
        {
            'chat': type(
                'DummyChat',
                (),
                {
                    'completions': type(
                        'DummyCompletions',
                        (),
                        {
                            'create': lambda *args, **kwargs: _FakeResponse(''),
                        },
                    )(),
                },
            )(),
        },
    )()

    result = client.query('prompt', system_prompt='system')

    assert result == ''


def test_ai_client_wraps_provider_failure_in_runtime_error():
    client = AIClient.__new__(AIClient)
    client.model = 'test-model'

    def _raise(*args, **kwargs):
        response = httpx.Response(
            429,
            request=httpx.Request('GET', 'https://example.com'),
            json={'error': {'message': 'rate limit exceeded'}},
        )
        raise RateLimitError('rate limit exceeded', response=response, body={'error': {'message': 'rate limit exceeded'}})

    client.client = type(
        'DummyClient',
        (),
        {
            'chat': type(
                'DummyChat',
                (),
                {
                    'completions': type(
                        'DummyCompletions',
                        (),
                        {'create': _raise},
                    )(),
                },
            )(),
        },
    )()

    with pytest.raises(RuntimeError, match='rate limit exceeded'):
        client.query('prompt')


def test_selector_generator_returns_failed_selector_on_malformed_json():
    generator = SelectorGenerator.__new__(SelectorGenerator)
    generator.ai_client = type('DummyAI', (), {'query': lambda *args, **kwargs: 'not-json'})()

    result = generator.suggest_alternatives('[data-testid="submit"]', 'element not found')

    assert result == ['[data-testid="submit"]']


def test_test_data_generator_uses_fallback_for_malformed_json():
    data_gen = TestDataGenerator.__new__(TestDataGenerator)
    data_gen.ai_client = type('DummyAI', (), {'query': lambda *args, **kwargs: '{not valid json}'})()

    result = data_gen.generate_checkout_data()

    assert result == {
        'firstName': 'Test',
        'lastName': 'User',
        'postalCode': '12345',
    }
