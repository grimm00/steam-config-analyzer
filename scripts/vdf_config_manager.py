#!/usr/bin/env python3
"""
VDF Configuration Manager for Steam

This tool can read and write Steam shortcut configurations from localconfig.vdf
with JSON as the intermediate format for frontend integration.
"""

import vdf
import json
import os
import sys
import shutil
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class VDFConfigManager:
    """Manages Steam VDF configuration files with read/write capabilities."""
    
    def __init__(self, steam_user_id: str = "107256425"):
        """
        Initialize the VDF Config Manager.
        
        Args:
            steam_user_id: Steam user ID (default: 107256425)
        """
        self.steam_user_id = steam_user_id
        self.steam_config_path = Path.home() / ".local" / "share" / "Steam" / "userdata" / steam_user_id / "config"
        self.localconfig_path = self.steam_config_path / "localconfig.vdf"
        self.backup_dir = Path("data/backups")
        self.output_file = Path("data/shortcuts_config.json")
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Known app ID mappings (Steam app ID -> App Name)
        # This can be extended or loaded from a config file
        self.app_id_mappings = {
            "3241660": "R.E.P.O.",
            # Add more mappings as needed
        }
        
    def is_steam_running(self) -> bool:
        """Check if Steam is currently running."""
        try:
            result = subprocess.run(['pgrep', '-f', 'steam'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def create_backup(self) -> str:
        """Create a timestamped backup of localconfig.vdf."""
        if not self.localconfig_path.exists():
            raise FileNotFoundError(f"localconfig.vdf not found at {self.localconfig_path}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"localconfig_backup_{timestamp}.vdf"
        
        shutil.copy2(self.localconfig_path, backup_path)
        print(f"Backup created: {backup_path}")
        return str(backup_path)
    
    def parse_localconfig(self) -> Dict[str, Any]:
        """Parse localconfig.vdf file and return the data."""
        if not self.localconfig_path.exists():
            raise FileNotFoundError(f"localconfig.vdf not found at {self.localconfig_path}")
        
        try:
            # Try text parsing first (since we confirmed it's ASCII text)
            with open(self.localconfig_path, 'r', encoding='utf-8') as f:
                data = vdf.load(f, mapper=vdf.VDFDict)
            return data
        except Exception as e:
            print(f"Text parsing failed: {e}")
            try:
                # Fallback to binary parsing
                with open(self.localconfig_path, 'rb') as f:
                    data = vdf.binary_load(f)
                return data
            except Exception as e2:
                raise Exception(f"Both text and binary parsing failed: {e2}")
    
    def extract_shortcuts(self) -> Dict[str, Any]:
        """
        Extract shortcut configurations from localconfig.vdf.
        
        Returns:
            Dictionary containing shortcut data with essential fields only
        """
        data = self.parse_localconfig()
        
        # Navigate to the apps section
        apps_section = data.get("UserLocalConfigStore", {}).get("Software", {}).get("Valve", {}).get("Steam", {}).get("apps", {})
        
        shortcuts = {}
        
        # Look for apps with LaunchOptions (these are likely non-Steam games)
        for app_id, app_data in apps_section.items():
            if isinstance(app_data, dict) and "LaunchOptions" in app_data:
                # Extract essential fields
                shortcut_data = {
                    "appid": app_id,
                    "LaunchOptions": app_data.get("LaunchOptions", ""),
                    "Playtime": app_data.get("Playtime", "0"),
                    "LastPlayed": app_data.get("LastPlayed", "0"),
                    "ResolutionOverride": app_data.get("ResolutionOverride", ""),
                }
                
                # Try to get additional info from other sections
                # Check if this is a non-Steam game by looking for negative app IDs in shortcuts.vdf
                shortcuts_path = self.steam_config_path / "shortcuts.vdf"
                if shortcuts_path.exists():
                    try:
                        with open(shortcuts_path, 'rb') as f:
                            shortcuts_data = vdf.binary_load(f)
                        
                        # Find matching shortcut by launch options
                        for shortcut_id, shortcut_info in shortcuts_data.get("shortcuts", {}).items():
                            if (shortcut_info.get("LaunchOptions", "").replace("%command% ", "") == 
                                app_data.get("LaunchOptions", "").replace("%command% ", "")):
                                shortcut_data.update({
                                    "AppName": shortcut_info.get("AppName", f"App {app_id}"),
                                    "Exe": shortcut_info.get("Exe", ""),
                                    "StartDir": shortcut_info.get("StartDir", ""),
                                    "IsHidden": shortcut_info.get("IsHidden", 0),
                                    "AllowDesktopConfig": shortcut_info.get("AllowDesktopConfig", 1),
                                    "AllowOverlay": shortcut_info.get("AllowOverlay", 1),
                                })
                                break
                    except Exception as e:
                        print(f"Warning: Could not read shortcuts.vdf: {e}")
                
                # If we couldn't get name from shortcuts.vdf, try known mappings
                if "AppName" not in shortcut_data:
                    shortcut_data["AppName"] = self.app_id_mappings.get(app_id, f"App {app_id}")
                
                shortcuts[app_id] = shortcut_data
        
        return shortcuts
    
    def save_shortcuts_json(self, shortcuts: Dict[str, Any]) -> None:
        """Save shortcuts data to JSON file."""
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(shortcuts, f, indent=2, ensure_ascii=False)
        
        print(f"Shortcuts saved to: {self.output_file}")
    
    def load_shortcuts_json(self) -> Dict[str, Any]:
        """Load shortcuts data from JSON file."""
        if not self.output_file.exists():
            raise FileNotFoundError(f"Shortcuts JSON not found at {self.output_file}")
        
        with open(self.output_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def update_localconfig(self, shortcuts: Dict[str, Any]) -> None:
        """
        Update localconfig.vdf with modified shortcut data.
        
        Args:
            shortcuts: Dictionary containing updated shortcut configurations
        """
        if self.is_steam_running():
            raise RuntimeError("Steam is currently running. Please close Steam before updating configuration.")
        
        # Create backup before making changes
        backup_path = self.create_backup()
        
        try:
            # Parse current localconfig.vdf
            data = self.parse_localconfig()
            
            # Navigate to the apps section
            apps_section = data["UserLocalConfigStore"]["Software"]["Valve"]["Steam"]["apps"]
            
            # Update each shortcut
            for app_id, shortcut_data in shortcuts.items():
                if app_id in apps_section:
                    # Update only the fields we care about
                    if "LaunchOptions" in shortcut_data:
                        apps_section[app_id]["LaunchOptions"] = shortcut_data["LaunchOptions"]
                    if "ResolutionOverride" in shortcut_data:
                        apps_section[app_id]["ResolutionOverride"] = shortcut_data["ResolutionOverride"]
                else:
                    print(f"Warning: App ID {app_id} not found in localconfig.vdf")
            
            # Write back to file
            with open(self.localconfig_path, 'w', encoding='utf-8') as f:
                vdf.dump(data, f, pretty=True)
            
            print(f"Successfully updated localconfig.vdf")
            print(f"Backup available at: {backup_path}")
            
        except Exception as e:
            print(f"Error updating localconfig.vdf: {e}")
            print(f"Restore from backup: {backup_path}")
            raise
    
    def restore_backup(self, backup_path: str) -> None:
        """Restore localconfig.vdf from a backup file."""
        if self.is_steam_running():
            raise RuntimeError("Steam is currently running. Please close Steam before restoring configuration.")
        
        backup_file = Path(backup_path)
        if not backup_file.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        shutil.copy2(backup_file, self.localconfig_path)
        print(f"Restored localconfig.vdf from: {backup_path}")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="VDF Configuration Manager for Steam")
    parser.add_argument("command", choices=["extract", "update", "backup", "restore"], 
                       help="Command to execute")
    parser.add_argument("--user-id", default="107256425", 
                       help="Steam user ID (default: 107256425)")
    parser.add_argument("--backup-path", 
                       help="Path to backup file (for restore command)")
    
    args = parser.parse_args()
    
    try:
        manager = VDFConfigManager(args.user_id)
        
        if args.command == "extract":
            print("Extracting shortcuts from localconfig.vdf...")
            shortcuts = manager.extract_shortcuts()
            manager.save_shortcuts_json(shortcuts)
            print(f"Found {len(shortcuts)} shortcuts with launch options")
            
        elif args.command == "update":
            print("Updating localconfig.vdf with JSON data...")
            shortcuts = manager.load_shortcuts_json()
            manager.update_localconfig(shortcuts)
            
        elif args.command == "backup":
            print("Creating backup of localconfig.vdf...")
            backup_path = manager.create_backup()
            
        elif args.command == "restore":
            if not args.backup_path:
                print("Error: --backup-path required for restore command")
                sys.exit(1)
            print(f"Restoring from backup: {args.backup_path}")
            manager.restore_backup(args.backup_path)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
