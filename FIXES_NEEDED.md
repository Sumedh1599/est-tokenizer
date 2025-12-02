# Fixes Needed for Context Preservation

## Current Issues:
1. ✅ Token reduction working (37.5% - 80%)
2. ❌ Context preservation failing (0%)
3. ❌ Words being lost during phrase matching

## Root Cause:
- Phrase matching is consuming words but not preserving all of them
- When "quick fox" matches to "lomawakaH" (just fox), "quick" is lost
- Single word matching threshold (10%) is correct, but words aren't being processed individually when phrases fail

## Solution Needed:
1. Ensure phrase matching only accepts if score is high enough to preserve meaning
2. Fall back to individual word matching for all words in a failed phrase
3. Process all words sequentially, ensuring none are skipped
4. Improve decoder to reconstruct context from Sanskrit tokens

## Status:
- Lowered thresholds ✅
- Disabled semantic chunking for short sentences ✅
- Need to fix phrase matching to not consume words incorrectly ⚠️

