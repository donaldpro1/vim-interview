from typing import Dict, List
from .models import UserPreference, NotificationPreferences


def get_initial_users() -> List[UserPreference]:
    """Get initial mock user data."""
    return [
        UserPreference(
            userId=1,
            email="ironman@avengers.com",
            telephone="+123456789",
            preferences=NotificationPreferences(email=True, sms=True)
        ),
        UserPreference(
            userId=2,
            email="loki@avengers.com",
            telephone="+123456788",
            preferences=NotificationPreferences(email=True, sms=False)
        ),
        UserPreference(
            userId=3,
            email="hulk@avengers.com",
            telephone="+123456787",
            preferences=NotificationPreferences(email=False, sms=False)
        ),
        UserPreference(
            userId=4,
            email="blackwidow@avengers.com",
            telephone="+123456786",
            preferences=NotificationPreferences(email=True, sms=True)
        )
    ]


def get_initial_user_dict() -> Dict[int, UserPreference]:
    """Get initial users as a dictionary keyed by userId."""
    users = get_initial_users()
    return {user.userId: user for user in users}


def get_initial_email_mapping() -> Dict[str, int]:
    """Get initial email to userId mapping."""
    users = get_initial_users()
    return {user.email: user.userId for user in users} 