
import React, { useState } from 'react';
import { Header } from './components/Header';
import { CodeReviewer } from './components/CodeReviewer';
import { ContextEngineer } from './components/ContextEngineer';
import { IDEService } from './components/IDEService';
import { CodeIcon } from './components/icons/CodeIcon';
import { SparklesIcon } from './components/icons/SparklesIcon';
import { GithubIcon } from './components/icons/GithubIcon';
import type { CodeFile } from './types';

type View = 'reviewer' | 'contextEngine' | 'ide';

export default function App(): React.ReactNode {
  const [activeView, setActiveView] = useState<View>('reviewer');
  const [contextFiles, setContextFiles] = useState<CodeFile[]>([]);

  const navItemClasses = (view: View) => 
    `flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
      activeView === view
        ? 'bg-indigo-600 text-white'
        : 'text-gray-300 hover:bg-gray-700'
    }`;

  const handleLoadRepoInContext = (files: CodeFile[]) => {
    setContextFiles(files);
    setActiveView('contextEngine');
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-200 font-sans">
      <Header />
      <main className="p-4 md:p-8">
        <div className="container mx-auto max-w-7xl">
          {/* Navigation Tabs */}
          <div className="mb-6 flex justify-center">
            <div className="flex items-center gap-2 p-1 bg-gray-800 rounded-lg">
              <button onClick={() => setActiveView('reviewer')} className={navItemClasses('reviewer')}>
                <SparklesIcon className="w-5 h-5" />
                Code Reviewer
              </button>
              <button onClick={() => setActiveView('ide')} className={navItemClasses('ide')}>
                <GithubIcon className="w-5 h-5" />
                IDE
              </button>
              <button onClick={() => setActiveView('contextEngine')} className={navItemClasses('contextEngine')}>
                <CodeIcon className="w-5 h-5" />
                Context Engineer
              </button>
            </div>
          </div>

          {/* Page Content */}
          {activeView === 'reviewer' && <CodeReviewer />}
          {activeView === 'ide' && <IDEService onUseInContext={handleLoadRepoInContext} />}
          {activeView === 'contextEngine' && (
            <ContextEngineer 
              initialFiles={contextFiles} 
              onFilesLoaded={() => setContextFiles([])} 
            />
          )}
        </div>
      </main>
    </div>
  );
}
