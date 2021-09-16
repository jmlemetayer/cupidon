export interface RadarrSettings {
  url: string;
  api_key: string;
  data_dir: string;
}

export interface SonarrSettings {
  url: string;
  api_key: string;
  data_dir: string;
}

export interface SeedboxSettings {
  url: string;
  username: string;
  password: string;
}

export interface SynologyDestinationSettings {
  movies: string;
  tv_shows: string;
  files: string;
}

export interface SynologySettings {
  url: string;
  username: string;
  password: string;
  destination: SynologyDestinationSettings;
}

export interface Settings {
  radarr: RadarrSettings;
  sonarr: SonarrSettings;
  seedbox: SeedboxSettings;
  synology: SynologySettings;
}
