import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'ai.d4e.play',
  appName: 'Party Games Hub',
  webDir: 'dist',
  server: {
    androidScheme: 'http'
  }
};

export default config;
