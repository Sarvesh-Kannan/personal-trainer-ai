import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Default configuration that can be overridden by environment variables
class Config:
    """Configuration class for the application"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCt6NWL9kIkw3b9Z1Ad86X47piJSKjrEks")
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL", "https://gaoljwhtzjpaeaegwxes.supabase.co")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdhb2xqd2h0empwYWVhZWd3eGVzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NjUyNDQ0MCwiZXhwIjoyMDYyMTAwNDQwfQ.cvKWmWzsG7OiXSLTQRGeX1FMco29Miz_e9HTuMRMAFQ")
    
    # Flask Configuration
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"  # Convert string to boolean
    
    # Other Configuration
    PORT = int(os.getenv("PORT", "5000"))
    
    @classmethod
    def get_supabase_credentials(cls):
        """Get Supabase credentials as a dictionary"""
        return {
            "url": cls.SUPABASE_URL,
            "key": cls.SUPABASE_KEY
        }
        
    @classmethod
    def get_gemini_config(cls):
        """Get Gemini API configuration"""
        return {
            "api_key": cls.GEMINI_API_KEY,
            "generation_config": {
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
        } 