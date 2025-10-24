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
import glob
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class GameNameResolver:
    """Resolves Steam app IDs to human-readable game names using multiple fallback methods."""
    
    def __init__(self, steam_user_id: str = "107256425"):
        """
        Initialize the Game Name Resolver.
        
        Args:
            steam_user_id: Steam user ID (default: 107256425)
        """
        self.steam_user_id = steam_user_id
        self.steam_path = Path.home() / ".local" / "share" / "Steam"
        self.steamapps_path = self.steam_path / "steamapps"
        self.library_cache_path = self.steam_path / "userdata" / steam_user_id / "config" / "librarycache"
        self.shortcuts_path = self.steam_path / "userdata" / steam_user_id / "config" / "shortcuts.vdf"
        self.cache_file = Path("data/app_name_cache.json")
        
        # Manual mappings for games not found in other sources
        self.manual_mappings = {
            "3241660": "R.E.P.O.",
            # Add more mappings as needed
        }
        
        # System apps to filter out (optional)
        self.system_apps = {
            "steam linux runtime", "proton", "steamworks", "steam client"
        }
        
        # Load cached mappings
        self.cached_mappings = self._load_cache()
    
    def _load_cache(self) -> Dict[str, str]:
        """Load cached app ID to name mappings."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load app name cache: {e}")
        return {}
    
    def _save_cache(self) -> None:
        """Save app ID to name mappings to cache."""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cached_mappings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save app name cache: {e}")
    
    def _get_name_from_app_manifest(self, app_id: str) -> Optional[str]:
        """Get game name from app manifest file (primary method)."""
        manifest_path = self.steamapps_path / f"appmanifest_{app_id}.acf"
        if not manifest_path.exists():
            return None
        
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple parsing for the name field
                for line in content.split('\n'):
                    if '"name"' in line and '\t' in line:
                        # Extract name from line like: "name"		"Game Name"
                        parts = line.split('\t')
                        if len(parts) >= 3:
                            name = parts[-1].strip().strip('"')
                            return name
        except Exception as e:
            print(f"Warning: Could not parse app manifest for {app_id}: {e}")
        
        return None
    
    def _get_name_from_library_cache(self, app_id: str) -> Optional[str]:
        """Get game name from library cache JSON (fallback 1)."""
        cache_file = self.library_cache_path / f"{app_id}.json"
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Library cache has complex structure, look for descriptions
                for item in data:
                    if isinstance(item, list) and len(item) >= 2:
                        if item[0] == "descriptions" and isinstance(item[1], dict):
                            desc_data = item[1].get("data", {})
                            # Try to extract name from description or other fields
                            # This is a simplified approach - library cache is complex
                            pass
        except Exception as e:
            print(f"Warning: Could not parse library cache for {app_id}: {e}")
        
        return None
    
    def _get_name_from_shortcuts(self, app_id: str) -> Optional[str]:
        """Get game name from shortcuts.vdf (fallback 2)."""
        if not self.shortcuts_path.exists():
            return None
        
        try:
            with open(self.shortcuts_path, 'rb') as f:
                shortcuts_data = vdf.binary_load(f)
            
            # Look for matching shortcut by comparing with localconfig data
            # This is complex since we need to match by launch options or other criteria
            for shortcut_id, shortcut_info in shortcuts_data.get("shortcuts", {}).items():
                if shortcut_info.get("AppName"):
                    # For now, we'll use this as a general fallback
                    # In practice, we'd need to match by launch options or other criteria
                    pass
        except Exception as e:
            print(f"Warning: Could not parse shortcuts.vdf: {e}")
        
        return None
    
    def get_game_name(self, app_id: str, force_refresh: bool = False) -> str:
        """
        Get game name for an app ID using multiple fallback methods.
        
        Args:
            app_id: Steam app ID
            force_refresh: Force refresh from sources, bypass cache
            
        Returns:
            Game name or fallback name
        """
        # Check cache first (unless force refresh)
        if not force_refresh and app_id in self.cached_mappings:
            return self.cached_mappings[app_id]
        
        # Try app manifest (primary method)
        name = self._get_name_from_app_manifest(app_id)
        if name:
            self.cached_mappings[app_id] = name
            return name
        
        # Try library cache (fallback 1)
        name = self._get_name_from_library_cache(app_id)
        if name:
            self.cached_mappings[app_id] = name
            return name
        
        # Try shortcuts.vdf (fallback 2)
        name = self._get_name_from_shortcuts(app_id)
        if name:
            self.cached_mappings[app_id] = name
            return name
        
        # Try manual mappings (fallback 3)
        if app_id in self.manual_mappings:
            name = self.manual_mappings[app_id]
            self.cached_mappings[app_id] = name
            return name
        
        # Final fallback
        fallback_name = f"App {app_id}"
        self.cached_mappings[app_id] = fallback_name
        return fallback_name
    
    def is_system_app(self, app_id: str, app_name: str) -> bool:
        """Check if an app is a system app (Proton, Steam Runtime, etc.)."""
        name_lower = app_name.lower()
        return any(system_name in name_lower for system_name in self.system_apps)
    
    def refresh_cache(self) -> None:
        """Refresh the entire cache by re-scanning all sources."""
        print("Refreshing app name cache...")
        self.cached_mappings.clear()
        self._save_cache()
        print(f"Cache refreshed. Found {len(self.cached_mappings)} mappings.")


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
        self.output_file = Path("data/all_games_config.json")
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize game name resolver
        self.name_resolver = GameNameResolver(steam_user_id)
        
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
    
    def extract_all_games(self, include_system_apps: bool = False, mode: str = "sparse", include_managed: bool = False) -> Dict[str, Any]:
        """
        Extract all game configurations from localconfig.vdf.
        
        Args:
            include_system_apps: Whether to include system apps (Proton, Steam Runtime, etc.)
            mode: Extraction mode - "sparse" (only existing fields) or "standard" (all fields)
            include_managed: Whether to include Steam-managed fields (cloud, autocloud, BadgeData)
            
        Returns:
            Dictionary containing all game data with essential fields
        """
        data = self.parse_localconfig()
        
        # Navigate to the apps section
        apps_section = data.get("UserLocalConfigStore", {}).get("Software", {}).get("Valve", {}).get("Steam", {}).get("apps", {})
        
        all_games = {}
        
        print(f"Found {len(apps_section)} apps in localconfig.vdf")
        print(f"Extraction mode: {mode} (managed fields: {'included' if include_managed else 'excluded'})")
        
        # Define field categories
        essential_fields = {"LastPlayed", "Playtime", "LaunchOptions"}
        optional_user_fields = {"ResolutionOverride", "ResolutionOverrideInternalDisplay", "Playtime2wks", "PlaytimeDisconnected"}
        managed_fields = {"cloud", "autocloud", "BadgeData"}
        eula_fields = set()  # Will be populated dynamically
        
        # Process all apps
        for app_id, app_data in apps_section.items():
            if not isinstance(app_data, dict):
                continue
            
            # Get game name using the resolver
            app_name = self.name_resolver.get_game_name(app_id)
            
            # Skip system apps if not requested
            if not include_system_apps and self.name_resolver.is_system_app(app_id, app_name):
                continue
            
            # Start with essential fields that are always added by the tool
            game_data = {
                "appid": app_id,
                "AppName": app_name,
            }
            
            # Extract fields based on mode
            if mode == "sparse":
                # Sparse mode: only include fields that actually exist
                for field_name, field_value in app_data.items():
                    # Skip EULA fields unless include_managed is True
                    if field_name.endswith("_eula_0") or field_name.endswith("_eula_1"):
                        if include_managed:
                            game_data[field_name] = field_value
                        continue
                    
                    # Skip managed fields unless include_managed is True
                    if field_name in managed_fields:
                        if include_managed:
                            game_data[field_name] = field_value
                        continue
                    
                    # Include all other fields (essential + optional user fields)
                    game_data[field_name] = field_value
                    
            else:  # standard mode
                # Standard mode: include all fields with defaults for missing ones
                for field in essential_fields | optional_user_fields:
                    game_data[field] = app_data.get(field, "")
                
                # Add managed fields if requested
                if include_managed:
                    for field in managed_fields:
                        if field in app_data:
                            game_data[field] = app_data[field]
                
                # Add EULA fields if requested
                if include_managed:
                    for field_name, field_value in app_data.items():
                        if field_name.endswith("_eula_0") or field_name.endswith("_eula_1"):
                            game_data[field_name] = field_value
            
            # Try to get additional info from shortcuts.vdf for non-Steam games
            if app_data.get("LaunchOptions"):
                shortcuts_path = self.steam_config_path / "shortcuts.vdf"
                if shortcuts_path.exists():
                    try:
                        with open(shortcuts_path, 'rb') as f:
                            shortcuts_data = vdf.binary_load(f)
                        
                        # Find matching shortcut by launch options
                        for shortcut_id, shortcut_info in shortcuts_data.get("shortcuts", {}).items():
                            if (shortcut_info.get("LaunchOptions", "").replace("%command% ", "") == 
                                app_data.get("LaunchOptions", "").replace("%command% ", "")):
                                # Add shortcut fields based on mode
                                shortcut_fields = ["Exe", "StartDir", "IsHidden", "AllowDesktopConfig", "AllowOverlay"]
                                for field in shortcut_fields:
                                    if mode == "sparse":
                                        # Only add if it exists and has a value
                                        if field in shortcut_info and shortcut_info[field]:
                                            game_data[field] = shortcut_info[field]
                                    else:
                                        # Standard mode: add with default
                                        game_data[field] = shortcut_info.get(field, "" if field in ["Exe", "StartDir"] else 0)
                                break
                    except Exception as e:
                        print(f"Warning: Could not read shortcuts.vdf: {e}")
            
            all_games[app_id] = game_data
        
        # Save the name resolver cache
        self.name_resolver._save_cache()
        
        print(f"Extracted {len(all_games)} games (system apps {'included' if include_system_apps else 'excluded'})")
        return all_games
    
    def extract_shortcuts(self) -> Dict[str, Any]:
        """
        Extract shortcut configurations from localconfig.vdf (legacy method for compatibility).
        
        Returns:
            Dictionary containing shortcut data with essential fields only
        """
        # Use the new method but filter to only games with launch options
        all_games = self.extract_all_games(include_system_apps=False, mode="standard")
        shortcuts = {}
        
        for app_id, game_data in all_games.items():
            if game_data.get("LaunchOptions"):
                shortcuts[app_id] = game_data
        
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
            
            # Define field categories for validation
            safe_user_fields = {
                "LaunchOptions", "ResolutionOverride", "ResolutionOverrideInternalDisplay",
                "Playtime2wks", "PlaytimeDisconnected"
            }
            managed_fields = {"cloud", "autocloud", "BadgeData"}
            dangerous_fields = set()  # EULA fields and others
            
            # Update each shortcut
            for app_id, shortcut_data in shortcuts.items():
                if app_id not in apps_section:
                    print(f"Warning: App ID {app_id} not found in localconfig.vdf")
                    continue
                
                # Validate and update fields
                for field_name, field_value in shortcut_data.items():
                    # Skip tool-added fields
                    if field_name in {"appid", "AppName"}:
                        continue
                    
                    # Check for dangerous fields
                    if field_name.endswith("_eula_0") or field_name.endswith("_eula_1"):
                        print(f"Warning: EULA field {field_name} detected - skipping for safety")
                        continue
                    
                    # Check for managed fields
                    if field_name in managed_fields:
                        print(f"Warning: Steam-managed field {field_name} detected - skipping for safety")
                        continue
                    
                    # Handle field deletion (null values)
                    if field_value is None:
                        if field_name in apps_section[app_id]:
                            del apps_section[app_id][field_name]
                            print(f"Deleted field {field_name} from app {app_id}")
                        continue
                    
                    # Handle empty strings (don't write, delete if exists)
                    if field_value == "":
                        if field_name in apps_section[app_id]:
                            del apps_section[app_id][field_name]
                            print(f"Removed empty field {field_name} from app {app_id}")
                        continue
                    
                    # Update field value
                    if field_name in safe_user_fields:
                        apps_section[app_id][field_name] = field_value
                        print(f"Updated {field_name} for app {app_id}")
                    else:
                        print(f"Warning: Unknown field {field_name} - updating anyway")
                        apps_section[app_id][field_name] = field_value
            
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
    parser = argparse.ArgumentParser(description="Enhanced VDF Configuration Manager for Steam")
    parser.add_argument("command", choices=["extract", "extract-all", "update", "backup", "restore", "refresh-cache"], 
                       help="Command to execute")
    parser.add_argument("--user-id", default="107256425", 
                       help="Steam user ID (default: 107256425)")
    parser.add_argument("--backup-path", 
                       help="Path to backup file (for restore command)")
    parser.add_argument("--include-system", action="store_true",
                       help="Include system apps (Proton, Steam Runtime) in extraction")
    parser.add_argument("--mode", choices=["sparse", "standard"], default="sparse",
                       help="Extraction mode: sparse (only existing fields) or standard (all fields)")
    parser.add_argument("--include-managed", action="store_true",
                       help="Include Steam-managed fields (cloud, autocloud, BadgeData, EULA)")
    
    args = parser.parse_args()
    
    try:
        manager = VDFConfigManager(args.user_id)
        
        if args.command == "extract":
            print("Extracting shortcuts (games with launch options) from localconfig.vdf...")
            shortcuts = manager.extract_shortcuts()
            manager.save_shortcuts_json(shortcuts)
            print(f"Found {len(shortcuts)} shortcuts with launch options")
            
        elif args.command == "extract-all":
            print("Extracting all games from localconfig.vdf...")
            all_games = manager.extract_all_games(
                include_system_apps=args.include_system,
                mode=args.mode,
                include_managed=args.include_managed
            )
            manager.save_shortcuts_json(all_games)
            print(f"Found {len(all_games)} games total")
            
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
            
        elif args.command == "refresh-cache":
            print("Refreshing app name cache...")
            manager.name_resolver.refresh_cache()
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
