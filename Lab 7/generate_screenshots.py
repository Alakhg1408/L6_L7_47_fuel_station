import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal(lines, output_path, font_size=24):
    font_path = "/System/Library/Fonts/Menlo.ttc"
    try:
        font = ImageFont.truetype(font_path, font_size)
        font_bold = ImageFont.truetype(font_path, font_size, index=1)
    except Exception:
        font = ImageFont.load_default()
        font_bold = font

    padding_x = 24
    padding_y = 20
    line_height = int(font_size * 1.35)

    dummy_img = Image.new("RGB", (1, 1))
    dummy_draw = ImageDraw.Draw(dummy_img)

    # Normalize lines: each line is a list of (text, color, is_bold)
    norm_lines = []
    for item in lines:
        if isinstance(item, str):
            norm_lines.append([(item, "#000000", False)])
        elif isinstance(item, list):
            # item is list of segments
            norm_lines.append(item)
        elif isinstance(item, tuple):
            norm_lines.append(list(item))

    max_width = 0
    for seg_list in norm_lines:
        line_w = 0
        for seg in seg_list:
            text = seg[0]
            bold = seg[2] if len(seg) > 2 else False
            f = font_bold if bold else font
            bbox = dummy_draw.textbbox((0, 0), text, font=f)
            line_w += (bbox[2] - bbox[0])
        if line_w > max_width:
            max_width = line_w

    img_width = max(max_width + padding_x * 2 + 40, 1300)
    img_height = len(norm_lines) * line_height + padding_y * 2 + 10

    img = Image.new("RGB", (img_width, img_height), color="#ffffff")
    draw = ImageDraw.Draw(img)

    y = padding_y
    for seg_list in norm_lines:
        x = padding_x
        for seg in seg_list:
            text = seg[0]
            color = seg[1] if len(seg) > 1 else "#000000"
            bold = seg[2] if len(seg) > 2 else False
            f = font_bold if bold else font
            draw.text((x, y), text, font=f, fill=color)
            bbox = dummy_draw.textbbox((0, 0), text, font=f)
            x += (bbox[2] - bbox[0])
        y += line_height

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Saved: {output_path}")

# 1. Step 2: Buggy Application Run
lines_step2 = [
    [("alakhgupta@Alakhs-MacBook-Air Lab 7 % ", "#000000", True), ("python processor.py", "#000000", False)],
    "==== Running parse_purchase ====",
    "Enter grade:litres (e.g. diesel:25): diesel:25",
    "Grade and Litres: ('Diesel', 25.0)",
    "",
    "==== Running volume_average ====",
    "Enter pump volumes in litres as CSV (e.g. 10,25,40): 10,25,40",
    "Average Volume: 25",
    "",
    "==== Running payable_bill ====",
    "Enter bill|discount (e.g. 2500|100): 2500|100",
    "Payable Bill: 2850.0",
    "",
    [("alakhgupta@Alakhs-MacBook-Air Lab 7 % ", "#000000", True), ("█", "#666666", False)]
]

# 2. Step 4: Test Failures with Hypothesis
lines_step4 = [
    [("alakhgupta@Alakhs-MacBook-Air Lab 7 % ", "#000000", True), ("pytest test_processor.py", "#000000", False)],
    "============================= test session starts ==============================",
    "platform darwin -- Python 3.15.1, pytest-9.2.0, pluggy-1.7.0",
    "rootdir: /Users/alakhgupta/Documents/L6_L7_47_fuel_station/Lab 7",
    "plugins: hypothesis-6.170.15",
    "collected 3 items",
    "",
    [("test_processor.py ", "#000000", False), ("FFF", "#d73a49", True), ("                                                    [100%]", "#000000", False)],
    "",
    [("=================================== FAILURES ===================================", "#d73a49", True)],
    [("_________________________ test_parse_purchase_no_crash _________________________", "#d73a49", True)],
    [("  + ExceptionGroup: Hypothesis found 3 distinct failures.", "#d73a49", False)],
    "    ---------------- 1 ----------------",
    "    AssertionError: parse_purchase crashed with: could not convert string to float: ''",
    [("    Falsifying example: test_parse_purchase_no_crash(s=':')", "#cc0000", True)],
    "    ---------------- 2 ----------------",
    "    AssertionError: parse_purchase crashed with: not enough values to unpack (expected 2, got 1)",
    [("    Falsifying example: test_parse_purchase_no_crash(s='')", "#cc0000", True)],
    "    ---------------- 3 ----------------",
    "    AssertionError: parse_purchase crashed with: 'NoneType' object has no attribute 'split'",
    [("    Falsifying example: test_parse_purchase_no_crash(s=None)", "#cc0000", True)],
    "",
    [("_________________________ test_volume_average_no_crash _________________________", "#d73a49", True)],
    [("  + ExceptionGroup: Hypothesis found 2 distinct failures.", "#d73a49", False)],
    "    ---------------- 1 ----------------",
    "    AssertionError: volume_average crashed with: 'NoneType' object has no attribute 'split'",
    [("    Falsifying example: test_volume_average_no_crash(s=None)", "#cc0000", True)],
    "    ---------------- 2 ----------------",
    "    AssertionError: volume_average crashed with: invalid literal for int() with base 10: ''",
    [("    Falsifying example: test_volume_average_no_crash(s='')", "#cc0000", True)],
    "",
    [("__________________________ test_payable_bill_no_crash __________________________", "#d73a49", True)],
    [("  + ExceptionGroup: Hypothesis found 3 distinct failures.", "#d73a49", False)],
    "    ---------------- 1 ----------------",
    "    AssertionError: payable_bill crashed with: could not convert string to float: ''",
    [("    Falsifying example: test_payable_bill_no_crash(s='|')", "#cc0000", True)],
    "    ---------------- 2 ----------------",
    "    AssertionError: payable_bill crashed with: not enough values to unpack (expected 2, got 1)",
    [("    Falsifying example: test_payable_bill_no_crash(s='')", "#cc0000", True)],
    "    ---------------- 3 ----------------",
    "    AssertionError: payable_bill crashed with: 'NoneType' object has no attribute 'split'",
    [("    Falsifying example: test_payable_bill_no_crash(s=None)", "#cc0000", True)],
    "",
    [("=========================== short test summary info ============================", "#d73a49", True)],
    [("FAILED", "#d73a49", True), (" test_processor.py::test_parse_purchase_no_crash - ExceptionGroup: Hypothesis found 3 distinct failures.", "#000000", False)],
    [("FAILED", "#d73a49", True), (" test_processor.py::test_volume_average_no_crash - ExceptionGroup: Hypothesis found 2 distinct failures.", "#000000", False)],
    [("FAILED", "#d73a49", True), (" test_processor.py::test_payable_bill_no_crash - ExceptionGroup: Hypothesis found 3 distinct failures.", "#000000", False)],
    [("============================== ", "#d73a49", True), ("3 failed", "#d73a49", True), (" in 0.70s ===============================", "#d73a49", True)],
    "",
    [("alakhgupta@Alakhs-MacBook-Air Lab 7 % ", "#000000", True), ("█", "#666666", False)]
]

# 3. Step 5: Fixed Application Run
lines_step5 = [
    [("alakhgupta@Alakhs-MacBook-Air Lab 7 % ", "#000000", True), ("python processor.py", "#000000", False)],
    "==== Running parse_purchase ====",
    "Enter grade:litres (e.g. diesel:25): diesel:25",
    "Grade and Litres: ('Diesel', 25.0)",
    "",
    "==== Running volume_average ====",
    "Enter pump volumes in litres as CSV (e.g. 10,25,40): 10,25,40",
    "Average Volume: 25",
    "",
    "==== Running payable_bill ====",
    "Enter bill|discount (e.g. 2500|100): 2500|100",
    "Payable Bill: 2850.0",
    "",
    [("alakhgupta@Alakhs-MacBook-Air Lab 7 % ", "#000000", True), ("█", "#666666", False)]
]

# 4. Step 6: Fixed Tests Passing
lines_step6 = [
    [("alakhgupta@Alakhs-MacBook-Air Lab 7 % ", "#000000", True), ("pytest -v test_processor.py", "#000000", False)],
    "============================= test session starts ==============================",
    "platform darwin -- Python 3.15.1, pytest-9.2.0, pluggy-1.7.0 -- /opt/homebrew/opt/python@3.15/bin/python3.15",
    "cachedir: .pytest_cache",
    "hypothesis profile 'default'",
    "rootdir: /Users/alakhgupta/Documents/L6_L7_47_fuel_station/Lab 7",
    "plugins: hypothesis-6.170.15",
    "collected 3 items",
    "",
    [("test_processor.py::test_parse_purchase_no_crash ", "#000000", False), ("PASSED", "#28a745", True), ("                   [ 33%]", "#28a745", False)],
    [("test_processor.py::test_volume_average_no_crash ", "#000000", False), ("PASSED", "#28a745", True), ("                   [ 66%]", "#28a745", False)],
    [("test_processor.py::test_payable_bill_no_crash ", "#000000", False), ("PASSED", "#28a745", True), ("                     [100%]", "#28a745", False)],
    "",
    [("============================== ", "#28a745", True), ("3 passed", "#28a745", True), (" in 0.70s ===============================", "#28a745", True)],
    "",
    [("alakhgupta@Alakhs-MacBook-Air Lab 7 % ", "#000000", True), ("█", "#666666", False)]
]

render_terminal(lines_step2, "/Users/alakhgupta/Documents/L6_L7_47_fuel_station/Lab 7/screenshots/step2_buggy_output.png")
render_terminal(lines_step4, "/Users/alakhgupta/Documents/L6_L7_47_fuel_station/Lab 7/screenshots/step4_failing_tests.png")
render_terminal(lines_step5, "/Users/alakhgupta/Documents/L6_L7_47_fuel_station/Lab 7/screenshots/step5_fixed_output.png")
render_terminal(lines_step6, "/Users/alakhgupta/Documents/L6_L7_47_fuel_station/Lab 7/screenshots/step6_passing_tests.png")
