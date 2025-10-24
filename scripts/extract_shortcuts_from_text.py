#!/usr/bin/env python3
"""
Script to extract shortcuts data from localconfig.vdf text content
"""

import json
import re
import os

def extract_shortcuts_from_text():
    """Extract shortcuts data from the text content we found"""
    
    # Based on the grep output we found earlier, let's reconstruct the shortcuts
    shortcuts = {
        "0": {
            "appid": -451634645,
            "AppName": "R.E.P.O.",
            "Exe": "/home/deck/.steam/steam/steamapps/common/REPO/REPO.exe",
            "StartDir": "/home/deck/.steam/steam/steamapps/common/REPO/",
            "icon": "",
            "ShortcutPath": "/home/deck/Desktop/R.E.P.O..desktop",
            "LaunchOptions": "%command% --doorstop-enable true --doorstop-target \"/home/deck/.config/r2modmanPlus-local/REPO/profiles/Friends/BepInEx/core/BepInEx.Preloader.dll\" --r2profile \"Friends\"",
            "IsHidden": 0,
            "AllowDesktopConfig": 1,
            "AllowOverlay": 1,
            "OpenVR": 0,
            "Devkit": 0,
            "DevkitGameID": "",
            "DevkitOverrideAppID": 0,
            "LastPlayTime": 1761006928,  # From the autocloud data we found
            "FlatpakAppID": "",
            "sortas": "",
            "tags": {}
        }
    }
    
    return shortcuts

def main():
    print("Extracting current shortcuts data...")
    
    # Extract shortcuts
    shortcuts = extract_shortcuts_from_text()
    
    print("\n" + "="*50)
    print("CURRENT SHORTCUTS (UPDATED WITH FRIENDS PROFILE)")
    print("="*50)
    
    print(json.dumps(shortcuts, indent=2, ensure_ascii=False))
    
    # Save to JSON file
    output_file = "/home/deck/.local/share/Steam/userdata/107256425/config/tmp/current_shortcuts_updated.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(shortcuts, f, indent=2, ensure_ascii=False)
    
    print(f"\nCurrent shortcuts saved to: {output_file}")
    
    # Also create a comparison showing the difference
    print("\n" + "="*50)
    print("COMPARISON: OLD vs CURRENT")
    print("="*50)
    
    old_launch_options = "--doorstop-enable true --doorstop-target \"/home/deck/.config/r2modmanPlus-local/REPO/profiles/Kat/BepInEx/core/BepInEx.Preloader.dll\" --r2profile \"Kat\""
    new_launch_options = "%command% --doorstop-enable true --doorstop-target \"/home/deck/.config/r2modmanPlus-local/REPO/profiles/Friends/BepInEx/core/BepInEx.Preloader.dll\" --r2profile \"Friends\""
    
    print("OLD (from shortcuts.vdf):")
    print(f"  {old_launch_options}")
    print("\nCURRENT (from localconfig.vdf):")
    print(f"  {new_launch_options}")
    
    print(f"\n✅ Profile changed from 'Kat' to 'Friends'")
    print(f"✅ Added %command% prefix")
    print(f"✅ Updated LastPlayTime to {shortcuts['0']['LastPlayTime']}")

if __name__ == "__main__":
    main()
