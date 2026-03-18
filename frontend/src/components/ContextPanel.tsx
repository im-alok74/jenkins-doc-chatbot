import React from 'react';
import { ChatContext } from '../types';

interface ContextPanelProps {
  context: ChatContext;
  setContext: (ctx: ChatContext) => void;
  visible: boolean;
}

const buildStatusOptions = ['Success', 'Failed', 'Running'];

const ContextPanel: React.FC<ContextPanelProps> = ({ context, setContext, visible }) => {
  if (!visible) return null;

  return (
    <div className="bg-gray-800 p-4 rounded-lg mb-4">
      <h3 className="text-orange-500 text-lg mb-2">Jenkins Context</h3>
      <div className="mb-2">
        <label className="text-gray-300">Job Name:</label>
        <input
          type="text"
          className="w-full bg-gray-700 text-white px-2 py-1 rounded-lg mt-1"
          value={context.job_name || ''}
          onChange={e => setContext({ ...context, job_name: e.target.value })}
        />
      </div>
      <div className="mb-2">
        <label className="text-gray-300">Build ID:</label>
        <input
          type="text"
          className="w-full bg-gray-700 text-white px-2 py-1 rounded-lg mt-1"
          value={context.build_id || ''}
          onChange={e => setContext({ ...context, build_id: e.target.value })}
        />
      </div>
      <div className="mb-2">
        <label className="text-gray-300">Console Log:</label>
        <textarea
          className="w-full bg-gray-700 text-white px-2 py-1 rounded-lg mt-1"
          rows={3}
          value={context.console_log || ''}
          onChange={e => setContext({ ...context, console_log: e.target.value })}
        />
      </div>
      <div className="mb-2">
        <label className="text-gray-300">Build Status:</label>
        <select
          className="w-full bg-gray-700 text-white px-2 py-1 rounded-lg mt-1"
          value={context.build_status || ''}
          onChange={e => setContext({ ...context, build_status: e.target.value as any })}
        >
          <option value="">Select status</option>
          {buildStatusOptions.map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default ContextPanel;
