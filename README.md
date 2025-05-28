# Nagatha Mastodon Submind

This FastAPI-based microservice performs administrative tasks on a Mastodon server as part of the Nagatha AI system. It provides endpoints for health checks, user evaluations, activity monitoring, and more.

## Development

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root to configure environment variables.

3. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

4. Run tests:

   ```bash
   pytest --cov=app
   ```