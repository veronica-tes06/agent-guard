# Database setup: creates the connection to MySQL that the rest of the backend uses.

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Read backend/.env and put its values into environment variables.
# It looks in the current folder, which is why uvicorn is started from backend/.
load_dotenv()

# Database address from .env. The second argument is a fallback used if .env is missing.
DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+pymysql://agentguard:agentguard@localhost:3307/agentguard"
)

# The engine holds a pool of reusable connections to MySQL.
# pool_pre_ping checks a connection is still alive before using it, so requests don't fail after MySQL restarts.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


