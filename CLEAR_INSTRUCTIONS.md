# Clear Instructions Guide

This document provides guidelines for writing clear, actionable instructions when requesting changes or providing feedback in this repository.

## What Makes Instructions Clear

### ✅ Clear Instructions Include:

1. **Specific File References**
   - Exact file paths: `Red&Queen/knowledge_system.py`
   - Line numbers when applicable: `line 202`
   - Function or class names: `RedQueenKnowledgeSystem.make_we_knowledged()`

2. **Concrete Actions**
   - "Change variable X from Y to Z"
   - "Add function that does A, B, and C"
   - "Update documentation section X with information Y"

3. **Expected Behavior**
   - What the code should do after changes
   - What output or result is expected
   - How to verify the changes work correctly

4. **Technical Specifications**
   - Data types and formats
   - Parameter names and types
   - Return values and their types

### Example of Clear Instructions:
```
In Red&Queen/rq_random_utils.py:
1. Change line 92 from `num_skip = random.randint(0, 255)` to `num_skip = random.randint(1, 4)`
2. Add a new function `getrandom(from_val, to_val)` that returns an integer using the R&Q algorithm
3. Update the module docstring to document this new function
```

## What Makes Instructions Unclear

### ❌ Unclear Instructions Contain:

1. **Vague Requests**
   - "Fix that"
   - "Make it better"
   - "Change everything"

2. **Ambiguous Language**
   - "Maybe do something with the random stuff"
   - "I think it needs work"
   - "Not really correct"

3. **Mixed or Confusing Content**
   - Multiple unrelated requests in one comment
   - Unclear pronouns without context
   - Garbled or incomplete sentences

4. **Missing Context**
   - No file names or locations
   - No explanation of what's wrong
   - No description of desired outcome

### Example of Unclear Instructions:
```
@copilot fix that stuff
the thing is not working right
change it to be better
you know what I mean
```

## How to Request Changes Effectively

### Step 1: Identify the Problem
- Which file has the issue?
- What is the current behavior?
- What is wrong with it?

### Step 2: Describe the Solution
- What should change?
- What should the new behavior be?
- Are there any constraints or requirements?

### Step 3: Provide Context
- Why is this change needed?
- How does it relate to the overall system?
- Are there dependencies or related changes?

## Template for Clear Instructions

```markdown
**File:** [path/to/file.py]
**Location:** [function name, line number, or class]

**Current Behavior:**
[What the code currently does]

**Requested Change:**
[Specific modification needed]

**Expected Result:**
[What should happen after the change]

**Additional Context:**
[Any relevant background or requirements]
```

## Examples from This Repository

### ✅ Good Example:
```
@copilot
1. create a function that accepts sensor values and uses them for entropy seeding
2. write RunOnce func
3. write getrandom(from, to) func
4. modify docs and repo's code to reflect corrected random proc
```

This is clear because:
- Lists specific functions to create
- Defines function purposes
- Mentions documentation updates

### ❌ Poor Example:
```
@copilot fix that
chang e s
NEED MACHINE'S CHANNEL - NOT TMP'S HUMAN'S INJECT I ON S
```

This is unclear because:
- No specific files or functions mentioned
- No description of what needs fixing
- Contains confusing, non-technical language

## Best Practices

1. **Be Specific**: Name exact files, functions, and line numbers
2. **Be Technical**: Use proper programming terminology
3. **Be Complete**: Provide all necessary information in one message
4. **Be Professional**: Use clear language without extraneous content
5. **Be Testable**: Explain how to verify the changes work

## Getting Help

If you're unsure how to phrase a request:
1. Identify what you want to change
2. Write down the current state
3. Write down the desired state
4. Review your message for clarity before posting

## Conclusion

Clear instructions lead to:
- Faster implementation
- Fewer misunderstandings
- Better code quality
- More efficient collaboration

Take the time to write clear, specific instructions, and you'll get better results.
