#!/usr/bin/env python3
"""
Script to download icons from LaMetric and upload them to AWTRIX device.

This script helps you easily upload the necessary icons for the Stock Display blueprint
to your AWTRIX 3 device.
"""

import argparse
import sys
import urllib.request
import urllib.error
import json
import re
import uuid
from pathlib import Path
from typing import List, Tuple


# Default recommended icons for Stock Display
DEFAULT_ICONS = {
    "stock-up": 40160,
    "stock-down": 40176,
    "stock-neutral": 40161,
}

# HTTP request timeout in seconds
REQUEST_TIMEOUT = 10


def validate_ip_or_hostname(address: str) -> bool:
    """
    Validate if the address is a valid IP address or hostname.
    
    Args:
        address: IP address or hostname to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not address:
        return False
    
    # Check for localhost
    if address in ['localhost', '127.0.0.1']:
        return True
    
    # Check for IPv4
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ipv4_pattern, address):
        # Verify each octet is <= 255
        try:
            octets = address.split('.')
            return all(0 <= int(octet) <= 255 for octet in octets)
        except (ValueError, AttributeError):
            return False
    
    # Check for hostname (simplified check, allows single char labels)
    hostname_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$|^[a-zA-Z0-9]$'
    return bool(re.match(hostname_pattern, address))


def sanitize_icon_name(name: str) -> str:
    """
    Sanitize icon name to contain only safe characters.
    
    Args:
        name: Icon name to sanitize
        
    Returns:
        Sanitized name with only alphanumeric, hyphens, and underscores
    """
    # Replace any character that's not alphanumeric, hyphen, or underscore
    sanitized = re.sub(r'[^a-zA-Z0-9\-_]', '_', name)
    # Remove any leading/trailing underscores
    sanitized = sanitized.strip('_')
    return sanitized if sanitized else "icon"


def download_icon(icon_id: int) -> Tuple[bytes, str]:
    """
    Download an icon from LaMetric by its ID.
    
    Args:
        icon_id: The LaMetric icon ID
        
    Returns:
        Tuple of (icon_data, file_extension)
        
    Raises:
        urllib.error.URLError: If download fails
    """
    # Try GIF first (preferred by AWTRIX), then PNG
    for ext in ['gif', 'png']:
        url = f"https://developer.lametric.com/content/apps/icon_thumbs/{icon_id}.{ext}"
        try:
            with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT) as response:
                data = response.read()
                if data:
                    print(f"  ✓ Downloaded icon {icon_id} ({ext.upper()}, 8x8)")
                    return data, ext
        except urllib.error.HTTPError:
            continue
    
    raise ValueError(f"Could not download icon {icon_id} - icon not found or server error")



def upload_icon_to_awtrix(device_ip: str, icon_name: str, icon_data: bytes, file_ext: str) -> bool:
    """
    Upload an icon to AWTRIX device via HTTP.
    
    Args:
        device_ip: IP address of the AWTRIX device
        icon_name: Name for the icon file (without extension)
        icon_data: Binary icon data
        file_ext: File extension (png or gif)
        
    Returns:
        True if successful, False otherwise
    """
    # Sanitize the icon name to prevent path traversal or special character issues
    safe_icon_name = sanitize_icon_name(icon_name)
    
    # AWTRIX uses an /edit endpoint for file uploads
    url = f"http://{device_ip}/edit"
    
    # Create multipart form data with unique boundary
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    
    # Build the multipart body
    body = []
    body.append(f'--{boundary}'.encode())
    body.append(f'Content-Disposition: form-data; name="data"; filename="/ICONS/{safe_icon_name}.{file_ext}"'.encode())
    body.append(f'Content-Type: image/{file_ext}'.encode())
    body.append(b'')
    body.append(icon_data)
    body.append(f'--{boundary}--'.encode())
    body.append(b'')
    
    body_bytes = b'\r\n'.join(body)
    
    # Create request
    req = urllib.request.Request(
        url,
        data=body_bytes,
        headers={
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(body_bytes))
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            if response.status in [200, 201]:
                print(f"  ✓ Uploaded {safe_icon_name}.{file_ext} to AWTRIX")
                return True
            else:
                print(f"  ✗ Upload failed with status {response.status}")
                return False
    except (urllib.error.URLError, OSError) as e:
        print(f"  ✗ Upload failed: {e}")
        return False


def process_icon(device_ip: str, icon_name: str, icon_id: int) -> bool:
    """
    Download an icon from LaMetric and upload it to AWTRIX.
    
    Args:
        device_ip: IP address of the AWTRIX device
        icon_name: Name for the icon
        icon_id: LaMetric icon ID
        
    Returns:
        True if successful, False otherwise
    """
    print(f"\nProcessing {icon_name} (ID: {icon_id})...")
    
    try:
        # Download icon from LaMetric
        icon_data, file_ext = download_icon(icon_id)
        
        # Upload to AWTRIX
        return upload_icon_to_awtrix(device_ip, icon_name, icon_data, file_ext)
    
    except (urllib.error.URLError, OSError, ValueError) as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Download icons from LaMetric and upload them to AWTRIX device.',
        epilog='Example: %(prog)s 192.168.1.100 --default-icons'
    )
    
    parser.add_argument(
        'device_ip',
        nargs='?',
        help='IP address of the AWTRIX device (e.g., 192.168.1.100). If not provided, you will be prompted.'
    )
    
    parser.add_argument(
        '--default-icons',
        action='store_true',
        help='Upload the default recommended icons for Stock Display'
    )
    
    parser.add_argument(
        '--icon',
        action='append',
        nargs=2,
        metavar=('NAME', 'ID'),
        help='Add a custom icon (can be used multiple times). Example: --icon my-icon 12345'
    )
    
    parser.add_argument(
        '--list-default',
        action='store_true',
        help='List the default recommended icons and exit'
    )
    
    args = parser.parse_args()
    
    # List default icons and exit
    if args.list_default:
        print("Default recommended icons for Stock Display:")
        print()
        for name, icon_id in DEFAULT_ICONS.items():
            print(f"  {name:20} - ID: {icon_id}")
        return 0
    
    # Prompt for device IP if not provided
    if not args.device_ip:
        print("AWTRIX Device IP Address")
        print("=" * 60)
        device_ip = input("Enter the IP address or hostname of your AWTRIX device: ").strip()
        if not device_ip:
            print("Error: No IP address provided")
            return 1
        args.device_ip = device_ip
    
    # Validate device IP format
    if not validate_ip_or_hostname(args.device_ip):
        print(f"Error: '{args.device_ip}' does not appear to be a valid IP address or hostname")
        print("Please provide a valid IP address (e.g., 192.168.1.100) or hostname")
        return 1
    
    # Build list of icons to upload
    icons_to_upload = {}
    
    if args.default_icons:
        icons_to_upload.update(DEFAULT_ICONS)
    
    if args.icon:
        for name, icon_id in args.icon:
            try:
                icon_id_int = int(icon_id)
                if icon_id_int <= 0:
                    print(f"Error: Icon ID must be a positive integer, got '{icon_id}'")
                    return 1
                icons_to_upload[name] = icon_id_int
            except ValueError:
                print(f"Error: Icon ID must be a positive integer, got '{icon_id}'")
                return 1
    
    # Validate we have icons to upload
    if not icons_to_upload:
        print("Error: No icons specified. Use --default-icons or --icon to specify icons to upload.")
        print("Run with --help for more information.")
        return 1
    
    # Process all icons
    print(f"Uploading {len(icons_to_upload)} icon(s) to AWTRIX at {args.device_ip}")
    print("=" * 60)
    
    success_count = 0
    for icon_name, icon_id in icons_to_upload.items():
        if process_icon(args.device_ip, icon_name, icon_id):
            success_count += 1
    
    # Summary
    print()
    print("=" * 60)
    print(f"Summary: {success_count}/{len(icons_to_upload)} icons uploaded successfully")
    
    return 0 if success_count == len(icons_to_upload) else 1


if __name__ == "__main__":
    sys.exit(main())
