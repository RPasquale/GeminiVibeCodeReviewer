
import { GoogleGenAI, Type, Chat, GenerateContentResponse } from "@google/genai";
import type { ReviewResult, CodeFile } from '../types';

if (!process.env.API_KEY) {
    throw new Error("API_KEY environment variable is not set");
}

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

const responseSchema = {
    type: Type.OBJECT,
    properties: {
        summary: {
            type: Type.STRING,
            description: "A brief, one-sentence summary of the code's quality.",
        },
        feedback: {
            type: Type.ARRAY,
            description: "A list of feedback items categorized by area of concern.",
            items: {
                type: Type.OBJECT,
                properties: {
                    category: {
                        type: Type.STRING,
                        description: "The category of feedback (e.g., 'Bugs & Errors', 'Performance', 'Security', 'Best Practices', 'Readability').",
                    },
                    details: {
                        type: Type.STRING,
                        description: "Detailed feedback for this category, formatted in Markdown. Use code snippets with triple backticks where appropriate.",
                    }
                },
                required: ["category", "details"]
            }
        }
    },
    required: ["summary", "feedback"]
};


export async function getCodeReview(code: string, language: string, isRoastMode: boolean): Promise<ReviewResult> {
  const seriousPrompt = `
    You are an expert code reviewer, a principal engineer with decades of experience in software development. 
    Your task is to provide a comprehensive and professional review of the following ${language} code.

    Analyze the code for the following aspects:
    1.  **Bugs and Errors:** Identify potential bugs, logical errors, or edge cases that are not handled correctly.
    2.  **Performance:** Point out any performance bottlenecks and suggest optimizations.
    3.  **Security:** Highlight potential security vulnerabilities (e.g., injection attacks, data exposure).
    4.  **Best Practices & Conventions:** Check if the code follows established best practices, design patterns, and language-specific conventions.
    5.  **Readability & Maintainability:** Evaluate the code's clarity, structure, and ease of maintenance. Suggest improvements for variable names, comments, and overall organization.

    Provide a structured JSON response. The feedback for each category should be detailed, constructive, and include code snippets to illustrate your points when necessary. Format your detailed feedback using Markdown.

    Here is the code to review:
    \`\`\`${language}
    ${code}
    \`\`\`
  `;

  const roastPrompt = `
    You are a sarcastic, witty, and brutally honest code critic with a dark sense of humor. A true keyboard warrior who has seen it all and is not impressed.
    Your goal is to "roast" the following ${language} code. Don't hold back. Make fun of the programmer's choices, question their skills, and deliver your feedback as a series of burns. Your feedback should still point out actual flaws (bugs, bad practices, performance issues etc.), but do it in the most hilariously insulting way possible.
    
    For example, instead of "Consider using a more descriptive variable name", you might say "Did you fall asleep on the keyboard to come up with the variable name 'data'? My cat could do better."
    Instead of "This could be optimized", try "I've seen faster glaciers. This function is a performance nightmare."

    Your tone should be arrogant, condescending, and funny. You are the Gordon Ramsay of code reviews.

    Provide a structured JSON response. The feedback for each category should be a detailed, constructive (in a roasting way) burn. Include code snippets to illustrate your points when necessary. Format your detailed feedback using Markdown.

    Here is the code to roast. Try not to laugh too hard:
    \`\`\`${language}
    ${code}
    \`\`\`
  `;

  const prompt = isRoastMode ? roastPrompt : seriousPrompt;
  const temperature = isRoastMode ? 0.7 : 0.2;

  try {
    const response = await ai.models.generateContent({
        model: "gemini-2.5-flash",
        contents: prompt,
        config: {
            responseMimeType: "application/json",
            responseSchema: responseSchema,
            temperature: temperature,
        },
    });

    const textResponse = response.text.trim();
    const parsedResponse = JSON.parse(textResponse);

    // Basic validation
    if (!parsedResponse.summary || !Array.isArray(parsedResponse.feedback)) {
        throw new Error("Invalid response structure from API.");
    }

    return {
        ...parsedResponse,
        isRoast: isRoastMode,
    } as ReviewResult;

  } catch (error) {
    console.error("Error calling Gemini API:", error);
    throw new Error("Failed to get code review from Gemini API.");
  }
}

export class ContextChatService {
    private chat: Chat | null = null;

    public async startChat(files: CodeFile[]): Promise<GenerateContentResponse> {
        this.chat = ai.chats.create({
            model: 'gemini-2.5-flash',
            config: {
                systemInstruction: `You are an expert AI software engineer. The user has provided you with the following code files as context for this conversation. Your task is to use this context to answer questions, provide suggestions, and help the user with their code. Be concise and helpful.`,
            },
        });

        const contextPrompt = `
I have provided you with ${files.length} file(s) for context. Here is the content:
---
${files.map(file => `
### File: ${file.name}

\`\`\`
${file.content}
\`\`\`
`).join('\n---\n')}
---
I will now ask you questions about this codebase. Please confirm that you have processed the context and are ready.`;
        
        return this.chat.sendMessage({ message: contextPrompt });
    }

    public async sendMessage(message: string): Promise<GenerateContentResponse> {
        if (!this.chat) {
            throw new Error("Chat not started. Call startChat first.");
        }
        return this.chat.sendMessage({ message });
    }
}
