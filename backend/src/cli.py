#!/usr/bin/env python3
"""
CLI interface for Steam Config Analyzer.

This module provides the command-line interface for the Steam configuration management tool.
"""

import argparse
import sys
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from core.config_manager import VDFConfigManager


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
