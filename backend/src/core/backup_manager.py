"""
Backup manager for Steam configuration files.

This module handles creating, managing, and restoring backups of Steam configuration files.
"""

import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List


class BackupManager:
    """Manages backups of Steam configuration files."""
    
    def __init__(self, localconfig_path: Path, backup_dir: Path):
        """
        Initialize the backup manager.
        
        Args:
            localconfig_path: Path to localconfig.vdf file
            backup_dir: Directory to store backups
        """
        self.localconfig_path = localconfig_path
        self.backup_dir = backup_dir
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def is_steam_running(self) -> bool:
        """Check if Steam is currently running."""
        try:
            result = subprocess.run(['pgrep', '-f', 'steam'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def create_backup(self) -> str:
        """
        Create a timestamped backup of localconfig.vdf.
        
        Returns:
            Path to the created backup file
            
        Raises:
            FileNotFoundError: If localconfig.vdf doesn't exist
        """
        if not self.localconfig_path.exists():
            raise FileNotFoundError(f"localconfig.vdf not found at {self.localconfig_path}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"localconfig_backup_{timestamp}.vdf"
        
        shutil.copy2(self.localconfig_path, backup_path)
        print(f"Backup created: {backup_path}")
        return str(backup_path)
    
    def restore_backup(self, backup_path: str) -> None:
        """
        Restore localconfig.vdf from a backup file.
        
        Args:
            backup_path: Path to the backup file to restore from
            
        Raises:
            RuntimeError: If Steam is running
            FileNotFoundError: If backup file doesn't exist
        """
        if self.is_steam_running():
            raise RuntimeError("Steam is currently running. Please close Steam before restoring configuration.")
        
        backup_file = Path(backup_path)
        if not backup_file.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        shutil.copy2(backup_file, self.localconfig_path)
        print(f"Restored localconfig.vdf from: {backup_path}")
    
    def list_backups(self) -> List[Path]:
        """
        List all available backup files.
        
        Returns:
            List of backup file paths, sorted by creation time (newest first)
        """
        backup_files = list(self.backup_dir.glob("localconfig_backup_*.vdf"))
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return backup_files
    
    def cleanup_old_backups(self, keep_count: int = 10) -> None:
        """
        Clean up old backup files, keeping only the most recent ones.
        
        Args:
            keep_count: Number of recent backups to keep
        """
        backup_files = self.list_backups()
        
        if len(backup_files) > keep_count:
            files_to_delete = backup_files[keep_count:]
            for backup_file in files_to_delete:
                backup_file.unlink()
                print(f"Deleted old backup: {backup_file}")
    
    def get_backup_info(self, backup_path: Path) -> dict:
        """
        Get information about a backup file.
        
        Args:
            backup_path: Path to the backup file
            
        Returns:
            Dictionary with backup information
        """
        stat = backup_path.stat()
        return {
            "path": str(backup_path),
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime),
            "modified": datetime.fromtimestamp(stat.st_mtime)
        }
