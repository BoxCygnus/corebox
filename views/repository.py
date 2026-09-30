import io
import re
import json
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import config
from i18n import t, format_datetime_by_lang
from database import db
from auth import is_admin, get_current_user_email
from parsers import extract_from_excel, extract_from_docx, extract_from_pdf, extract_first_unit

def render_repository_view(lang: str):
    """
    Renders Kho Dữ Liệu (Data Repository) view:
    - 3 Collapsible Major Sections (Thu nhỏ vào khay):
      1. Cập nhật tệp danh mục (Upload & Smart Extraction from .docx, .xlsx, .pdf)
      2. Quản lý các tệp danh mục đã tải lên (Managed Files with delete & stats)
      3. Danh mục tổng hợp toàn bộ Kho Dữ Liệu (Master Viewer with search, pagination, export)
    - Full persistence via Cloudflare KV & localStorage
    """
    user_is_admin = is_admin()
    user_email = get_current_user_email() or "guest"

    # Execute any pending catalog sync script
    if "repo_sync_js" in st.session_state and st.session_state["repo_sync_js"]:
        js_code = st.session_state.pop("repo_sync_js")
        components.html(f"<script>{js_code}</script>", height=0, width=0)

    st.markdown(f"## 📁 {t('repo_title', lang)}")
    st.caption(t('repo_desc', lang))
    st.divider()

    # Admin notice if regular user
    if not user_is_admin:
        st.info(f"ℹ️ {t('repo_admin_only_notice', lang)}")

    # 1. MAJOR SECTION: CẬP NHẬT KHO DỮ LIỆU (Upload & Extract)
    with st.expander(f"📤 **{t('repo_update_section', lang)}**", expanded=True):
        if user_is_admin:
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
                t("upload_catalog_label", lang),
                type=["xlsx", "docx", "pdf"],
                key="repo_file_uploader"
            )

            if uploaded_file is not None:
                filename = uploaded_file.name
                ext = filename.rsplit(".", 1)[-1].lower()

                col_u1, col_u2 = st.columns([3, 1], vertical_alignment="center")
                with col_u1:
                    st.write(f"📄 **{t('selected_file', lang)}:** `{filename}` ({uploaded_file.size / 1024:.1f} KB)")
                with col_u2:
                    process_btn = st.button(f"⚡ {t('btn_process_file', lang)}", type="primary", use_container_width=True)

                if process_btn:
                    with st.spinner(t("extracting_spinner", lang)):
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
                            st.error(f"Lỗi trích xuất: {e}")
                            return

                        if not records:
                            st.warning(t("msg_no_table_found", lang))
                        else:
                            inserted_count = db.add_work_codes(records, filename, user_email)
                            cat_json = db.export_catalog_json()
                            st.session_state["repo_sync_js"] = f"""
                            if (window.parent && window.parent.coreboxSaveCatalog) {{
                                window.parent.coreboxSaveCatalog({json.dumps(cat_json)});
                            }}
                            """
                            st.success(t("msg_upload_success", lang, count=inserted_count, filename=filename))
                            st.rerun()
        else:
            st.caption(f"🔒 {t('repo_admin_only_notice', lang)}")

    st.markdown("<div style='margin-top: 0.6rem;'></div>", unsafe_allow_html=True)

    # 2. MAJOR SECTION: QUẢN LÝ KHO DỮ LIỆU
    files = db.get_uploaded_files()
    with st.expander(f"📑 **{t('repo_files_section_collapsible', lang)}**", expanded=True):
        if not files:
            st.info(t("msg_no_files", lang))
        else:
            for f in files:
                fname = f["filename"]
                fcount = f.get("total_records", 0)
                fuser = f.get("uploaded_by", "")
                ftime_formatted = format_datetime_by_lang(f.get("uploaded_at", ""), lang)

                with st.container(border=True):
                    col_f1, col_f2 = st.columns([7, 3], vertical_alignment="center")
                    with col_f1:
                        st.markdown(f"📄 **{fname}** — `{fcount:,} mã CV`")
                        st.caption(f"{t('uploaded_by_prefix', lang)}: `{fuser}` | {t('uploaded_at_prefix', lang)}: {ftime_formatted}")
                    with col_f2:
                        if user_is_admin:
                            if st.button(f"🗑️ {t('btn_delete_file', lang)}", key=f"del_file_{fname}", use_container_width=True):
                                db.delete_uploaded_file(fname)
                                cat_json = db.export_catalog_json()
                                st.session_state["repo_sync_js"] = f"""
                                if (window.parent && window.parent.coreboxSaveCatalog) {{
                                    window.parent.coreboxSaveCatalog({json.dumps(cat_json)});
                                }}
                                """
                                st.warning(t("msg_delete_file_success", lang, filename=fname))
                                st.rerun()
                        else:
                            st.caption(f"🔒 {t('view_only_perm', lang)}")

    st.markdown("<div style='margin-top: 0.6rem;'></div>", unsafe_allow_html=True)

    # 3. MAJOR SECTION: DANH MỤC TỔNG HỢP KHO DỮ LIỆU
    with st.expander(f"📚 **{t('master_view_section_collapsible', lang)}**", expanded=True):
        total_records = db.count_work_codes()
        if total_records == 0:
            st.info(t("msg_repo_empty_browse", lang))
        else:
            # Filter & Search row
            col_s1, col_s2 = st.columns([2, 3])
            with col_s1:
                file_options = [t("all_option", lang)] + [f["filename"] for f in files]
                selected_file_filter = st.selectbox(t("filter_by_file", lang), options=file_options, key="repo_file_filter")
            with col_s2:
                search_query = st.text_input(
                    t("search_label", lang),
                    placeholder=t("search_code_or_name", lang),
                    key="repo_search_input"
                )

            filter_source = None if selected_file_filter == t("all_option", lang) else selected_file_filter
            matching_count = db.count_work_codes(search=search_query or None, source_file=filter_source)
            st.caption(t("total_records", lang, count=f"{matching_count:,}"))

            # Pagination
            page_size = 50
            total_pages = max(1, (matching_count + page_size - 1) // page_size)
            page_col1, page_col2 = st.columns([2, 8], vertical_alignment="center")
            with page_col1:
                current_page_num = st.number_input(t("page_label", lang), min_value=1, max_value=total_pages, value=1, step=1, key="repo_page_num")
            with page_col2:
                st.caption(t("showing_page_info", lang, current=current_page_num, total=total_pages))

            offset = (current_page_num - 1) * page_size
            records = db.get_work_codes(search=search_query or None, source_file=filter_source, limit=page_size, offset=offset)

            if records:
                for r in records:
                    r["unit"] = extract_first_unit(r.get("unit", ""))
                df = pd.DataFrame(records)[["code", "raw_code", "name", "unit", "source_file"]]
                df.columns = [
                    t("col_norm_code", lang),
                    t("col_raw_code", lang),
                    t("col_work_name", lang),
                    t("col_unit", lang),
                    t("col_source_file", lang)
                ]
                st.dataframe(df, use_container_width=True, hide_index=True)

                # Export button
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_all = pd.DataFrame(db.get_work_codes(search=search_query or None, source_file=filter_source, limit=10000, offset=0))
                    if not df_all.empty:
                        for idx_row in range(len(df_all)):
                            df_all.at[idx_row, "unit"] = extract_first_unit(df_all.at[idx_row, "unit"])
                        df_all = df_all[["code", "raw_code", "name", "unit", "source_file"]]
                        df_all.columns = [
                            t("col_norm_code", lang),
                            t("col_raw_code", lang),
                            t("col_work_name", lang),
                            t("col_unit", lang),
                            t("col_source_file", lang)
                        ]
                        df_all.to_excel(writer, sheet_name='Kho_Du_Lieu', index=False)
                output.seek(0)
                
                st.markdown('<div style="margin-top: 1rem; margin-bottom: 0.5cm;">', unsafe_allow_html=True)
                st.download_button(
                    label=f"📥 {t('btn_export_repo', lang)}",
                    data=output,
                    file_name="corebox_kho_du_lieu.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="dl_btn_repo_xlsx"
                )
                st.markdown('</div>', unsafe_allow_html=True)

