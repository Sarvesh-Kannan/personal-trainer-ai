import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Default configuration that can be overridden by environment variables
class Config:
    """Configuration class for the application"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY")
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL", "YOUR_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "YOUR_API_KEY")
    
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
