# 🎨 Icons Upload Guide

## Required Icons

This blueprint uses three icons for stock trend visualization:

- **stock-up** (40160) - Green arrow for price increases
- **stock-down** (40176) - Red arrow for price decreases
- **stock-neutral** (40161) - Neutral icon for minimal changes

**Important:** AWTRIX supports GIF format icons. The upload script automatically prioritizes downloading GIF versions over PNG format for better compatibility.

You can find more icons at [developer.lametric.com/icons](https://developer.lametric.com/icons) or create custom ones.

## 📤 Automatic Script to Upload Icons

We've included a script that automatically downloads the recommended icons from LaMetric and uploads them to your AWTRIX device.

### Easiest method - Just run the script

```bash
# Linux/Mac - prompts for IP
./upload_icons.sh

# Windows - prompts for IP
upload_icons.bat

# Or use Python directly
python3 upload_icons.py
```

When you run the script without any parameters, it will:

1. Prompt you to enter your AWTRIX device IP address
2. Automatically download all 3 stock icons from LaMetric
3. Upload them to your AWTRIX device

### Quick usage with IP address

```bash
# Provide IP address directly (Linux/Mac)
./upload_icons.sh 192.168.1.100

# Provide IP address directly (Windows)
upload_icons.bat 192.168.1.100

# Or use Python directly
python3 upload_icons.py 192.168.1.100
```

### Advanced options

```bash
# Display the list of default icons without uploading
./upload_icons.sh --list-default

# Upload specific custom icons (prompts for IP if not provided)
./upload_icons.sh --icon my-icon 12345 --icon another-icon 67890

# Combine default and custom icons
./upload_icons.sh 192.168.1.100 --default-icons --icon custom-icon 99999

# Upload only custom icons (no defaults)
./upload_icons.sh 192.168.1.100 --icon my-custom-icon 54321
```

### What the script does

- Downloads icons from LaMetric's public icon library (prioritizes GIF format)
- Converts and uploads them to your AWTRIX device `/ICONS/` folder via HTTP API
- No additional dependencies needed - uses only Python 3 standard library
- Works on Linux, Mac, and Windows

The script automatically downloads icons from LaMetric and uploads them to your AWTRIX via HTTP. No additional dependencies are needed, it only uses Python 3 standard library.

## Using Custom Icons

You can use any icon from LaMetric or upload custom ones to your AWTRIX `/ICONS/` folder. The blueprint references icons by their LaMetric ID, which will be automatically named based on the icon ID.

**Icon format:** GIF format is recommended for best compatibility with AWTRIX.
