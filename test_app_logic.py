import os
from database import db
from parsers import extract_from_excel, extract_from_docx, inspect_dgth_sheet

def run_tests():
    print("=== TEST 1: CATALOG EXTRACTION FROM EXCEL ===")
    sample_cat_xlsx = "sample_data/danh_muc_dinh_muc_mau.xlsx"
    with open(sample_cat_xlsx, "rb") as f:
        bytes_data = f.read()
    records = extract_from_excel(bytes_data, "danh_muc_dinh_muc_mau.xlsx")
    print(f"Extracted {len(records)} records from catalog excel.")
    assert len(records) > 0, "No records extracted!"

    # Check normalization
    code_map = {r["raw_code"]: r["code"] for r in records}
    print("Raw AB.123 ->", code_map.get("AB.123"))
    print("Raw AF.1234 ->", code_map.get("AF.1234"))
    assert code_map.get("AB.123") == "AB.12300", "AB.123 was not padded to AB.12300!"
    assert code_map.get("AF.1234") == "AF.12340", "AF.1234 was not padded to AF.12340!"

    # Save to DB
    inserted = db.add_work_codes(records, "danh_muc_dinh_muc_mau.xlsx", "happyclone96@gmail.com")
    print(f"Inserted into database: {inserted} records.")

    print("\n=== TEST 2: USER MANAGEMENT & APPROVAL FLOW ===")
    db.delete_user("test.engineer@gmail.com")
    new_user = db.register_or_get_user("test.engineer@gmail.com", "Test Engineer")
    print("New user registered:", new_user["email"], "Status:", new_user["status"])
    assert new_user["status"] == "pending", "New user should have status 'pending'!"

    db.update_user_status("test.engineer@gmail.com", "active")
    updated_user = db.get_user("test.engineer@gmail.com")
    print("After approval status:", updated_user["status"])
    assert updated_user["status"] == "active", "Approved user should have status 'active'!"

    print("\n=== TEST 3: ĐGTH SHEET INSPECTION WITH SECTION GROUPING ===")
    sample_inspect_xlsx = "sample_data/du_toan_kiem_tra_DGTH.xlsx"
    with open(sample_inspect_xlsx, "rb") as f:
        bytes_inspect = f.read()
    
    lookup = db.get_all_codes_lookup()
    res = inspect_dgth_sheet(bytes_inspect, lookup)
    assert res["success"] is True, f"Inspection failed: {res}"

    print(f"Inspection Summary:")
    print(f"- Total items: {res['total_items']}")
    print(f"- Valid items: {res['valid_items']}")
    print(f"- Error items: {res['error_items']}")
    print(f"- Section count: {res['section_count']}")

    assert res["section_count"] == 3, f"Expected 3 sections, got {res['section_count']}"
    assert res["error_items"] == 3, f"Expected 3 error items (AF.99999, AK.999, XX.88888), got {res['error_items']}"

    for s in res["sections"]:
        print(f"\n[Section: {s['title']}] Total: {s['total_count']}, Valid: {s['valid_count']}, Errors: {s['error_count']}")
        for it in s["items"]:
            if it["status"] != "VALID":
                print(f"   -> ERROR at STT {it['stt']} (row {it['row_index']}): Code '{it['raw_code']}' - {it['status_desc']}")

    print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    run_tests()
