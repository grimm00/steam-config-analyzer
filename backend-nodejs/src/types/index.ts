/**
 * Core type definitions for Steam Config Analyzer
 * 
 * These types are shared between backend, frontend, and plugins
 */

export interface GameConfig {
  appid: string;
  AppName: string;
  LastPlayed?: string;
  Playtime?: number;
  PlaytimeDisconnected?: number;
  LaunchOptions?: string;
  ResolutionOverride?: string;
  ResolutionOverrideInternalDisplay?: string;
  Playtime2wks?: number;
  cloud?: CloudConfig;
  autocloud?: AutoCloudConfig;
  BadgeData?: string;
  [key: string]: unknown; // For EULA fields and other dynamic fields
}

export interface CloudConfig {
  last_sync_state?: string;
  quota_bytes?: string;
  quota_files?: string;
  used_bytes?: string;
  used_files?: string;
}

export interface AutoCloudConfig {
  lastlaunch?: string;
  lastsync?: string;
}

export interface SteamConfig {
  [appid: string]: GameConfig;
}

export interface VDFData {
  UserLocalConfigStore?: {
    Software?: {
      Valve?: {
        Steam?: {
          apps?: SteamConfig;
        };
      };
    };
  };
}

export interface ShortcutsData {
  shortcuts?: {
    [index: string]: {
      appid: number;
      AppName: string;
      Exe: string;
      StartDir: string;
      LaunchOptions?: string;
      [key: string]: unknown;
    };
  };
}

export interface ExtractionOptions {
  includeSystemApps?: boolean;
  mode?: 'sparse' | 'standard';
  includeManaged?: boolean;
}

export interface BackupInfo {
  filename: string;
  timestamp: string;
  size: number;
  path: string;
}

export interface GameNameCache {
  [appid: string]: string;
}

export type ExtractionMode = 'sparse' | 'standard';

export type FieldCategory = 'essential' | 'optional' | 'managed' | 'eula' | 'system';

export interface FieldInfo {
  name: string;
  category: FieldCategory;
  description: string;
  safeToModify: boolean;
  frequency: number; // Percentage of games that have this field
}

// CLI Command Types
export interface ExtractAllOptions {
  output?: string;
  mode?: ExtractionMode;
  includeSystemApps?: boolean;
  includeManaged?: boolean;
}

export interface UpdateOptions {
  input: string;
  backup?: boolean;
  dryRun?: boolean;
}

export interface RestoreOptions {
  backup: string;
  confirm?: boolean;
}

// Error Types
export class SteamConfigError extends Error {
  constructor(message: string, public readonly code?: string) {
    super(message);
    this.name = 'SteamConfigError';
  }
}

export class VDFParseError extends SteamConfigError {
  constructor(message: string, public readonly filePath?: string) {
    super(message, 'VDF_PARSE_ERROR');
    this.name = 'VDFParseError';
  }
}

export class BackupError extends SteamConfigError {
  constructor(message: string, public readonly operation?: string) {
    super(message, 'BACKUP_ERROR');
    this.name = 'BackupError';
  }
}

export class ValidationError extends SteamConfigError {
  constructor(message: string, public readonly field?: string) {
    super(message, 'VALIDATION_ERROR');
    this.name = 'ValidationError';
  }
}

// Utility Types
export type SteamProcessStatus = 'running' | 'stopped' | 'unknown';

export interface SteamPaths {
  steamPath: string;
  userDataPath: string;
  configPath: string;
  steamappsPath: string;
  libraryCachePath: string;
}

export interface AppManifest {
  appid: string;
  name: string;
  installdir: string;
  state: number;
  [key: string]: unknown;
}
