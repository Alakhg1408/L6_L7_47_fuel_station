import math

def parse_purchase(text):
    if not isinstance(text, str):
        return None
    try:
        parts = text.split(':')
        if len(parts) != 2:
            return None
        grade = parts[0].strip()
        litres_str = parts[1].strip()
        if not grade or not litres_str:
            return None
        litres = float(litres_str)
        if math.isnan(litres) or math.isinf(litres) or litres < 0:
            return None
        return grade.title(), litres
    except (ValueError, OverflowError):
        return None

def volume_average(volumes_csv):
    if not isinstance(volumes_csv, str):
        return 0
    try:
        parts = [p.strip() for p in volumes_csv.split(',') if p.strip()]
        if not parts:
            return 0
        values = [int(p) for p in parts]
        return sum(values) // len(values)
    except (ValueError, OverflowError, ZeroDivisionError):
        return 0

def payable_bill(text):
    if not isinstance(text, str):
        return 0.0
    try:
        parts = text.split('|')
        if len(parts) != 2:
            return 0.0
        bill_str = parts[0].strip()
        discount_str = parts[1].strip()
        if not bill_str or not discount_str:
            return 0.0
        bill = float(bill_str)
        discount = float(discount_str)
        if math.isnan(bill) or math.isinf(bill) or math.isnan(discount) or math.isinf(discount):
            return 0.0
        if bill < 0 or discount < 0:
            return 0.0
        total = bill * 1.18 - discount
        return max(total, 0.0)
    except (ValueError, OverflowError):
        return 0.0

def main():
    print("==== Running parse_purchase ====")
    user_input = input("Enter grade:litres (e.g. diesel:25): ")
    result = parse_purchase(user_input)
    print("Grade and Litres:", result)

    print("\n==== Running volume_average ====")
    user_input = input("Enter pump volumes in litres as CSV (e.g. 10,25,40): ")
    result = volume_average(user_input)
    print("Average Volume:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 2500|100): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result)

if __name__ == "__main__":
    main()
