from helpers.ai_client import AIClient


class SelectorGenerator:
    """AI-powered selector generator helper"""
    
    def __init__(self):
        self.ai_client = AIClient()
    
    def generate_selector(self, element_description: str, page_context: str = '') -> str:
        """
        Generate a robust selector for an element based on description
        
        Args:
            element_description: Description of the element to locate
            page_context: Optional context about the page
            
        Returns:
            Generated selector string
        """
        prompt = f"""
Generate a robust Playwright selector for the following element:
Element: {element_description}
{f'Page Context: {page_context}' if page_context else ''}

Requirements:
- Prefer data-testid, aria-label, or role-based selectors
- Avoid fragile selectors like nth-child or absolute paths
- Return ONLY the selector string, no explanation
- Use Playwright syntax (e.g., 'button[name="submit"]', 'text=Login', '[data-testid="user-menu"]')

Selector:"""

        system_prompt = 'You are an expert in web automation and CSS selectors. Generate robust, maintainable selectors for Playwright tests.'
        
        selector = self.ai_client.query(
            prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=100
        )
        
        return selector.replace('```', '').replace('`', '').strip()
    
    def suggest_alternatives(self, failed_selector: str, error_message: str) -> list[str]:
        """
        Suggest alternative selectors if the primary one fails
        
        Args:
            failed_selector: The selector that failed
            error_message: Error message from the failure
            
        Returns:
            List of alternative selectors
        """
        prompt = f"""
A Playwright selector failed:
Selector: {failed_selector}
Error: {error_message}

Suggest 3 alternative selectors that might work better.
Return them as a JSON array of strings, nothing else.

Example format: ["selector1", "selector2", "selector3"]"""

        system_prompt = 'You are an expert in debugging web automation selectors. Provide practical alternatives.'
        
        response = self.ai_client.query(
            prompt,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=200
        )
        
        try:
            import json
            return json.loads(response)
        except:
            return [failed_selector]
