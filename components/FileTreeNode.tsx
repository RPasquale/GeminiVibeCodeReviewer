
import React, { useState } from 'react';
import type { TreeNode } from '../types';
import { FileIcon } from './icons/FileIcon';
import { FolderIcon } from './icons/FolderIcon';
import { ChevronRightIcon } from './icons/ChevronRightIcon';

interface FileTreeNodeProps {
  node: TreeNode;
  onFileSelect: (path: string) => void;
  activeFile: string | null;
  depth: number;
}

export function FileTreeNode({ node, onFileSelect, activeFile, depth }: FileTreeNodeProps): React.ReactNode {
  const [isOpen, setIsOpen] = useState(false);

  const isFolder = node.type === 'folder';
  const isActive = activeFile === node.path;
  
  const handleToggle = () => {
    if (isFolder) {
      setIsOpen(!isOpen);
    } else {
      onFileSelect(node.path);
    }
  };
  
  const indentStyle = { paddingLeft: `${depth * 1.25}rem` };

  return (
    <li>
      <button
        onClick={handleToggle}
        className={`w-full flex items-center gap-2 text-left px-2 py-1 rounded-md transition-colors ${
            isActive ? 'bg-indigo-600 text-white' : 'hover:bg-gray-700'
        }`}
        style={indentStyle}
      >
        {isFolder ? (
          <>
            <ChevronRightIcon className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-90' : ''}`} />
            <FolderIcon className="w-4 h-4 text-indigo-400" />
          </>
        ) : (
          <FileIcon className="w-4 h-4 text-gray-400 ml-4" /> // ml-4 to align with folder content
        )}
        <span className="truncate">{node.name}</span>
      </button>
      {isFolder && isOpen && node.children && (
        <ul>
          {node.children.map(child => (
            <FileTreeNode 
              key={child.path} 
              node={child} 
              onFileSelect={onFileSelect} 
              activeFile={activeFile}
              depth={depth + 1}
            />
          ))}
        </ul>
      )}
    </li>
  );
}
