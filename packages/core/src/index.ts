/**
 * @sixfinger/core - Browser fingerprinting library
 * Main entry point
 */

import {
  getCanvasFingerprint,
  getWebGLFingerprint,
  getAudioFingerprint,
  getFontFingerprint,
  getHardwareFingerprint,
  getScreenFingerprint,
  getBrowserFingerprint,
  getTimezoneFingerprint,
  getPluginsFingerprint,
  getTouchFingerprint,
  getBatteryFingerprint,
  getNetworkFingerprint,
  getMediaFingerprint,
  getColorDepthFingerprint,
  getDoNotTrackFingerprint,
  FingerprintComponents
} from './signals';
import { generateHash } from './hash';

export interface FingerprintResult {
  hash: string;
  components: FingerprintComponents;
}

/**
 * Main fingerprinting function
 * Collects 15+ browser signals and generates a unique 32-char hash
 */
export async function getFingerprint(): Promise<FingerprintResult> {
  // Collect all components
  const components: FingerprintComponents = {
    canvas: getCanvasFingerprint(),
    webgl: getWebGLFingerprint(),
    audio: getAudioFingerprint(),
    fonts: getFontFingerprint(),
    hardware: getHardwareFingerprint(),
    screen: getScreenFingerprint(),
    browser: getBrowserFingerprint(),
    timezone: getTimezoneFingerprint(),
    plugins: getPluginsFingerprint(),
    touch: getTouchFingerprint(),
    battery: await getBatteryFingerprint(),
    network: getNetworkFingerprint(),
    media: await getMediaFingerprint(),
    colorDepth: getColorDepthFingerprint(),
    doNotTrack: getDoNotTrackFingerprint()
  };

  // Combine all components into a single string
  const combinedString = Object.entries(components)
    .sort(([keyA], [keyB]) => keyA.localeCompare(keyB))
    .map(([key, value]) => `${key}:${value}`)
    .join('|');

  // Generate 32-character hash
  const hash = await generateHash(combinedString);

  return {
    hash,
    components
  };
}

// Export signal functions for advanced usage
export * from './signals';
export * from './hash';
