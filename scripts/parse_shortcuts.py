#!/usr/bin/env python3
"""
Script to parse Steam shortcuts.vdf file using the vdf library
"""

import vdf
import json
import sys
import os

def parse_shortcuts_vdf(file_path):
    """Parse the shortcuts.vdf file and return the data"""
    try:
        with open(file_path, 'rb') as f:
            # VDF files are typically binary, so we read as binary
            data = vdf.load(f, mapper=vdf.VDFDict)
        return data
    except Exception as e:
        print(f"Error parsing VDF file: {e}")
        # Try alternative approach
        try:
            with open(file_path, 'rb') as f:
                data = vdf.binary_load(f)
            return data
        except Exception as e2:
            print(f"Alternative parsing also failed: {e2}")
            return None

def main():
    # Path to the shortcuts.vdf file (relative to project root)
    shortcuts_path = "../data/shortcuts.vdf"
    
    if not os.path.exists(shortcuts_path):
        print(f"File not found: {shortcuts_path}")
        return
    
    print("Parsing shortcuts.vdf file...")
    data = parse_shortcuts_vdf(shortcuts_path)
    
    if data is None:
        print("Failed to parse the file")
        return
    
    print("\n" + "="*50)
    print("SHORTCUTS.VDF PARSED CONTENT")
    print("="*50)
    
    # Pretty print the data
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    # Also save to a JSON file for easier inspection
    output_file = "../data/shortcuts_parsed.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nParsed data also saved to: {output_file}")

if __name__ == "__main__":
    main()
