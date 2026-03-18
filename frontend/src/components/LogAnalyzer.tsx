import React, { useState } from 'react';
import { LogAnalysisResponse } from '../types';
import { analyzeLog } from '../services/api';

const LogAnalyzer: React.FC = () => {
  const [log, setLog] = useState('');
  const [result, setResult] = useState<LogAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await analyzeLog({ console_log: log });
      setResult(res);
    } catch (e) {
      setError('Failed to analyze log. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-900 p-4 rounded-lg h-full">
      <h3 className="text-orange-500 text-lg mb-2">Log Analyzer</h3>
      <textarea
        className="w-full bg-gray-700 text-white px-2 py-1 rounded-lg mb-2"
        rows={6}
        placeholder="Paste Jenkins console log here..."
        value={log}
        onChange={e => setLog(e.target.value)}
        disabled={loading}
      />
      <button
        className="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 disabled:bg-gray-600"
        onClick={handleAnalyze}
        disabled={loading || !log.trim()}
      >
        Analyze
      </button>
      {loading && <div className="mt-2 text-gray-400">Analyzing...</div>}
      {error && <div className="mt-2 text-red-500">{error}</div>}
      {result && (
        <div className="mt-4 bg-gray-800 p-3 rounded-lg">
          <div className="text-orange-400 font-semibold mb-1">Error Type: {result.error_type}</div>
          <div className="text-gray-300 mb-1">Root Cause: {result.root_cause}</div>
          <div className="text-gray-300 mb-1">Summary: {result.summary}</div>
          <div className="text-gray-300 mb-1">Relevant Stage: {result.relevant_stage}</div>
          <div className="text-gray-300 mb-1">Fix Suggestions:</div>
          <ul className="list-disc list-inside text-gray-200">
            {result.fix_suggestions.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default LogAnalyzer;
