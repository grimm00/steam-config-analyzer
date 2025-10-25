"""
Configuration manager for Steam VDF files.

This module handles the main configuration management operations including extraction,
updating, and validation of Steam game configurations.
"""

import json
import vdf
from pathlib import Path
from typing import Dict, Any

from .vdf_parser import VDFParser
from .game_resolver import GameNameResolver
from .backup_manager import BackupManager


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
        self.backup_dir = Path("instance/data/backups")
        self.output_file = Path("instance/data/all_games_config.json")
        
        # Initialize components
        self.parser = VDFParser(self.steam_config_path)
        self.name_resolver = GameNameResolver(steam_user_id)
        self.backup_manager = BackupManager(self.localconfig_path, self.backup_dir)
    
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
        data = self.parser.parse_localconfig()
        
        # Navigate to the apps section
        apps_section = self.parser.get_apps_section(data)
        
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
                try:
                    shortcuts_data = self.parser.parse_shortcuts()
                    shortcuts_section = self.parser.get_shortcuts_section(shortcuts_data)
                    
                    # Find matching shortcut by launch options
                    for shortcut_id, shortcut_info in shortcuts_section.items():
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
        if self.backup_manager.is_steam_running():
            raise RuntimeError("Steam is currently running. Please close Steam before updating configuration.")
        
        # Create backup before making changes
        backup_path = self.backup_manager.create_backup()
        
        try:
            # Parse current localconfig.vdf
            data = self.parser.parse_localconfig()
            
            # Navigate to the apps section
            apps_section = self.parser.get_apps_section(data)
            
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
            self.parser.write_localconfig(data)
            
            print(f"Successfully updated localconfig.vdf")
            print(f"Backup available at: {backup_path}")
            
        except Exception as e:
            print(f"Error updating localconfig.vdf: {e}")
            print(f"Restore from backup: {backup_path}")
            raise
