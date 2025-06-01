from typing import Dict, Optional
from .data.models import UserPreference
from .data import get_initial_user_dict, get_initial_email_mapping


class UserDatabase:
    """In-memory database for user preferences."""
    
    def __init__(self):
        # Initialize with mock data from external source
        self._user_preferences: Dict[int, UserPreference] = get_initial_user_dict()
        # Convenience mapping for email to userId
        self._email_to_user_id: Dict[str, int] = get_initial_email_mapping()
    
    def get_all_users(self) -> list[UserPreference]:
        """Get all user preferences."""
        return list(self._user_preferences.values())
    
    def get_user_by_id(self, user_id: int) -> Optional[UserPreference]:
        """Get user by ID."""
        return self._user_preferences.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[UserPreference]:
        """Get user by email."""
        user_id = self._email_to_user_id.get(email)
        if user_id:
            return self._user_preferences.get(user_id)
        return None
    
    def create_user(self, user: UserPreference) -> UserPreference:
        """Create a new user."""
        self._user_preferences[user.userId] = user
        self._email_to_user_id[user.email] = user.userId
        return user
    
    def update_user(self, user_id: int, user: UserPreference) -> UserPreference:
        """Update an existing user."""
        old_user = self._user_preferences.get(user_id)
        if old_user and old_user.email != user.email:
            # Update email mapping if email changed
            del self._email_to_user_id[old_user.email]
            self._email_to_user_id[user.email] = user_id
        
        user.userId = user_id  # Ensure consistency
        self._user_preferences[user_id] = user
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        user = self._user_preferences.get(user_id)
        if user:
            del self._email_to_user_id[user.email]
            del self._user_preferences[user_id]
            return True
        return False
    
    def get_next_user_id(self) -> int:
        """Get the next available user ID."""
        return max(self._user_preferences.keys()) + 1 if self._user_preferences else 1
    
    def user_exists_by_id(self, user_id: int) -> bool:
        """Check if user exists by ID."""
        return user_id in self._user_preferences
    
    def user_exists_by_email(self, email: str) -> bool:
        """Check if user exists by email."""
        return email in self._email_to_user_id


# Global database instance
user_db = UserDatabase() 