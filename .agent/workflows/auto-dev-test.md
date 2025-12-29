---
description: Automated development cycle with planning, coding, deployment, and screenshot verification
---

# Automated Development & Testing Workflow

This workflow automates the complete development cycle from planning to verification using screenshots and intelligent testing.

## Prerequisites

### Required Tools
- ✅ Android emulator (auto-starts if not running)
- ✅ Python 3.8+ 
- ✅ ADB in PATH
- ✅ Git configured
- ✅ Backend server (FastAPI)
- ✅ GitHub CLI (`gh`) configured

### Setup (One-time)

```bash
# Make scripts executable
chmod +x deploy.sh install_latest.sh

# Install Python dependencies (if needed)
pip3 install pillow pytesseract opencv-python

# Verify GitHub CLI authentication
gh auth status
```

## Quick Start

### Option 1: Automated Orchestration (Recommended)
Use the workflow orchestrator for hands-free execution:

```bash
python3 scripts/workflow_orchestrator.py "Add dark mode toggle to settings"
```

The orchestrator will:
1. ✅ Validate environment
2. 📋 Create implementation plan  
3. 🏗️ Build locally (with retry logic)
4. 🚢 Deploy and trigger CI
5. 📱 Install APK on emulator
6. 🧪 Run automated tests
7. ✔️ Verify implementation
8. 📊 Generate comprehensive report

### Option 2: Manual Step-by-Step
Follow the stages below for manual execution.

---

## Workflow Stages

### Stage 1: Environment Validation

Verify all prerequisites before starting:

```bash
# Check emulator status
adb devices | grep "emulator"

# Verify backend connectivity  
curl http://localhost:8081/health

# Confirm Git status
git status

# Validate Python environment
python3 --version
```

**Success Criteria:**
- ✅ Emulator online (or auto-starts)
- ✅ Backend accessible
- ✅ Git workspace clean
- ✅ Required tools available

---

### Stage 2: Planning & Context Gathering

The agent analyzes the prompt and creates a detailed plan:

- **Intent Classification**: Feature, bug fix, refactor, or UI change
- **Scope Detection**: Affected layers (UI, logic, backend, database)  
- **Dependency Mapping**: Related components
- **Risk Assessment**: High-risk areas

**Plan Output**: 
- Files to modify/create
- Implementation steps
- Testing strategy
- Success criteria

---

### Stage 3: Code Implementation

Write code following best practices:

**Quality Gates:**
- ✅ Lint checks pass
- ✅ No hardcoded strings
- ✅ Error handling implemented
- ✅ Logging added
- ✅ Comments for complex logic

---

### Stage 4: Local Build & Fix Issues

// turbo
Build locally before deploying:

```bash
cd /Users/softsuave/Documents/custom-env-android-fastapi/frontend
./gradlew assembleDebug
```

**If build fails:**
1. Review error messages
2. Fix compilation errors
3. Update dependencies if needed
4. Re-run build
5. **Repeat until successful**

**Only proceed after successful local build!**

---

### Stage 5: Deployment

// turbo
Deploy changes and trigger CI build:

```bash
cd /Users/softsuave/Documents/custom-env-android-fastapi
./deploy.sh
```

This script:
- Checks & starts backend + ngrok (if not running)
- Fetches ngrok public URL
- Updates `ApiConfig.kt`
- Commits and pushes to GitHub
- Triggers GitHub Actions build

**Monitor build status:**
```bash
gh run watch
```

---

### Stage 6: Installation

// turbo
Install built APK on emulator:

```bash
cd /Users/softsuave/Documents/custom-env-android-fastapi
./install_latest.sh
```

This script:
- Checks for running emulator (auto-starts if needed)
- Downloads latest APK from GitHub release
- Installs on emulator with `-r` flag
- Launches the app

---

### Stage 7: Automated Testing

// turbo
Run automated UI tests with screenshot capture:

```bash
cd /Users/softsuave/Documents/custom-env-android-fastapi
python3 scripts/test_runner.py <test_name>
```

**Example Test Script**: Create `scripts/my_feature_test.py`

```python
from test_runner import AndroidTestRunner, TestStep

def test_my_feature():
    runner = AndroidTestRunner(output_dir="test_results/my_feature")
    
    steps = [
        TestStep(
            name="App loaded",
            action="wait",
            wait_after=3.0,
            screenshot_name="01_app_loaded"
        ),
        TestStep(
            name="Tap settings button",
            action="tap",
            element_text="Settings",  # Finds element dynamically!
            wait_after=1.0,
            screenshot_name="02_settings_opened"
        ),
        TestStep(
            name="Toggle feature",
            action="tap",
            coordinates=(600, 400),
            wait_after=1.0,
            screenshot_name="03_feature_enabled"
        ),
        TestStep(
            name="Navigate back",
            action="back",
            wait_after=1.0,
            screenshot_name="04_back_to_home"
        ),
    ]
    
    for step in steps:
        runner.execute_step(step)
    
    return runner.generate_report()
```

**Dynamic Element Finding**: Use `element_text` instead of hardcoded coordinates!

---

### Stage 8: Screenshot Verification

Review captured screenshots:

```bash
# Screenshots saved in:
test_results/<test_name>_<timestamp>/*.png

# View test report:
cat test_results/<test_name>_<timestamp>/test_report.json
```

**Verification Checklist:**
- ✅ UI elements are visible and correct
- ✅ Text content matches requirements
- ✅ Navigation flow works end-to-end
- ✅ No visual regressions
- ✅ Error states handled properly

---

### Stage 9: Log Analysis

Check for errors and crashes:

```bash
# View app-specific errors
adb logcat | grep "com.saibabui.androidapp"

# Check for crashes
adb logcat | grep -i "fatal\|exception"

# Performance metrics
adb shell dumpsys meminfo com.saibabui.androidapp
```

---

### Stage 10: Final Verdict

**SUCCESS Criteria:**
- ✅ All planned features implemented
- ✅ Local build succeeds
- ✅ CI build succeeds
- ✅ APK installs without errors
- ✅ Screenshots show expected UI flow
- ✅ No crashes in logs
- ✅ Performance metrics acceptable

**If SUCCESSFUL:**
- 🎉 Mark workflow complete
- 📦 Archive screenshots with timestamp
- 📝 Generate summary report
- ✅ Ready for review/merge

**If FAILED:**
- 🔍 Identify root cause
- 📋 List specific failures
- 🔧 Suggest fixes
- ↩️ Optional: Rollback changes

---

## Advanced Features

### 1. Parallel Test Execution
Run multiple test scenarios:

```bash
python3 scripts/test_runner.py login_flow &
python3 scripts/test_runner.py todo_crud &
wait
```

### 2. Performance Monitoring

```bash
# CPU usage
adb shell top -n 1 | grep com.saibabui.android app

# Memory usage  
adb shell dumpsys meminfo com.saibabui.androidapp | grep TOTAL

# Battery impact
adb shell dumpsys batterystats | grep com.saibabui.androidapp
```

### 3. Video Recording

```bash
# Start recording
adb shell screenrecord /sdcard/test.mp4 &
RECORD_PID=$!

# Run your test
python3 scripts/test_runner.py my_test

# Stop recording
kill $RECORD_PID
adb pull /sdcard/test.mp4
```

---

## Configuration

### Workflow Settings
Create `config/workflow_config.json`:

```json
{
  "emulator_name": "Pixel_6",
  "build_timeout_minutes": 10,
  "test_retry_attempts": 2,
  "screenshot_comparison_threshold": 0.95,
  "auto_rollback_on_failure": false
}
```

---

## Troubleshooting

### Build Failures
```bash
# Clean build
cd frontend
./gradlew clean

# Check for dependency issues
./gradlew dependencies

# Verbose build output
./gradlew assembleDebug --stacktrace
```

### Emulator Issues
```bash
# List available AVDs
emulator -list-avds

# Cold boot emulator
emulator -avd Pixel_6 -no-snapshot-load

# Reset emulator
adb shell pm clear com.saibabui.androidapp
```

### Test Failures
```bash
# Dump UI hierarchy for debugging
adb shell uiautomator dump
adb pull /sdcard/window_dump.xml
cat window_dump.xml
```

---

## File Structure

```
custom-env-android-fastapi/
├── scripts/
│   ├── test_runner.py          # Automated test framework
│   ├── workflow_orchestrator.py # Complete workflow automation
│   └── my_feature_test.py      # Your custom tests
├── test_results/
│   └── <test_name>_<timestamp>/
│       ├── *.png               # Screenshots
│       └── test_report.json    # Test results
├── workflow_runs/
│   └── <timestamp>/
│       ├── workflow.log        # Execution log
│       └── plan.json           # Implementation plan
├── deploy.sh                   # Deployment script
└── install_latest.sh           # Installation script
```

---

## CI/CD Integration

The workflow integrates with GitHub Actions:

1. **Trigger**: `git push` runs `android-debug-build.yml`
2. **Build**: Compiles APK and runs unit tests
3. **Artifact**: Uploads `app-debug.apk`
4. **Release**: Creates GitHub release with APK
5. **Install**: `install_latest.sh` downloads and installs

---

## Best Practices

1. **Always build locally first** - Catch errors before CI
2. **Use dynamic element finding** - Avoid hardcoded coordinates
3. **Capture screenshots at key points** - Evidence of flow
4. **Check logs after tests** - Find hidden errors
5. **Archive successful test results** - Baseline for regression
6. **Document test scenarios** - Make tests maintainable

---

## Example: Complete Workflow Run

```bash
# 1. Start workflow orchestrator
python3 scripts/workflow_orchestrator.py "Add swipe to delete for tasks"

# Output will show:
# 🚀 Starting Automated Workflow
# 🔍 Stage 1: Environment Validation  
# 📋 Stage 2: Planning
# 🏗️ Stage 3: Local Build & Validation
# 🚢 Stage 4: Deployment
# 📱 Stage 5: Installation
# 🧪 Stage 6: Automated Testing
# ✔️ Stage 7: Verification
# ✅ WORKFLOW COMPLETED SUCCESSFULLY

# 2. Review results
cat workflow_runs/<timestamp>/workflow.log
open test_results/add_swipe_to_delete_*/
```

---

## Notes

- Screenshots saved in `test_results/YYYY-MM-DD_HH-MM-SS/`
- Logs saved in `workflow_runs/<timestamp>/workflow.log`
- Build wait time typically 3-5 minutes
- Test execution time depends on scenario complexity
- Dynamic element finding adds ~1-2s per interaction

**This workflow is production-ready and battle-tested!** 🚀

