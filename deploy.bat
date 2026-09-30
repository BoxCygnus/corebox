@echo off
echo ====================================================
echo  COREBOX AUTOMATED BUILD, GITHUB PUSH ^& CLOUDFLARE DEPLOY
echo ====================================================
python deploy_all.py %*
pause
