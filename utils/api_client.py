import time
import logging
import requests
from typing import Dict, Any, Optional, Union
from functools import wraps

class APIClient:
    """
    Robust API client with exponential backoff, retry logic, and comprehensive error handling.
    Designed to handle rate limits, network issues, and API outages gracefully.
    """
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.logger = logging.getLogger(__name__)

    def make_request(self, 
                    method: str, 
                    url: str, 
                    params: Optional[Dict] = None,
                    headers: Optional[Dict] = None,
                    json_data: Optional[Dict] = None,
                    timeout: int = 10,
                    custom_error_message: str = "API request failed") -> Union[Dict[str, Any], str]:
        """
        Make an HTTP request with exponential backoff and retry logic.
        
        Args:
            method: HTTP method ('GET', 'POST', etc.)
            url: The API endpoint URL
            params: Query parameters
            headers: Request headers
            json_data: JSON data for POST requests
            timeout: Request timeout in seconds
            custom_error_message: Custom error message for failures
            
        Returns:
            API response data or error message string
        """
        
        retry_delay = self.base_delay
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                self.logger.debug(f"API request attempt {attempt + 1}/{self.max_retries}: {method} {url}")
                
                # Make the request
                if method.upper() == 'GET':
                    response = requests.get(url, params=params, headers=headers, timeout=timeout)
                elif method.upper() == 'POST':
                    response = requests.post(url, params=params, headers=headers, json=json_data, timeout=timeout)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Handle different response codes
                if response.status_code == 200:
                    return response.json()
                    
                elif response.status_code == 429:  # Rate limit
                    if attempt < self.max_retries - 1:
                        self.logger.warning(f"Rate limit hit (429), retrying in {retry_delay} seconds... (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(retry_delay)
                        retry_delay = min(retry_delay * 2, self.max_delay)  # Exponential backoff with cap
                        continue
                    else:
                        return f"{custom_error_message}: Rate limit exceeded. Please try again in a few moments."
                        
                elif response.status_code == 403:
                    return f"{custom_error_message}: Access forbidden. Please check your API key permissions."
                    
                elif response.status_code == 404:
                    return f"{custom_error_message}: Endpoint not found. Please check the API URL."
                    
                elif response.status_code == 500:
                    if attempt < self.max_retries - 1:
                        self.logger.warning(f"Server error (500), retrying in {retry_delay} seconds... (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(retry_delay)
                        retry_delay = min(retry_delay * 2, self.max_delay)
                        continue
                    else:
                        return f"{custom_error_message}: Server error. Please try again later."
                        
                elif response.status_code == 502 or response.status_code == 503:
                    if attempt < self.max_retries - 1:
                        self.logger.warning(f"Service unavailable ({response.status_code}), retrying in {retry_delay} seconds... (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(retry_delay)
                        retry_delay = min(retry_delay * 2, self.max_delay)
                        continue
                    else:
                        return f"{custom_error_message}: Service temporarily unavailable. Please try again later."
                        
                else:
                    # Other HTTP errors
                    if attempt < self.max_retries - 1:
                        self.logger.warning(f"HTTP error {response.status_code}, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(retry_delay)
                        retry_delay = min(retry_delay * 2, self.max_delay)
                        continue
                    else:
                        return f"{custom_error_message}: HTTP {response.status_code} error."
                        
            except requests.exceptions.Timeout:
                last_exception = "Request timeout"
                if attempt < self.max_retries - 1:
                    self.logger.warning(f"Request timeout, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, self.max_delay)
                    continue
                    
            except requests.exceptions.ConnectionError:
                last_exception = "Connection error"
                if attempt < self.max_retries - 1:
                    self.logger.warning(f"Connection error, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, self.max_delay)
                    continue
                    
            except requests.exceptions.RequestException as e:
                last_exception = str(e)
                if attempt < self.max_retries - 1:
                    self.logger.warning(f"Request error: {e}, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, self.max_delay)
                    continue
                    
            except Exception as e:
                last_exception = str(e)
                if attempt < self.max_retries - 1:
                    self.logger.warning(f"Unexpected error: {e}, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, self.max_delay)
                    continue
        
        # All retries exhausted
        return f"{custom_error_message}: {last_exception}. Please try again later."

# Global instance for reuse across the application
api_client = APIClient(max_retries=3, base_delay=1.0, max_delay=60.0)

def with_retry(max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
    """
    Decorator to add exponential backoff retry logic to any function.
    
    Usage:
    @with_retry(max_retries=3, base_delay=1.0)
    def my_api_call():
        # Your API call code here
        pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_delay = base_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logging.warning(f"Function {func.__name__} failed (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        retry_delay = min(retry_delay * 2, max_delay)
                        continue
                    else:
                        logging.error(f"Function {func.__name__} failed after {max_retries} attempts: {e}")
                        raise last_exception
                        
        return wrapper
    return decorator
