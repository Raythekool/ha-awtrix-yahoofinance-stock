@echo off
REM Script to upload stock icons to AWTRIX device
REM Usage: upload_icons.bat [DEVICE_IP] [OPTIONS]

python upload_icons.py --default-icons %*
