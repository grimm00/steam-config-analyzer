#!/usr/bin/env python3
"""
Script to parse Steam localconfig.vdf file to find current shortcuts
"""

import vdf
import json
import sys
import os

def parse_localconfig_vdf(file_path):
    """Parse the localconfig.vdf file and look for shortcuts"""
    try:
        with open(file_path, 'rb') as f:
            data = vdf.binary_load(f)
        return data
    except Exception as e:
        print(f"Error parsing localconfig.vdf: {e}")
        return None

def find_shortcuts_in_config(data, path=""):
    """Recursively search for shortcuts in the config data"""
    shortcuts_found = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            
            # Check if this looks like a shortcuts section
            if key.lower() == 'shortcuts' or 'shortcut' in key.lower():
                shortcuts_found.append((current_path, value))
            
            # Recursively search nested structures
            if isinstance(value, (dict, list)):
                shortcuts_found.extend(find_shortcuts_in_config(value, current_path))
    
    elif isinstance(data, list):
        for i, item in enumerate(data):
            current_path = f"{path}[{i}]"
            if isinstance(item, (dict, list)):
                shortcuts_found.extend(find_shortcuts_in_config(item, current_path))
    
    return shortcuts_found

def main():
    # Path to the localconfig.vdf file
    config_path = "/home/deck/.local/share/Steam/userdata/107256425/config/localconfig.vdf"
    
    if not os.path.exists(config_path):
        print(f"File not found: {config_path}")
        return
    
    print("Parsing localconfig.vdf file...")
    data = parse_localconfig_vdf(config_path)
    
    if data is None:
        print("Failed to parse the file")
        return
    
    print("\n" + "="*50)
    print("SEARCHING FOR SHORTCUTS IN LOCALCONFIG.VDF")
    print("="*50)
    
    # Search for shortcuts
    shortcuts_found = find_shortcuts_in_config(data)
    
    if shortcuts_found:
        print(f"Found {len(shortcuts_found)} potential shortcuts sections:")
        for path, content in shortcuts_found:
            print(f"\nPath: {path}")
            print("Content:")
            print(json.dumps(content, indent=2, ensure_ascii=False))
    else:
        print("No shortcuts sections found in localconfig.vdf")
        
        # Let's also check the top-level structure
        print("\nTop-level keys in localconfig.vdf:")
        if isinstance(data, dict):
            for key in data.keys():
                print(f"  - {key}")
    
    # Save the full data for inspection
    output_file = "/home/deck/.local/share/Steam/userdata/107256425/config/tmp/localconfig_parsed.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nFull data also saved to: {output_file}")

if __name__ == "__main__":
    main()
