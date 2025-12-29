# Automated Development Workflow

Production-ready workflow for automated Android app development, testing, and deployment.

## 🚀 Quick Start

### One-Command Automated Workflow
```bash
python3 scripts/workflow_orchestrator.py "Your feature description here"
```

This will automatically:
1. ✅ Validate environment
2. 📋 Create implementation plan
3. 🏗️ Build locally
4. 🚢 Deploy to CI/CD
5. 📱 Install on emulator
6. 🧪 Run automated tests
7. 📊 Generate reports

## 📋 Manual Workflow

### 1. Deploy Changes
```bash
./deploy.sh
```
- Auto-starts backend + ngrok
- Updates API configuration
- Pushes to GitHub
- Triggers CI build

### 2. Install Latest Build
```bash
./install_latest.sh
```
- Auto-starts emulator if needed
- Downloads latest APK
- Installs and launches app

### 3. Run Automated Tests
```bash
# Use the test runner
python3 scripts/test_runner.py my_feature_test

# Or run a specific test script
python3 scripts/example_todo_test.py
```

## 🧪 Writing Tests

Create a new test file in `scripts/`:

```python
from test_runner import AndroidTestRunner, TestStep

def test_my_feature():
    runner = AndroidTestRunner(output_dir="test_results/my_feature")
    
    steps = [
        TestStep(
            name="Wait for app",
            action="wait",
            wait_after=2.0,
            screenshot_name="01_loaded"
        ),
        TestStep(
            name="Tap button",
            action="tap",
            element_text="ButtonText",  # Finds element dynamically!
            screenshot_name="02_tapped"
        ),
    ]
    
    for step in steps:
        runner.execute_step(step)
    
    return runner.generate_report()
```

## 📸 Test Actions

- `action="tap"` - Tap at coordinates or use `element_text` for dynamic finding
- `action="swipe"` - Swipe gesture  
- `action="input"` - Type text
- `action="back"` - Press back button
- `action="wait"` - Wait/delay
- `action="screenshot"` - Capture screenshot

## 📁 File Structure

```
custom-env-android-fastapi/
├── scripts/
│   ├── test_runner.py           # Test framework
│   ├── workflow_orchestrator.py # Complete automation
│   └── example_todo_test.py     # Example test
├── test_results/                # Test outputs
│   └── <test_name>_<timestamp>/
│       ├── *.png                # Screenshots
│       └── test_report.json     # Results
├── workflow_runs/               # Workflow logs
├── deploy.sh                    # Deployment script
└── install_latest.sh            # Installation script
```

## 🔧 Configuration

### Prerequisites
- Android emulator (auto-starts)
- Python 3.8+
- ADB in PATH
- Git configured
- FastAPI backend
- GitHub CLI (`gh`)

### One-Time Setup
```bash
chmod +x deploy.sh install_latest.sh
chmod +x scripts/*.py
pip3 install pillow pytesseract opencv-python
gh auth status
```

## 📊 Features

### ✅ Automated Orchestration
- Complete hands-free workflow execution
- Automatic error detection and retry logic
- Build validation before deployment
- Comprehensive logging

### ✅ Dynamic Element Finding
- No hardcoded coordinates
- Searches by text or content-desc
- Automatic coordinate calculation

### ✅ Screenshot Capture
- Automatic screenshot at each step
- Timestamped filenames
- Saved with test results

### ✅ Error Detection
- Logcat monitoring
- Build error parsing
- Performance metrics

### ✅ Emulator Management
- Auto-starts if not running
- Waits for boot completion
- Healthchecks

## 🎯 Workflow Slash Command

Use the `/auto-dev-test` slash command in the agent to access the full workflow documentation.

## 📚 Examples

### Run Complete Workflow
```bash
python3 scripts/workflow_orchestrator.py "Add dark mode toggle"
```

### Run Just Tests (Skip Workflow)
```bash
python3 scripts/test_runner.py dark_mode_test
```

### Deploy and Install Only
```bash
./deploy.sh && ./install_latest.sh
```

### Check Logs
```bash
# Workflow logs
cat workflow_runs/<timestamp>/workflow.log

# Test results
cat test_results/<test>_<timestamp>/test_report.json

# App logs
adb logcat | grep "com.saibabui.androidapp"
```

## 🐛 Troubleshooting

### Build Failures
```bash
cd frontend
./gradlew clean assembleDebug --stacktrace
```

### Emulator Issues
```bash
emulator -list-avds
emulator -avd Pixel_6 -no-snapshot-load
```

### Test Failures
```bash
# Dump UI for debugging
adb shell uiautomator dump
adb pull /sdcard/window_dump.xml
```

## 🎉 Success Criteria

- ✅ Local build succeeds
- ✅ CI build succeeds  
- ✅ APK installs without errors
- ✅ All test steps pass
- ✅ No crashes in logs
- ✅ Screenshots show expected flow

---

**Made with ❤️ for automated Android development**
