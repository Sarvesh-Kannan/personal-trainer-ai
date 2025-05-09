import os
from supabase import create_client
from utils.config import Config

class SupabaseClient:
    def __init__(self):
        """Initialize the Supabase client with credentials from configuration"""
        credentials = Config.get_supabase_credentials()
        self.supabase_url = credentials["url"]
        self.supabase_key = credentials["key"]
        
        if not self.supabase_url or not self.supabase_key:
            print("Warning: Supabase credentials not found in environment variables.")
            # Using mock mode if credentials aren't available
            self.mock_mode = True
        else:
            self.supabase = create_client(self.supabase_url, self.supabase_key)
            self.mock_mode = False
    
    def create_user(self, user_data):
        """Create a new user in the database"""
        if self.mock_mode:
            # Mock implementation for testing without database
            return {"id": "mock-user-id", **user_data}
            
        # Insert user data into users table
        result = self.supabase.table('users').insert(user_data).execute()
        return result.data[0] if result.data else None
    
    def get_user(self, user_id):
        """Get user data by ID"""
        if self.mock_mode:
            # Mock implementation
            return {"id": user_id, "name": "Test User", "email": "test@example.com"}
            
        # Query user data
        result = self.supabase.table('users').select('*').eq('id', user_id).execute()
        return result.data[0] if result.data else None
    
    def update_user(self, user_id, updated_data):
        """Update user data"""
        if self.mock_mode:
            # Mock implementation
            return {"id": user_id, **updated_data}
            
        # Update user data
        result = self.supabase.table('users').update(updated_data).eq('id', user_id).execute()
        return result.data[0] if result.data else None
    
    def save_plan(self, user_id, plan_data):
        """Save a fitness plan for a user"""
        if self.mock_mode:
            # Mock implementation
            return {"id": "mock-plan-id", "user_id": user_id, **plan_data}
            
        # Add user_id to plan data
        plan_data["user_id"] = user_id
        
        # Insert plan data
        result = self.supabase.table('fitness_plans').insert(plan_data).execute()
        return result.data[0] if result.data else None
    
    def get_plan(self, user_id):
        """Get the latest fitness plan for a user"""
        if self.mock_mode:
            # Mock implementation
            return {
                "id": "mock-plan-id", 
                "user_id": user_id,
                "mealPlan": {"days": 7},
                "workoutPlan": {"days": 5},
                "created_at": "2023-01-01T00:00:00"
            }
            
        # Query plan data, ordered by creation date (newest first)
        result = self.supabase.table('fitness_plans').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(1).execute()
        return result.data[0] if result.data else None 