import React, { useState } from 'react';
import { DocSearchResult } from '../types';
import { searchDocs } from '../services/api';

const DocSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<DocSearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    setLoading(true);
    setError('');
    setResults([]);
    try {
      const res = await searchDocs(query);
      setResults(res.results);
    } catch (e) {
      setError('Failed to search docs. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-900 p-4 rounded-lg h-full">
      <h3 className="text-orange-500 text-lg mb-2">Documentation Search</h3>
      <div className="flex mb-2">
        <input
          type="text"
          className="flex-1 bg-gray-700 text-white px-2 py-1 rounded-lg"
          placeholder="Search Jenkins docs..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          disabled={loading}
        />
        <button
          className="ml-2 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 disabled:bg-gray-600"
          onClick={handleSearch}
          disabled={loading || !query.trim()}
        >
          Search
        </button>
      </div>
      {loading && <div className="mt-2 text-gray-400">Searching...</div>}
      {error && <div className="mt-2 text-red-500">{error}</div>}
      {results.length > 0 && (
        <div className="mt-4">
          {results.map((r, i) => (
            <div key={i} className="bg-gray-800 p-3 rounded-lg mb-2">
              <div className="text-orange-400 font-semibold">Source: {r.source}</div>
              <div className="text-gray-200 mb-1">{r.content}</div>
              <div className="text-gray-400 text-xs">Relevance Score: {r.relevance_score.toFixed(2)}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DocSearch;
