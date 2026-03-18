import React, { useEffect, useRef } from 'react';
import { ConversationTurn, ChatResponse } from '../types';

interface ChatWindowProps {
  history: ConversationTurn[];
  botResponses: ChatResponse[];
  typing: boolean;
  onCopy: (msg: string) => void;
  onClear: () => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ history, botResponses, typing, onCopy, onClear }) => {
  const chatRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [history, botResponses, typing]);

  return (
    <div className="flex flex-col h-full bg-gray-900 rounded-lg p-4 overflow-y-auto" ref={chatRef}>
      <div className="mb-2 flex justify-between items-center">
        <span className="text-sm text-gray-400">Chat History</span>
        <button
          className="text-xs text-orange-500 hover:underline"
          onClick={onClear}
        >
          Clear Chat
        </button>
      </div>
      {history.map((msg, idx) => {
        const isUser = msg.role === 'user';
        const botResp = !isUser ? botResponses.find((r, i) => i === idx / 2) : null;
        return (
          <div key={idx} className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-2`}>
            <div className={`max-w-xs px-4 py-2 rounded-lg ${isUser ? 'bg-orange-500 text-white' : 'bg-gray-700 text-gray-200'} relative`}>
              {msg.content}
              {!isUser && botResp && (
                <div className="mt-2 text-xs text-gray-400">
                  <div>Sources: {botResp.sources.join(', ')}</div>
                  <div>Confidence: {botResp.confidence.toFixed(2)}</div>
                  <button
                    className="absolute top-1 right-1 text-xs text-orange-400 hover:text-orange-500"
                    onClick={() => onCopy(botResp.response)}
                  >
                    Copy
                  </button>
                </div>
              )}
            </div>
          </div>
        );
      })}
      {typing && (
        <div className="flex justify-start mb-2">
          <div className="bg-gray-700 text-gray-200 px-4 py-2 rounded-lg flex items-center">
            <span className="mr-2">Assistant is typing</span>
            <span className="flex space-x-1">
              <span className="animate-bounce">.</span>
              <span className="animate-bounce delay-75">.</span>
              <span className="animate-bounce delay-150">.</span>
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWindow;
