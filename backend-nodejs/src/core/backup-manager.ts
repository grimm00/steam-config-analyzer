/**
 * Backup manager for Steam configuration files.
 * 
 * This module handles creating, managing, and restoring backups of Steam configuration files.
 */

import { copyFile, mkdir, readdir, stat, unlink } from 'fs/promises';
import { existsSync } from 'fs';
import { join, basename } from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';
import type { BackupInfo, BackupError } from '../types/index.js';

const execAsync = promisify(exec);

export class BackupManager {
  private readonly localconfigPath: string;
  private readonly backupDir: string;

  /**
   * Initialize the backup manager.
   * 
   * @param localconfigPath - Path to localconfig.vdf file
   * @param backupDir - Directory to store backups
   */
  constructor(localconfigPath: string, backupDir: string) {
    this.localconfigPath = localconfigPath;
    this.backupDir = backupDir;
  }

  /**
   * Ensure backup directory exists.
   * 
   * @throws {BackupError} If directory creation fails
   */
  private async ensureBackupDir(): Promise<void> {
    try {
      await mkdir(this.backupDir, { recursive: true });
    } catch (error) {
      throw new BackupError(`Failed to create backup directory: ${error}`, this.backupDir);
    }
  }

  /**
   * Check if Steam is currently running.
   * 
   * @returns True if Steam is running
   */
  async isSteamRunning(): Promise<boolean> {
    try {
      const { stdout } = await execAsync('pgrep -f steam');
      return stdout.trim().length > 0;
    } catch (error) {
      // pgrep returns non-zero exit code when no processes found
      return false;
    }
  }

  /**
   * Create a timestamped backup of localconfig.vdf.
   * 
   * @returns Path to the created backup file
   * @throws {BackupError} If localconfig.vdf doesn't exist or backup fails
   */
  async createBackup(): Promise<string> {
    if (!existsSync(this.localconfigPath)) {
      throw new BackupError(`localconfig.vdf not found at ${this.localconfigPath}`, this.localconfigPath);
    }

    await this.ensureBackupDir();

    try {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
      const backupPath = join(this.backupDir, `localconfig_backup_${timestamp}.vdf`);
      
      await copyFile(this.localconfigPath, backupPath);
      console.log(`Backup created: ${backupPath}`);
      return backupPath;
    } catch (error) {
      throw new BackupError(`Failed to create backup: ${error}`, this.localconfigPath);
    }
  }

  /**
   * Restore localconfig.vdf from a backup file.
   * 
   * @param backupPath - Path to the backup file to restore from
   * @throws {BackupError} If Steam is running, backup doesn't exist, or restore fails
   */
  async restoreBackup(backupPath: string): Promise<void> {
    if (await this.isSteamRunning()) {
      throw new BackupError('Steam is currently running. Please close Steam before restoring configuration.', backupPath);
    }

    if (!existsSync(backupPath)) {
      throw new BackupError(`Backup file not found: ${backupPath}`, backupPath);
    }

    try {
      await copyFile(backupPath, this.localconfigPath);
      console.log(`Restored localconfig.vdf from: ${backupPath}`);
    } catch (error) {
      throw new BackupError(`Failed to restore backup: ${error}`, backupPath);
    }
  }

  /**
   * List all available backup files.
   * 
   * @returns List of backup file paths, sorted by creation time (newest first)
   * @throws {BackupError} If directory reading fails
   */
  async listBackups(): Promise<string[]> {
    try {
      await this.ensureBackupDir();
      const files = await readdir(this.backupDir);
      
      const backupFiles = files
        .filter(file => file.startsWith('localconfig_backup_') && file.endsWith('.vdf'))
        .map(file => join(this.backupDir, file));

      // Sort by modification time (newest first)
      const filesWithStats = await Promise.all(
        backupFiles.map(async (file) => {
          const stats = await stat(file);
          return { file, mtime: stats.mtime };
        })
      );

      return filesWithStats
        .sort((a, b) => b.mtime.getTime() - a.mtime.getTime())
        .map(item => item.file);
    } catch (error) {
      throw new BackupError(`Failed to list backups: ${error}`, this.backupDir);
    }
  }

  /**
   * Clean up old backup files, keeping only the most recent ones.
   * 
   * @param keepCount - Number of recent backups to keep (default: 10)
   * @throws {BackupError} If cleanup fails
   */
  async cleanupOldBackups(keepCount: number = 10): Promise<void> {
    try {
      const backupFiles = await this.listBackups();
      
      if (backupFiles.length > keepCount) {
        const filesToDelete = backupFiles.slice(keepCount);
        
        for (const backupFile of filesToDelete) {
          await unlink(backupFile);
          console.log(`Deleted old backup: ${backupFile}`);
        }
      }
    } catch (error) {
      throw new BackupError(`Failed to cleanup old backups: ${error}`, this.backupDir);
    }
  }

  /**
   * Get information about a backup file.
   * 
   * @param backupPath - Path to the backup file
   * @returns Backup information object
   * @throws {BackupError} If file doesn't exist or stat fails
   */
  async getBackupInfo(backupPath: string): Promise<BackupInfo> {
    try {
      const stats = await stat(backupPath);
      return {
        path: backupPath,
        size: stats.size,
        created: stats.birthtime,
        modified: stats.mtime
      };
    } catch (error) {
      throw new BackupError(`Failed to get backup info: ${error}`, backupPath);
    }
  }

  /**
   * Validate that a backup file is valid and readable.
   * 
   * @param backupPath - Path to the backup file
   * @returns True if backup is valid
   */
  async validateBackup(backupPath: string): Promise<boolean> {
    try {
      if (!existsSync(backupPath)) {
        return false;
      }

      const stats = await stat(backupPath);
      if (stats.size === 0) {
        return false;
      }

      // TODO: Add VDF format validation when VDF parser is available
      // For now, just check that file exists and has content
      return true;
    } catch (error) {
      return false;
    }
  }

  /**
   * Get the backup directory path.
   * 
   * @returns Path to backup directory
   */
  getBackupDir(): string {
    return this.backupDir;
  }

  /**
   * Get the localconfig.vdf path.
   * 
   * @returns Path to localconfig.vdf
   */
  getLocalconfigPath(): string {
    return this.localconfigPath;
  }

  /**
   * Check if backup directory exists.
   * 
   * @returns True if backup directory exists
   */
  hasBackupDir(): boolean {
    return existsSync(this.backupDir);
  }

  /**
   * Get the number of backup files.
   * 
   * @returns Number of backup files
   */
  async getBackupCount(): Promise<number> {
    try {
      const backups = await this.listBackups();
      return backups.length;
    } catch (error) {
      return 0;
    }
  }

  /**
   * Get the total size of all backup files.
   * 
   * @returns Total size in bytes
   */
  async getTotalBackupSize(): Promise<number> {
    try {
      const backups = await this.listBackups();
      let totalSize = 0;

      for (const backup of backups) {
        const stats = await stat(backup);
        totalSize += stats.size;
      }

      return totalSize;
    } catch (error) {
      return 0;
    }
  }
}
