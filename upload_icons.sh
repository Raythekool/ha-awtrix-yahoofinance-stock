#!/bin/bash
# Script to upload stock icons to AWTRIX device
# Usage: ./upload_icons.sh [DEVICE_IP] [OPTIONS]

python3 upload_icons.py --default-icons "$@"
