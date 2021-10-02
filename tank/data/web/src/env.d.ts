interface ImportMetaEnv extends Readonly<Record<string, string>> {
    readonly VITE_BACKEND: string
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv
  }
  