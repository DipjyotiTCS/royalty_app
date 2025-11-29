# Royalty Reconciliation Tool — Flask Version

This is a Python/Flask wrapper around your existing frontend build.  
The UI will look and behave exactly like your current app because it uses the same compiled assets from the Vite/React build (`dist/`).

## Project structure

- `app.py` — Flask application entry point
- `dist/` — pre-built frontend (HTML/CSS/JS) from your original project
- `requirements.txt` — Python dependencies

## How to run

1. **Create and activate a virtual environment (recommended)**

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   # or on cmd
   .venv\Scripts\activate.bat
   # or on macOS/Linux
   source .venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask app**

   ```bash
   python app.py
   ```

4. Open your browser at: <http://localhost:5000>

The frontend is served from the `dist/` directory, so the look and feel will stay **exactly** the same as your current TypeScript/Node-based build.
You can now extend `app.py` with API routes, database connections, authentication, etc., fully in Python.
