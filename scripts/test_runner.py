#!/usr/bin/env python3
"""
Automated Test Runner for Android App
Executes UI interactions and captures screenshots for verification
"""

import subprocess
import time
import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict
import xml.etree.ElementTree as ET


@dataclass
class TestStep:
    """Represents a single test action"""
    name: str
    action: str  # 'tap', 'swipe', 'input', 'wait', 'screenshot', 'back'
    coordinates: Optional[Tuple[int, int]] = None
    text: Optional[str] = None
    wait_after: float = 1.0
    screenshot_name: Optional[str] = None
    element_text: Optional[str] = None  # For dynamic element finding


class AndroidTestRunner:
    """Automated test runner for Android UI testing"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = []
        self.screenshot_count = 0
        
    def execute_step(self, step: TestStep) -> bool:
        """Execute a single test step"""
        print(f"📍 {step.name}")
        
        try:
            # Find element dynamically if element_text provided
            if step.element_text and not step.coordinates:
                step.coordinates = self._find_element(step.element_text)
                if not step.coordinates:
                    raise ValueError(f"Element not found: {step.element_text}")
            
            # Execute action
            if step.action == 'tap':
                self._tap(step.coordinates)
            elif step.action == 'swipe':
                self._swipe(step.coordinates)
            elif step.action == 'input':
                self._input_text(step.text)
            elif step.action == 'wait':
                time.sleep(step.wait_after)
            elif step.action == 'back':
                self._press_back()
            elif step.action == 'screenshot':
                pass  # Just capture screenshot
            
            time.sleep(step.wait_after)
            
            # Capture screenshot if specified
            if step.screenshot_name or step.action == 'screenshot':
                screenshot_name = step.screenshot_name or f"step_{self.screenshot_count:02d}"
                screenshot_path = self._capture_screenshot(screenshot_name)
                
                self.results.append({
                    'step': step.name,
                    'action': step.action,
                    'status': 'passed',
                    'screenshot': str(screenshot_path)
                })
                self.screenshot_count += 1
            else:
                self.results.append({
                    'step': step.name,
                    'action': step.action,
                    'status': 'passed'
                })
            
            return True
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            self.results.append({
                'step': step.name,
                'action': step.action,
                'status': 'failed',
                'error': str(e)
            })
            return False
    
    def _find_element(self, search_text: str) -> Optional[Tuple[int, int]]:
        """Find element coordinates dynamically using UI Automator"""
        try:
            # Dump UI hierarchy
            subprocess.run("adb shell uiautomator dump".split(), 
                          check=True, capture_output=True)
            subprocess.run("adb pull /sdcard/window_dump.xml".split(), 
                          check=True, capture_output=True)
            
            # Parse XML
            tree = ET.parse('window_dump.xml')
            
            for elem in tree.iter():
                text = elem.get('text', '')
                content_desc = elem.get('content-desc', '')
                
                if search_text.lower() in text.lower() or \
                   search_text.lower() in content_desc.lower():
                    bounds = elem.get('bounds')
                    if bounds:
                        # Parse bounds like "[x1,y1][x2,y2]"
                        import re
                        coords = re.findall(r'\d+', bounds)
                        if len(coords) >= 4:
                            x1, y1, x2, y2 = map(int, coords[:4])
                            center_x = (x1 + x2) // 2
                            center_y = (y1 + y2) // 2
                            print(f"   Found at ({center_x}, {center_y})")
                            return (center_x, center_y)
            
            return None
            
        except Exception as e:
            print(f"   Warning: Could not find element: {e}")
            return None
    
    def _tap(self, coords: Tuple[int, int]):
        """Simulate tap at coordinates"""
        subprocess.run(f"adb shell input tap {coords[0]} {coords[1]}".split(), 
                      check=True)
    
    def _swipe(self, coords: Tuple[int, int, int, int]):
        """Simulate swipe gesture"""
        x1, y1, x2, y2 = coords
        subprocess.run(f"adb shell input swipe {x1} {y1} {x2} {y2} 300".split(), 
                      check=True)
    
    def _input_text(self, text: str):
        """Input text (escape spaces)"""
        escaped = text.replace(' ', '%s')
        subprocess.run(f"adb shell input text {escaped}".split(), 
                      check=True)
    
    def _press_back(self):
        """Press back button"""
        subprocess.run("adb shell input keyevent 4".split(), 
                      check=True)
    
    def _capture_screenshot(self, name: str) -> Path:
        """Capture and pull screenshot"""
        timestamp = time.strftime("%H%M%S")
        filename = f"{timestamp}_{name}.png"
        device_path = f"/sdcard/{filename}"
        local_path = self.output_dir / filename
        
        subprocess.run(f"adb shell screencap -p {device_path}".split(), 
                      check=True)
        subprocess.run(f"adb pull {device_path} {local_path}".split(), 
                      check=True, capture_output=True)
        subprocess.run(f"adb shell rm {device_path}".split(), 
                      check=True)
        
        print(f"   📸 Screenshot saved: {filename}")
        return local_path
    
    def generate_report(self) -> Dict:
        """Generate test execution report"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.get('status') == 'passed')
        failed = total - passed
        
        report = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'total_steps': total,
            'passed': passed,
            'failed': failed,
            'success_rate': f"{(passed/total*100):.1f}%" if total > 0 else "0%",
            'results': self.results,
            'screenshots': [r['screenshot'] for r in self.results if 'screenshot' in r]
        }
        
        # Save JSON report
        report_path = self.output_dir / 'test_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Test Report saved: {report_path}")
        return report
    
    def check_logcat_errors(self, package: str = "com.saibabui.androidapp") -> List[str]:
        """Check for errors in logcat"""
        try:
            # Clear old logs
            subprocess.run("adb logcat -c".split(), check=True)
            time.sleep(2)
            
            # Get recent logs
            result = subprocess.run(
                f"adb logcat -d *:E".split(),
                capture_output=True, text=True
            )
            
            errors = [line for line in result.stdout.split('\n') 
                     if package in line and ('Error' in line or 'Exception' in line)]
            
            return errors[:10]  # Return first 10 errors
            
        except Exception as e:
            print(f"Warning: Could not check logcat: {e}")
            return []


def create_sample_test() -> List[TestStep]:
    """Create a sample test scenario"""
    return [
        TestStep(
            name="Wait for app to load",
            action="wait",
            wait_after=3.0,
            screenshot_name="01_app_loaded"
        ),
        TestStep(
            name="Capture home screen",
            action="screenshot",
            wait_after=1.0,
            screenshot_name="02_home_screen"
        ),
        # Add more steps based on your app's flow
    ]


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python test_runner.py <test_name>")
        print("Example: python test_runner.py todo_add_task")
        sys.exit(1)
    
    test_name = sys.argv[1]
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_dir = f"test_results/{test_name}_{timestamp}"
    
    print(f"🧪 Starting test: {test_name}")
    print(f"📁 Output directory: {output_dir}\n")
    
    runner = AndroidTestRunner(output_dir=output_dir)
    
    # Create test steps (customize based on your needs)
    steps = create_sample_test()
    
    # Execute all steps
    for step in steps:
        if not runner.execute_step(step):
            print(f"⚠️  Step failed, continuing...")
    
    # Check for errors
    errors = runner.check_logcat_errors()
    if errors:
        print(f"\n⚠️  Found {len(errors)} errors in logcat:")
        for error in errors[:5]:
            print(f"  {error[:100]}...")
    
    # Generate report
    report = runner.generate_report()
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Steps:    {report['total_steps']}")
    print(f"Passed:         {report['passed']} ✅")
    print(f"Failed:         {report['failed']} ❌")
    print(f"Success Rate:   {report['success_rate']}")
    print(f"Screenshots:    {len(report['screenshots'])}")
    print(f"{'='*60}\n")
    
    # Exit code based on success
    sys.exit(0 if report['failed'] == 0 else 1)


if __name__ == "__main__":
    main()
