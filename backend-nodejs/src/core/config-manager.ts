/**
 * Configuration manager for Steam VDF files.
 * 
 * This module handles the main configuration management operations including extraction,
 * updating, and validation of Steam game configurations.
 */

import { writeFile, readFile, mkdir } from 'fs/promises';
import { existsSync } from 'fs';
import { join, dirname } from 'path';
import { homedir } from 'os';
import { VDFParser } from './vdf-parser.js';
import { GameNameResolver } from './game-resolver.js';
import { BackupManager } from './backup-manager.js';
import type { 
  SteamConfig, 
  GameConfig, 
  ShortcutsData, 
  ExtractionOptions, 
  UpdateOptions,
  ValidationError,
  SteamConfigError
} from '../types/index.js';

export class VDFConfigManager {
  private readonly steamUserId: string;
  private readonly steamConfigPath: string;
  private readonly localconfigPath: string;
  private readonly backupDir: string;
  private readonly outputFile: string;
  
  // Initialize components
  private readonly parser: VDFParser;
  private readonly nameResolver: GameNameResolver;
  private readonly backupManager: BackupManager;

  /**
   * Initialize the VDF Config Manager.
   * 
   * @param steamUserId - Steam user ID (default: "107256425")
   */
  constructor(steamUserId: string = '107256425') {
    this.steamUserId = steamUserId;
    this.steamConfigPath = join(homedir(), '.local', 'share', 'Steam', 'userdata', steamUserId, 'config');
    this.localconfigPath = join(this.steamConfigPath, 'localconfig.vdf');
    this.backupDir = join('instance', 'data', 'backups');
    this.outputFile = join('instance', 'data', 'all_games_config.json');
    
    // Initialize components
    this.parser = new VDFParser(this.steamConfigPath);
    this.nameResolver = new GameNameResolver(steamUserId);
    this.backupManager = new BackupManager(this.localconfigPath, this.backupDir);
  }

  /**
   * Extract all game configurations from localconfig.vdf.
   * 
   * @param options - Extraction options
   * @returns Dictionary containing all game data with essential fields
   */
  async extractAllGames(options: ExtractionOptions = {}): Promise<SteamConfig> {
    const {
      includeSystemApps = false,
      mode = 'sparse',
      includeManaged = false
    } = options;

    const data = await this.parser.parseLocalconfig();
    
    // Navigate to the apps section
    const appsSection = this.parser.getAppsSection(data);
    
    const allGames: SteamConfig = {};
    
    console.log(`Found ${Object.keys(appsSection).length} apps in localconfig.vdf`);
    console.log(`Extraction mode: ${mode} (managed fields: ${includeManaged ? 'included' : 'excluded'})`);
    
    // Define field categories
    const essentialFields = new Set(['LastPlayed', 'Playtime', 'LaunchOptions']);
    const optionalUserFields = new Set([
      'ResolutionOverride', 
      'ResolutionOverrideInternalDisplay', 
      'Playtime2wks', 
      'PlaytimeDisconnected'
    ]);
    const managedFields = new Set(['cloud', 'autocloud', 'BadgeData']);
    
    // Process all apps
    for (const [appId, appData] of Object.entries(appsSection)) {
      if (typeof appData !== 'object' || appData === null) {
        continue;
      }
      
      // Get game name using the resolver
      const appName = await this.nameResolver.getGameName(appId);
      
      // Skip system apps if not requested
      if (!includeSystemApps && this.nameResolver.isSystemApp(appId, appName)) {
        continue;
      }
      
      // Start with essential fields that are always added by the tool
      const gameData: GameConfig = {
        appid: appId,
        AppName: appName,
      };
      
      // Extract fields based on mode
      if (mode === 'sparse') {
        // Sparse mode: only include fields that actually exist
        for (const [fieldName, fieldValue] of Object.entries(appData)) {
          // Skip EULA fields unless includeManaged is true
          if (fieldName.endsWith('_eula_0') || fieldName.endsWith('_eula_1')) {
            if (includeManaged) {
              (gameData as any)[fieldName] = fieldValue;
            }
            continue;
          }
          
          // Skip managed fields unless includeManaged is true
          if (managedFields.has(fieldName)) {
            if (includeManaged) {
              (gameData as any)[fieldName] = fieldValue;
            }
            continue;
          }
          
          // Include all other fields (essential + optional user fields)
          (gameData as any)[fieldName] = fieldValue;
        }
      } else {
        // Standard mode: include all fields with defaults for missing ones
        for (const field of [...essentialFields, ...optionalUserFields]) {
          (gameData as any)[field] = (appData as any)[field] ?? '';
        }
        
        // Add managed fields if requested
        if (includeManaged) {
          for (const field of managedFields) {
            if (field in appData) {
              (gameData as any)[field] = (appData as any)[field];
            }
          }
        }
        
        // Add EULA fields if requested
        if (includeManaged) {
          for (const [fieldName, fieldValue] of Object.entries(appData)) {
            if (fieldName.endsWith('_eula_0') || fieldName.endsWith('_eula_1')) {
              (gameData as any)[fieldName] = fieldValue;
            }
          }
        }
      }
      
      // Try to get additional info from shortcuts.vdf for non-Steam games
      if ((appData as any).LaunchOptions) {
        try {
          const shortcutsData = await this.parser.parseShortcuts();
          const shortcutsSection = this.parser.getShortcutsSection(shortcutsData);
          
          // Find matching shortcut by launch options
          for (const [shortcutId, shortcutInfo] of Object.entries(shortcutsSection)) {
            const shortcutLaunchOptions = (shortcutInfo as any)?.LaunchOptions?.replace('%command% ', '') ?? '';
            const appLaunchOptions = (appData as any).LaunchOptions?.replace('%command% ', '') ?? '';
            
            if (shortcutLaunchOptions === appLaunchOptions) {
              // Add shortcut fields based on mode
              const shortcutFields = ['Exe', 'StartDir', 'IsHidden', 'AllowDesktopConfig', 'AllowOverlay'];
              for (const field of shortcutFields) {
                if (mode === 'sparse') {
                  // Only add if it exists and has a value
                  if (field in shortcutInfo && (shortcutInfo as any)[field]) {
                    (gameData as any)[field] = (shortcutInfo as any)[field];
                  }
                } else {
                  // Standard mode: add with default
                  const defaultValue = ['Exe', 'StartDir'].includes(field) ? '' : 0;
                  (gameData as any)[field] = (shortcutInfo as any)[field] ?? defaultValue;
                }
              }
              break;
            }
          }
        } catch (error) {
          console.warn(`Warning: Could not read shortcuts.vdf: ${error}`);
        }
      }
      
      allGames[appId] = gameData;
    }
    
    console.log(`Extracted ${Object.keys(allGames).length} games (system apps ${includeSystemApps ? 'included' : 'excluded'})`);
    return allGames;
  }

  /**
   * Extract shortcut configurations from localconfig.vdf (legacy method for compatibility).
   * 
   * @returns Dictionary containing shortcut data with essential fields only
   */
  async extractShortcuts(): Promise<SteamConfig> {
    // Use the new method but filter to only games with launch options
    const allGames = await this.extractAllGames({ 
      includeSystemApps: false, 
      mode: 'standard' 
    });
    const shortcuts: SteamConfig = {};
    
    for (const [appId, gameData] of Object.entries(allGames)) {
      if (gameData.LaunchOptions) {
        shortcuts[appId] = gameData;
      }
    }
    
    return shortcuts;
  }

  /**
   * Save shortcuts data to JSON file.
   * 
   * @param shortcuts - Shortcuts data to save
   * @returns Promise that resolves when file is saved
   */
  async saveShortcutsJson(shortcuts: SteamConfig): Promise<void> {
    try {
      await mkdir(dirname(this.outputFile), { recursive: true });
      await writeFile(this.outputFile, JSON.stringify(shortcuts, null, 2), 'utf-8');
      console.log(`Shortcuts saved to: ${this.outputFile}`);
    } catch (error) {
      throw new SteamConfigError(`Failed to save shortcuts JSON: ${error}`, this.outputFile);
    }
  }

  /**
   * Load shortcuts data from JSON file.
   * 
   * @returns Promise that resolves with loaded shortcuts data
   * @throws {SteamConfigError} If file doesn't exist or loading fails
   */
  async loadShortcutsJson(): Promise<SteamConfig> {
    if (!existsSync(this.outputFile)) {
      throw new SteamConfigError(`Shortcuts JSON not found at ${this.outputFile}`, this.outputFile);
    }
    
    try {
      const content = await readFile(this.outputFile, 'utf-8');
      return JSON.parse(content) as SteamConfig;
    } catch (error) {
      throw new SteamConfigError(`Failed to load shortcuts JSON: ${error}`, this.outputFile);
    }
  }

  /**
   * Update localconfig.vdf with modified shortcut data.
   * 
   * @param options - Update options
   * @returns Promise that resolves when update is complete
   * @throws {SteamConfigError} If Steam is running or update fails
   */
  async updateLocalconfig(options: UpdateOptions): Promise<void> {
    const { shortcuts, createBackup = true, dryRun = false } = options;

    if (await this.backupManager.isSteamRunning()) {
      throw new SteamConfigError('Steam is currently running. Please close Steam before updating configuration.', this.localconfigPath);
    }
    
    // Create backup before making changes
    let backupPath: string | undefined;
    if (createBackup) {
      backupPath = await this.backupManager.createBackup();
    }
    
    try {
      // Parse current localconfig.vdf
      const data = await this.parser.parseLocalconfig();
      
      // Navigate to the apps section
      const appsSection = this.parser.getAppsSection(data);
      
      // Define field categories for validation
      const safeUserFields = new Set([
        'LaunchOptions', 
        'ResolutionOverride', 
        'ResolutionOverrideInternalDisplay',
        'Playtime2wks', 
        'PlaytimeDisconnected'
      ]);
      const managedFields = new Set(['cloud', 'autocloud', 'BadgeData']);
      
      // Update each shortcut
      for (const [appId, shortcutData] of Object.entries(shortcuts)) {
        if (!(appId in appsSection)) {
          console.warn(`Warning: App ID ${appId} not found in localconfig.vdf`);
          continue;
        }
        
        // Validate and update fields
        for (const [fieldName, fieldValue] of Object.entries(shortcutData)) {
          // Skip tool-added fields
          if (['appid', 'AppName'].includes(fieldName)) {
            continue;
          }
          
          // Check for dangerous fields
          if (fieldName.endsWith('_eula_0') || fieldName.endsWith('_eula_1')) {
            console.warn(`Warning: EULA field ${fieldName} detected - skipping for safety`);
            continue;
          }
          
          // Check for managed fields
          if (managedFields.has(fieldName)) {
            console.warn(`Warning: Steam-managed field ${fieldName} detected - skipping for safety`);
            continue;
          }
          
          // Handle field deletion (null values)
          if (fieldValue === null) {
            if (fieldName in (appsSection as any)[appId]) {
              delete (appsSection as any)[appId][fieldName];
              console.log(`Deleted field ${fieldName} from app ${appId}`);
            }
            continue;
          }
          
          // Handle empty strings (don't write, delete if exists)
          if (fieldValue === '') {
            if (fieldName in (appsSection as any)[appId]) {
              delete (appsSection as any)[appId][fieldName];
              console.log(`Removed empty field ${fieldName} from app ${appId}`);
            }
            continue;
          }
          
          // Update field value
          if (safeUserFields.has(fieldName)) {
            (appsSection as any)[appId][fieldName] = fieldValue;
            console.log(`Updated ${fieldName} for app ${appId}`);
          } else {
            console.warn(`Warning: Unknown field ${fieldName} - updating anyway`);
            (appsSection as any)[appId][fieldName] = fieldValue;
          }
        }
      }
      
      if (!dryRun) {
        // Write back to file
        await this.parser.writeLocalconfig(data);
        console.log('Successfully updated localconfig.vdf');
        if (backupPath) {
          console.log(`Backup available at: ${backupPath}`);
        }
      } else {
        console.log('Dry run completed - no changes made to localconfig.vdf');
      }
      
    } catch (error) {
      console.error(`Error updating localconfig.vdf: ${error}`);
      if (backupPath) {
        console.log(`Restore from backup: ${backupPath}`);
      }
      throw new SteamConfigError(`Failed to update localconfig.vdf: ${error}`, this.localconfigPath);
    }
  }

  /**
   * Validate game configuration data.
   * 
   * @param config - Game configuration to validate
   * @returns Array of validation errors
   */
  validateFields(config: GameConfig): ValidationError[] {
    const errors: ValidationError[] = [];
    
    // Check required fields
    if (!config.appid) {
      errors.push(new ValidationError('appid is required', 'appid'));
    }
    
    if (!config.AppName) {
      errors.push(new ValidationError('AppName is required', 'AppName'));
    }
    
    // Validate field types and values
    if (config.Playtime !== undefined && (typeof config.Playtime !== 'number' || config.Playtime < 0)) {
      errors.push(new ValidationError('Playtime must be a non-negative number', 'Playtime'));
    }
    
    if (config.Playtime2wks !== undefined && (typeof config.Playtime2wks !== 'number' || config.Playtime2wks < 0)) {
      errors.push(new ValidationError('Playtime2wks must be a non-negative number', 'Playtime2wks'));
    }
    
    if (config.PlaytimeDisconnected !== undefined && (typeof config.PlaytimeDisconnected !== 'number' || config.PlaytimeDisconnected < 0)) {
      errors.push(new ValidationError('PlaytimeDisconnected must be a non-negative number', 'PlaytimeDisconnected'));
    }
    
    return errors;
  }

  /**
   * Get the Steam user ID.
   * 
   * @returns Steam user ID
   */
  getSteamUserId(): string {
    return this.steamUserId;
  }

  /**
   * Get the Steam config path.
   * 
   * @returns Steam config directory path
   */
  getSteamConfigPath(): string {
    return this.steamConfigPath;
  }

  /**
   * Get the output file path.
   * 
   * @returns Output file path
   */
  getOutputFilePath(): string {
    return this.outputFile;
  }

  /**
   * Get the backup manager instance.
   * 
   * @returns Backup manager instance
   */
  getBackupManager(): BackupManager {
    return this.backupManager;
  }

  /**
   * Get the game name resolver instance.
   * 
   * @returns Game name resolver instance
   */
  getNameResolver(): GameNameResolver {
    return this.nameResolver;
  }

  /**
   * Get the VDF parser instance.
   * 
   * @returns VDF parser instance
   */
  getParser(): VDFParser {
    return this.parser;
  }
}
