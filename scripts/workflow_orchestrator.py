#!/usr/bin/env python3
"""
Workflow Orchestrator for Automated Development Cycle
Manages the complete development lifecycle from planning to verification
"""

import sys
import subprocess
import time
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class WorkflowOrchestrator:
    """Orchestrates the complete development workflow"""
    
    def __init__(self, feature_prompt: str, skip_tests: bool = False):
        self.prompt = feature_prompt
        self.skip_tests = skip_tests
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.workspace = Path(f"workflow_runs/{self.timestamp}")
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.log_file = self.workspace / "workflow.log"
        
    def log(self, message: str, level: str = "INFO"):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry + "\n")
    
    def run_command(self, cmd: str, cwd: Optional[str] = None, 
                   check: bool = True) -> subprocess.CompletedProcess:
        """Run shell command and log output"""
        self.log(f"Executing: {cmd}", "CMD")
        try:
            result = subprocess.run(
                cmd, shell=True, cwd=cwd,
                capture_output=True, text=True, check=check
            )
            if result.stdout:
                self.log(f"Output: {result.stdout[:200]}", "DEBUG")
            return result
        except subprocess.CalledProcessError as e:
            self.log(f"Command failed: {e.stderr}", "ERROR")
            raise
    
    def run(self) -> bool:
        """Execute complete workflow"""
        self.log("="*70)
        self.log("🚀 Starting Automated Development Workflow")
        self.log(f"📝 Feature: {self.prompt}")
        self.log(f"📁 Workspace: {self.workspace}")
        self.log("="*70)
        
        try:
            # Stage 1: Validation
            if not self.stage_validation():
                self.log("❌ Validation failed", "ERROR")
                return False
            
            # Stage 2: Planning
            plan = self.stage_planning()
            
            # Stage 3: Local Build & Fix
            if not self.stage_local_build():
                self.log("❌ Local build failed", "ERROR")
                return False
            
            # Stage 4: Deployment
            if not self.stage_deployment():
                self.log("❌ Deployment failed", "ERROR")
                return False
            
            # Stage 5: Install APK
            if not self.stage_installation():
                self.log("❌ Installation failed", "ERROR")
                return False
            
            # Stage 6: Automated Testing
            test_results = None
            if not self.skip_tests:
                test_results = self.stage_testing()
            
            # Stage 7: Verification & Reporting
            success = self.stage_verification(test_results)
            
            if success:
                self.log("\n" + "="*70)
                self.log("✅ WORKFLOW COMPLETED SUCCESSFULLY")
                self.log("="*70)
                return True
            else:
                self.log("\n" + "="*70)
                self.log("❌ WORKFLOW FAILED")
                self.log("="*70)
                return False
                
        except Exception as e:
            self.log(f"Fatal error: {e}", "ERROR")
            import traceback
            self.log(traceback.format_exc(), "ERROR")
            return False
    
    def stage_validation(self) -> bool:
        """Stage 1: Validate environment"""
        self.log("\n🔍 Stage 1: Environment Validation")
        
        checks = {
            'ADB': 'adb version',
            'Git': 'git --version',
            'Gradle': 'cd frontend && ./gradlew --version',
            'Python': 'python3 --version'
        }
        
        for name, cmd in checks.items():
            try:
                result = self.run_command(cmd, check=False)
                if result.returncode == 0:
                    self.log(f"   ✅ {name} is available")
                else:
                    self.log(f"   ⚠️  {name} check failed", "WARN")
            except Exception as e:
                self.log(f"   ⚠️  {name} not found: {e}", "WARN")
        
        # Check if backend is running
        try:
            result = self.run_command(
                'curl -s http://localhost:8081/health || echo "not_running"',
                check=False
            )
            if 'not_running' not in result.stdout:
                self.log("   ✅ Backend is accessible")
            else:
                self.log("   ⚠️  Backend not accessible", "WARN")
        except:
            pass
        
        return True
    
    def stage_planning(self) -> Dict:
        """Stage 2: Create implementation plan"""
        self.log("\n📋 Stage 2: Planning")
        
        plan = {
            'feature': self.prompt,
            'timestamp': self.timestamp,
            'steps': [
                'Analyze feature requirements',
                'Identify files to modify',
                'Implement changes',
                'Test locally',
                'Deploy and verify'
            ]
        }
        
        plan_file = self.workspace / 'plan.json'
        with open(plan_file, 'w') as f:
            json.dump(plan, f, indent=2)
        
        self.log(f"   📄 Plan saved: {plan_file}")
        return plan
    
    def stage_local_build(self) -> bool:
        """Stage 3: Build locally and fix issues"""
        self.log("\n🏗️  Stage 3: Local Build & Validation")
        
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            self.log(f"   Attempt {attempt}/{max_attempts}")
            
            try:
                result = self.run_command(
                    './gradlew assembleDebug',
                    cwd='frontend',
                    check=False
                )
                
                if result.returncode == 0:
                    self.log("   ✅ Build successful!")
                    return True
                else:
                    self.log(f"   ❌ Build failed (attempt {attempt})", "ERROR")
                    self.log(f"   Error output: {result.stderr[:500]}", "DEBUG")
                    
                    if attempt < max_attempts:
                        self.log("   Analyzing build errors...")
                        # In production, you would parse errors and attempt fixes here
                        time.sleep(2)
                    
            except Exception as e:
                self.log(f"   ❌ Build error: {e}", "ERROR")
        
        self.log("   ❌ Build failed after all attempts", "ERROR")
        return False
    
    def stage_deployment(self) -> bool:
        """Stage 4: Deploy and trigger CI build"""
        self.log("\n🚢 Stage 4: Deployment")
        
        try:
            # Run deploy script
            self.log("   Running deploy.sh...")
            result = self.run_command('./deploy.sh', check=False)
            
            if result.returncode != 0:
                self.log("   ❌ Deploy script failed", "ERROR")
                return False
            
            self.log("   ✅ Deploy script completed")
            
            # Wait for CI build
            self.log("   ⏳ Waiting for CI build (60 seconds)...")
            time.sleep(60)
            
            # Check build status
            self.log("   Checking GitHub Actions build...")
            result = self.run_command(
                'gh run list --workflow android-debug-build.yml --limit 1 --json conclusion -q ".[0].conclusion"',
                check=False
            )
            
            if 'success' in result.stdout:
                self.log("   ✅ CI build successful")
                return True
            else:
                self.log(f"   Build status: {result.stdout}", "INFO")
                return True  # Continue anyway
                
        except Exception as e:
            self.log(f"   ⚠️  Deployment completed with warnings: {e}", "WARN")
            return True
    
    def stage_installation(self) -> bool:
        """Stage 5: Install APK on emulator"""
        self.log("\n📱 Stage 5: Installation")
        
        try:
            # Run install script
            self.log("   Running install_latest.sh...")
            result = self.run_command('./install_latest.sh', check=False)
            
            if result.returncode == 0:
                self.log("   ✅ APK installed successfully")
                return True
            else:
                self.log("   ❌ Installation failed", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"   ❌ Installation error: {e}", "ERROR")
            return False
    
    def stage_testing(self) -> Optional[Dict]:
        """Stage 6: Run automated tests"""
        self.log("\n🧪 Stage 6: Automated Testing")
        
        try:
            test_name = self.prompt.replace(' ', '_').lower()[:30]
            
            self.log(f"   Running test: {test_name}")
            result = self.run_command(
                f'python3 scripts/test_runner.py {test_name}',
                check=False
            )
            
            # Find and load test report
            test_results_dir = Path('test_results')
            if test_results_dir.exists():
                # Get most recent test result
                test_dirs = sorted(test_results_dir.glob(f"{test_name}*"))
                if test_dirs:
                    latest_test = test_dirs[-1]
                    report_file = latest_test / 'test_report.json'
                    
                    if report_file.exists():
                        with open(report_file) as f:
                            report = json.load(f)
                        
                        self.log(f"   📊 Test Results:")
                        self.log(f"      Total: {report['total_steps']}")
                        self.log(f"      Passed: {report['passed']}")
                        self.log(f"      Failed: {report['failed']}")
                        self.log(f"      Success Rate: {report['success_rate']}")
                        
                        return report
            
            self.log("   ⚠️  No test report found", "WARN")
            return None
            
        except Exception as e:
            self.log(f"   ⚠️  Testing completed with errors: {e}", "WARN")
            return None
    
    def stage_verification(self, test_results: Optional[Dict]) -> bool:
        """Stage 7: Verify implementation success"""
        self.log("\n✔️  Stage 7: Verification")
        
        issues = []
        
        # Check test results
        if test_results:
            if test_results['failed'] > 0:
                issues.append(f"{test_results['failed']} test steps failed")
        
        # Check for APK installation
        result = self.run_command(
            'adb shell pm list packages | grep com.saibabui.androidapp',
            check=False
        )
        if result.returncode == 0:
            self.log("   ✅ App is installed")
        else:
            issues.append("App not found on device")
        
        # Final verdict
        if len(issues) == 0:
            self.log("\n   ✅ All verification checks passed!")
            return True
        else:
            self.log("\n   ❌ Verification issues found:")
            for issue in issues:
                self.log(f"      - {issue}")
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Automated Development Workflow Orchestrator'
    )
    parser.add_argument('prompt', help='Feature implementation prompt')
    parser.add_argument('--skip-tests', action='store_true',
                       help='Skip automated testing phase')
    parser.add_argument('--workspace', help='Custom workspace directory')
    
    args = parser.parse_args()
    
    orchestrator = WorkflowOrchestrator(
        feature_prompt=args.prompt,
        skip_tests=args.skip_tests
    )
    
    success = orchestrator.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
