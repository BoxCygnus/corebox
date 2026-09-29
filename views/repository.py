import io
import streamlit as st
import pandas as pd
import config
from i18n import t
from database import db
from auth import is_admin, get_current_user_email
from parsers import extract_from_excel, extract_from_docx, extract_from_pdf

def render_repository_view(lang: str):
    """
    Renders Kho Dữ Liệu (Data Repository) view:
    - Smart Extraction from .docx, .xlsx, .pdf
    - Work code normalization XX.YYYYY
    - File management with source_file tag (Admin only for upload / delete)
    - 'Xem danh mục tổng hợp' (Master Repository Viewer)
    """
    user_is_admin = is_admin()
    user_email = get_current_user_email() or "guest"

    st.markdown(f"## 📁 {t('repo_title', lang)}")
    st.caption(t('repo_desc', lang))
    st.divider()

    # Admin notice if regular user
    if not user_is_admin:
        st.info(f"ℹ️ {t('repo_admin_only_notice', lang, admin_email=config.ADMIN_EMAIL)}")

    # 1. FILE UPLOAD & EXTRACTION SECTION (Admin Only)
    if user_is_admin:
        with st.expander(f"📤 {t('repo_upload_section', lang)}", expanded=True):
            st.markdown(f"*{t('repo_upload_hint', lang)}*")
            st.markdown(
                f"""
                <div style="background:rgba(30,58,138,0.2); padding:0.75rem 1rem; border-radius:8px; border-left:4px solid #38bdf8; margin-bottom:1rem; font-size:0.9rem;">
                    💡 <b>{t('repo_normalize_rule', lang)}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

            uploaded_file = st.file_uploader(
                "Chọn tệp danh mục định mức (.xlsx, .docx, .pdf):",
                type=["xlsx", "docx", "pdf"],
                key="repo_file_uploader"
            )

            if uploaded_file is not None:
                filename = uploaded_file.name
                ext = filename.rsplit(".", 1)[-1].lower()

                col_u1, col_u2 = st.columns([3, 1], vertical_alignment="center")
                with col_u1:
                    st.write(f"📄 **Tệp đã chọn:** `{filename}` ({uploaded_file.size / 1024:.1f} KB)")
                with col_u2:
                    process_btn = st.button(f"⚡ {t('btn_process_file', lang)}", type="primary", use_container_width=True)

                if process_btn:
                    with st.spinner("Đang trích xuất thông minh và chuẩn hóa mã hiệu..."):
                        file_bytes = uploaded_file.getvalue()
                        records = []
                        try:
                            if ext == "xlsx":
                                records = extract_from_excel(file_bytes, filename)
                            elif ext == "docx":
                                records = extract_from_docx(file_bytes, filename)
                            elif ext == "pdf":
                                records = extract_from_pdf(file_bytes, filename)
                        except Exception as e:
                            st.error(f"Lỗi xử lý tệp: {e}")
                            return

                        if not records:
                            st.warning("Không tìm thấy bảng dữ liệu hợp lệ chứa cột Mã CV và Tên công việc trong tệp này.")
                        else:
                            # Save to database
                            inserted_count = db.add_work_codes(records, filename, user_email)
                            st.success(t("msg_upload_success", lang, count=inserted_count, filename=filename))
                            st.rerun()

    # 2. MANAGED FILES LIST
    st.markdown(f"### 📑 {t('repo_files_section', lang)}")
    files = db.get_uploaded_files()

    if not files:
        st.info(t("msg_no_files", lang))
    else:
        for f in files:
            fname = f["filename"]
            fcount = f.get("total_records", 0)
            fuser = f.get("uploaded_by", "")
            ftime = f.get("uploaded_at", "")

            with st.container(border=True):
                col_f1, col_f2 = st.columns([7, 3], vertical_alignment="center")
                with col_f1:
                    st.markdown(f"📄 **{fname}** — `{fcount:,} mã CV`")
                    st.caption(f"Tải lên bởi: `{fuser}` | Lúc: {ftime}")
                with col_f2:
                    if user_is_admin:
                        if st.button(f"🗑️ {t('btn_delete_file', lang)}", key=f"del_file_{fname}", use_container_width=True):
                            db.delete_uploaded_file(fname)
                            st.warning(t("msg_delete_file_success", lang, filename=fname))
                            st.rerun()
                    else:
                        st.caption("🔒 Quyền xem")

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. MASTER REPOSITORY VIEWER ("Xem danh mục tổng hợp")
    st.divider()
    st.markdown(f"### 📚 {t('master_view_title', lang)}")

    total_records = db.count_work_codes()
    if total_records == 0:
        st.info("Kho dữ liệu hiện chưa có bản ghi nào. Hãy tải lên tệp mẫu để xem danh mục.")
        return

    # Filter & Search row
    col_s1, col_s2 = st.columns([2, 3])
    with col_s1:
        file_options = ["Tất cả"] + [f["filename"] for f in files]
        selected_file_filter = st.selectbox(t("filter_by_file", lang), options=file_options, key="repo_file_filter")
    with col_s2:
        search_query = st.text_input(
            "Tìm kiếm:",
            placeholder=t("search_code_or_name", lang),
            key="repo_search_input"
        )

    filter_source = None if selected_file_filter == "Tất cả" else selected_file_filter
    matching_count = db.count_work_codes(search=search_query or None, source_file=filter_source)
    st.caption(t("total_records", lang, count=f"{matching_count:,}"))

    # Pagination
    page_size = 50
    total_pages = max(1, (matching_count + page_size - 1) // page_size)
    page_col1, page_col2 = st.columns([2, 8], vertical_alignment="center")
    with page_col1:
        current_page_num = st.number_input("Trang", min_value=1, max_value=total_pages, value=1, step=1, key="repo_page_num")
    with page_col2:
        st.caption(f"Hiển thị trang {current_page_num} / {total_pages} (50 mã mỗi trang)")

    offset = (current_page_num - 1) * page_size
    records = db.get_work_codes(search=search_query or None, source_file=filter_source, limit=page_size, offset=offset)

    if records:
        df = pd.DataFrame(records)[["code", "raw_code", "name", "unit", "source_file"]]
        df.columns = ["Mã chuẩn hóa (XX.YYYYY)", "Mã gốc trong file", "Tên công việc", "ĐVT", "Tệp nguồn"]
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Export button for repository
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_all = pd.DataFrame(db.get_work_codes(search=search_query or None, source_file=filter_source, limit=10000, offset=0))
            if not df_all.empty:
                df_all = df_all[["code", "raw_code", "name", "unit", "source_file"]]
                df_all.columns = ["Mã chuẩn hóa (XX.YYYYY)", "Mã gốc trong file", "Tên công việc", "ĐVT", "Tệp nguồn"]
                df_all.to_excel(writer, sheet_name='Kho_Du_Lieu', index=False)
        output.seek(0)
        
        st.download_button(
            label=f"📥 {t('btn_export_repo', lang)}",
            data=output,
            file_name="corebox_kho_du_lieu.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_btn_repo_xlsx"
        )
