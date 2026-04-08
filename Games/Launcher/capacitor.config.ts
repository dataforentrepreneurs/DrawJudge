import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.sahai.partygameshub',
  appName: 'Party Games Hub',
  webDir: 'dist',
  server: {
    androidScheme: 'http'
  }
};

export default config;
