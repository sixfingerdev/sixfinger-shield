interface FingerprintDisplayProps {
  fingerprint: {
    hash: string;
    components: Record<string, string>;
  };
  riskScore: {
    risk_score: number;
    is_bot: boolean;
    visit_count: number;
  } | null;
}

export default function FingerprintDisplay({ fingerprint, riskScore }: FingerprintDisplayProps) {
  const getRiskColor = (score: number) => {
    if (score < 30) return 'text-green-600 dark:text-green-400';
    if (score < 60) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getRiskLabel = (score: number) => {
    if (score < 30) return 'Low Risk';
    if (score < 60) return 'Medium Risk';
    return 'High Risk (Bot Likely)';
  };

  return (
    <div className="space-y-6">
      {/* Hash Display */}
      <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6 bg-gray-50 dark:bg-gray-900">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
          Fingerprint Hash
        </h3>
        <div className="font-mono text-2xl text-blue-600 dark:text-blue-400 break-all">
          {fingerprint.hash}
        </div>
      </div>

      {/* Risk Score */}
      {riskScore && (
        <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6 bg-gray-50 dark:bg-gray-900">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
            Risk Assessment
          </h3>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Score</div>
              <div className={`text-3xl font-bold ${getRiskColor(riskScore.risk_score)}`}>
                {riskScore.risk_score.toFixed(1)}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Status</div>
              <div className={`text-xl font-semibold ${getRiskColor(riskScore.risk_score)}`}>
                {getRiskLabel(riskScore.risk_score)}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Visits</div>
              <div className="text-3xl font-bold text-gray-900 dark:text-white">
                {riskScore.visit_count}
              </div>
            </div>
          </div>
          <div className="mt-4">
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
              <div
                className={`h-3 rounded-full transition-all duration-300 ${
                  riskScore.risk_score < 30
                    ? 'bg-green-600'
                    : riskScore.risk_score < 60
                    ? 'bg-yellow-600'
                    : 'bg-red-600'
                }`}
                style={{ width: `${Math.min(riskScore.risk_score, 100)}%` }}
              />
            </div>
          </div>
        </div>
      )}

      {/* Components */}
      <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6 bg-gray-50 dark:bg-gray-900">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Browser Signals ({Object.keys(fingerprint.components).length})
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {Object.entries(fingerprint.components).map(([key, value]) => (
            <div
              key={key}
              className="border border-gray-200 dark:border-gray-700 rounded p-3 bg-white dark:bg-gray-800"
            >
              <div className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase mb-1">
                {key}
              </div>
              <div className="text-sm text-gray-900 dark:text-white font-mono break-all line-clamp-2">
                {typeof value === 'string' && value.length > 100
                  ? value.substring(0, 100) + '...'
                  : value}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
