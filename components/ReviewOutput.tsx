
import React from 'react';
import type { ReviewResult } from '../types';
import { SparklesIcon } from './icons/SparklesIcon';

interface ReviewOutputProps {
  review: ReviewResult | null;
  error: string | null;
}

const CategoryIcon = ({ category, isRoast }: { category: string, isRoast: boolean }): React.ReactNode => {
    const lowerCategory = category.toLowerCase();
    
    if (isRoast) {
        if (lowerCategory.includes('bug')) return <span role="img" aria-label="clown face">🤡</span>;
        if (lowerCategory.includes('performance')) return <span role="img" aria-label="turtle">🐢</span>;
        if (lowerCategory.includes('security')) return <span role="img" aria-label="open door">🚪</span>;
        if (lowerCategory.includes('best practice')) return <span role="img" aria-label="facepalm">🤦</span>;
        if (lowerCategory.includes('readability')) return <span role="img" aria-label="exploding head">🤯</span>;
        return <span role="img" aria-label="trash can">🗑️</span>;
    }

    if (lowerCategory.includes('bug')) return <span role="img" aria-label="bug">🐛</span>;
    if (lowerCategory.includes('performance')) return <span role="img" aria-label="rocket">🚀</span>;
    if (lowerCategory.includes('security')) return <span role="img" aria-label="shield">🛡️</span>;
    if (lowerCategory.includes('best practice')) return <span role="img" aria-label="star">⭐</span>;
    if (lowerCategory.includes('readability')) return <span role="img" aria-label="book">📖</span>;
    return <span role="img" aria-label="clipboard">📋</span>;
};

// A simple markdown-to-react component to handle code blocks and lists
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

export function ReviewOutput({ review, error }: ReviewOutputProps): React.ReactNode {
  if (error) {
    return (
      <div className="flex items-center justify-center h-full text-center p-4">
        <div>
          <p className="text-red-400 text-lg font-semibold">An Error Occurred</p>
          <p className="text-gray-400 mt-2">{error}</p>
        </div>
      </div>
    );
  }

  if (!review) {
    return (
      <div className="flex items-center justify-center h-full text-center p-4">
        <div>
          <SparklesIcon className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-300">Ready for Review</h3>
          <p className="text-gray-500 mt-2">
            Paste your code on the left, select the language, and click "Review Code" to see the magic happen.
          </p>
        </div>
      </div>
    );
  }

  const isRoast = review.isRoast;

  return (
    <div className="p-6 h-full overflow-y-auto">
      <h2 className={`text-2xl font-bold mb-4 border-b pb-2 ${isRoast ? 'text-orange-400 border-orange-700' : 'text-white border-gray-700'}`}>
        {isRoast ? '🔥 Code Roast Analysis 🔥' : 'Code Review Analysis'}
      </h2>
      <div className={`${isRoast ? 'bg-orange-900/50' : 'bg-gray-700/50'} p-4 rounded-lg mb-6`}>
        <h3 className={`text-lg font-semibold mb-2 ${isRoast ? 'text-orange-300' : 'text-indigo-400'}`}>Summary</h3>
        <p className="text-gray-300">{review.summary}</p>
      </div>

      <div className="space-y-6">
        {review.feedback.map((item, index) => (
          <div key={index} className={`p-4 rounded-lg border ${isRoast ? 'bg-gray-900/50 border-orange-800' : 'bg-gray-900/50 border-gray-700'}`}>
            <h4 className="flex items-center gap-2 text-md font-semibold text-gray-200 mb-3">
              <CategoryIcon category={item.category} isRoast={isRoast} /> {item.category}
            </h4>
            <div className="text-gray-400 text-sm prose-invert">
                <SimpleMarkdownRenderer content={item.details} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
