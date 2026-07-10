import json
from helpers.ai_client import AIClient


class TestDataGenerator:
    """AI-powered test data generator"""
    
    def __init__(self):
        self.ai_client = AIClient()
    
    def generate_checkout_data(self) -> dict:
        """
        Generate realistic checkout form data using AI
        
        Returns:
            Dictionary with firstName, lastName, postalCode
        """
        prompt = """
Generate realistic test data for an e-commerce checkout form.
Return ONLY a JSON object with these fields:
- firstName: A realistic first name
- lastName: A realistic last name
- postalCode: A valid US ZIP code (5 digits)

Example format:
{"firstName": "John", "lastName": "Smith", "postalCode": "12345"}

Generate different data each time. Return ONLY the JSON, no explanation.
"""
        
        system_prompt = 'You are a test data generator. Return only valid JSON.'
        
        try:
            response = self.ai_client.query(
                prompt,
                system_prompt=system_prompt,
                temperature=0.8,
                max_tokens=100
            )
            
            # Clean response
            response_clean = response.strip()
            if response_clean.startswith('```json'):
                response_clean = response_clean[7:]
            if response_clean.startswith('```'):
                response_clean = response_clean[3:]
            if response_clean.endswith('```'):
                response_clean = response_clean[:-3]
            response_clean = response_clean.strip()
            
            data = json.loads(response_clean)
            
            # Validate required fields
            if all(key in data for key in ['firstName', 'lastName', 'postalCode']):
                return data
            else:
                return self._get_fallback_data()
                
        except Exception as e:
            print(f'AI data generation failed: {e}, using fallback')
            return self._get_fallback_data()
    
    def generate_user_credentials(self, user_type: str = 'standard') -> dict:
        """
        Generate user credentials for testing
        
        Args:
            user_type: Type of user (standard, admin, guest)
            
        Returns:
            Dictionary with username, password, email
        """
        prompt = f"""
Generate realistic test credentials for a {user_type} user account.
Return ONLY a JSON object with:
- username: A realistic username (lowercase, no spaces)
- password: A strong password (8-12 chars, mixed case, numbers)
- email: A realistic email address

Return ONLY the JSON, no explanation.
"""
        
        try:
            response = self.ai_client.query(
                prompt,
                system_prompt='You are a test data generator. Return only valid JSON.',
                temperature=0.7,
                max_tokens=150
            )
            
            response_clean = response.strip()
            if '```' in response_clean:
                response_clean = response_clean.split('```')[1]
                if response_clean.startswith('json'):
                    response_clean = response_clean[4:]
            response_clean = response_clean.strip()
            
            return json.loads(response_clean)
        except Exception:
            return {
                'username': f'{user_type}_user_test',
                'password': 'Test123!',
                'email': f'{user_type}@test.com'
            }
    
    def _get_fallback_data(self) -> dict:
        """Fallback data if AI generation fails"""
        return {
            'firstName': 'Test',
            'lastName': 'User',
            'postalCode': '12345'
        }
