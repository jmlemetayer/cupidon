export interface RadaarSettings {
  api_key: string;
}

export interface SonaarSettings {
  api_key: string;
}

export interface Settings {
  radaar: RadaarSettings;
  sonaar: SonaarSettings;
}
