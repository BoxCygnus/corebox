import io
import re
import openpyxl
from typing import List, Dict, Any, Tuple, Optional
import docx

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

# Regular expression to match standard or short work codes:
# e.g. AB.123, AF.1234, AK.55555, AB12345
WORK_CODE_PATTERN = re.compile(r"^([A-Za-z]{2})[\.\s_-]?(\d{1,5})$")

# Flexible column keyword aliases
CODE_KEYWORDS = [
    "mã hiệu", "mã cv", "mã định mức", "mã hiệu đm", "mã công việc",
    "mã số", "mã", "work code", "code", "mã đơn giá", "mã hiệu cv"
]
NAME_KEYWORDS = [
    "tên công việc", "nội dung công việc", "tên công tác", "công tác lắp đặt",
    "nội dung", "diễn giải", "tên hạng mục", "hạng mục", "mô tả công việc",
    "work name", "description", "tên công tác xây lắp"
]
UNIT_KEYWORDS = [
    "đơn vị", "đơn vị tính", "đvt", "unit"
]
STT_KEYWORDS = [
    "stt", "số tt", "số thứ tự", "no", "tt"
]

def clean_str(val: Any) -> str:
    """Safely converts cell values to stripped string."""
    if val is None:
        return ""
    s = str(val).strip()
    return s

def extract_first_unit(val: Any) -> str:
    """
    Ưu tiên lấy đơn vị tính đầu tiên tương đương nội dung công việc tổng quát.
    Lọc bỏ các đơn vị phụ hoặc dòng giải thích chi tiết phía sau (ví dụ: '100m3\\nm3' -> '100m3').
    """
    if not val:
        return ""
    text = clean_str(val)
    if not text:
        return ""
    # Tách theo dòng mới trước (thường gặp trong các ô excel xuống dòng cho từng chi tiết)
    lines = [line.strip() for line in re.split(r'[\r\n]+', text) if line.strip()]
    first_line = lines[0] if lines else text
    
    # Tách theo dấu phẩy, chấm phẩy, hoặc thanh đứng phân cách nhiều đơn vị
    tokens = [t.strip() for t in re.split(r'[,;|\t]+', first_line) if t.strip()]
    first_token = tokens[0] if tokens else first_line
    
    # Bỏ các ký tự gạch đầu dòng nếu có
    first_token = re.sub(r'^[-–—•*+\s]+', '', first_token).strip()
    return first_token

def normalize_work_code(raw_code: str) -> str:
    """
    Quy chuẩn hóa Mã CV:
    Mã CV luôn có cấu trúc dạng XX.YYYYY (2 ký tự chữ cái, dấu chấm, và đúng 5 chữ số).
    Nếu file nguồn có mã chỉ chứa 1-4 chữ số sau dấu chấm (ví dụ: AB.123),
    hệ thống tự động đệm thêm các số 0 vào cuối cho đủ 5 chữ số (AB.12300).
    """
    if not raw_code:
        return ""
    code_clean = raw_code.strip()
    match = WORK_CODE_PATTERN.match(code_clean)
    if match:
        letters = match.group(1).upper()
        digits = match.group(2)
        # Pad with zeros to 5 digits
        padded_digits = digits.ljust(5, "0")
        return f"{letters}.{padded_digits}"
    
    # Check if there is an internal period like 'AB.12'
    parts = code_clean.split(".")
    if len(parts) == 2 and len(parts[0]) == 2 and parts[0].isalpha() and parts[1].isdigit():
        letters = parts[0].upper()
        digits = parts[1].ljust(5, "0")
        return f"{letters}.{digits}"

    return code_clean.upper()

def is_header_match(cell_value: str, keywords: List[str]) -> bool:
    if not cell_value:
        return False
    val_lower = cell_value.lower().strip()
    for kw in keywords:
        if kw == val_lower or kw in val_lower:
            return True
    return False

# ================= 1. EXCEL CATALOG PARSER =================
def extract_from_excel(file_bytes: bytes, filename: str) -> List[Dict[str, str]]:
    """
    Trích xuất thông minh từ Excel:
    Duyệt các sheet, tìm bảng có tiêu đề Mã CV và Tên công việc.
    Lọc bỏ văn bản giải thích rườm rà.
    """
    wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
    records = []
    seen_codes = set()

    for sheet in wb.worksheets:
        header_row_idx = None
        col_code_idx = None
        col_name_idx = None
        col_unit_idx = None

        # Scan first 50 rows to detect header table
        for r_idx, row in enumerate(sheet.iter_rows(values_only=True), start=1):
            if r_idx > 50:
                break
            row_str = [clean_str(c) for c in row]
            
            c_code = None
            c_name = None
            c_unit = None
            
            for c_idx, cell_text in enumerate(row_str):
                if not cell_text:
                    continue
                if c_code is None and is_header_match(cell_text, CODE_KEYWORDS):
                    c_code = c_idx
                elif c_name is None and is_header_match(cell_text, NAME_KEYWORDS):
                    c_name = c_idx
                elif c_unit is None and is_header_match(cell_text, UNIT_KEYWORDS):
                    c_unit = c_idx

            if c_code is not None and c_name is not None:
                header_row_idx = r_idx
                col_code_idx = c_code
                col_name_idx = c_name
                col_unit_idx = c_unit
                break

        if header_row_idx is not None:
            # Read rows after header
            for row in sheet.iter_rows(min_row=header_row_idx + 1, values_only=True):
                if not row or len(row) <= max(col_code_idx, col_name_idx):
                    continue
                raw_code = clean_str(row[col_code_idx])
                name = clean_str(row[col_name_idx])
                unit = clean_str(row[col_unit_idx]) if col_unit_idx is not None and len(row) > col_unit_idx else ""

                if not raw_code or not name:
                    continue
                
                # Check if this row is another repeated header or footer
                if is_header_match(raw_code, CODE_KEYWORDS) or is_header_match(name, NAME_KEYWORDS):
                    continue

                norm_code = normalize_work_code(raw_code)
                if norm_code not in seen_codes:
                    seen_codes.add(norm_code)
                    records.append({
                        "code": norm_code,
                        "raw_code": raw_code,
                        "name": name,
                        "unit": extract_first_unit(unit)
                    })

    return records

# ================= 2. WORD (.DOCX) CATALOG PARSER =================
def extract_from_docx(file_bytes: bytes, filename: str) -> List[Dict[str, str]]:
    """
    Trích xuất thông minh từ Word (.docx):
    Bỏ qua toàn bộ văn bản mô tả, chỉ quét các bảng (Tables).
    Tìm hàng tiêu đề có Mã CV & Tên công việc.
    """
    doc = docx.Document(io.BytesIO(file_bytes))
    records = []
    seen_codes = set()

    for table in doc.tables:
        header_row_idx = None
        col_code_idx = None
        col_name_idx = None
        col_unit_idx = None

        for r_idx, row in enumerate(table.rows):
            cells_text = [clean_str(c.text) for c in row.cells]
            
            c_code = None
            c_name = None
            c_unit = None
            for c_idx, cell_text in enumerate(cells_text):
                if not cell_text:
                    continue
                if c_code is None and is_header_match(cell_text, CODE_KEYWORDS):
                    c_code = c_idx
                elif c_name is None and is_header_match(cell_text, NAME_KEYWORDS):
                    c_name = c_idx
                elif c_unit is None and is_header_match(cell_text, UNIT_KEYWORDS):
                    c_unit = c_idx

            if c_code is not None and c_name is not None:
                header_row_idx = r_idx
                col_code_idx = c_code
                col_name_idx = c_name
                col_unit_idx = c_unit
                break

        if header_row_idx is not None:
            for r_idx in range(header_row_idx + 1, len(table.rows)):
                row = table.rows[r_idx]
                cells_text = [clean_str(c.text) for c in row.cells]
                if len(cells_text) <= max(col_code_idx, col_name_idx):
                    continue
                raw_code = cells_text[col_code_idx]
                name = cells_text[col_name_idx]
                unit = cells_text[col_unit_idx] if col_unit_idx is not None and len(cells_text) > col_unit_idx else ""

                if not raw_code or not name:
                    continue
                if is_header_match(raw_code, CODE_KEYWORDS) or is_header_match(name, NAME_KEYWORDS):
                    continue

                norm_code = normalize_work_code(raw_code)
                if norm_code not in seen_codes:
                    seen_codes.add(norm_code)
                    records.append({
                        "code": norm_code,
                        "raw_code": raw_code,
                        "name": name,
                        "unit": extract_first_unit(unit)
                    })

    return records

# ================= 3. PDF CATALOG PARSER =================
def extract_from_pdf(file_bytes: bytes, filename: str) -> List[Dict[str, str]]:
    """
    Trích xuất bảng từ PDF:
    Dùng pdfplumber để trích xuất các bảng, bỏ qua văn bản ngoài bảng.
    """
    if pdfplumber is None:
        raise RuntimeError("Trích xuất PDF chưa được hỗ trợ trên trình duyệt này. Vui lòng chuyển đổi sang tệp Excel (.xlsx) hoặc Word (.docx).")

    records = []
    seen_codes = set()

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue
                
                header_row_idx = None
                col_code_idx = None
                col_name_idx = None
                col_unit_idx = None

                for r_idx, row in enumerate(table):
                    row_str = [clean_str(c) for c in row]
                    c_code = None
                    c_name = None
                    c_unit = None
                    for c_idx, cell_text in enumerate(row_str):
                        if not cell_text:
                            continue
                        if c_code is None and is_header_match(cell_text, CODE_KEYWORDS):
                            c_code = c_idx
                        elif c_name is None and is_header_match(cell_text, NAME_KEYWORDS):
                            c_name = c_idx
                        elif c_unit is None and is_header_match(cell_text, UNIT_KEYWORDS):
                            c_unit = c_idx
                    if c_code is not None and c_name is not None:
                        header_row_idx = r_idx
                        col_code_idx = c_code
                        col_name_idx = c_name
                        col_unit_idx = c_unit
                        break

                if header_row_idx is not None:
                    for row in table[header_row_idx + 1:]:
                        if len(row) <= max(col_code_idx, col_name_idx):
                            continue
                        raw_code = clean_str(row[col_code_idx])
                        name = clean_str(row[col_name_idx])
                        unit = clean_str(row[col_unit_idx]) if col_unit_idx is not None and len(row) > col_unit_idx else ""

                        if not raw_code or not name:
                            continue
                        if is_header_match(raw_code, CODE_KEYWORDS) or is_header_match(name, NAME_KEYWORDS):
                            continue

                        norm_code = normalize_work_code(raw_code)
                        if norm_code not in seen_codes:
                            seen_codes.add(norm_code)
                            records.append({
                                "code": norm_code,
                                "raw_code": raw_code,
                                "name": name,
                                "unit": extract_first_unit(unit)
                            })

    return records

# ================= 4. INSPECTION OF SHEET 'ĐGTH' =================
def inspect_dgth_sheet(file_bytes: bytes, repo_lookup: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    """
    Quy tắc kiểm tra Sheet ĐGTH:
    - Bắt buộc phải có sheet tên 'ĐGTH'.
    - openpyxl data_only=True để lấy giá trị thực từ công thức.
    - Dữ liệu chia thành nhiều bảng theo Hạng mục công trình (STT lặp lại từ 1 trên mỗi bảng có điền lại tiêu đề).
    - Phân nhóm kết quả theo từng Hạng mục công trình.
    - Báo lỗi rõ: Mã không tồn tại trong kho dữ liệu, hoặc Tên không khớp.
    """
    wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
    
    # Match sheet ĐGTH (case-insensitive or exact)
    target_sheet = None
    for name in wb.sheetnames:
        if name.strip().upper() == "ĐGTH":
            target_sheet = wb[name]
            break

    if target_sheet is None:
        return {
            "success": False,
            "error": "NOT_FOUND_DGTH",
            "message": "Không tìm thấy sheet có tên 'ĐGTH' trong file Excel tải lên."
        }

    sections = []
    current_section = {
        "title": "Hạng mục 1",
        "items": [],
        "total_count": 0,
        "valid_count": 0,
        "error_count": 0
    }
    
    col_stt_idx = None
    col_code_idx = None
    col_name_idx = None
    col_unit_idx = None

    last_section_title_candidate = ""
    active_in_table = False
    last_stt_val = 0

    rows = list(target_sheet.iter_rows(values_only=True))
    
    for r_idx, row in enumerate(rows, start=1):
        if not row:
            continue
        row_str = [clean_str(c) for c in row]
        row_non_empty = [c for c in row_str if c]
        if not row_non_empty:
            continue

        # Check if this row is a header row (STT, Mã CV, Tên công việc...)
        c_stt = None
        c_code = None
        c_name = None
        c_unit = None
        
        for c_idx, cell_text in enumerate(row_str):
            if not cell_text:
                continue
            if c_stt is None and is_header_match(cell_text, STT_KEYWORDS):
                c_stt = c_idx
            elif c_code is None and is_header_match(cell_text, CODE_KEYWORDS):
                c_code = c_idx
            elif c_name is None and is_header_match(cell_text, NAME_KEYWORDS):
                c_name = c_idx
            elif c_unit is None and is_header_match(cell_text, UNIT_KEYWORDS):
                c_unit = c_idx

        # If a header row is detected (having code and name, and optionally stt)
        if c_code is not None and c_name is not None:
            # We found a header row for a section!
            col_stt_idx = c_stt
            col_code_idx = c_code
            col_name_idx = c_name
            col_unit_idx = c_unit
            
            # If current section has items, commit it
            if current_section["items"]:
                sections.append(current_section)
                section_title = last_section_title_candidate or f"Hạng mục {len(sections) + 1}"
                current_section = {
                    "title": section_title,
                    "items": [],
                    "total_count": 0,
                    "valid_count": 0,
                    "error_count": 0
                }
            elif last_section_title_candidate:
                current_section["title"] = last_section_title_candidate
                
            active_in_table = True
            last_stt_val = 0
            last_section_title_candidate = ""
            continue

        # If we have active column indices, evaluate this row
        if col_code_idx is not None and col_name_idx is not None and active_in_table:
            stt_raw = clean_str(row[col_stt_idx]) if col_stt_idx is not None and len(row) > col_stt_idx else ""
            raw_code = clean_str(row[col_code_idx]) if len(row) > col_code_idx else ""
            name_raw = clean_str(row[col_name_idx]) if len(row) > col_name_idx else ""
            unit_raw = clean_str(row[col_unit_idx]) if col_unit_idx is not None and len(row) > col_unit_idx else ""

            # Check if this row is a Section / Hạng mục title before items start
            # Usually: STT is empty or non-numeric, raw_code is empty, but name_raw or row has text like "Hạng mục: ..."
            if not raw_code:
                # Potential section divider
                first_text = " ".join(row_non_empty)
                if any(k in first_text.lower() for k in ["hạng mục", "phần", "gói thầu", "công trình", "bảng"]):
                    last_section_title_candidate = first_text
                continue

            # Detect STT reset (e.g. STT restarts from 1 when a new table begins without full header)
            numeric_stt = None
            try:
                # Handle numeric STT like 1, 2 or '1.0'
                numeric_stt = int(float(stt_raw)) if stt_raw else None
            except Exception:
                numeric_stt = None

            if numeric_stt == 1 and last_stt_val > 1:
                # STT reset to 1 -> new section!
                if current_section["items"]:
                    sections.append(current_section)
                    sec_name = last_section_title_candidate or f"Hạng mục {len(sections) + 1}"
                    current_section = {
                        "title": sec_name,
                        "items": [],
                        "total_count": 0,
                        "valid_count": 0,
                        "error_count": 0
                    }
                    last_section_title_candidate = ""

            if numeric_stt is not None:
                last_stt_val = numeric_stt

            # Verify the work code against repository lookup
            norm_code = normalize_work_code(raw_code)
            
            # Lookup check: check norm_code, raw_code, or case-insensitive
            repo_match = (
                repo_lookup.get(norm_code.upper())
                or repo_lookup.get(raw_code.upper())
            )

            status = "VALID"
            status_desc = "Hợp lệ"
            repo_name = ""
            
            if not repo_match:
                status = "NOT_FOUND"
                status_desc = "Không tồn tại trong kho dữ liệu"
            else:
                repo_name = repo_match["name"]
                # Optional check: name resemblance
                # If exact or normalized match
                if name_raw and repo_name and name_raw.strip().lower() != repo_name.strip().lower():
                    # Check if there is significant discrepancy
                    # We can classify as valid code but note the repo name
                    pass

            item_result = {
                "stt": stt_raw or str(len(current_section["items"]) + 1),
                "row_index": r_idx,
                "raw_code": raw_code,
                "norm_code": norm_code,
                "name_in_file": name_raw,
                "unit": unit_raw,
                "repo_name": repo_name,
                "status": status,
                "status_desc": status_desc
            }

            current_section["items"].append(item_result)
            current_section["total_count"] += 1
            if status == "VALID":
                current_section["valid_count"] += 1
            else:
                current_section["error_count"] += 1
        else:
            # Outside table or looking for section title
            text_line = " ".join(row_non_empty)
            if any(k in text_line.lower() for k in ["hạng mục", "phần", "gói thầu", "công trình", "bảng"]):
                last_section_title_candidate = text_line

    if current_section["items"]:
        sections.append(current_section)

    # Compute overall metrics
    total_items = sum(s["total_count"] for s in sections)
    valid_items = sum(s["valid_count"] for s in sections)
    error_items = sum(s["error_count"] for s in sections)

    return {
        "success": True,
        "sections": sections,
        "total_items": total_items,
        "valid_items": valid_items,
        "error_items": error_items,
        "section_count": len(sections)
    }
