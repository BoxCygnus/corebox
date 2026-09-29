@echo off
chcp 65001 > nul
echo ============================================================
echo   KHOI DONG COREBOX VA TAO LINK CHIA SE MIEN PHI QUA CLOUDFLARE
echo ============================================================
echo.
echo [1/2] Dang khoi chay may chu Corebox Web App...
start "Corebox Web App" py -m streamlit run app.py --server.port 8501 --server.headless true

echo [2/2] Dang ket noi Cloudflare Tunnel (Mien phi, khong can mo port)...
timeout /t 3 > nul
echo.
echo ===========================================================================
echo  CHU Y: Duong link chia se truc tuyen (dang: https://xxx.trycloudflare.com)
echo  se xuat hien ngay ben duoi. Hay copy link do gui cho moi nguoi!
echo ===========================================================================
echo.
"C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:8501
pause
