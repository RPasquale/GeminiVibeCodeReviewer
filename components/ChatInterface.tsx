
import React, { useState, useRef, useEffect } from 'react';
import type { ChatMessage } from '../types';
import { SendIcon } from './icons/SendIcon';
import { UserIcon } from './icons/UserIcon';
import { BotIcon } from './icons/BotIcon';

interface ChatInterfaceProps {
  messages: ChatMessage[];
  onSendMessage: (message: string) => void;
  isChatStarted: boolean;
  isLoading: boolean;
}

// A simple markdown-to-react component to handle code blocks
const SimpleMarkdownRenderer = ({ content }: { content: string }): React.ReactNode => {
    const parts = content.split(/(\`\`\`[\s\S]*?\`\`\`)/g);
    return parts.map((part, index) => {
        if (part.startsWith('```')) {
            const code = part.replace(/```[\w]*\n/g, '').replace(/```/g, '');
            return (
                <pre key={index} className="bg-gray-900/70 rounded-md p-3 my-2 text-sm overflow-x-auto">
                    <code>{code}</code>
                </pre>
            );
        }
        return part.split('\n').map((line, lineIndex) => (
            <p key={`${index}-${lineIndex}`} className="mb-2 last:mb-0">{line}</p>
        ));
    });
};


export function ChatInterface({ messages, onSendMessage, isChatStarted, isLoading }: ChatInterfaceProps): React.ReactNode {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = () => {
    if (input.trim()) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!isChatStarted) {
    return (
      <div className="flex items-center justify-center h-full text-center p-4">
        <div>
          <h3 className="text-xl font-semibold text-gray-300">Context Chat</h3>
          <p className="text-gray-500 mt-2">
            Add some files and click "Start Session" to begin your conversation.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full p-4">
      <div className="flex-grow overflow-y-auto mb-4 pr-2">
        {messages.map((msg, index) => (
          <div key={index} className={`flex items-start gap-3 my-4 ${msg.role === 'user' ? 'justify-end' : ''}`}>
            {msg.role === 'model' && <BotIcon className="w-8 h-8 flex-shrink-0 text-indigo-400 mt-1" />}
            <div className={`max-w-xl p-3 rounded-lg text-white ${msg.role === 'user' ? 'bg-indigo-600' : 'bg-gray-700'}`}>
              <div className="text-sm prose-invert max-w-none">
                  <SimpleMarkdownRenderer content={msg.content} />
              </div>
            </div>
            {msg.role === 'user' && <UserIcon className="w-8 h-8 flex-shrink-0 text-gray-300 mt-1" />}
          </div>
        ))}
        {isLoading && (
            <div className="flex items-start gap-3 my-4">
                 <BotIcon className="w-8 h-8 flex-shrink-0 text-indigo-400 mt-1" />
                 <div className="max-w-xl p-3 rounded-lg bg-gray-700 text-white">
                    <div className="flex items-center gap-2">
                        <span className="animate-pulse">...</span>
                    </div>
                 </div>
            </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="flex items-center gap-2 border-t border-gray-700 pt-4">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about the code..."
          className="w-full p-2 bg-gray-900 border border-gray-600 rounded-lg text-gray-300 focus:ring-2 focus:ring-indigo-500 outline-none resize-none transition-colors"
          rows={1}
        />
        <button
          onClick={handleSend}
          disabled={isLoading || !input.trim()}
          className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-900 text-white p-2 rounded-lg transition-colors disabled:cursor-not-allowed"
        >
            <SendIcon className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}
