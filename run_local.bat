@echo off
chcp 65001 > nul
echo ============================================================
echo   KHOI DONG HE THONG QUAN LY DU AN COREBOX (LOCAL)
echo ============================================================
echo.
py -m streamlit run app.py --server.port 8501 --server.headless false
pause
