/**
 * Hash generation utilities
 */

/**
 * Generate SHA-256 hash
 */
async function sha256(message: string): Promise<string> {
  if (typeof crypto !== 'undefined' && crypto.subtle) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
  }
  
  // Fallback for environments without crypto.subtle
  return simpleHash(message);
}

/**
 * Simple hash fallback
 */
function simpleHash(str: string): string {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  
  // Convert to hex and pad to 64 chars (32 bytes)
  const hex = Math.abs(hash).toString(16);
  return hex.padStart(64, '0').substring(0, 64);
}

/**
 * Generate 32-character fingerprint hash
 */
export async function generateHash(components: string): Promise<string> {
  const fullHash = await sha256(components);
  // Return first 32 characters for a 32-char hash
  return fullHash.substring(0, 32);
}
