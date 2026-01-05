# @sixfinger/core

Browser fingerprinting core library for SixFinger Shield.

## Installation

```bash
npm install @sixfinger/core
```

## Usage

```typescript
import { getFingerprint } from '@sixfinger/core';

async function identify() {
  const result = await getFingerprint();
  
  console.log('Hash:', result.hash); // 32-character unique hash
  console.log('Components:', result.components);
}

identify();
```

## API

### `getFingerprint(): Promise<FingerprintResult>`

Collects 15+ browser signals and generates a unique 32-character hash.

**Returns:**
```typescript
{
  hash: string; // 32-char SHA-256 based hash
  components: {
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
}
```

## Browser Signals

| Signal | Description |
|--------|-------------|
| canvas | Canvas fingerprinting data |
| webgl | WebGL renderer and vendor info |
| audio | Audio context fingerprint |
| fonts | Available system fonts |
| hardware | CPU cores, memory, GPU |
| screen | Screen resolution & color depth |
| browser | User agent & platform |
| timezone | Timezone & offset |
| plugins | Browser plugins |
| touch | Touch support capabilities |
| battery | Battery status |
| network | Network information |
| media | Media devices enumeration |
| colorDepth | Color depth & pixel ratio |
| doNotTrack | Do Not Track setting |

## License

MIT
