/// <reference types="vite/client" />

declare interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
  readonly VITE_APP_NAME: string;
  readonly VITE_APP_VERSION: string;
  readonly VITE_ENV: string;
  // more env variables...
}

declare global {
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
}
