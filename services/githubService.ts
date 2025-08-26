import type { TreeNode } from '../types';

interface GitHubFile {
  path: string;
  type: 'tree' | 'blob';
}

export function parseGitHubUrl(url: string): { owner: string; repo: string } | null {
  const match = url.match(/github\.com\/([^/]+)\/([^/]+)/);
  if (match && match[1] && match[2]) {
    return { owner: match[1], repo: match[2].replace('.git', '') };
  }
  return null;
}

async function fetchRepoTree(owner: string, repo: string, branch: string): Promise<GitHubFile[]> {
    const response = await fetch(`https://api.github.com/repos/${owner}/${repo}/git/trees/${branch}?recursive=1`);
    if (!response.ok) {
        throw new Error(`Failed to fetch repository tree for branch ${branch}. Status: ${response.status}`);
    }
    const data = await response.json();
    if (!data.tree) {
      throw new Error("Invalid response from GitHub API: 'tree' property is missing.");
    }
    return data.tree;
}

export async function getRepoTreeFiles(owner: string, repo: string): Promise<GitHubFile[]> {
    try {
        return await fetchRepoTree(owner, repo, 'main');
    } catch (e) {
        console.warn("Failed to fetch 'main' branch, trying 'master'...");
        return await fetchRepoTree(owner, repo, 'master');
    }
}

export function buildFileTree(files: GitHubFile[]): TreeNode[] {
    const root: TreeNode = { name: 'root', path: '', type: 'folder', children: [] };
    const nodeMap: { [path: string]: TreeNode } = { '': root };

    // Filter out submodule files (type gitlink) which we can't read
    const validFiles = files.filter((file: any) => file.type !== 'commit');

    validFiles.forEach(file => {
        const parts = file.path.split('/');
        let parentNode = root;

        parts.forEach((part, index) => {
            const currentPath = parts.slice(0, index + 1).join('/');
            
            let currentNode = parentNode.children?.find(child => child.path === currentPath);

            if (!currentNode) {
                const type = (index === parts.length - 1 && file.type === 'blob') ? 'file' : 'folder';
                const newNode: TreeNode = {
                    name: part,
                    path: currentPath,
                    type,
                    children: type === 'folder' ? [] : undefined,
                };
                parentNode.children = parentNode.children || [];
                parentNode.children.push(newNode);
                currentNode = newNode;
            }
            parentNode = currentNode;
        });
    });

    const sortNodes = (nodes: TreeNode[]) => {
        nodes.sort((a, b) => {
            if (a.type === 'folder' && b.type === 'file') return -1;
            if (a.type === 'file' && b.type === 'folder') return 1;
            return a.name.localeCompare(b.name);
        });
        nodes.forEach(node => {
            if (node.children) {
                sortNodes(node.children);
            }
        });
    };
    if (root.children) {
        sortNodes(root.children);
    }

    return root.children || [];
}

async function fetchFileContent(owner: string, repo: string, path: string, branch: string): Promise<string> {
    const response = await fetch(`https://raw.githubusercontent.com/${owner}/${repo}/${branch}/${path}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch file content for ${path} from branch ${branch}.`);
    }
    return response.text();
}

export async function getFileContent(owner: string, repo: string, path: string): Promise<string> {
    try {
        return await fetchFileContent(owner, repo, path, 'main');
    } catch (e) {
        console.warn(`Failed to fetch ${path} from 'main' branch, trying 'master'...`);
        return await fetchFileContent(owner, repo, path, 'master');
    }
}