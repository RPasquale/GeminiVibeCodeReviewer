
import React from 'react';

interface RoastModeToggleProps {
  isRoastMode: boolean;
  onToggle: (isRoastMode: boolean) => void;
}

export function RoastModeToggle({ isRoastMode, onToggle }: RoastModeToggleProps): React.ReactNode {
  const toggleId = React.useId();
  return (
    <div className="flex items-center gap-2">
      <label htmlFor={toggleId} className="text-sm font-medium text-gray-300 cursor-pointer select-none">
        Roast Mode <span role="img" aria-label="fire">🔥</span>
      </label>
      <button
        id={toggleId}
        type="button"
        role="switch"
        aria-checked={isRoastMode}
        onClick={() => onToggle(!isRoastMode)}
        className={`${
          isRoastMode ? 'bg-orange-500' : 'bg-gray-600'
        } relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 focus:ring-offset-gray-900`}
      >
        <span
          aria-hidden="true"
          className={`${
            isRoastMode ? 'translate-x-5' : 'translate-x-0'
          } pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out`}
        />
      </button>
    </div>
  );
}
