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

# Detect Android SDK location
if [ -z "$ANDROID_HOME" ]; then
    # Common locations for Android SDK on macOS
    POSSIBLE_SDK_PATHS=(
        "$HOME/Library/Android/sdk"
        "$HOME/Android/sdk"
        "/usr/local/android-sdk"
    )
    
    for SDK_PATH in "${POSSIBLE_SDK_PATHS[@]}"; do
        if [ -d "$SDK_PATH" ]; then
            export ANDROID_HOME="$SDK_PATH"
            break
        fi
    done
fi

# Set up emulator path
if [ -n "$ANDROID_HOME" ]; then
    EMULATOR_CMD="$ANDROID_HOME/emulator/emulator"
    # Also add to PATH for other tools
    export PATH="$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools:$PATH"
else
    # Try to find emulator in PATH
    EMULATOR_CMD=$(which emulator 2>/dev/null || echo "")
fi

# Check if emulator is running
echo "🔍 Checking for active emulator..."
DEVICE_COUNT=$(adb devices | grep -v "List of devices" | grep -c "device$" || true)

if [ "$DEVICE_COUNT" -eq 0 ]; then
    echo "⚠️  No emulator detected. Starting emulator..."
    
    # Verify emulator command exists
    if [ -z "$EMULATOR_CMD" ] || [ ! -f "$EMULATOR_CMD" ]; then
        echo "❌ Error: Emulator command not found."
        echo "   Please ensure Android SDK is installed and ANDROID_HOME is set."
        echo "   Common location on macOS: ~/Library/Android/sdk"
        exit 1
    fi
    
    # Get list of available AVDs
    AVDS=$("$EMULATOR_CMD" -list-avds)
    
    if [ -z "$AVDS" ]; then
        echo "❌ Error: No Android Virtual Devices (AVDs) found."
        echo "   Please create an AVD using Android Studio first."
        exit 1
    fi
    
    # Get the first AVD
    FIRST_AVD=$(echo "$AVDS" | head -n 1)
    echo "   Starting AVD: $FIRST_AVD"
    
    # Start emulator in background
    "$EMULATOR_CMD" -avd "$FIRST_AVD" -no-snapshot-load -no-audio > /dev/null 2>&1 &
    EMULATOR_PID=$!
    
    echo "⏳ Waiting for emulator to boot (this may take 1-2 minutes)..."
    
    # Wait for device to be detected
    TIMEOUT=120  # 2 minutes timeout
    ELAPSED=0
    while [ "$ELAPSED" -lt "$TIMEOUT" ]; do
        sleep 2
        ELAPSED=$((ELAPSED + 2))
        
        # Check if emulator is online
        BOOT_STATUS=$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')
        
        if [ "$BOOT_STATUS" = "1" ]; then
            echo "✅ Emulator is ready!"
            break
        fi
        
        # Show progress every 10 seconds
        if [ $((ELAPSED % 10)) -eq 0 ]; then
            echo "   Still booting... ($ELAPSED seconds elapsed)"
        fi
    done
    
    if [ "$ELAPSED" -ge "$TIMEOUT" ]; then
        echo "❌ Error: Emulator failed to boot within $TIMEOUT seconds."
        echo "   Please check Android Studio or start the emulator manually."
        exit 1
    fi
    
    # Wait a bit more for UI to stabilize
    echo "⏳ Waiting for UI to stabilize..."
    sleep 5
else
    echo "✅ Emulator is already running"
fi

echo "📱 Installing on device..."
adb install -r -g "app-debug/app-debug.apk"

echo "🚀 Launching app..."
# Launch the main activity
adb shell monkey -p com.saibabui.androidapp -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1

echo "✨ Done! Latest build is running on your device."
