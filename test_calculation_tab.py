from datetime import date
from features.calculation.calculation_logic import calculate_end_date, calculate_extended_end_date

def test_calculation_logic():
    print("--- Testing Calculation Logic ---")

    start_date = date(2025, 7, 21)

    # 1. Test calculate_end_date
    print("\nStep 1: Testing calculate_end_date...")
    end_date_days = calculate_end_date(start_date, 10, "Days")
    if end_date_days == date(2025, 7, 31):
        print("SUCCESS: Correct end date for Days.")
    else:
        print(f"FAILURE: Incorrect end date for Days. Expected 2025-07-31, got {end_date_days}")

    end_date_months = calculate_end_date(start_date, 2, "Months")
    if end_date_months == date(2025, 9, 21):
        print("SUCCESS: Correct end date for Months.")
    else:
        print(f"FAILURE: Incorrect end date for Months. Expected 2025-09-21, got {end_date_months}")

    end_date_years = calculate_end_date(start_date, 1, "Years")
    if end_date_years == date(2026, 7, 21):
        print("SUCCESS: Correct end date for Years.")
    else:
        print(f"FAILURE: Incorrect end date for Years. Expected 2026-07-21, got {end_date_years}")

    # 2. Test calculate_extended_end_date
    print("\nStep 2: Testing calculate_extended_end_date...")
    base_end_date = date(2025, 10, 15)
    extended_date_days = calculate_extended_end_date(base_end_date, 5, "Days")
    if extended_date_days == date(2025, 10, 20):
        print("SUCCESS: Correct extended end date for Days.")
    else:
        print(f"FAILURE: Incorrect extended end date for Days. Expected 2025-10-20, got {extended_date_days}")

    extended_date_months = calculate_extended_end_date(base_end_date, 3, "Months")
    if extended_date_months == date(2026, 1, 15):
        print("SUCCESS: Correct extended end date for Months.")
    else:
        print(f"FAILURE: Incorrect extended end date for Months. Expected 2026-01-15, got {extended_date_months}")

    extended_date_years = calculate_extended_end_date(base_end_date, 2, "Years")
    if extended_date_years == date(2027, 10, 15):
        print("SUCCESS: Correct extended end date for Years.")
    else:
        print(f"FAILURE: Incorrect extended end date for Years. Expected 2027-10-15, got {extended_date_years}")

if __name__ == '__main__':
    test_calculation_logic()
