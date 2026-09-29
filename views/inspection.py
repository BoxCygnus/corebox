import io
import streamlit as st
import pandas as pd
from i18n import t
from database import db
from parsers import inspect_dgth_sheet

def render_inspection_view(lang: str):
    """
    Renders Kiểm tra mã công việc (Work Code Inspection) view:
    - In-memory session processing, zero permanent server storage
    - Strict ĐGTH sheet check with openpyxl data_only=True
    - Grouping by 'Hạng mục công trình' based on table headers & STT reset to 1
    - Instant missing code detection
    - Overview metrics & st.expander per section
    - Downloadable Excel report
    """
    st.markdown(f"## 🔍 {t('inspect_title', lang)}")
    st.caption(t('inspect_desc', lang))
    st.divider()

    # Informational notice boxes
    col_note1, col_note2 = st.columns(2)
    with col_note1:
        st.markdown(
            f"""
            <div style="background:rgba(15,23,42,0.6); padding:0.85rem 1rem; border-radius:10px; border-left:4px solid #10b981; font-size:0.88rem;">
                {t('inspect_temp_note', lang)}
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_note2:
        st.markdown(
            f"""
            <div style="background:rgba(15,23,42,0.6); padding:0.85rem 1rem; border-radius:10px; border-left:4px solid #f59e0b; font-size:0.88rem;">
                {t('inspect_sheet_rule', lang)}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Check if repository is empty
    total_repo_codes = db.count_work_codes()
    if total_repo_codes == 0:
        st.warning(f"⚠️ {t('msg_repo_empty_warn', lang)}")

    uploaded_excel = st.file_uploader(
        t("upload_inspect_label", lang),
        type=["xlsx", "xlsm"],
        key="inspect_file_uploader",
        help="Chỉ xử lý trong bộ nhớ phiên làm việc, file sẽ được giải phóng ngay sau đó."
    )

    if uploaded_excel is not None:
        filename = uploaded_excel.name
        col_act1, col_act2 = st.columns([3, 1], vertical_alignment="center")
        with col_act1:
            st.write(f"📄 **Tệp kiểm tra:** `{filename}` ({uploaded_excel.size / 1024:.1f} KB)")
        with col_act2:
            inspect_btn = st.button(f"🚀 {t('btn_inspect', lang)}", type="primary", use_container_width=True)

        if inspect_btn or "inspection_results" in st.session_state:
            if inspect_btn:
                with st.spinner("Đang đọc sheet 'ĐGTH' với data_only=True và phân nhóm theo Hạng mục..."):
                    file_bytes = uploaded_excel.getvalue()
                    # In-memory lookup dict from DB
                    repo_lookup = db.get_all_codes_lookup()
                    results = inspect_dgth_sheet(file_bytes, repo_lookup)
                    st.session_state["inspection_results"] = results
                    st.session_state["inspection_file"] = filename

            results = st.session_state.get("inspection_results")
            if not results:
                return

            if not results.get("success"):
                st.error(f"❌ {results.get('message', t('msg_sheet_dgth_not_found', lang))}")
                return

            st.success(t("msg_inspect_success", lang, filename=st.session_state.get("inspection_file", filename)))

            # METRIC OVERVIEW
            st.markdown(f"### 📊 {t('inspect_summary_metrics', lang)}")
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            with m_col1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div style="color:#94a3b8; font-size:0.85rem; font-weight:600;">{t('metric_total_items', lang)}</div>
                        <div class="metric-val metric-val-info">{results['total_items']:,}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with m_col2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div style="color:#94a3b8; font-size:0.85rem; font-weight:600;">{t('metric_valid_items', lang)}</div>
                        <div class="metric-val metric-val-success">{results['valid_items']:,}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with m_col3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div style="color:#94a3b8; font-size:0.85rem; font-weight:600;">{t('metric_error_items', lang)}</div>
                        <div class="metric-val metric-val-danger">{results['error_items']:,}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with m_col4:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div style="color:#94a3b8; font-size:0.85rem; font-weight:600;">{t('metric_sections', lang)}</div>
                        <div class="metric-val metric-val-info" style="color:#c084fc;">{results['section_count']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # FILTER OPTIONS
            filter_mode = st.radio(
                "Chế độ hiển thị kết quả:",
                options=["Tất cả", "Chỉ hiển thị công việc LỖI / KHÔNG TỒN TẠI", "Chỉ hiển thị công việc HỢP LỆ"],
                horizontal=True,
                key="inspect_filter_mode"
            )

            st.markdown(f"### 📑 {t('inspect_results_by_section', lang)}")

            # EXPANDER PER SECTION (Hạng mục công trình)
            export_rows = []

            for s_idx, sec in enumerate(results["sections"]):
                sec_title = sec["title"]
                sec_total = sec["total_count"]
                sec_valid = sec["valid_count"]
                sec_error = sec["error_count"]

                # Badge description
                status_badge = "🟢 Toàn bộ hợp lệ" if sec_error == 0 else f"🔴 {sec_error} mã lỗi"
                expander_label = f"📁 {sec_title}  ({sec_total} công việc | {status_badge})"

                # Auto-expand if there are errors
                is_expanded = (sec_error > 0)

                with st.expander(expander_label, expanded=is_expanded):
                    items = sec["items"]
                    if filter_mode == "Chỉ hiển thị công việc LỖI / KHÔNG TỒN TẠI":
                        filtered_items = [it for it in items if it["status"] != "VALID"]
                    elif filter_mode == "Chỉ hiển thị công việc HỢP LỆ":
                        filtered_items = [it for it in items if it["status"] == "VALID"]
                    else:
                        filtered_items = items

                    if not filtered_items:
                        st.info("Không có dòng công việc nào phù hợp với bộ lọc đã chọn.")
                    else:
                        table_data = []
                        for it in filtered_items:
                            is_err = it["status"] != "VALID"
                            status_icon = "❌ Không có trong kho" if is_err else "✅ Hợp lệ"
                            table_data.append({
                                t("th_stt", lang): it["stt"],
                                "Dòng Excel": it["row_index"],
                                t("th_code_in_file", lang): it["raw_code"],
                                t("th_code_normalized", lang): it["norm_code"],
                                t("th_name_in_file", lang): it["name_in_file"],
                                t("th_repo_name", lang): it["repo_name"] or "—",
                                t("th_check_status", lang): status_icon
                            })
                            # Prepare for report
                            export_rows.append({
                                "Hạng mục công trình": sec_title,
                                "STT": it["stt"],
                                "Dòng Excel": it["row_index"],
                                "Mã trong file": it["raw_code"],
                                "Mã chuẩn hóa": it["norm_code"],
                                "Tên công việc trong file": it["name_in_file"],
                                "Tên trong kho": it["repo_name"],
                                "Trạng thái": status_icon
                            })

                        df_sec = pd.DataFrame(table_data)
                        st.dataframe(df_sec, use_container_width=True, hide_index=True)

            # EXPORT INSPECTION REPORT BUTTON
            if export_rows:
                st.divider()
                rep_out = io.BytesIO()
                with pd.ExcelWriter(rep_out, engine='xlsxwriter') as writer:
                    df_rep = pd.DataFrame(export_rows)
                    df_rep.to_excel(writer, sheet_name='Bao_Cao_Kiem_Tra', index=False)
                rep_out.seek(0)

                st.download_button(
                    label=f"📥 {t('btn_export_inspect_report', lang)}",
                    data=rep_out,
                    file_name=f"bao_cao_kiem_tra_{st.session_state.get('inspection_file', 'DGTH')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="dl_btn_inspect_report"
                )
