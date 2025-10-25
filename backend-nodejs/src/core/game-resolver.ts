/**
 * Game name resolver for Steam app IDs.
 * 
 * This module handles resolving Steam app IDs to human-readable game names using multiple fallback methods.
 */

import { readFile, writeFile, mkdir } from 'fs/promises';
import { existsSync } from 'fs';
import { join, dirname } from 'path';
import { homedir } from 'os';
import type { AppManifest, LibraryCache } from '../types/index.js';

export class GameNameResolver {
  private readonly steamUserId: string;
  private readonly steamPath: string;
  private readonly steamappsPath: string;
  private readonly libraryCachePath: string;
  private readonly shortcutsPath: string;
  private readonly cacheFile: string;
  private readonly cachedMappings: Map<string, string> = new Map();

  // Manual mappings for games not found in other sources
  private readonly manualMappings: Record<string, string> = {
    '3241660': 'R.E.P.O.',
    // Add more mappings as needed
  };

  // System apps to filter out (optional)
  private readonly systemApps: Set<string> = new Set([
    'steam linux runtime',
    'proton',
    'steamworks',
    'steam client'
  ]);

  /**
   * Initialize the Game Name Resolver.
   * 
   * @param steamUserId - Steam user ID (default: "107256425")
   */
  constructor(steamUserId: string = '107256425') {
    this.steamUserId = steamUserId;
    this.steamPath = join(homedir(), '.local', 'share', 'Steam');
    this.steamappsPath = join(this.steamPath, 'steamapps');
    this.libraryCachePath = join(this.steamPath, 'userdata', steamUserId, 'config', 'librarycache');
    this.shortcutsPath = join(this.steamPath, 'userdata', steamUserId, 'config', 'shortcuts.vdf');
    this.cacheFile = join('instance', 'data', 'app_name_cache.json');

    // Load cached mappings
    this.loadCache();
  }

  /**
   * Load cached app ID to name mappings.
   * 
   * @returns Promise that resolves when cache is loaded
   */
  private async loadCache(): Promise<void> {
    if (existsSync(this.cacheFile)) {
      try {
        const content = await readFile(this.cacheFile, 'utf-8');
        const data = JSON.parse(content) as Record<string, string>;
        
        // Convert to Map
        for (const [appId, name] of Object.entries(data)) {
          this.cachedMappings.set(appId, name);
        }
      } catch (error) {
        console.warn(`Warning: Could not load app name cache: ${error}`);
      }
    }
  }

  /**
   * Save app ID to name mappings to cache.
   * 
   * @returns Promise that resolves when cache is saved
   */
  private async saveCache(): Promise<void> {
    try {
      await mkdir(dirname(this.cacheFile), { recursive: true });
      
      // Convert Map to object
      const data: Record<string, string> = {};
      for (const [appId, name] of this.cachedMappings) {
        data[appId] = name;
      }
      
      await writeFile(this.cacheFile, JSON.stringify(data, null, 2), 'utf-8');
    } catch (error) {
      console.warn(`Warning: Could not save app name cache: ${error}`);
    }
  }

  /**
   * Get game name from app manifest file (primary method).
   * 
   * @param appId - Steam app ID
   * @returns Game name or null if not found
   */
  private async getNameFromAppManifest(appId: string): Promise<string | null> {
    const manifestPath = join(this.steamappsPath, `appmanifest_${appId}.acf`);
    
    if (!existsSync(manifestPath)) {
      return null;
    }

    try {
      const content = await readFile(manifestPath, 'utf-8');
      
      // Simple parsing for the name field
      for (const line of content.split('\n')) {
        if (line.includes('"name"') && line.includes('\t')) {
          // Extract name from line like: "name"		"Game Name"
          const parts = line.split('\t');
          if (parts.length >= 3) {
            const name = parts[parts.length - 1].trim().replace(/^"/, '').replace(/"$/, '');
            return name;
          }
        }
      }
    } catch (error) {
      console.warn(`Warning: Could not parse app manifest for ${appId}: ${error}`);
    }

    return null;
  }

  /**
   * Get game name from library cache JSON (fallback 1).
   * 
   * @param appId - Steam app ID
   * @returns Game name or null if not found
   */
  private async getNameFromLibraryCache(appId: string): Promise<string | null> {
    const cacheFilePath = join(this.libraryCachePath, `${appId}.json`);
    
    if (!existsSync(cacheFilePath)) {
      return null;
    }

    try {
      const content = await readFile(cacheFilePath, 'utf-8');
      const data = JSON.parse(content) as LibraryCache;
      
      // Library cache has complex structure, look for descriptions
      for (const item of data) {
        if (Array.isArray(item) && item.length >= 2) {
          if (item[0] === 'descriptions' && typeof item[1] === 'object' && item[1] !== null) {
            const descData = (item[1] as any).data;
            if (descData && typeof descData === 'object') {
              // Try to extract name from description or other fields
              // This is a simplified approach - library cache is complex
              // TODO: Implement proper library cache parsing when needed
            }
          }
        }
      }
    } catch (error) {
      console.warn(`Warning: Could not parse library cache for ${appId}: ${error}`);
    }

    return null;
  }

  /**
   * Get game name from shortcuts.vdf (fallback 2).
   * 
   * @param appId - Steam app ID
   * @returns Game name or null if not found
   */
  private async getNameFromShortcuts(appId: string): Promise<string | null> {
    if (!existsSync(this.shortcutsPath)) {
      return null;
    }

    try {
      // TODO: Implement shortcuts.vdf parsing when VDF parser is available
      // For now, return null as this requires VDF binary parsing
      console.warn('Shortcuts.vdf parsing not yet implemented - requires VDF parser');
      return null;
    } catch (error) {
      console.warn(`Warning: Could not parse shortcuts.vdf: ${error}`);
    }

    return null;
  }

  /**
   * Get game name for an app ID using multiple fallback methods.
   * 
   * @param appId - Steam app ID
   * @param forceRefresh - Force refresh from sources, bypass cache
   * @returns Game name or fallback name
   */
  async getGameName(appId: string, forceRefresh: boolean = false): Promise<string> {
    // Check cache first (unless force refresh)
    if (!forceRefresh && this.cachedMappings.has(appId)) {
      return this.cachedMappings.get(appId)!;
    }

    // Try app manifest (primary method)
    let name = await this.getNameFromAppManifest(appId);
    if (name) {
      this.cachedMappings.set(appId, name);
      await this.saveCache();
      return name;
    }

    // Try library cache (fallback 1)
    name = await this.getNameFromLibraryCache(appId);
    if (name) {
      this.cachedMappings.set(appId, name);
      await this.saveCache();
      return name;
    }

    // Try shortcuts.vdf (fallback 2)
    name = await this.getNameFromShortcuts(appId);
    if (name) {
      this.cachedMappings.set(appId, name);
      await this.saveCache();
      return name;
    }

    // Try manual mappings (fallback 3)
    if (appId in this.manualMappings) {
      name = this.manualMappings[appId];
      this.cachedMappings.set(appId, name);
      await this.saveCache();
      return name;
    }

    // Final fallback
    const fallbackName = `App ${appId}`;
    this.cachedMappings.set(appId, fallbackName);
    await this.saveCache();
    return fallbackName;
  }

  /**
   * Check if an app is a system app (Proton, Steam Runtime, etc.).
   * 
   * @param appId - Steam app ID
   * @param appName - App name to check
   * @returns True if it's a system app
   */
  isSystemApp(appId: string, appName: string): boolean {
    const nameLower = appName.toLowerCase();
    return Array.from(this.systemApps).some(systemName => nameLower.includes(systemName));
  }

  /**
   * Refresh the entire cache by re-scanning all sources.
   * 
   * @returns Promise that resolves when cache is refreshed
   */
  async refreshCache(): Promise<void> {
    console.log('Refreshing app name cache...');
    this.cachedMappings.clear();
    await this.saveCache();
    console.log(`Cache refreshed. Found ${this.cachedMappings.size} mappings.`);
  }

  /**
   * Get the number of cached mappings.
   * 
   * @returns Number of cached mappings
   */
  getCacheSize(): number {
    return this.cachedMappings.size;
  }

  /**
   * Check if an app ID is in the cache.
   * 
   * @param appId - Steam app ID
   * @returns True if app ID is cached
   */
  isCached(appId: string): boolean {
    return this.cachedMappings.has(appId);
  }

  /**
   * Get all cached app IDs.
   * 
   * @returns Array of cached app IDs
   */
  getCachedAppIds(): string[] {
    return Array.from(this.cachedMappings.keys());
  }

  /**
   * Add a manual mapping for an app ID.
   * 
   * @param appId - Steam app ID
   * @param name - Game name
   */
  addManualMapping(appId: string, name: string): void {
    this.manualMappings[appId] = name;
    this.cachedMappings.set(appId, name);
  }

  /**
   * Remove a manual mapping for an app ID.
   * 
   * @param appId - Steam app ID
   */
  removeManualMapping(appId: string): void {
    delete this.manualMappings[appId];
    this.cachedMappings.delete(appId);
  }

  /**
   * Get the cache file path.
   * 
   * @returns Path to cache file
   */
  getCacheFilePath(): string {
    return this.cacheFile;
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
   * Get the Steam path.
   * 
   * @returns Steam installation path
   */
  getSteamPath(): string {
    return this.steamPath;
  }
}
