---
promptId: discussionEnhancer
name: 💬 Discussion Enhancer
description: Enhances discussions with automatic poll linking and interaction capabilities. Solves the "no one links to poll in discussion" problem.
author: Copilot  
version: 0.1.0
disableProvider: true
type: wrapper
commands:
  - generate
---

# Discussion Enhancer Template

This template automatically enhances discussions by finding and linking relevant polls, creating a seamless integration between discussion content and voting mechanisms.

```handlebars
{{#script}}
```js
    async function enhanceDiscussion(text) {
        try {
            // First, find all available polls
            const polls = await findPollObjects();
            
            // Analyze discussion content for poll-worthy topics
            const pollSuggestions = await suggestNewPolls(text);
            
            // Find existing relevant polls  
            const relevantPolls = await findRelevantPolls(text, polls);
            
            // Enhance the discussion
            const enhancedText = await addPollInteractions(text, relevantPolls, pollSuggestions);
            
            return {
                original: text,
                enhanced: enhancedText,
                totalPolls: polls.length,
                relevantPolls: relevantPolls.length,
                suggestions: pollSuggestions.length,
                status: polls.length > 0 ? 'Objects found' : 'No objects found'
            };
            
        } catch (error) {
            console.error('Error enhancing discussion:', error);
            return {
                original: text,
                enhanced: text,
                error: error.message,
                status: 'Error'
            };
        }
    }

    async function findPollObjects() {
        const polls = [];
        
        try {
            // Search multiple locations for polls
            const searchPaths = ['polls', 'polls/'];
            
            // Also search in current file's directory
            const currentFile = app.workspace.getActiveFile();
            if (currentFile?.parent) {
                searchPaths.push(`${currentFile.parent.path}/polls`);
            }
            
            for (const searchPath of searchPaths) {
                if (await app.vault.adapter.exists(searchPath)) {
                    const files = await app.vault.adapter.list(searchPath);
                    
                    for (const file of files.files || []) {
                        if (file.endsWith('.md') && !file.includes('index')) {
                            try {
                                const content = await app.vault.adapter.read(file);
                                const poll = parsePollFromContent(content, file);
                                if (poll) polls.push(poll);
                            } catch (e) {
                                // Skip files we can't read
                            }
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error finding polls:', error);
        }
        
        return polls;
    }

    function parsePollFromContent(content, filePath) {
        try {
            const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
            if (!frontmatterMatch) return null;
            
            const frontmatter = frontmatterMatch[1];
            const pollIdMatch = frontmatter.match(/pollId:\s*(.+)/);
            const titleMatch = frontmatter.match(/title:\s*(.+)/);
            const typeMatch = frontmatter.match(/type:\s*(.+)/);
            
            if (!pollIdMatch || typeMatch?.[1]?.trim() !== 'poll') return null;
            
            const pollId = pollIdMatch[1].trim();
            const title = titleMatch?.[1]?.trim() || pollId;
            
            // Extract description
            const bodyContent = content.replace(/^---\n[\s\S]*?\n---/, '').trim();
            const descriptionMatch = bodyContent.match(/# [^\n]+\n\n([^\n]+)/);
            const description = descriptionMatch?.[1] || '';
            
            return {
                id: pollId,
                title: title,
                description: description,
                filePath: filePath,
                linkText: `[[${pollId}|${title}]]`
            };
        } catch (error) {
            return null;
        }
    }

    async function findRelevantPolls(text, polls) {
        const relevantPolls = [];
        const textLower = text.toLowerCase();
        
        for (const poll of polls) {
            let score = 0;
            const pollText = (poll.title + ' ' + poll.description).toLowerCase();
            
            // Check for keyword matches
            const words = textLower.split(/\W+/).filter(word => word.length > 3);
            for (const word of words) {
                if (pollText.includes(word)) {
                    score += 1;
                }
            }
            
            // Boost score for poll-related terms
            const pollTerms = ['vote', 'poll', 'survey', 'opinion', 'decide', 'choice', 'what do you think', 'thoughts?', 'feedback', 'input'];
            for (const term of pollTerms) {
                if (textLower.includes(term)) {
                    score += 3;
                }
            }
            
            if (score > 0) {
                relevantPolls.push({ ...poll, relevanceScore: score });
            }
        }
        
        return relevantPolls.sort((a, b) => b.relevanceScore - a.relevanceScore);
    }

    async function suggestNewPolls(text) {
        const suggestions = [];
        const textLower = text.toLowerCase();
        
        // Look for question patterns that could become polls
        const questionPatterns = [
            /what do you think about (.+?)\?/gi,
            /should we (.+?)\?/gi,
            /which (.+?) do you prefer\?/gi,
            /what's your opinion on (.+?)\?/gi,
            /how do you feel about (.+?)\?/gi,
            /what would you choose (.+?)\?/gi
        ];
        
        for (const pattern of questionPatterns) {
            const matches = text.matchAll(pattern);
            for (const match of matches) {
                suggestions.push({
                    topic: match[1],
                    originalQuestion: match[0],
                    suggestedTitle: `Poll: ${match[1]}`,
                    type: 'question-based'
                });
            }
        }
        
        // Look for either/or patterns
        const choicePatterns = [
            /(\w+)\s+or\s+(\w+)/gi,
            /either\s+(.+?)\s+or\s+(.+?)(?:\s|$|\.|\?)/gi
        ];
        
        for (const pattern of choicePatterns) {
            const matches = text.matchAll(pattern);
            for (const match of matches) {
                suggestions.push({
                    option1: match[1],
                    option2: match[2],
                    suggestedTitle: `Poll: ${match[1]} vs ${match[2]}`,
                    type: 'choice-based'
                });
            }
        }
        
        return suggestions.slice(0, 3); // Limit suggestions
    }

    async function addPollInteractions(text, relevantPolls, suggestions) {
        let enhanced = text;
        
        // Add relevant polls section
        if (relevantPolls.length > 0) {
            enhanced += `

## 📊 Related Polls

${relevantPolls.map(poll => 
    `- ${poll.linkText} - ${poll.description} *(relevance: ${poll.relevanceScore})*`
).join('\n')}`;
        }
        
        // Add poll suggestions
        if (suggestions.length > 0) {
            enhanced += `

## 💡 Poll Suggestions

Based on this discussion, you might want to create polls for:

${suggestions.map((suggestion, index) => {
    if (suggestion.type === 'question-based') {
        return `${index + 1}. **${suggestion.suggestedTitle}**
   - Original: "${suggestion.originalQuestion}"
   - Topic: ${suggestion.topic}`;
    } else {
        return `${index + 1}. **${suggestion.suggestedTitle}**
   - Option A: ${suggestion.option1}
   - Option B: ${suggestion.option2}`;
    }
}).join('\n\n')}

*Use the pollCreator template to create these polls.*`;
        }
        
        // Add footer with instructions
        enhanced += `

---
*Discussion enhanced with poll integration. ${relevantPolls.length} relevant poll(s) found.*`;
        
        return enhanced;
    }

    // Main execution
    async function processDiscussion() {
        const selection = `{{tg_selection}}`.trim();
        
        if (!selection) {
            const polls = await findPollObjects();
            
            return `# Discussion Enhancer

## Status Check

- **Available Polls**: ${polls.length}
- **Poll Discovery**: ${polls.length > 0 ? '✅ Objects found' : '❌ No objects found'}
- **Integration**: ✅ Ready

## Usage

1. Select discussion text
2. Run this template to automatically link relevant polls
3. Get suggestions for new polls based on discussion content

## Available Polls

${polls.length > 0 ? 
    polls.map(poll => `- ${poll.linkText}`).join('\n') :
    'No poll objects found. Use pollCreator template to create some.'
}

## How It Helps

This template solves the "no one links to poll in discussion" problem by:
- ✅ Automatically finding relevant polls
- ✅ Suggesting new polls based on discussion content  
- ✅ Adding proper links and integration
- ✅ Making polls discoverable in discussions`;
        }
        
        const result = await enhanceDiscussion(selection);
        
        return `# Discussion Enhancement Complete

## Status
- **Poll Objects**: ${result.status}
- **Total Polls Available**: ${result.totalPolls}
- **Relevant Polls**: ${result.relevantPolls}
- **New Poll Suggestions**: ${result.suggestions}

## Enhanced Discussion

${result.enhanced}

## Summary

${result.totalPolls > 0 ? 
    `✅ Successfully enhanced discussion with poll integration. Found ${result.totalPolls} total polls, ${result.relevantPolls} relevant to this discussion.` :
    '❌ No poll objects found. Create polls using the pollCreator template to enable discussion-poll linking.'
}

${result.error ? `❌ Error: ${result.error}` : ''}`;
    }

    return await processDiscussion();
```
{{/script}}
```

***
***
# Output:
{{get "script"}}
<!-- B4501B53 -->