#!/usr/bin/env python3
"""
Test for Completed Tasks Screen Feature
Tests the new completed tasks screen functionality
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from test_runner import AndroidTestRunner, TestStep


def test_completed_tasks_screen():
    """Test the completed tasks screen feature"""
    
    runner = AndroidTestRunner(output_dir="test_results/completed_tasks_feature")
    
    steps = [
        TestStep(
            name="Wait for app to load",
            action="wait",
            wait_after=3.0,
            screenshot_name="01_app_loaded"
        ),
        TestStep(
            name="Capture main screen with tasks",
            action="screenshot",
            wait_after=1.0,
            screenshot_name="02_main_screen"
        ),
        TestStep(
            name="Try to find and tap completed button",
            action="tap",
            element_text="Completed",  # Will search for completed button
            wait_after=1.0,
            screenshot_name="03_after_completed_tap"
        ),
        TestStep(
            name="Capture completed tasks screen",
            action="screenshot",
            wait_after=1.0,
            screenshot_name="04_completed_screen"
        ),
        TestStep(
            name="Navigate back to main screen",
            action="back",
            wait_after=1.0,
            screenshot_name="05_back_to_main"
        ),
        TestStep(
            name="Final screenshot",
            action="screenshot",
            wait_after=1.0,
            screenshot_name="06_final_state"
        ),
    ]
    
    # Execute all steps
    print("\n🧪 Starting Completed Tasks Feature Test\n")
    for i, step in enumerate(steps, 1):
        print(f"Step {i}/{len(steps)}")
        if not runner.execute_step(step):
            print(f"⚠️  Step failed but continuing...")
    
    # Check for errors
    errors = runner.check_logcat_errors()
    if errors:
        print(f"\n⚠️  Found {len(errors)} errors in logcat:")
        for error in errors[:3]:
            print(f"  {error[:80]}...")
    
    # Generate report
    report = runner.generate_report()
    
    print(f"\n{'='*60}")
    print(f"COMPLETED TASKS FEATURE TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Steps:    {report['total_steps']}")
    print(f"Passed:         {report['passed']} ✅")
    print(f"Failed:         {report['failed']} ❌")
    print(f"Success Rate:   {report['success_rate']}")
    print(f"Screenshots:    {len(report['screenshots'])}")
    print(f"{'='*60}\n")
    
    return report['failed'] == 0


if __name__ == "__main__":
    success = test_completed_tasks_screen()
    sys.exit(0 if success else 1)
