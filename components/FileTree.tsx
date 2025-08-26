
import React from 'react';
import type { TreeNode } from '../types';
import { FileTreeNode } from './FileTreeNode';

interface FileTreeProps {
  tree: TreeNode[];
  onFileSelect: (path: string) => void;
  activeFile: string | null;
}

export function FileTree({ tree, onFileSelect, activeFile }: FileTreeProps): React.ReactNode {
  return (
    <ul className="text-sm text-gray-300">
      {tree.map(node => (
        <FileTreeNode 
          key={node.path} 
          node={node} 
          onFileSelect={onFileSelect} 
          activeFile={activeFile}
          depth={0}
        />
      ))}
    </ul>
  );
}
