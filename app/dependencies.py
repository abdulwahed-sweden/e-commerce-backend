"""
Dependency injections for the application
"""
from .database import get_db

# Re-export get_db for consistency
get_db = get_db