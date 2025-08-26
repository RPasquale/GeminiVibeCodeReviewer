
import React from 'react';

interface IconProps {
  className?: string;
}

export function SparklesIcon({ className }: IconProps): React.ReactNode {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      width="24" 
      height="24" 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="2" 
      strokeLinecap="round" 
      strokeLinejoin="round" 
      className={className}
    >
      <path d="M12 3a6 6 0 0 0 9 9a9 9 0 1 1-9-9Z"></path>
      <path d="M18 10a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1Z"></path>
      <path d="M21 17a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1Z"></path>
    </svg>
  );
}
