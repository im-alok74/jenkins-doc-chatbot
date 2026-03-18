import React, { useState, useEffect } from 'react';
import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';
import ContextPanel from './components/ContextPanel';
import LogAnalyzer from './components/LogAnalyzer';
import DocSearch from './components/DocSearch';
import Sidebar from './components/Sidebar';
import { ChatContext, ConversationTurn, ChatResponse } from './types';
import { sendChat, getHealth } from './services/api';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('chat');
  const [contextPanelVisible, setContextPanelVisible] = useState(true);
  const [context, setContext] = useState<ChatContext>({});
  const [history, setHistory] = useState<ConversationTurn[]>([]);
  const [botResponses, setBotResponses] = useState<ChatResponse[]>([]);
  const [typing, setTyping] = useState(false);
  const [healthStatus, setHealthStatus] = useState<'online' | 'offline'>('offline');
  const [error, setError] = useState('');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await getHealth();
        setHealthStatus(res.status === 'ok' ? 'online' : 'offline');
      } catch {
        setHealthStatus('offline');
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleSend = async (msg: string) => {
    setTyping(true);
    setError('');
    setHistory([...history, { role: 'user', content: msg }]);
    try {
      const payload = {
        query: msg,
        context,
        conversation_history: [...history, { role: 'user', content: msg }],
      };
      const resp = await sendChat(payload);
      setHistory([...history, { role: 'user', content: msg }, { role: 'assistant', content: resp.response }]);
      setBotResponses([...botResponses, resp]);
    } catch {
      setError('Failed to get response. Please try again.');
    } finally {
      setTyping(false);
    }
  };

  const handleCopy = (msg: string) => {
    navigator.clipboard.writeText(msg);
  };

  const handleClear = () => {
    setHistory([]);
    setBotResponses([]);
    setError('');
  };

  return (
    <div className="min-h-screen bg-gray-950 flex flex-row">
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        contextPanelVisible={contextPanelVisible}
        setContextPanelVisible={setContextPanelVisible}
        healthStatus={healthStatus}
      />
      <div className="flex-1 flex flex-col p-6">
        <header className="mb-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-orange-500">Jenkins AI Chatbot</h1>
          {error && <div className="text-red-500 text-sm">{error}</div>}
        </header>
        {contextPanelVisible && (
          <ContextPanel context={context} setContext={setContext} visible={contextPanelVisible} />
        )}
        <div className="flex-1 flex flex-col">
          {activeTab === 'chat' && (
            <>
              <ChatWindow
                history={history}
                botResponses={botResponses}
                typing={typing}
                onCopy={handleCopy}
                onClear={handleClear}
              />
              <ChatInput onSend={handleSend} disabled={typing || healthStatus === 'offline'} />
            </>
          )}
          {activeTab === 'log' && <LogAnalyzer />}
          {activeTab === 'docs' && <DocSearch />}
        </div>
      </div>
    </div>
  );
};

export default App;
