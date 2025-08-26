
import React, { useState, useCallback } from 'react';
import { CodeEditor } from './CodeEditor';
import { LanguageSelector } from './LanguageSelector';
import { ReviewOutput } from './ReviewOutput';
import { Loader } from './Loader';
import { SparklesIcon } from './icons/SparklesIcon';
import { getCodeReview } from '../services/geminiService';
import { SUPPORTED_LANGUAGES } from '../constants';
import type { ReviewResult } from '../types';
import { RoastModeToggle } from './RoastModeToggle';
import { FireIcon } from './icons/FireIcon';

export function CodeReviewer(): React.ReactNode {
  const [code, setCode] = useState<string>('');
  const [language, setLanguage] = useState<string>(SUPPORTED_LANGUAGES[0].value);
  const [review, setReview] = useState<ReviewResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [isRoastMode, setIsRoastMode] = useState<boolean>(false);

  const handleReview = useCallback(async () => {
    if (!code.trim()) {
      setError('Please enter some code to review.');
      return;
    }
    setIsLoading(true);
    setError(null);
    setReview(null);

    try {
      const result = await getCodeReview(code, language, isRoastMode);
      setReview(result);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(`An error occurred: ${err.message}`);
      } else {
        setError('An unknown error occurred during the review.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [code, language, isRoastMode]);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* Left Panel: Code Input */}
      <div className="flex flex-col gap-4">
        <div className="flex flex-col sm:flex-row gap-4 items-center justify-between flex-wrap">
          <div className="flex items-center gap-4">
              <LanguageSelector
                language={language}
                onLanguageChange={setLanguage}
                languages={SUPPORTED_LANGUAGES}
              />
              <RoastModeToggle isRoastMode={isRoastMode} onToggle={setIsRoastMode} />
          </div>
          <button
            onClick={handleReview}
            disabled={isLoading}
            className={`w-full sm:w-auto flex items-center justify-center gap-2 font-bold py-2 px-4 rounded-md transition-colors duration-200 ${
              isRoastMode 
                ? 'bg-orange-600 hover:bg-orange-700 disabled:bg-orange-900'
                : 'bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-900'
            } disabled:cursor-not-allowed text-white`}
          >
            {isRoastMode ? <FireIcon className="w-5 h-5" /> : <SparklesIcon className="w-5 h-5" />}
            {isLoading ? 'Analyzing...' : isRoastMode ? 'Roast My Code' : 'Review Code'}
          </button>
        </div>
        <CodeEditor
          code={code}
          onCodeChange={setCode}
          language={language}
        />
      </div>

      {/* Right Panel: Review Output */}
      <div className="bg-gray-800 rounded-lg p-1 min-h-[60vh] lg:min-h-[75vh]">
        {isLoading ? (
          <div className="flex items-center justify-center h-full">
            <Loader />
          </div>
        ) : (
          <ReviewOutput review={review} error={error} />
        )}
      </div>
    </div>
  );
}
