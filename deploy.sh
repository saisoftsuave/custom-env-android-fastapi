#!/bin/bash

# Deploy Script for Todo App
# 1. Starts Backend and Ngrok if not running
# 2. Fetches current ngrok URL
# 3. Updates Android ApiConfig
# 4. Commits and Pushes to trigger GitHub Actions

set -e

# Function to check if a process is running
is_running() {
    pgrep -f "$1" > /dev/null
}

echo "🔍 Checking system status..."

# 1. Start Backend
if ! is_running "uvicorn main:app"; then
    echo "🔸 Backend not running. Starting uvicorn..."
    cd backend
    # Check for venv
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    fi
    # Start in background and redirect output to avoid clutter
    uvicorn main:app --reload --port 8081 > ../backend.log 2>&1 &
    BACKEND_PID=$!
    echo "   Backend started (PID: $BACKEND_PID). Logs at backend.log"
    cd ..
    sleep 3 # Wait for startup
else
    echo "✅ Backend is already running."
fi

# 2. Start Ngrok
if ! curl -s http://localhost:4040/api/tunnels > /dev/null; then
    echo "🔸 Ngrok not running. Starting ngrok..."
    # Start ngrok in background
    ngrok http 8081 > ngrok.log 2>&1 &
    NGROK_PID=$!
    echo "   Ngrok started (PID: $NGROK_PID). Logs at ngrok.log"
    sleep 5 # Wait for tunnel to initialize
else
    echo "✅ Ngrok is already running."
fi

# 3. Fetch ngrok URL
echo "🎣 Fetching Ngrok URL..."
# Retry logic as it might take a moment if just started
for i in {1..5}; do
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])" 2>/dev/null || echo "")
    
    if [ -n "$NGROK_URL" ] && [ "$NGROK_URL" != "null" ]; then
        break
    fi
    echo "   Waiting for tunnel... ($i/5)"
    sleep 2
done

if [ -z "$NGROK_URL" ] || [ "$NGROK_URL" == "null" ]; then
    echo "❌ Error: Could not obtain ngrok URL. Check ngrok.log"
    exit 1
fi

echo "✅ Ngrok URL: $NGROK_URL"

# 4. Update Android Config
CONFIG_FILE="frontend/app/src/main/java/com/saibabui/androidapp/data/api/ApiConfig.kt"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Error: Config file not found at $CONFIG_FILE"
    exit 1
fi

echo "📝 Updating ApiConfig.kt..."
# Use temporary file for cross-platform compatibility
sed -i '' "s|const val BASE_URL = \".*\"|const val BASE_URL = \"$NGROK_URL\"|" "$CONFIG_FILE"

if grep -q "$NGROK_URL" "$CONFIG_FILE"; then
    echo "   Updated BASE_URL to $NGROK_URL"
else
    echo "❌ Error: Failed to update file."
    exit 1
fi

# 5. Git Operations
echo "📦 Git Operations..."

# Detect current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "   Current branch: $CURRENT_BRANCH"

git add "$CONFIG_FILE"

# Check for other changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  There are uncommitted changes in the repository:"
    git status --short
    
    read -p "❓ Do you want to commit ALL changes and push? (y/n): " -n 1 -r
    echo    # Move to a new line
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "   Staging all changes..."
        git add .
        git commit -m "Auto-deploy update: $NGROK_URL"
        echo "   Committed all changes."
        
        echo "🚀 Pushing to origin/$CURRENT_BRANCH..."
        git push origin "$CURRENT_BRANCH"
    else
        echo "⚠️  Skipping push of other changes. Only local config updated."
        exit 0
    fi
else
    # Only config file changed or no changes at all
    if git diff --staged --quiet; then
        echo "   No changes to commit (URL hasn't changed & no other changes)."
    else
        git commit -m "Update API URL to $NGROK_URL"
        echo "   Committed config changes."
        
        echo "🚀 Pushing to origin/$CURRENT_BRANCH..."
        git push origin "$CURRENT_BRANCH"
    fi
fi

echo "✨ Deploy sequence complete!"
echo "   - Backend running on port 8081"
echo "   - Ngrok tunneling $NGROK_URL -> localhost:8081"
echo "   - Android config updated"
echo "   - Changes pushed to GitHub"

