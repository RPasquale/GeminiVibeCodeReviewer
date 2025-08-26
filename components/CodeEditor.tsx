
import React from 'react';

interface CodeEditorProps {
  code: string;
  onCodeChange: (code: string) => void;
  language: string;
}

export function CodeEditor({ code, onCodeChange, language }: CodeEditorProps): React.ReactNode {
  return (
    <div className="relative h-full">
      <textarea
        value={code}
        onChange={(e) => onCodeChange(e.target.value)}
        placeholder={`Paste your ${language} code here...`}
        className="w-full h-[60vh] lg:h-[75vh] p-4 bg-gray-900 border border-gray-700 rounded-lg text-gray-300 font-mono text-sm leading-relaxed focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none resize-none transition-colors duration-200"
        spellCheck="false"
      />
    </div>
  );
}
