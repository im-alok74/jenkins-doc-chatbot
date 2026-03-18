import React from 'react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  contextPanelVisible: boolean;
  setContextPanelVisible: (v: boolean) => void;
  healthStatus: 'online' | 'offline';
}

const tabs = [
  { key: 'chat', label: 'Chat' },
  { key: 'log', label: 'Log Analyzer' },
  { key: 'docs', label: 'Doc Search' },
];

const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab, contextPanelVisible, setContextPanelVisible, healthStatus }) => {
  return (
    <div className="bg-gray-800 h-full w-48 flex flex-col p-4">
      <div className="flex items-center mb-6">
        <span className="w-3 h-3 rounded-full mr-2" style={{ background: healthStatus === 'online' ? '#22c55e' : '#ef4444' }}></span>
        <span className="text-gray-200 font-bold">Backend {healthStatus === 'online' ? 'Online' : 'Offline'}</span>
      </div>
      {tabs.map(tab => (
        <button
          key={tab.key}
          className={`mb-2 px-3 py-2 rounded-lg text-left text-gray-200 font-medium ${activeTab === tab.key ? 'bg-orange-500' : 'bg-gray-700'} hover:bg-orange-400`}
          onClick={() => setActiveTab(tab.key)}
        >
          {tab.label}
        </button>
      ))}
      <button
        className={`mt-6 px-3 py-2 rounded-lg text-left text-gray-200 font-medium ${contextPanelVisible ? 'bg-orange-500' : 'bg-gray-700'} hover:bg-orange-400`}
        onClick={() => setContextPanelVisible(!contextPanelVisible)}
      >
        {contextPanelVisible ? 'Hide Context Panel' : 'Show Context Panel'}
      </button>
    </div>
  );
};

export default Sidebar;
