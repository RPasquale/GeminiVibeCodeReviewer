
import React, { useState, useCallback } from 'react';
import { parseGitHubUrl, getRepoTreeFiles, buildFileTree, getFileContent } from '../services/githubService';
import type { CodeFile, TreeNode } from '../types';
import { FileTree } from './FileTree';
import { CodeEditor } from './CodeEditor';
import { Loader } from './Loader';
import { GithubIcon } from './icons/GithubIcon';
import { SparklesIcon } from './icons/SparklesIcon';

interface IDEServiceProps {
    onUseInContext: (files: CodeFile[]) => void;
}

export function IDEService({ onUseInContext }: IDEServiceProps): React.ReactNode {
    const [repoUrl, setRepoUrl] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isFetchingFile, setIsFetchingFile] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [fileTree, setFileTree] = useState<TreeNode[]>([]);
    const [repoInfo, setRepoInfo] = useState<{owner: string, repo: string} | null>(null);
    const [fileContents, setFileContents] = useState<Record<string, string>>({});
    const [activeFile, setActiveFile] = useState<string | null>(null);
    const [allFilePaths, setAllFilePaths] = useState<string[]>([]);


    const handleLoadRepo = useCallback(async () => {
        const parsed = parseGitHubUrl(repoUrl);
        if (!parsed) {
            setError('Invalid GitHub repository URL.');
            return;
        }

        setIsLoading(true);
        setError(null);
        setFileTree([]);
        setActiveFile(null);
        setFileContents({});
        setRepoInfo(parsed);

        try {
            const files = await getRepoTreeFiles(parsed.owner, parsed.repo);
            const tree = buildFileTree(files);
            setFileTree(tree);
            setAllFilePaths(files.filter(f => f.type === 'blob').map(f => f.path));
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load repository.');
        } finally {
            setIsLoading(false);
        }
    }, [repoUrl]);
    
    const handleFileSelect = useCallback(async (path: string) => {
        setActiveFile(path);
        if (fileContents[path] || !repoInfo) return;

        setIsFetchingFile(true);
        try {
            const content = await getFileContent(repoInfo.owner, repoInfo.repo, path);
            setFileContents(prev => ({...prev, [path]: content}));
        } catch (err) {
            setError(err instanceof Error ? `Failed to load file ${path}: ${err.message}` : `Failed to load file ${path}.`);
        } finally {
            setIsFetchingFile(false);
        }
    }, [repoInfo, fileContents]);

    const handleCodeChange = (newCode: string) => {
        if (activeFile) {
            setFileContents(prev => ({...prev, [activeFile]: newCode}));
        }
    };
    
    const handleUseInContext = async () => {
        if (!repoInfo || allFilePaths.length === 0) {
            setError("No repository loaded or repository is empty.");
            return;
        }

        setIsLoading(true);
        setError(null);
        
        try {
            const allFiles: CodeFile[] = await Promise.all(
                allFilePaths.map(async (path) => {
                    // Use already loaded/edited content if available
                    if (fileContents[path]) {
                        return { name: path, content: fileContents[path] };
                    }
                    // Otherwise, fetch it
                    const content = await getFileContent(repoInfo.owner, repoInfo.repo, path);
                    return { name: path, content };
                })
            );
            onUseInContext(allFiles);
        } catch (err) {
             setError(err instanceof Error ? `Failed to load all files: ${err.message}` : `An unknown error occurred while preparing files.`);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col gap-4">
            <div className="flex flex-col sm:flex-row gap-4 items-center">
                <div className="relative flex-grow w-full">
                    <GithubIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                        type="text"
                        value={repoUrl}
                        onChange={(e) => setRepoUrl(e.target.value)}
                        placeholder="e.g., https://github.com/react-js/react-js.github.io"
                        className="w-full bg-gray-800 border border-gray-700 rounded-md pl-10 pr-4 py-2 text-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none"
                    />
                </div>
                <button
                    onClick={handleLoadRepo}
                    disabled={isLoading || !repoUrl.trim()}
                    className="w-full sm:w-auto bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-900 text-white font-bold py-2 px-4 rounded-md transition-colors"
                >
                    {isLoading ? 'Loading...' : 'Load Repo'}
                </button>
                 <button
                    onClick={handleUseInContext}
                    disabled={isLoading || fileTree.length === 0}
                    className="w-full sm:w-auto flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 disabled:bg-green-900 text-white font-bold py-2 px-4 rounded-md transition-colors"
                >
                   <SparklesIcon className="w-5 h-5"/> Use in Context Engineer
                </button>
            </div>
            {error && <p className="text-red-400 text-center">{error}</p>}
            
            <div className="grid grid-cols-1 md:grid-cols-12 gap-4 min-h-[70vh]">
                <div className="md:col-span-3 bg-gray-800 rounded-lg p-2 overflow-y-auto">
                    {isLoading ? (
                         <div className="flex items-center justify-center h-full">
                           <Loader/>
                         </div>
                    ) : fileTree.length > 0 ? (
                        <FileTree tree={fileTree} onFileSelect={handleFileSelect} activeFile={activeFile} />
                    ) : (
                        <div className="text-center text-gray-500 p-4">Enter a repository URL to get started.</div>
                    )}
                </div>
                <div className="md:col-span-9 bg-gray-800 rounded-lg p-1">
                    {isFetchingFile ? (
                        <div className="flex items-center justify-center h-full"><Loader/></div>
                    ) : activeFile ? (
                        <CodeEditor 
                            code={fileContents[activeFile] || ''}
                            onCodeChange={handleCodeChange}
                            language="" // Language detection can be added later
                        />
                    ) : (
                        <div className="flex items-center justify-center h-full text-gray-500">Select a file to view its content.</div>
                    )}
                </div>
            </div>
        </div>
    );
}
