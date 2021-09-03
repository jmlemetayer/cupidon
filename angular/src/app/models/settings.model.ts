export interface RadarrSettings {
  url: string;
  api_key: string;
}

export interface SonarrSettings {
  url: string;
  api_key: string;
}

export interface Settings {
  radarr: RadarrSettings;
  sonarr: SonarrSettings;
}
