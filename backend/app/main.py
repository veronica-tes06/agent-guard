# The FastAPI application: defines the API endpoints.

from fastapi import FastAPI
from sqlalchemy import text

from .db import engine

# Create the application. The title is shown on the /docs page.
app = FastAPI(title="AgentGuard API")


# Register the function below to handle GET requests to /api/health.
# All endpoints start with /api, so the frontend's dev server can forward them here.
@app.get("/api/health")
def health():
    """Checks the API is up and can reach MySQL."""
    try:
        # Borrow a connection from the engine and run the cheapest possible query.
        # "with" returns the connection to the pool afterwards.
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        database = "ok"
    except Exception as e:
        # SQLAlchemy wraps the driver's error. e.orig is the original MySQL message        reason = getattr(e, "orig", None) or e
        database = f"error: {reason}"
    # FastAPI converts the returned dictionary to JSON automatically.
    return {"api": "ok", "database": database}
