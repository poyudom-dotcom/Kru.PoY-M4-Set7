import sys
import os
import subprocess

# ==============================================================================
# ⚙️ ชุดทดสอบข้อสอบทั้ง 5 ข้อสำหรับ Kru.PoY-M4-Set7 (ข้อละ 4 เคส = ข้อละ 4 คะแนน)
# ==============================================================================
EXAM_TEST_CASES = {
    # ข้อ 1: คำนวณเงินทอน (pay - price)
    "Examination_1.py": [
        (["100", "70"], "30"),
        (["50", "50"], "0"),
        (["500", "120"], "380"),
        (["1000", "450"], "550")
    ],
    # ข้อ 2: ตรวจสอบอุณหภูมิร่างกาย (>= 37.5 Fever, < 37.5 Normal)
    "Examination_2.py": [
        (["36.5"], "Normal"),
        (["37.4"], "Normal"),
        (["37.5"], "Fever"),
        (["38.6"], "Fever")
    ],
    # ข้อ 3: คำนวณราคาสินค้าตามสถานะสมาชิก (is_member: 1 ลด 10%, 0 ไม่ลด)
    "Examination_3.py": [
        (["100", "1"], "90.0"),
        (["100", "0"], "100.0"),
        (["250", "1"], "225.0"),
        (["500", "0"], "500.0")
    ],
    # ข้อ 4: คำนวณค่าจอดรถ (<=1 ชม: 0, 2-4 ชม: 20, >4 ชม: 50)
    "Examination_4.py": [
        (["1"], "0"),
        (["3"], "20"),
        (["4"], "20"),
        (["5"], "50")
    ],
    # ข้อ 5: ประเมินค่าดัชนีมวลกาย (<18.5 Underweight, 18.5-22.9 Normal, >=23 Overweight)
    "Examination_5.py": [
        (["17.5"], "Underweight"),
        (["18.5"], "Normal"),
        (["22.0"], "Normal"),
        (["25.0"], "Overweight")
    ]
}

def find_file(base_name):
    """ค้นหาไฟล์รองรับทั้งชื่อที่มีและไม่มี .py"""
    if os.path.exists(base_name):
        return base_name
    elif os.path.exists(f"{base_name}.py"):
        return f"{base_name}.py"
    elif os.path.exists(base_name.replace(".py", "")):
        return base_name.replace(".py", "")
    return None

def run_test(file_path, inputs):
    """รันไฟล์และดึงค่า Output"""
    try:
        input_data = "\n".join(inputs)
        process = subprocess.run(
            [sys.executable, file_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=3,
            encoding='utf-8',
            errors='ignore'
        )
        return process.stdout.strip()
    except Exception:
        return None

def compare_outputs(actual, expected):
    """เปรียบเทียบผลลัพธ์ รองรับทั้งข้อความและทศนิยม"""
    if actual is None:
        return False
    actual_clean = actual.strip()
    expected_clean = expected.strip()
    
    if actual_clean.lower() == expected_clean.lower():
        return True
    
    try:
        return abs(float(actual_clean) - float(expected_clean)) < 1e-5
    except ValueError:
        return False

def main():
    total_score = 0
    max_total_score = 20
    summary_rows = []

    for exam_name, test_cases in EXAM_TEST_CASES.items():
        file_path = find_file(exam_name)
        passed_cases = 0
        total_cases = len(test_cases)
        
        if file_path:
            for inputs, expected in test_cases:
                output = run_test(file_path, inputs)
                if compare_outputs(output, expected):
                    passed_cases += 1
        
        # คะแนนยืดหยุ่น: ผ่าน 1 เคส = 1 คะแนน
        score_for_exam = passed_cases 
        total_score += score_for_exam
        
        if passed_cases == total_cases:
            status_icon = "✅ ผ่านครบ"
        elif passed_cases > 0:
            status_icon = "🟡 ผ่านบางส่วน"
        else:
            status_icon = "❌ ไม่ผ่าน"

        summary_rows.append(
            f"| `{exam_name}` | {status_icon} | {passed_cases}/{total_cases} เคส | **{score_for_exam} / 4** |"
        )

    markdown_summary = f"""# 📊 สรุปผลการสอบวิชาเขียนโปรแกรม (Set 7)

| ข้อสอบ | สถานะการตรวจ | ผ่าน Test Cases | คะแนนที่ได้ |
| :--- | :---: | :---: | :---: |
{chr(10).join(summary_rows)}

---

### 🎯 **คะแนนรวมทั้งหมด: {total_score} / {max_total_score} คะแนน**
"""

    print(markdown_summary)

    summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary_file:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(markdown_summary)

if __name__ == "__main__":
    main()
