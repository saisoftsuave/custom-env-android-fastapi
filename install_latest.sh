#!/bin/bash

# Install Latest Build Script
# 1. Finds the latest GitHub Actions run for the current branch
# 2. Waits for it to complete
# 3. Downloads the APK artifact
# 4. Installs it on the connected Android device/emulator

set -e

echo "🔍 Finding latest workflow run..."
CURRENT_BRANCH=$(git branch --show-current)
echo "   Branch: $CURRENT_BRANCH"

# Get the Run ID of the most recent run for this branch
RUN_ID=$(gh run list --branch "$CURRENT_BRANCH" --workflow android-debug-build.yml --limit 1 --json databaseId -q ".[0].databaseId")

if [ -z "$RUN_ID" ]; then
    echo "❌ Error: No recent workflow runs found for branch '$CURRENT_BRANCH'."
    echo "   Did you run ./deploy.sh yet?"
    exit 1
fi

echo "   Latest Run ID: $RUN_ID"
echo "👀 Watching build status..."
gh run watch "$RUN_ID"

echo "📥 Downloading artifact..."
# Remove existing download if any
rm -rf app-debug
rm -f app-debug.apk

# Download to a specific directory to avoid conflicts
mkdir -p app-debug
gh run download "$RUN_ID" -n app-debug --dir app-debug

if [ ! -f "app-debug/app-debug.apk" ]; then
    echo "❌ Error: APK file not found in downloaded artifact."
    exit 1
fi

echo "📱 Installing on device..."
adb install -r -g "app-debug/app-debug.apk"

echo "🚀 Launching app..."
# Launch the main activity
adb shell monkey -p com.saibabui.androidapp -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1

echo "✨ Done! Latest build is running on your device."
