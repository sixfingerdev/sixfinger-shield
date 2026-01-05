import { getFingerprint } from '../index';

describe('getFingerprint', () => {
  beforeEach(() => {
    // Mock DOM APIs
    global.document = {
      createElement: jest.fn(() => ({
        getContext: jest.fn(() => ({
          textBaseline: '',
          font: '',
          fillStyle: '',
          fillRect: jest.fn(),
          fillText: jest.fn(),
          measureText: jest.fn(() => ({ width: 100 })),
          toDataURL: jest.fn(() => 'mock-canvas-data')
        })),
        toDataURL: jest.fn(() => 'mock-canvas-data'),
        width: 0,
        height: 0
      }))
    } as any;

    global.window = {
      AudioContext: undefined,
      screen: {
        width: 1920,
        height: 1080,
        availWidth: 1920,
        availHeight: 1080,
        colorDepth: 24
      },
      devicePixelRatio: 2,
      doNotTrack: '1'
    } as any;

    global.navigator = {
      userAgent: 'Mozilla/5.0',
      language: 'en-US',
      platform: 'Win32',
      hardwareConcurrency: 8,
      maxTouchPoints: 0,
      plugins: [],
      mediaDevices: undefined
    } as any;

    global.Intl = {
      DateTimeFormat: jest.fn(() => ({
        resolvedOptions: () => ({ timeZone: 'America/New_York' })
      }))
    } as any;

    global.crypto = {
      subtle: {
        digest: jest.fn(async () => {
          const arr = new Uint8Array(32);
          for (let i = 0; i < 32; i++) arr[i] = i;
          return arr.buffer;
        })
      }
    } as any;
  });

  it('should generate a fingerprint with hash and components', async () => {
    const result = await getFingerprint();

    expect(result).toHaveProperty('hash');
    expect(result).toHaveProperty('components');
    expect(typeof result.hash).toBe('string');
    expect(result.hash.length).toBe(32);
  });

  it('should generate consistent hash for same components', async () => {
    const result1 = await getFingerprint();
    const result2 = await getFingerprint();

    expect(result1.hash).toBe(result2.hash);
  });

  it('should collect all 15+ components', async () => {
    const result = await getFingerprint();

    expect(result.components).toHaveProperty('canvas');
    expect(result.components).toHaveProperty('webgl');
    expect(result.components).toHaveProperty('audio');
    expect(result.components).toHaveProperty('fonts');
    expect(result.components).toHaveProperty('hardware');
    expect(result.components).toHaveProperty('screen');
    expect(result.components).toHaveProperty('browser');
    expect(result.components).toHaveProperty('timezone');
    expect(result.components).toHaveProperty('plugins');
    expect(result.components).toHaveProperty('touch');
    expect(result.components).toHaveProperty('battery');
    expect(result.components).toHaveProperty('network');
    expect(result.components).toHaveProperty('media');
    expect(result.components).toHaveProperty('colorDepth');
    expect(result.components).toHaveProperty('doNotTrack');

    // Verify we have 15 components
    expect(Object.keys(result.components).length).toBe(15);
  });

  it('should handle missing APIs gracefully', async () => {
    // Remove some APIs
    (global.window as any).AudioContext = undefined;
    (global.navigator as any).mediaDevices = undefined;

    const result = await getFingerprint();

    expect(result.hash).toBeTruthy();
    expect(result.components.audio).toBe('unsupported');
    expect(result.components.media).toBe('unsupported');
  });
});
