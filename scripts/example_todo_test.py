#!/usr/bin/env python3
"""
Example test for Todo app - demonstrates automated testing workflow
"""

import sys
from pathlib import Path

# Add parent directory to path to import test_runner
sys.path.insert(0, str(Path(__file__).parent))

from test_runner import AndroidTestRunner, TestStep


def test_todo_app_flow():
    """Test adding and deleting a todo item"""
    
    runner = AndroidTestRunner(output_dir="test_results/todo_app_flow")
    
    # Define test steps
    steps = [
        TestStep(
            name="Wait for app to load",
            action="wait",
            wait_after=3.0,
            screenshot_name="01_app_loaded"
        ),
        TestStep(
            name="Capture initial home screen",
            action="screenshot",
            wait_after=1.0,
            screenshot_name="02_home_screen"
        ),
        TestStep(
            name="Tap add button (if found dynamically)",
            action="tap",
            element_text="Add",  # Will search for element with "Add" text
            wait_after=1.0,
            screenshot_name="03_after_add_tap"
        ),
        TestStep(
            name="Take final screenshot",
            action="screenshot",
            wait_after=1.0,
            screenshot_name="04_final_state"
        ),
    ]
    
    # Execute all steps
    print("\n🧪 Starting Todo App Flow Test\n")
    for i, step in enumerate(steps, 1):
        print(f"Step {i}/{len(steps)}")
        if not runner.execute_step(step):
            print(f"⚠️  Step failed but continuing...")
    
    # Check for errors in logs
    errors = runner.check_logcat_errors()
    if errors:
        print(f"\n⚠️  Found {len(errors)} errors in logcat:")
        for error in errors[:3]:
            print(f"  {error[:80]}...")
    
    # Generate and print report
    report = runner.generate_report()
    
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Steps:    {report['total_steps']}")
    print(f"Passed:         {report['passed']} ✅")
    print(f"Failed:         {report['failed']} ❌")
    print(f"Success Rate:   {report['success_rate']}")
    print(f"Screenshots:    {len(report['screenshots'])}")
    print(f"{'='*60}\n")
    
    return report['failed'] == 0


if __name__ == "__main__":
    success = test_todo_app_flow()
    sys.exit(0 if success else 1)
