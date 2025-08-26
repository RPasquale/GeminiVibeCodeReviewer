
import React, { useState, useRef, useEffect } from 'react';
import { FileList } from './FileList';
import { ChatInterface } from './ChatInterface';
import { ContextChatService } from '../services/geminiService';
import type { CodeFile, ChatMessage } from '../types';

interface ContextEngineerProps {
  initialFiles?: CodeFile[];
  onFilesLoaded?: () => void;
}

export function ContextEngineer({ initialFiles, onFilesLoaded }: ContextEngineerProps): React.ReactNode {
  const [files, setFiles] = useState<CodeFile[]>([]);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isChatStarted, setIsChatStarted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const chatServiceRef = useRef<ContextChatService | null>(null);

  useEffect(() => {
    if (initialFiles && initialFiles.length > 0) {
      setFiles(initialFiles);
      if (onFilesLoaded) {
        onFilesLoaded();
      }
    }
  }, [initialFiles, onFilesLoaded]);


  const handleAddFiles = (newFiles: CodeFile[]) => {
    if (isChatStarted) return; // Don't allow adding files after chat has started
    setFiles((prevFiles) => [...prevFiles, ...newFiles]);
    setError(null);
  };

  const handleRemoveFile = (fileName: string) => {
    if (isChatStarted) return;
    setFiles((prevFiles) => prevFiles.filter((file) => file.name !== fileName));
  };

  const handleStartChat = async () => {
    if (files.length === 0) {
      setError("Please add at least one file to start the chat.");
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      chatServiceRef.current = new ContextChatService();
      const response = await chatServiceRef.current.startChat(files);
      setMessages([{ role: 'model', content: response.text }]);
      setIsChatStarted(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unknown error occurred.");
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleSendMessage = async (message: string) => {
      if (!chatServiceRef.current) return;
      
      const userMessage: ChatMessage = { role: 'user', content: message };
      setMessages(prev => [...prev, userMessage]);
      setIsLoading(true);

      try {
          const response = await chatServiceRef.current.sendMessage(message);
          const modelMessage: ChatMessage = { role: 'model', content: response.text };
          setMessages(prev => [...prev, modelMessage]);
      } catch (err) {
          const errorMessage = err instanceof Error ? err.message : "An unknown error occurred.";
          setError(errorMessage);
          setMessages(prev => [...prev, { role: 'model', content: `Error: ${errorMessage}` }]);
      } finally {
          setIsLoading(false);
      }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="lg:col-span-1">
        <FileList
            files={files}
            onAddFiles={handleAddFiles}
            onRemoveFile={handleRemoveFile}
            onStartChat={handleStartChat}
            isChatStarted={isChatStarted}
            isLoading={isLoading}
            error={error}
        />
      </div>
      <div className="lg:col-span-2 bg-gray-800 rounded-lg min-h-[75vh]">
        <ChatInterface 
            messages={messages}
            onSendMessage={handleSendMessage}
            isChatStarted={isChatStarted}
            isLoading={isLoading}
        />
      </div>
    </div>
  );
}
