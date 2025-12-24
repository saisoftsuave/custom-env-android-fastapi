---
description: Run the FastAPI backend with ngrok for Android app testing
---

# Running Backend with Ngrok

This workflow exposes the local FastAPI backend via ngrok for Android app connectivity.

## Prerequisites

1. **Install ngrok** (if not already installed):
   ```bash
   # On macOS
   brew install ngrok/ngrok/ngrok
   ```

2. **Authenticate ngrok** (one-time setup):
   - Sign up at https://ngrok.com
   - Get your auth token from the dashboard
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN
   ```

## Steps

// turbo-all

1. **Start the FastAPI backend**:
   ```bash
   cd /Users/softsuave/Documents/custom-env-android-fastapi/backend
   source .venv/bin/activate  # If using virtual environment
   uvicorn main:app --reload --port 8081
   ```

2. **In a new terminal, start ngrok**:
   ```bash
   ngrok http 8081
   ```

3. **Copy the HTTPS URL** from ngrok output (e.g., `https://xxxx-xxxx.ngrok.io`)

4. **Update Android app configuration**:
   - Open `frontend/app/src/main/java/com/saibabui/androidapp/data/api/ApiConfig.kt`
   - Replace `BASE_URL` with the ngrok URL

5. **Build and run the Android app**:
   ```bash
   cd /Users/softsuave/Documents/custom-env-android-fastapi/frontend
   ./gradlew installDebug
   ```

## Notes

- Ngrok free tier provides a random URL that changes each restart
- The backend must be running before starting ngrok
- Keep both terminals open during testing
