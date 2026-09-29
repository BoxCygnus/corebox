@echo off
chcp 65001 > nul
echo ============================================================
echo   XEM TRUOC BAN CLOUDFLARE PAGES (PAGES.DEV) TREN MAY
echo ============================================================
echo.
echo Dang build lai goi Pages moi nhat...
py build_pages.py
echo.
echo Dang khoi dong may chu web tai cong 8080...
echo Hay mo trinh duyet truy cap: http://localhost:8080
echo.
start http://localhost:8080
py -m http.server 8080 --directory public
pause
