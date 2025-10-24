#!/usr/bin/env python3
"""
Script to parse Steam localconfig.vdf file and extract current shortcuts data
"""

import vdf
import json
import sys
import os
import re

def parse_localconfig_vdf(file_path):
    """Parse the localconfig.vdf file and return the data"""
    try:
        with open(file_path, 'rb') as f:
            data = vdf.binary_load(f)
        return data
    except Exception as e:
        print(f"Error parsing localconfig.vdf: {e}")
        return None

def extract_shortcuts_from_config(data):
    """Extract shortcuts data from the localconfig.vdf structure"""
    shortcuts = {}
    
    # Navigate through the config structure to find shortcuts
    # The structure is typically: UserLocalConfigStore -> Software -> Valve -> Steam -> apps
    try:
        apps = data.get('UserLocalConfigStore', {}).get('Software', {}).get('Valve', {}).get('Steam', {}).get('apps', {})
        
        shortcut_index = 0
        for app_id, app_data in apps.items():
            # Check if this app has LaunchOptions (indicating it's a shortcut)
            if 'LaunchOptions' in app_data:
                # Extract shortcut data
                shortcut = {
                    'appid': int(app_id),
                    'AppName': app_data.get('name', f'App {app_id}'),
                    'Exe': app_data.get('LaunchOptions', ''),
                    'StartDir': app_data.get('StartDir', ''),
                    'icon': app_data.get('icon', ''),
                    'ShortcutPath': app_data.get('ShortcutPath', ''),
                    'LaunchOptions': app_data.get('LaunchOptions', ''),
                    'IsHidden': app_data.get('IsHidden', 0),
                    'AllowDesktopConfig': app_data.get('AllowDesktopConfig', 1),
                    'AllowOverlay': app_data.get('AllowOverlay', 1),
                    'OpenVR': app_data.get('OpenVR', 0),
                    'Devkit': app_data.get('Devkit', 0),
                    'DevkitGameID': app_data.get('DevkitGameID', ''),
                    'DevkitOverrideAppID': app_data.get('DevkitOverrideAppID', 0),
                    'LastPlayTime': app_data.get('LastPlayed', 0),
                    'FlatpakAppID': app_data.get('FlatpakAppID', ''),
                    'sortas': app_data.get('sortas', ''),
                    'tags': app_data.get('tags', {})
                }
                
                shortcuts[str(shortcut_index)] = shortcut
                shortcut_index += 1
                
    except Exception as e:
        print(f"Error extracting shortcuts: {e}")
        return {}
    
    return shortcuts

def main():
    # Path to the localconfig.vdf file
    config_path = "/home/deck/.local/share/Steam/userdata/107256425/config/localconfig.vdf"
    
    if not os.path.exists(config_path):
        print(f"File not found: {config_path}")
        return
    
    print("Parsing localconfig.vdf file for current shortcuts...")
    data = parse_localconfig_vdf(config_path)
    
    if data is None:
        print("Failed to parse the file")
        return
    
    print("\n" + "="*50)
    print("CURRENT SHORTCUTS FROM LOCALCONFIG.VDF")
    print("="*50)
    
    # Extract shortcuts
    shortcuts = extract_shortcuts_from_config(data)
    
    if shortcuts:
        print(f"Found {len(shortcuts)} shortcuts:")
        print(json.dumps(shortcuts, indent=2, ensure_ascii=False))
        
        # Save to JSON file
        output_file = "/home/deck/.local/share/Steam/userdata/107256425/config/tmp/current_shortcuts.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(shortcuts, f, indent=2, ensure_ascii=False)
        
        print(f"\nCurrent shortcuts saved to: {output_file}")
    else:
        print("No shortcuts found in localconfig.vdf")
        
        # Let's try a different approach - search for LaunchOptions directly
        print("\nSearching for LaunchOptions in the config...")
        def find_launch_options(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    if key == 'LaunchOptions':
                        print(f"Found LaunchOptions at {current_path}: {value}")
                    elif isinstance(value, (dict, list)):
                        find_launch_options(value, current_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    current_path = f"{path}[{i}]"
                    if isinstance(item, (dict, list)):
                        find_launch_options(item, current_path)
        
        find_launch_options(data)

if __name__ == "__main__":
    main()
