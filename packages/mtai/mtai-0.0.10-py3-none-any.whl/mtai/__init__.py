import os

"""Script used to define constants used across codebase."""

SECRET_KEY = os.getenv("SECRET_KEY", None)
API_URL = "https://api.ai.mediatranscribe.com/api/v1/ai"
