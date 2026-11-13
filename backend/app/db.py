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

# Factory for sessions. A session is how rows will be read and written through SQLAlchemy.
# Not used yet: needed once the first tables are added.
SessionLocal = sessionmaker(bind=engine, autoflush=False)

# Parent class for future table definitions, e.g. "class Policy(Base): ...".
# Not used yet either.
Base = declarative_base()
