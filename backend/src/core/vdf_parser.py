"""
VDF (Valve Data Format) parser for Steam configuration files.

This module handles parsing of Steam's VDF files, including localconfig.vdf and shortcuts.vdf.
"""

import vdf
from pathlib import Path
from typing import Dict, Any


class VDFParser:
    """Handles parsing of Steam VDF configuration files."""
    
    def __init__(self, steam_config_path: Path):
        """
        Initialize the VDF parser.
        
        Args:
            steam_config_path: Path to Steam config directory
        """
        self.steam_config_path = steam_config_path
        self.localconfig_path = steam_config_path / "localconfig.vdf"
        self.shortcuts_path = steam_config_path / "shortcuts.vdf"
    
    def parse_localconfig(self) -> Dict[str, Any]:
        """
        Parse localconfig.vdf file and return the data.
        
        Returns:
            Parsed VDF data as dictionary
            
        Raises:
            FileNotFoundError: If localconfig.vdf doesn't exist
            Exception: If both text and binary parsing fail
        """
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
    
    def parse_shortcuts(self) -> Dict[str, Any]:
        """
        Parse shortcuts.vdf file and return the data.
        
        Returns:
            Parsed VDF data as dictionary
            
        Raises:
            FileNotFoundError: If shortcuts.vdf doesn't exist
            Exception: If binary parsing fails
        """
        if not self.shortcuts_path.exists():
            raise FileNotFoundError(f"shortcuts.vdf not found at {self.shortcuts_path}")
        
        try:
            with open(self.shortcuts_path, 'rb') as f:
                data = vdf.binary_load(f)
            return data
        except Exception as e:
            raise Exception(f"Failed to parse shortcuts.vdf: {e}")
    
    def write_localconfig(self, data: Dict[str, Any]) -> None:
        """
        Write data to localconfig.vdf file.
        
        Args:
            data: VDF data to write
            
        Raises:
            Exception: If writing fails
        """
        try:
            with open(self.localconfig_path, 'w', encoding='utf-8') as f:
                vdf.dump(data, f, pretty=True)
        except Exception as e:
            raise Exception(f"Failed to write localconfig.vdf: {e}")
    
    def get_apps_section(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract the apps section from parsed localconfig.vdf data.
        
        Args:
            data: Parsed VDF data
            
        Returns:
            Apps section dictionary
        """
        return data.get("UserLocalConfigStore", {}).get("Software", {}).get("Valve", {}).get("Steam", {}).get("apps", {})
    
    def get_shortcuts_section(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract the shortcuts section from parsed shortcuts.vdf data.
        
        Args:
            data: Parsed VDF data
            
        Returns:
            Shortcuts section dictionary
        """
        return data.get("shortcuts", {})
