
export interface Language {
  value: string;
  label: string;
}

export interface FeedbackItem {
  category: string;
  details: string;
}

export interface ReviewResult {
  summary: string;
  feedback: FeedbackItem[];
  isRoast: boolean;
}

export interface CodeFile {
  name: string;
  content: string;
}

export interface ChatMessage {
  role: 'user' | 'model';
  content: string;
}

export interface TreeNode {
  path: string;
  name: string;
  type: 'file' | 'folder';
  children?: TreeNode[];
}
