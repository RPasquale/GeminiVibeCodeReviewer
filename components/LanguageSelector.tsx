
import React from 'react';
import type { Language } from '../types';

interface LanguageSelectorProps {
  language: string;
  onLanguageChange: (language: string) => void;
  languages: Language[];
}

export function LanguageSelector({ language, onLanguageChange, languages }: LanguageSelectorProps): React.ReactNode {
  return (
    <div className="w-full sm:w-auto">
      <label htmlFor="language-select" className="sr-only">Select Language</label>
      <select
        id="language-select"
        value={language}
        onChange={(e) => onLanguageChange(e.target.value)}
        className="w-full bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block p-2.5"
      >
        {languages.map((lang) => (
          <option key={lang.value} value={lang.value}>
            {lang.label}
          </option>
        ))}
      </select>
    </div>
  );
}
