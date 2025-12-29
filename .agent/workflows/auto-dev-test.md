---
description: Automated development cycle with planning, coding, deployment, and screenshot verification
---

# Automated Development & Testing Workflow

This workflow automates the complete development cycle from planning to verification using screenshots.

## Prerequisites
- Android emulator is running
- Python environment is set up
- Backend server is accessible
- deploy.sh script is configured

## Workflow Steps

### 1. Receive Feature Prompt
The user provides a feature request or requirement prompt describing what needs to be implemented.

### 2. Create Implementation Plan
The agent analyzes the prompt and creates a detailed plan including:
- Feature requirements breakdown
- Component/file changes needed
- UI/UX considerations
- Testing approach
- Expected user flow

### 3. Define Executable Steps
Break down the plan into specific, actionable steps:
- List all files to be modified or created
- Define the order of implementation
- Identify dependencies
- Specify success criteria

### 4. Write the Code
Implement the changes according to the plan:
- Create/modify Android app code (Kotlin/Java)
- Update backend FastAPI code if needed
- Ensure code follows best practices
- Add necessary imports and dependencies

### 5. Build Locally
// turbo
Build the Android app locally to check for compilation errors:
```bash
cd /Users/softsuave/Documents/custom-env-android-fastapi
./gradlew assembleDebug
```

This will:
- Compile all source code
- Check for syntax errors
- Verify dependencies
- Generate build output/logs

### 6. Check Build Errors
Analyze the build output:
- Check if build succeeded or failed
- Review error messages and warnings
- Identify compilation issues
- Note any missing dependencies or imports
- Check for lint errors or warnings

### 7. Fix Build Issues
If the build fails, fix all issues:
- Resolve compilation errors
- Fix import statements
- Update dependencies in build.gradle if needed
- Correct syntax errors
- Address lint warnings
- Re-run build to verify fixes

**Repeat steps 5-7 until build succeeds completely.**

Only proceed to deployment once the local build is successful.

### 8. Deploy Using deploy.sh
// turbo
Run the deployment script to sync changes:
```bash
cd /Users/softsuave/Documents/custom-env-android-fastapi
./deploy.sh
```

This script should:
- Update ngrok URL in the app
- Commit and push changes to GitHub
- Trigger CI/CD build

### 9. Wait for Build Completion
Monitor the GitHub Actions build:
- Check build status
- Wait for APK artifact to be generated
- Verify build succeeded

### 10. Install APK to Emulator
// turbo
Download and install the built APK to the emulator:
```bash
cd /Users/softsuave/Documents/custom-env-android-fastapi
# Download latest APK from GitHub releases
# Install to emulator
adb install -r path/to/app-debug.apk
```

### 11. Launch Application
// turbo
Start the application on the emulator:
```bash
adb shell am start -n com.example.todoapp/.MainActivity
```

Wait for app to fully load (2-3 seconds).

### 12. Create Screenshot Test Script
Create a Python script to automate the user flow and capture screenshots:
- Define the complete user journey
- Specify tap coordinates and actions
- Set screenshot capture points
- Save screenshots with descriptive names

### 13. Execute Automated Flow
// turbo
Run the Python script to interact with the app:
```bash
cd /Users/softsuave/Documents/custom-env-android-fastapi
python scripts/automated_flow_test.py
```

The script should:
- Perform ADB commands to interact with UI
- Capture screenshots at each step
- Save screenshots to a timestamped directory
- Log all actions taken

### 14. Verify Screenshots Exist
Check that all expected screenshots were captured:
- Verify screenshot directory is created
- Confirm all expected screenshots are present
- Check file sizes are valid (not corrupted)

### 15. Compare with Expected Flow
Analyze the screenshots to verify implementation:
- Check UI elements are present
- Verify text content is correct
- Confirm navigation flow works
- Validate button states and interactions

Optional: Use image comparison or OCR to automatically verify:
```python
# Example verification checks:
# - Is the expected button visible?
# - Does the text match requirements?
# - Are error states handled correctly?
# - Do success confirmations appear?
```

### 16. Generate Verification Report
Create a summary report including:
- ✅ Successful test steps
- ❌ Failed validations (if any)
- 📸 Screenshot paths
- 📝 Observations and notes
- 🎯 Success criteria met/not met

### 17. Final Verdict
Determine if the implementation is successful:

**SUCCESS criteria:**
- All planned features are implemented
- Screenshots show expected UI flow
- No crashes or errors in logs
- User flow completes end-to-end
- UI matches design requirements

**If SUCCESSFUL:**
- Log success message
- Archive screenshots with timestamp
- Mark workflow as complete
- Provide summary to user

**If FAILED:**
- Identify what went wrong
- Provide detailed failure analysis
- Suggest fixes or next steps
- Do NOT mark as complete

### 18. End of Workflow
Output final status and any next steps.

---

## Example Usage

User: "Add a dark mode toggle to the settings screen"

The workflow will:
1. Plan the dark mode implementation
2. Identify files to modify (themes, preferences, UI)
3. Write code for theme switching
4. Deploy and build
5. Install to emulator
6. Automate: Open app → Navigate to settings → Toggle dark mode → Verify theme changes
7. Capture screenshots of light mode, settings screen, and dark mode
8. Verify the toggle works correctly
9. Report success or issues

## Notes
- Screenshots are saved in `test_results/YYYY-MM-DD_HH-MM-SS/`
- Logs are saved alongside screenshots
- ADB commands assume emulator is already running
- Build wait time may vary (typically 3-5 minutes)
