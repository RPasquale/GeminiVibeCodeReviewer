#!/bin/bash

# Repository Rename Script
echo "🔄 Renaming repository from GeminiVibeCodeReviewer to VibeCodeReviewer..."

# Get the current directory name
current_dir=$(basename "$PWD")

if [ "$current_dir" = "GeminiVibeCodeReviewer" ]; then
    echo "📁 Current directory: $current_dir"
    
    # Go to parent directory
    cd ..
    
    # Rename the directory
    mv GeminiVibeCodeReviewer VibeCodeReviewer
    
    echo "✅ Directory renamed successfully!"
    echo "📁 New directory: VibeCodeReviewer"
    echo ""
    echo "🚀 Next steps:"
    echo "1. Navigate to the new directory: cd VibeCodeReviewer"
    echo "2. Start the application: ./start.sh"
    echo ""
    echo "💡 If you're using Git, you may also want to:"
    echo "   - Update the remote URL if you renamed the repository on GitHub"
    echo "   - Run: git remote set-url origin <new-repo-url>"
    
else
    echo "ℹ️  Current directory is already named correctly or doesn't match expected name."
    echo "   Current directory: $current_dir"
    echo ""
    echo "✅ All configuration files have been updated with the new name!"
    echo "🚀 You can now start the application with: ./start.sh"
fi
