export interface RadarrSettings {
  api_key: string;
}

export interface SonarrSettings {
  api_key: string;
}

export interface Settings {
  radarr: RadarrSettings;
  sonarr: SonarrSettings;
}
