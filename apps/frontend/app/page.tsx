'use client';

import { useState, useEffect } from 'react';
import FingerprintDisplay from '../components/FingerprintDisplay';

export default function Home() {
  const [fingerprint, setFingerprint] = useState<any>(null);
  const [riskScore, setRiskScore] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateFingerprint = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Dynamic import to avoid SSR issues
      const { getFingerprint } = await import('@sixfinger/core');
      const result = await getFingerprint();
      setFingerprint(result);

      // Submit to API
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/fingerprint`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(result),
      });

      if (response.ok) {
        const data = await response.json();
        setRiskScore(data);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate fingerprint');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 p-8">
      <div className="max-w-6xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
            🖐️ SixFinger Shield
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Open-source bot detection & device recognition
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
            Collects 15+ browser signals to generate a unique fingerprint
          </p>
        </header>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8 mb-8">
          <div className="text-center">
            <button
              onClick={generateFingerprint}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 px-8 rounded-lg transition-colors duration-200 text-lg"
            >
              {loading ? 'Generating...' : 'Generate Fingerprint'}
            </button>
            {error && (
              <p className="text-red-600 dark:text-red-400 mt-4">{error}</p>
            )}
          </div>

          {fingerprint && (
            <div className="mt-8">
              <FingerprintDisplay
                fingerprint={fingerprint}
                riskScore={riskScore}
              />
            </div>
          )}
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Features
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                📊 15+ Browser Signals
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Canvas, WebGL, Audio, Fonts, Hardware, and more
              </p>
            </div>
            <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                🔒 32-char Unique Hash
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                SHA-256 based fingerprint generation
              </p>
            </div>
            <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                🤖 Bot Detection
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Risk scoring API with rate limiting
              </p>
            </div>
            <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                ⚡ Client-side Only
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Single getFingerprint() function
              </p>
            </div>
          </div>
        </div>

        <footer className="text-center mt-8 text-gray-600 dark:text-gray-400">
          <p>MIT License • Production-ready with Docker & migrations</p>
        </footer>
      </div>
    </main>
  );
}
