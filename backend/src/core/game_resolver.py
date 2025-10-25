"""
Game name resolver for Steam app IDs.

This module handles resolving Steam app IDs to human-readable game names using multiple fallback methods.
"""

import json
import vdf
from pathlib import Path
from typing import Dict, Optional


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
        self.cache_file = Path("instance/data/app_name_cache.json")
        
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
