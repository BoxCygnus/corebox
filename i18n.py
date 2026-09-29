# Multi-language dictionary for COREBOX (Tiếng Việt & English)

TRANSLATIONS = {
    "vi": {
        # App brand & header
        "app_title": "Corebox",
        "app_subtitle": "Đơn giản hóa hành trình chuyển đổi số của bạn",
        "app_description": "Lưu trữ dữ liệu, kiểm tra tự động và các công cụ hỗ trợ.",
        "app_footer": "Phát triển bởi Box",
        
        # Navigation
        "nav_home": "Corebox",
        "nav_tools": "Công cụ",
        "nav_admin": "Quản trị viên",
        "nav_language": "Ngôn ngữ",
        "nav_search_placeholder": "Tìm kiếm chức năng...",
        "nav_repo": "Kho dữ liệu công việc",
        "nav_inspection": "Kiểm tra mã công việc",
        "nav_users": "Quản lý tài khoản",
        "nav_logout": "Đăng xuất",
        "nav_login": "Đăng nhập Google",
        "nav_guest": "Khách",
        "nav_admin_badge": "Quản trị viên",
        "nav_user_badge": "Người dùng",
        "nav_pending_badge": "Chờ duyệt",
        "explore_tools": "Khám phá công cụ →",
        
        # Auth & Approval
        "pending_title": "Tài khoản đang chờ phê duyệt",
        "pending_message": "Tài khoản của bạn ({email}) đã đăng nhập thành công nhưng đang chờ Admin ({admin_email}) phê duyệt. Vui lòng liên hệ quản trị viên.",
        "pending_tip": "Sau khi Admin phê duyệt, vui lòng tải lại trang để truy cập đầy đủ các tính năng của Corebox.",
        "login_prompt": "Vui lòng chọn hoặc nhập tài khoản Google để tiếp tục:",
        "login_button": "Đăng nhập",
        "switch_account": "Chuyển tài khoản",
        "logged_in_as": "Đang đăng nhập với: {email}",
        "access_denied": "Từ chối truy cập! Chức năng này chỉ dành riêng cho Admin ({admin_email}).",
        
        # Admin / User Management
        "user_mgmt_title": "Quản lý tài khoản",
        "user_mgmt_desc": "Duyệt hoặc từ chối các yêu cầu truy cập từ người dùng mới đăng nhập bằng Google.",
        "pending_users_section": "Danh sách tài khoản chờ duyệt ({count})",
        "approved_users_section": "Danh sách người dùng đã kích hoạt ({count})",
        "all_users_section": "Tất cả tài khoản trong hệ thống",
        "th_email": "Email Google",
        "th_name": "Họ và tên",
        "th_role": "Vai trò",
        "th_status": "Trạng thái",
        "th_registered_at": "Thời gian đăng ký",
        "th_actions": "Thao tác",
        "btn_approve": "Phê duyệt",
        "btn_reject": "Từ chối",
        "btn_make_admin": "Cấp quyền Admin",
        "btn_remove_admin": "Thu hồi Admin",
        "btn_delete_user": "Xóa tài khoản",
        "msg_approved_success": "Đã phê duyệt tài khoản {email} thành công!",
        "msg_rejected_success": "Đã từ chối tài khoản {email}.",
        "msg_no_pending": "Hiện tại không có tài khoản nào đang chờ phê duyệt.",
        "badge_root_admin": "👑 Admin chính thức",
        "badge_admin": "⚡ Quản trị viên",
        "badge_user": "👤 Người dùng",
        "last_updated_prefix": "Cập nhật lần cuối",
        "badge_protected": "Hệ thống bảo vệ",
        "btn_suspend": "Tạm khóa",
        "btn_delete": "Xóa",
        "btn_restore": "Khôi phục duyệt",
        "rejected_users_section": "Danh sách tài khoản đã từ chối ({count})",
        "admin_access_hint": "Vui lòng đăng nhập với tài khoản Admin để truy cập khu vực này.",
        "role_engineer": "Kỹ sư",
        "role_pending": "Chờ duyệt",
        
        # Tools: Data Repository
        "repo_title": "Kho dữ liệu công việc",
        "repo_desc": "Tự động trích xuất bảng Mã CV và Tên công việc từ file Word, Excel, PDF và chuẩn hóa định dạng XX.YYYYY.",
        "repo_admin_only_notice": "Lưu ý: Chỉ tài khoản Admin ({admin_email}) mới có quyền Tải lên, Cập nhật và Xóa file trong kho dữ liệu.",
        "repo_upload_section": "Tải lên tệp danh mục mới (.xlsx, .docx, .pdf)",
        "repo_upload_hint": "Hệ thống tự động lọc bỏ văn bản rườm rà, chỉ giữ lại bảng chứa Mã CV và Tên công việc.",
        "repo_normalize_rule": "Quy chuẩn Mã CV: Dạng XX.YYYYY (2 chữ cái, dấu chấm, 5 chữ số). Mã có 3-4 số sau dấu chấm (như AB.123) sẽ tự động đệm 0 thành AB.12300.",
        "btn_process_file": "Bắt đầu trích xuất & Lưu vào kho",
        "repo_files_section": "Quản lý các tệp danh mục đã tải lên",
        "th_filename": "Tên tệp nguồn",
        "th_total_codes": "Số lượng mã",
        "th_uploaded_by": "Người tải lên",
        "th_uploaded_at": "Ngày tải lên",
        "btn_delete_file": "Xóa tệp",
        "btn_view_master": "Xem danh mục tổng hợp",
        "master_view_title": "Danh mục tổng hợp toàn bộ Kho Dữ Liệu",
        "filter_by_file": "Lọc theo tệp nguồn:",
        "search_code_or_name": "Tìm kiếm theo Mã CV hoặc Tên công việc...",
        "total_records": "Tổng số bản ghi: {count}",
        "btn_export_repo": "Tải về danh mục (.xlsx)",
        "msg_upload_success": "Đã trích xuất và thêm thành công {count} mã công việc từ file '{filename}'.",
        "msg_delete_file_success": "Đã xóa toàn bộ dữ liệu của tệp '{filename}'.",
        "msg_no_files": "Chưa có tệp danh mục nào trong kho dữ liệu.",
        "confirm_delete_file": "Bạn có chắc chắn muốn xóa file này cùng tất cả mã định mức tương ứng?",
        "upload_catalog_label": "Chọn tệp danh mục định mức (.xlsx, .docx, .pdf):",
        "selected_file": "Tệp đã chọn",
        "extracting_spinner": "Đang trích xuất thông minh và chuẩn hóa mã hiệu...",
        "msg_no_table_found": "Không tìm thấy bảng dữ liệu hợp lệ chứa cột Mã CV và Tên công việc trong tệp này.",
        "uploaded_by_prefix": "Tải lên bởi",
        "uploaded_at_prefix": "Lúc",
        "view_only_perm": "Quyền xem",
        "msg_repo_empty_browse": "Kho dữ liệu hiện chưa có bản ghi nào. Hãy tải lên tệp mẫu để xem danh mục.",
        "all_option": "Tất cả",
        "search_label": "Tìm kiếm:",
        "page_label": "Trang",
        "showing_page_info": "Hiển thị trang {current} / {total} (50 mã mỗi trang)",
        "col_norm_code": "Mã chuẩn hóa (XX.YYYYY)",
        "col_raw_code": "Mã gốc trong file",
        "col_work_name": "Tên công việc",
        "col_unit": "ĐVT",
        "col_source_file": "Tệp nguồn",
        
        # Tools: Work Code Inspection
        "inspect_title": "Kiểm tra mã công việc",
        "inspect_desc": "Kiểm tra tự động mã CV trên sheet 'ĐGTH' với Kho dữ liệu, phân nhóm lỗi theo từng Hạng mục công trình.",
        "inspect_temp_note": "🔒 Bảo mật: Tệp Excel tải lên chỉ được xử lý tạm thời trong phiên làm việc (Session) và được xóa sạch ngay sau khi xử lý xong, không lưu trữ trên máy chủ.",
        "inspect_sheet_rule": "⚠️ Quy tắc: File phải chứa sheet có tên chính xác là 'ĐGTH'. Hệ thống đọc công thức theo giá trị thực (data_only=True).",
        "upload_inspect_label": "Chọn file dự toán / nghiệm thu Excel (.xlsx, .xlsm):",
        "btn_inspect": "Bắt đầu kiểm tra",
        "inspect_summary_metrics": "Tổng quan kết quả kiểm tra",
        "metric_total_items": "Tổng số công việc",
        "metric_valid_items": "Mã hợp lệ / Khớp",
        "metric_error_items": "Mã lỗi / Không tồn tại",
        "metric_sections": "Số Hạng mục công trình",
        "inspect_results_by_section": "Chi tiết kiểm tra theo từng Hạng mục công trình",
        "error_code_not_found": "Mã không tồn tại trong kho dữ liệu",
        "error_name_mismatch": "Tên công việc không khớp với kho dữ liệu",
        "status_valid": "Hợp lệ",
        "status_invalid": "Không tồn tại trong kho",
        "status_mismatch": "Lệch tên công việc",
        "th_stt": "STT",
        "th_code_in_file": "Mã trong file",
        "th_code_normalized": "Mã chuẩn hóa",
        "th_name_in_file": "Tên trong file",
        "th_repo_name": "Tên trong kho",
        "th_check_status": "Kết quả đối soát",
        "btn_export_inspect_report": "Xuất báo cáo kết quả kiểm tra (.xlsx)",
        "msg_sheet_dgth_not_found": "LỖI: Không tìm thấy sheet có tên 'ĐGTH' trong file Excel. Vui lòng kiểm tra lại tên sheet!",
        "msg_inspect_success": "Đã hoàn thành kiểm tra file '{filename}'!",
        "msg_repo_empty_warn": "Cảnh báo: Kho dữ liệu hiện đang trống. Hãy vào Tools -> Kho Dữ Liệu để tải tệp mẫu lên trước khi kiểm tra.",
        "inspect_upload_help": "Chỉ xử lý trong bộ nhớ phiên làm việc, file sẽ được giải phóng ngay sau đó.",
        "inspect_file_selected": "Tệp kiểm tra",
        "inspecting_spinner": "Đang đọc sheet 'ĐGTH' với data_only=True và phân nhóm theo Hạng mục...",
        "filter_mode_label": "Chế độ hiển thị kết quả:",
        "filter_all": "Tất cả",
        "filter_errors": "Chỉ hiển thị công việc LỖI / KHÔNG TỒN TẠI",
        "filter_valid": "Chỉ hiển thị công việc HỢP LỆ",
        "all_valid_badge": "🟢 Toàn bộ hợp lệ",
        "error_badge": "🔴 {count} mã lỗi",
        "jobs_count_label": "công việc",
        "no_matching_jobs": "Không có dòng công việc nào phù hợp với bộ lọc đã chọn.",
        "status_not_found_icon": "❌ Không có trong kho",
        "status_valid_icon": "✅ Hợp lệ",
        "th_excel_row": "Dòng Excel",
        
        # Home Dashboard Cards
        "home_quick_overview": "Tổng quan hệ thống",
        "home_card_repo_title": "Kho dữ liệu công việc",
        "home_card_repo_desc": "Lưu trữ tập trung, trích xuất thông minh từ Word, Excel, PDF và chuẩn hóa mã hiệu XX.YYYYY.",
        "home_card_inspect_title": "Kiểm tra mã công việc",
        "home_card_inspect_desc": "Tự động rà soát sheet ĐGTH, phân tách theo Hạng mục công trình, phát hiện ngay mã thiếu hoặc sai lệch.",
        "home_card_admin_title": "Quản lý tài khoản",
        "home_card_admin_desc": "Hệ sinh thái phân quyền an toàn, phê duyệt tài khoản Google mới, bảo vệ toàn vẹn dữ liệu.",
        "btn_go": "Truy cập ngay",
        "database_status": "Trạng thái Cơ sở dữ liệu",
        "db_cloudflare_d1": "Cloudflare D1",
        "db_sqlite_local": "SQLite Cục bộ",
    },
    
    "en": {
        # App brand & header
        "app_title": "Corebox",
        "app_subtitle": "Simplify your digital transformation journey",
        "app_description": "Data storage, automated inspection, and other supportive tools.",
        "app_footer": "Developed by Box",
        
        # Navigation
        "nav_home": "Corebox",
        "nav_tools": "Tools",
        "nav_admin": "Administrator",
        "nav_language": "Language",
        "nav_search_placeholder": "Search tools & functions...",
        "nav_repo": "Work Code Data Repository",
        "nav_inspection": "Work Code Inspection",
        "nav_users": "Account Management",
        "nav_logout": "Logout",
        "nav_login": "Google Sign-In",
        "nav_guest": "Guest",
        "nav_admin_badge": "Administrator",
        "nav_user_badge": "User",
        "nav_pending_badge": "Pending Approval",
        "explore_tools": "Explore the tools →",
        
        # Auth & Approval
        "pending_title": "Account Pending Approval",
        "pending_message": "Your account ({email}) has successfully signed in but is currently pending approval by Admin ({admin_email}). Please contact your administrator.",
        "pending_tip": "Once approved by the Administrator, please reload this page to access all Corebox features.",
        "login_prompt": "Please select or enter your Google account to proceed:",
        "login_button": "Sign In",
        "switch_account": "Switch Account",
        "logged_in_as": "Logged in as: {email}",
        "access_denied": "Access Denied! This feature is exclusively available to Admin ({admin_email}).",
        
        # Admin / User Management
        "user_mgmt_title": "Account Management",
        "user_mgmt_desc": "Approve or reject access requests from new users signing in via Google.",
        "pending_users_section": "Pending Approval Queue ({count})",
        "approved_users_section": "Active Users ({count})",
        "all_users_section": "All Accounts in System",
        "th_email": "Google Email",
        "th_name": "Full Name",
        "th_role": "Role",
        "th_status": "Status",
        "th_registered_at": "Registered At",
        "th_actions": "Actions",
        "btn_approve": "Approve",
        "btn_reject": "Reject",
        "btn_make_admin": "Grant Admin",
        "btn_remove_admin": "Revoke Admin",
        "btn_delete_user": "Delete Account",
        "msg_approved_success": "Account {email} has been approved successfully!",
        "msg_rejected_success": "Account {email} has been rejected.",
        "msg_no_pending": "There are currently no accounts waiting for approval.",
        "badge_root_admin": "👑 Official Admin",
        "badge_admin": "⚡ Administrator",
        "badge_user": "👤 User",
        "last_updated_prefix": "Last updated",
        "badge_protected": "System Protected",
        "btn_suspend": "Suspend",
        "btn_delete": "Delete",
        "btn_restore": "Restore",
        "rejected_users_section": "Rejected Accounts List ({count})",
        "admin_access_hint": "Please sign in with an Administrator account to access this area.",
        "role_engineer": "Engineer",
        "role_pending": "Pending Approval",
        
        # Tools: Data Repository
        "repo_title": "Work Code Data Repository",
        "repo_desc": "Intelligent extraction of Work Code and Name tables from Word, Excel, PDF with XX.YYYYY standardization.",
        "repo_admin_only_notice": "Note: Only Admin ({admin_email}) has permission to Upload, Update, and Delete files in the repository.",
        "repo_upload_section": "Upload New Catalog File (.xlsx, .docx, .pdf)",
        "repo_upload_hint": "The system automatically filters out non-table text and keeps only the Work Code and Work Name columns.",
        "repo_normalize_rule": "Code Rule: XX.YYYYY format (2 letters, dot, 5 digits). 3-4 digit suffixes (e.g. AB.123) are auto-padded with trailing zeros to AB.12300.",
        "btn_process_file": "Extract & Save to Repository",
        "repo_files_section": "Managed Catalog Files",
        "th_filename": "Source File",
        "th_total_codes": "Total Codes",
        "th_uploaded_by": "Uploaded By",
        "th_uploaded_at": "Upload Date",
        "btn_delete_file": "Delete File",
        "btn_view_master": "View Master Repository",
        "master_view_title": "Master Work Code Repository",
        "filter_by_file": "Filter by Source File:",
        "search_code_or_name": "Search by Work Code or Name...",
        "total_records": "Total records: {count}",
        "btn_export_repo": "Export Catalog (.xlsx)",
        "msg_upload_success": "Successfully extracted and stored {count} work codes from '{filename}'.",
        "msg_delete_file_success": "Successfully removed all records from '{filename}'.",
        "msg_no_files": "No catalog files have been uploaded yet.",
        "confirm_delete_file": "Are you sure you want to delete this file and all its associated work codes?",
        "upload_catalog_label": "Select catalog file (.xlsx, .docx, .pdf):",
        "selected_file": "Selected file",
        "extracting_spinner": "Intelligently extracting and standardizing work codes...",
        "msg_no_table_found": "No valid data table containing Work Code and Name columns was found in this file.",
        "uploaded_by_prefix": "Uploaded by",
        "uploaded_at_prefix": "At",
        "view_only_perm": "View only",
        "msg_repo_empty_browse": "The data repository is currently empty. Please upload a catalog file to browse.",
        "all_option": "All",
        "search_label": "Search:",
        "page_label": "Page",
        "showing_page_info": "Showing page {current} / {total} (50 codes per page)",
        "col_norm_code": "Normalized Code (XX.YYYYY)",
        "col_raw_code": "Original Code in File",
        "col_work_name": "Work Name",
        "col_unit": "Unit",
        "col_source_file": "Source File",
        
        # Tools: Work Code Inspection
        "inspect_title": "Work Code Inspection",
        "inspect_desc": "Automated verification of sheet 'ĐGTH' against Data Repository, grouped by Construction Section.",
        "inspect_temp_note": "🔒 Privacy: Uploaded inspection files are processed in-memory for the current session and permanently deleted afterwards.",
        "inspect_sheet_rule": "⚠️ Rule: File must contain a sheet named exactly 'ĐGTH'. Evaluated with data_only=True to read formula results.",
        "upload_inspect_label": "Select Excel project / inspection file (.xlsx, .xlsm):",
        "btn_inspect": "Run Inspection",
        "inspect_summary_metrics": "Inspection Summary Metrics",
        "metric_total_items": "Total Jobs",
        "metric_valid_items": "Valid / Matched",
        "metric_error_items": "Errors / Missing",
        "metric_sections": "Construction Sections",
        "inspect_results_by_section": "Inspection Details by Construction Section",
        "error_code_not_found": "Code does not exist in repository",
        "error_name_mismatch": "Work name does not match repository",
        "status_valid": "Valid",
        "status_invalid": "Not in Repository",
        "status_mismatch": "Name Mismatch",
        "th_stt": "No.",
        "th_code_in_file": "Code in File",
        "th_code_normalized": "Normalized Code",
        "th_name_in_file": "Name in File",
        "th_repo_name": "Repository Name",
        "th_check_status": "Verification Result",
        "btn_export_inspect_report": "Export Inspection Report (.xlsx)",
        "msg_sheet_dgth_not_found": "ERROR: Could not find sheet named 'ĐGTH' in the Excel file. Please verify sheet name!",
        "msg_inspect_success": "Completed inspection for file '{filename}'!",
        "msg_repo_empty_warn": "Warning: Data repository is currently empty. Please go to Tools -> Data Repository to upload a catalog first.",
        "inspect_upload_help": "Processed strictly in session memory and cleared immediately after.",
        "inspect_file_selected": "Inspection file",
        "inspecting_spinner": "Reading sheet 'ĐGTH' with data_only=True and grouping by sections...",
        "filter_mode_label": "Result display filter:",
        "filter_all": "All",
        "filter_errors": "Show only ERRORS / MISSING",
        "filter_valid": "Show only VALID jobs",
        "all_valid_badge": "🟢 All Valid",
        "error_badge": "🔴 {count} errors",
        "jobs_count_label": "jobs",
        "no_matching_jobs": "No jobs matching the selected filter.",
        "status_not_found_icon": "❌ Not in Repository",
        "status_valid_icon": "✅ Valid",
        "th_excel_row": "Excel Row",
        
        # Home Dashboard Cards
        "home_quick_overview": "System Overview",
        "home_card_repo_title": "Work Code Data Repository",
        "home_card_repo_desc": "Centralized storage, smart table extraction from Word, Excel, PDF, and XX.YYYYY standardization.",
        "home_card_inspect_title": "Work Code Inspection",
        "home_card_inspect_desc": "Automated scanning of sheet ĐGTH, grouping by section, instant detection of missing or mismatched codes.",
        "home_card_admin_title": "Account Management",
        "home_card_admin_desc": "Secure role-based ecosystem, Google account approval queue, full integrity protection.",
        "btn_go": "Open Tool",
        "database_status": "Database Backend Status",
        "db_cloudflare_d1": "Cloudflare D1",
        "db_sqlite_local": "Local SQLite",
    }
}

def t(key: str, lang: str = "vi", **kwargs) -> str:
    """Translate a key into the selected language with optional string interpolation."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["vi"])
    text = lang_dict.get(key, TRANSLATIONS["vi"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text

def format_datetime_by_lang(val: str, lang: str = "vi") -> str:
    """
    Format date/time string according to language preference:
    - vi: dd-mm-yyyy (e.g. 29-09-2026 21:17:50)
    - en: yyyy-mm-dd (e.g. 2026-09-29 21:17:50)
    """
    if not val:
        return ""
    val_clean = str(val).strip()
    try:
        time_part = ""
        date_part = val_clean
        if " " in val_clean:
            date_part, time_part = val_clean.split(" ", 1)
        elif "T" in val_clean:
            date_part, time_part = val_clean.split("T", 1)
            time_part = time_part.split(".")[0].rstrip("Z")

        delim = "-" if "-" in date_part else ("/" if "/" in date_part else None)
        if delim:
            parts = date_part.split(delim)
            if len(parts) == 3:
                if len(parts[0]) == 4:
                    yyyy, mm, dd = parts[0], parts[1].zfill(2), parts[2].zfill(2)
                elif len(parts[2]) == 4:
                    dd, mm, yyyy = parts[0].zfill(2), parts[1].zfill(2), parts[2]
                else:
                    yyyy, mm, dd = parts[0], parts[1], parts[2]

                if lang == "en":
                    formatted_date = f"{yyyy}-{mm}-{dd}"
                else:
                    formatted_date = f"{dd}-{mm}-{yyyy}"

                if time_part:
                    return f"{formatted_date} {time_part.strip()}"
                return formatted_date
    except Exception:
        pass
    return val_clean
