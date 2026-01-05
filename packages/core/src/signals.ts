/**
 * Browser signal collection utilities
 */

export interface FingerprintComponents {
  canvas: string;
  webgl: string;
  audio: string;
  fonts: string;
  hardware: string;
  screen: string;
  browser: string;
  timezone: string;
  plugins: string;
  touch: string;
  battery: string;
  network: string;
  media: string;
  colorDepth: string;
  doNotTrack: string;
}

/**
 * Get canvas fingerprint
 */
export function getCanvasFingerprint(): string {
  try {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    if (!ctx) return 'unsupported';

    canvas.width = 200;
    canvas.height = 50;

    ctx.textBaseline = 'top';
    ctx.font = '14px "Arial"';
    ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = '#f60';
    ctx.fillRect(125, 1, 62, 20);
    ctx.fillStyle = '#069';
    ctx.fillText('SixFinger 🖐️', 2, 15);
    ctx.fillStyle = 'rgba(102, 204, 0, 0.7)';
    ctx.fillText('SixFinger 🖐️', 4, 17);

    return canvas.toDataURL();
  } catch (e) {
    return 'error';
  }
}

/**
 * Get WebGL fingerprint
 */
export function getWebGLFingerprint(): string {
  try {
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl') as WebGLRenderingContext | null;
    
    if (!gl) return 'unsupported';

    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
    const vendor = debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : 'unknown';
    const renderer = debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : 'unknown';

    return `${vendor}~${renderer}`;
  } catch (e) {
    return 'error';
  }
}

/**
 * Get audio context fingerprint
 */
export function getAudioFingerprint(): string {
  try {
    const AudioContext = window.AudioContext || (window as any).webkitAudioContext;
    if (!AudioContext) return 'unsupported';

    const context = new AudioContext();
    const oscillator = context.createOscillator();
    const analyser = context.createAnalyser();
    const gainNode = context.createGain();
    const scriptProcessor = context.createScriptProcessor(4096, 1, 1);

    gainNode.gain.value = 0;
    oscillator.type = 'triangle';
    oscillator.connect(analyser);
    analyser.connect(scriptProcessor);
    scriptProcessor.connect(gainNode);
    gainNode.connect(context.destination);

    oscillator.start(0);
    
    const fingerprint = `${context.sampleRate}_${analyser.fftSize}`;
    
    oscillator.stop();
    context.close();

    return fingerprint;
  } catch (e) {
    return 'error';
  }
}

/**
 * Detect available fonts
 */
export function getFontFingerprint(): string {
  const baseFonts = ['monospace', 'sans-serif', 'serif'];
  const testFonts = [
    'Arial', 'Verdana', 'Times New Roman', 'Courier New', 'Georgia',
    'Comic Sans MS', 'Trebuchet MS', 'Arial Black', 'Impact'
  ];

  const testString = 'mmmmmmmmmmlli';
  const testSize = '72px';
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  
  if (!ctx) return 'unsupported';

  const baseFontWidths: { [key: string]: number } = {};
  
  baseFonts.forEach(baseFont => {
    ctx.font = `${testSize} ${baseFont}`;
    baseFontWidths[baseFont] = ctx.measureText(testString).width;
  });

  const detectedFonts: string[] = [];

  testFonts.forEach(font => {
    baseFonts.forEach(baseFont => {
      ctx.font = `${testSize} '${font}', ${baseFont}`;
      const width = ctx.measureText(testString).width;
      if (width !== baseFontWidths[baseFont]) {
        if (!detectedFonts.includes(font)) {
          detectedFonts.push(font);
        }
      }
    });
  });

  return detectedFonts.sort().join(',');
}

/**
 * Get hardware information
 */
export function getHardwareFingerprint(): string {
  const nav = navigator as any;
  const cores = nav.hardwareConcurrency || 'unknown';
  const memory = nav.deviceMemory || 'unknown';
  const gpu = getWebGLFingerprint();
  
  return `cores:${cores}_mem:${memory}_gpu:${gpu}`;
}

/**
 * Get screen information
 */
export function getScreenFingerprint(): string {
  const screen = window.screen;
  return `${screen.width}x${screen.height}_${screen.availWidth}x${screen.availHeight}_${screen.colorDepth}`;
}

/**
 * Get browser information
 */
export function getBrowserFingerprint(): string {
  const nav = navigator;
  return `${nav.userAgent}_${nav.language}_${nav.platform}`;
}

/**
 * Get timezone information
 */
export function getTimezoneFingerprint(): string {
  const offset = new Date().getTimezoneOffset();
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  return `${timezone}_${offset}`;
}

/**
 * Get plugins information
 */
export function getPluginsFingerprint(): string {
  try {
    const plugins = Array.from(navigator.plugins || [])
      .map(p => p.name)
      .sort()
      .join(',');
    return plugins || 'none';
  } catch (e) {
    return 'error';
  }
}

/**
 * Get touch support
 */
export function getTouchFingerprint(): string {
  const maxTouchPoints = navigator.maxTouchPoints || 0;
  const touchEvent = 'ontouchstart' in window;
  return `${maxTouchPoints}_${touchEvent}`;
}

/**
 * Get battery information
 */
export async function getBatteryFingerprint(): Promise<string> {
  try {
    const nav = navigator as any;
    if (!nav.getBattery) return 'unsupported';
    
    const battery = await nav.getBattery();
    return `${battery.charging}_${Math.round(battery.level * 100)}`;
  } catch (e) {
    return 'error';
  }
}

/**
 * Get network information
 */
export function getNetworkFingerprint(): string {
  try {
    const nav = navigator as any;
    const connection = nav.connection || nav.mozConnection || nav.webkitConnection;
    if (!connection) return 'unsupported';
    
    return `${connection.effectiveType}_${connection.downlink}_${connection.rtt}`;
  } catch (e) {
    return 'error';
  }
}

/**
 * Get media devices
 */
export async function getMediaFingerprint(): Promise<string> {
  try {
    if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
      return 'unsupported';
    }
    
    const devices = await navigator.mediaDevices.enumerateDevices();
    const kinds = devices.map(d => d.kind).sort().join(',');
    return kinds;
  } catch (e) {
    return 'error';
  }
}

/**
 * Get color depth
 */
export function getColorDepthFingerprint(): string {
  return `${screen.colorDepth}_${window.devicePixelRatio || 1}`;
}

/**
 * Get Do Not Track setting
 */
export function getDoNotTrackFingerprint(): string {
  const nav = navigator as any;
  const dnt = nav.doNotTrack || nav.msDoNotTrack || window.doNotTrack;
  return String(dnt || 'unknown');
}
