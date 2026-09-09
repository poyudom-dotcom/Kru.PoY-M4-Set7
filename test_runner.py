import os
import subprocess

TEST_CASES = {
    "Examination_1": [
        {"input": "100\n70\n", "expected": "30"},
        {"input": "500\n120\n", "expected": "380"}
    ],
    "Examination_2": [
        {"input": "37.5\n", "expected": "Fever"},
        {"input": "36.8\n", "expected": "Normal"}
    ],
    "Examination_3": [
        {"input": "100\n1\n", "expected": "90"},
        {"input": "100\n0\n", "expected": "100"}
    ],
    "Examination_4": [
        {"input": "1\n", "expected": "0"},
        {"input": "3\n", "expected": "20"},
        {"input": "5\n", "expected": "50"}
    ],
    "Examination_5": [
        {"input": "17.5\n", "expected": "Underweight"},
        {"input": "21.0\n", "expected": "Normal"},
        {"input": "25.4\n", "expected": "Overweight"}
    ]
}

def is_equal(actual, expected):
    clean_actual = actual.strip().lower()
    clean_expected = expected.strip().lower()
    
    if clean_actual == clean_expected:
        return True
        
    try:
        if float(clean_actual) == float(clean_expected):
            return True
    except ValueError:
        pass
        
    return False

def run_tests():
    all_passed = True
    
    for file_name, cases in TEST_CASES.items():
        py_file = f"{file_name}.py"
        if not os.path.exists(py_file):
            continue

        print(f"\n--- Testing {py_file} ---")
        for i, case in enumerate(cases, 1):
            try:
                process = subprocess.Popen(
                    ["python", py_file],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5
                )
                stdout, stderr = process.communicate(input=case["input"])
                
                if is_equal(stdout, case["expected"]):
                    print(f"  Test Case {i}: PASSED ✅")
                else:
                    got_clean = stdout.strip()
                    print(f"  Test Case {i}: FAILED ❌ (Got: '{got_clean}', Expected: '{case['expected']}')")
                    all_passed = False
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"  Test Case {i}: FAILED ❌ (Timeout - โค้ดติด Infinite Loop)")
                all_passed = False
            except Exception as e:
                print(f"  Test Case {i}: ERROR ❌ ({str(e)})")
                all_passed = False

    if not all_passed:
        exit(1)

if __name__ == "__main__":
    run_tests()
