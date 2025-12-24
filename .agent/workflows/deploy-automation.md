---
description: Automatically sync ngrok URL and trigger CI build
---

# One-Command Deploy

Use the `deploy.sh` script to automatically:
1. Fetch your local ngrok URL
2. Update the Android app configuration
3. Push changes to GitHub to trigger a debug build

## Usage

1. **Ensure Backend & Ngrok are running** (as per [Ngrok Workflow](ngrok-backend.md))

2. **Run the script**:
   ```bash
   chmod +x deploy.sh  # Only needed once
   ./deploy.sh
   ```

## What it does

- **Checks & Starts Services**: Automatically starts FastAPI backend (port 8081) and Ngrok if they aren't running
- **Fetches URL**: Gets the public HTTPS URL from ngrok
- **Updates Config**: Updates `ApiConfig.kt` with the new URL
- **Deploys**: Commits changes and pushes to `main` branch to trigger CI build
