
import React, { useRef } from 'react';
import type { CodeFile } from '../types';
import { PaperclipIcon } from './icons/PaperclipIcon';
import { SparklesIcon } from './icons/SparklesIcon';

interface FileListProps {
  files: CodeFile[];
  onAddFiles: (files: CodeFile[]) => void;
  onRemoveFile: (fileName: string) => void;
  onStartChat: () => void;
  isChatStarted: boolean;
  isLoading: boolean;
  error: string | null;
}

export function FileList({ files, onAddFiles, onRemoveFile, onStartChat, isChatStarted, isLoading, error }: FileListProps): React.ReactNode {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const fileList = event.target.files;
    if (!fileList) return;

    const newFiles: Promise<CodeFile>[] = Array.from(fileList).map(file => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          const content = e.target?.result as string;
          resolve({ name: file.name, content });
        };
        reader.onerror = reject;
        reader.readAsText(file);
      });
    });

    Promise.all(newFiles).then(onAddFiles);
    
    // Reset file input
    if(event.target) {
        event.target.value = '';
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg p-4 h-full flex flex-col">
      <h2 className="text-xl font-bold mb-4 text-white">Context Files</h2>
      <div className="flex-grow min-h-[200px] border-2 border-dashed border-gray-600 rounded-lg p-2 overflow-y-auto">
        {files.length === 0 ? (
          <div className="text-center text-gray-500 p-4">
            <p>Add files to build your context.</p>
          </div>
        ) : (
          <ul className="space-y-2">
            {files.map(file => (
              <li key={file.name} className="flex items-center justify-between bg-gray-700 p-2 rounded-md text-sm">
                <span className="text-gray-300 truncate">{file.name}</span>
                {!isChatStarted && (
                    <button onClick={() => onRemoveFile(file.name)} className="text-red-400 hover:text-red-300 ml-2">&times;</button>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>

      {error && <p className="text-red-400 text-sm mt-2">{error}</p>}
      
      <input type="file" multiple ref={fileInputRef} onChange={handleFileChange} className="hidden" />

      {!isChatStarted ? (
        <div className="mt-4 space-y-2">
            <button
                onClick={() => fileInputRef.current?.click()}
                className="w-full flex items-center justify-center gap-2 bg-gray-600 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-md transition-colors"
            >
                <PaperclipIcon className="w-5 h-5"/>
                Add Files
            </button>
            <button
                onClick={onStartChat}
                disabled={files.length === 0 || isLoading}
                className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-900 text-white font-bold py-2 px-4 rounded-md transition-colors disabled:cursor-not-allowed"
            >
                <SparklesIcon className="w-5 h-5"/>
                {isLoading ? 'Starting...' : 'Start Session'}
            </button>
        </div>
      ) : (
        <p className="text-center text-sm text-green-400 mt-4 p-2 bg-green-900/50 rounded-md">
            Chat session is active.
        </p>
      )}
    </div>
  );
}
