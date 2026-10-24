---
promptId: pollCreator
name: 📊 Poll Creator
description: Creates interactive polls that can be linked to in discussions. Automatically registers poll objects for cross-referencing.
author: Copilot
version: 0.1.0
disableProvider: true
type: wrapper
commands:
  - generate
---

# Poll Creator Template

This template creates interactive polls that can be linked to from discussions and automatically registers them in the knowledge graph.

```handlebars
{{#script}}
```js
    // Poll creation and registration system
    async function createPoll(title, description, options, settings = {}) {
        const pollId = `poll-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        const timestamp = new Date().toISOString();
        
        const poll = {
            id: pollId,
            title: title,
            description: description,
            options: options.map((option, index) => ({
                id: index,
                text: option,
                votes: 0
            })),
            createdAt: timestamp,
            isActive: true,
            settings: {
                allowMultipleVotes: settings.allowMultipleVotes || false,
                showResults: settings.showResults !== false,
                anonymous: settings.anonymous !== false,
                ...settings
            }
        };

        // Create poll file
        const pollFilePath = `polls/${pollId}.md`;
        const currentFolder = app.workspace.getActiveFile()?.parent?.path || '';
        const fullPollPath = currentFolder ? `${currentFolder}/${pollFilePath}` : pollFilePath;
        
        // Ensure polls directory exists
        const pollsDir = currentFolder ? `${currentFolder}/polls` : 'polls';
        if (!await app.vault.adapter.exists(pollsDir)) {
            await app.vault.createFolder(pollsDir);
        }

        const pollContent = generatePollMarkdown(poll);
        
        try {
            await app.vault.create(fullPollPath, pollContent);
            
            // Register poll in the conceptLinker system
            await registerPollObject(poll, fullPollPath);
            
            return {
                success: true,
                pollId: pollId,
                path: fullPollPath,
                linkText: `[[${pollId}|${title}]]`
            };
        } catch (error) {
            console.error('Failed to create poll:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    function generatePollMarkdown(poll) {
        const optionsHtml = poll.options.map(option => 
            `- [ ] ${option.text} (${option.votes} votes)`
        ).join('\n');

        return `---
title: ${poll.title}
type: poll
pollId: ${poll.id}
createdAt: ${poll.createdAt}
isActive: ${poll.isActive}
tags: [poll, discussion, voting]
---

# 📊 ${poll.title}

${poll.description}

## Options

${optionsHtml}

## Poll Information

- **Poll ID**: \`${poll.id}\`
- **Created**: ${poll.createdAt}
- **Status**: ${poll.isActive ? 'Active' : 'Closed'}
- **Multiple Votes**: ${poll.settings.allowMultipleVotes ? 'Allowed' : 'Not Allowed'}
- **Anonymous**: ${poll.settings.anonymous ? 'Yes' : 'No'}

## How to Vote

1. Check the box next to your preferred option(s)
2. Save the file to record your vote
3. Results are ${poll.settings.showResults ? 'visible to all' : 'hidden until poll closes'}

---
*This is an interactive poll. You can link to it using: \`[[${poll.id}]]\`*
`;
    }

    async function registerPollObject(poll, filePath) {
        try {
            // Register in a polls index file for easy discovery
            const pollsIndexPath = 'polls/polls-index.md';
            
            let indexContent = '';
            if (await app.vault.adapter.exists(pollsIndexPath)) {
                indexContent = await app.vault.adapter.read(pollsIndexPath);
            } else {
                indexContent = `---
title: Polls Index
type: poll-index
tags: [polls, index]
---

# 📊 Polls Index

This file tracks all polls for easy linking and discovery.

## Active Polls

`;
            }

            // Add poll entry to index
            const pollEntry = `- [[${poll.id}|${poll.title}]] - Created: ${poll.createdAt}\n`;
            
            if (indexContent.includes('## Active Polls')) {
                indexContent = indexContent.replace(
                    '## Active Polls\n',
                    `## Active Polls\n\n${pollEntry}`
                );
            } else {
                indexContent += `\n${pollEntry}`;
            }

            await app.vault.adapter.write(pollsIndexPath, indexContent);
            
            return true;
        } catch (error) {
            console.error('Failed to register poll object:', error);
            return false;
        }
    }

    // Parse input from the selection or prompt
    async function parsePollInput(input) {
        const lines = input.split('\n').map(line => line.trim()).filter(line => line.length > 0);
        
        if (lines.length < 3) {
            throw new Error('Poll must have at least a title, description, and two options');
        }

        const title = lines[0].replace(/^#+\s*/, ''); // Remove markdown headers
        const description = lines[1];
        const options = lines.slice(2);

        return { title, description, options };
    }

    // Main execution
    async function generatePoll() {
        try {
            const selection = `{{tg_selection}}`.trim();
            
            if (!selection) {
                return `# Poll Creator

Please provide poll information in the following format:

Poll Title
Poll description explaining what this poll is about
Option 1
Option 2
Option 3
...

Then run this template again with your poll information selected.`;
            }

            const { title, description, options } = await parsePollInput(selection);
            const result = await createPoll(title, description, options);

            if (result.success) {
                return `# Poll Created Successfully! 

**Poll ID**: \`${result.pollId}\`
**File**: ${result.path}
**Link**: ${result.linkText}

Your poll has been created and is now available for linking in discussions. 

## Quick Actions

- View poll: [[${result.pollId}]]
- Copy link: \`[[${result.pollId}|${title}]]\`
- View all polls: [[polls-index]]

The poll has been automatically registered in the knowledge graph and can be discovered by the conceptLinker system.`;
            } else {
                return `# Poll Creation Failed

Error: ${result.error}

Please check your input format and try again.`;
            }

        } catch (error) {
            return `# Error Creating Poll

${error.message}

## Expected Format:

Poll Title
Poll description
Option 1
Option 2
Option 3`;
        }
    }

    return await generatePoll();
```
{{/script}}
```

***
***
# Output:
{{get "script"}}
<!-- 40A640EB -->