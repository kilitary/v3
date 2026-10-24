---
promptId: pollLinker
name: 🔗 Poll Linker
description: Enhances discussions by automatically finding and linking relevant polls. Integrates with conceptLinker to solve the "no objects found" issue.
author: Copilot
version: 0.1.0
disableProvider: true
type: wrapper
commands:
  - generate
---

# Poll Linker Template

This template enhances the conceptLinker system to automatically find and link poll objects in discussions.

```handlebars
{{#script}}
```js
    // Enhanced poll discovery and linking system
    async function findPollObjects() {
        const polls = [];
        
        try {
            // Check if polls directory exists
            const pollsDir = 'polls';
            if (await app.vault.adapter.exists(pollsDir)) {
                const pollFiles = await app.vault.adapter.list(pollsDir);
                
                for (const file of pollFiles.files) {
                    if (file.endsWith('.md') && !file.endsWith('polls-index.md')) {
                        try {
                            const content = await app.vault.adapter.read(file);
                            const poll = parsePollFromContent(content, file);
                            if (poll) {
                                polls.push(poll);
                            }
                        } catch (error) {
                            console.warn(`Could not read poll file ${file}:`, error);
                        }
                    }
                }
            }
            
            // Also search for polls in current directory
            const currentFile = app.workspace.getActiveFile();
            if (currentFile?.parent) {
                const currentDir = currentFile.parent.path;
                const localPollsDir = `${currentDir}/polls`;
                
                if (await app.vault.adapter.exists(localPollsDir)) {
                    const localPollFiles = await app.vault.adapter.list(localPollsDir);
                    
                    for (const file of localPollFiles.files) {
                        if (file.endsWith('.md') && !file.endsWith('polls-index.md')) {
                            try {
                                const content = await app.vault.adapter.read(file);
                                const poll = parsePollFromContent(content, file);
                                if (poll) {
                                    polls.push(poll);
                                }
                            } catch (error) {
                                console.warn(`Could not read local poll file ${file}:`, error);
                            }
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error finding poll objects:', error);
        }
        
        return polls;
    }

    function parsePollFromContent(content, filePath) {
        try {
            // Extract frontmatter
            const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
            if (!frontmatterMatch) return null;
            
            const frontmatter = frontmatterMatch[1];
            const pollIdMatch = frontmatter.match(/pollId:\s*(.+)/);
            const titleMatch = frontmatter.match(/title:\s*(.+)/);
            const typeMatch = frontmatter.match(/type:\s*(.+)/);
            
            if (!pollIdMatch || typeMatch?.[1] !== 'poll') return null;
            
            const pollId = pollIdMatch[1].trim();
            const title = titleMatch?.[1]?.trim() || pollId;
            
            // Extract description from content
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
            console.warn('Error parsing poll content:', error);
            return null;
        }
    }

    async function findRelevantPolls(text, polls) {
        const relevantPolls = [];
        const words = text.toLowerCase().split(/\s+/);
        
        for (const poll of polls) {
            const pollWords = (poll.title + ' ' + poll.description).toLowerCase().split(/\s+/);
            
            // Calculate relevance score
            let score = 0;
            for (const word of words) {
                if (word.length > 3) { // Skip short words
                    for (const pollWord of pollWords) {
                        if (pollWord.includes(word) || word.includes(pollWord)) {
                            score++;
                        }
                    }
                }
            }
            
            // Check for specific poll-related keywords
            const pollKeywords = ['vote', 'poll', 'survey', 'opinion', 'decide', 'choice', 'select'];
            for (const keyword of pollKeywords) {
                if (text.toLowerCase().includes(keyword)) {
                    score += 2;
                }
            }
            
            if (score > 0) {
                relevantPolls.push({
                    ...poll,
                    relevanceScore: score
                });
            }
        }
        
        // Sort by relevance score
        return relevantPolls.sort((a, b) => b.relevanceScore - a.relevanceScore);
    }

    async function enhanceTextWithPollLinks(text) {
        const polls = await findPollObjects();
        
        if (polls.length === 0) {
            return {
                enhancedText: text,
                foundPolls: [],
                message: "No poll objects found. Create polls using the pollCreator template."
            };
        }
        
        const relevantPolls = await findRelevantPolls(text, polls);
        
        if (relevantPolls.length === 0) {
            return {
                enhancedText: text,
                foundPolls: polls,
                message: `Found ${polls.length} poll(s) but none are relevant to this discussion.`
            };
        }
        
        // Add poll links section to the text
        const pollLinksSection = `

## 📊 Related Polls

${relevantPolls.map(poll => 
    `- ${poll.linkText} - ${poll.description}`
).join('\n')}

---
*Auto-linked polls based on discussion content*`;

        return {
            enhancedText: text + pollLinksSection,
            foundPolls: polls,
            relevantPolls: relevantPolls,
            message: `Enhanced discussion with ${relevantPolls.length} relevant poll link(s).`
        };
    }

    // Main execution
    async function processPollLinking() {
        const selection = `{{tg_selection}}`.trim();
        
        if (!selection) {
            const polls = await findPollObjects();
            
            return `# Poll Linker

## Available Poll Objects

${polls.length > 0 ? 
    polls.map(poll => `- ${poll.linkText} - ${poll.description}`).join('\n') :
    'No poll objects found. Create some using the pollCreator template.'
}

## Usage

Select text from a discussion and run this template to automatically find and link relevant polls.

## Status

- **Total Polls Found**: ${polls.length}
- **Poll Discovery**: ${polls.length > 0 ? '✅ Working' : '❌ No objects found'}
- **Linking System**: ✅ Active`;
        }
        
        const result = await enhanceTextWithPollLinks(selection);
        
        return `# Poll Linking Results

${result.message}

## Enhanced Text

${result.enhancedText}

## Discovery Summary

- **Total Polls Available**: ${result.foundPolls.length}
- **Relevant Polls Found**: ${result.relevantPolls?.length || 0}
- **Status**: ${result.foundPolls.length > 0 ? '✅ Objects found and linking working' : '❌ No objects found - create polls first'}

${result.relevantPolls?.length > 0 ? `
## Linked Polls Details

${result.relevantPolls.map(poll => 
    `### ${poll.title}
- **ID**: \`${poll.id}\`
- **Relevance Score**: ${poll.relevanceScore}
- **Link**: ${poll.linkText}
- **Description**: ${poll.description}`
).join('\n\n')}` : ''}`;
    }

    return await processPollLinking();
```
{{/script}}
```

***
***
# Output:
{{get "script"}}
<!-- 04B8943C -->