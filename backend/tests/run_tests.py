#!/usr/bin/env python3
"""
Test runner script for the chatbot API tests
"""

import subprocess
import sys
import os

def run_tests():
    """Run the test suite"""
    print("🧪 Running Chatbot API Tests")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(backend_dir)
    
    # Run pytest with various options
    cmd = [
        "poetry", "run", "pytest",
        "tests/",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--strict-markers",  # Strict marker checking
        "--disable-warnings",  # Disable warnings for cleaner output
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code: {e.returncode}")
        return e.returncode

def run_specific_test(test_file: str):
    """Run a specific test file"""
    print(f"🧪 Running specific test: {test_file}")
    print("=" * 50)
    
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(backend_dir)
    
    cmd = [
        "poetry", "run", "pytest",
        f"tests/{test_file}",
        "-v",
        "--tb=short",
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✅ Test {test_file} passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Test {test_file} failed with exit code: {e.returncode}")
        return e.returncode

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test file
        test_file = sys.argv[1]
        exit_code = run_specific_test(test_file)
    else:
        # Run all tests
        exit_code = run_tests()
    
    sys.exit(exit_code)
