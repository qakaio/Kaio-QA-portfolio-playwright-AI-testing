from playwright.sync_api import Page
from helpers.ai_client import AIClient


class SmartWaits:
    """AI-powered smart wait strategies"""
    
    def __init__(self):
        self.ai_client = AIClient()
    
    def wait_for_element_intelligently(self, page: Page, element_description: str, timeout: int = 10000):
        """
        Wait for element using AI-generated strategy
        
        Args:
            page: Playwright page object
            element_description: Natural language description of element
            timeout: Maximum wait time in milliseconds
        """
        prompt = f"""
Given this element description: "{element_description}"

Suggest the best Playwright wait strategy. Choose ONE from:
1. wait_for_selector - for specific elements
2. wait_for_load_state - for page loading
3. wait_for_url - for navigation
4. wait_for_timeout - for time-based waits

Return ONLY the strategy name and a brief reason in JSON format:
{{"strategy": "wait_for_selector", "reason": "Element is specific and identifiable"}}
"""
        
        try:
            response = self.ai_client.query(
                prompt,
                system_prompt='You are a test automation expert. Return only JSON.',
                temperature=0.3,
                max_tokens=100
            )
            
            # Parse response
            import json
            response_clean = response.strip()
            if '```' in response_clean:
                response_clean = response_clean.split('```')[1]
                if response_clean.startswith('json'):
                    response_clean = response_clean[4:]
            response_clean = response_clean.strip()
            
            strategy_data = json.loads(response_clean)
            strategy = strategy_data.get('strategy', 'wait_for_load_state')
            
            print(f'🤖 AI Wait Strategy: {strategy} - {strategy_data.get("reason", "")}')
            
            # Apply strategy
            if strategy == 'wait_for_load_state':
                page.wait_for_load_state('networkidle', timeout=timeout)
            elif strategy == 'wait_for_url':
                page.wait_for_url('**', timeout=timeout)
            else:
                page.wait_for_load_state('domcontentloaded', timeout=timeout)
                
        except Exception as e:
            print(f'AI wait strategy failed: {e}, using default')
            page.wait_for_load_state('domcontentloaded', timeout=timeout)
    
    def suggest_optimal_timeout(self, action_type: str) -> int:
        """
        Suggest optimal timeout for different action types
        
        Args:
            action_type: Type of action (click, navigation, api_call, etc.)
            
        Returns:
            Suggested timeout in milliseconds
        """
        timeout_map = {
            'click': 5000,
            'navigation': 30000,
            'api_call': 15000,
            'animation': 2000,
            'form_submission': 10000
        }
        
        return timeout_map.get(action_type.lower(), 10000)
