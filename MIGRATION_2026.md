# Migration to Modern OpenAI API (September 2026)

## What Changed

The OpenAI Assistants API was **sunset on August 26, 2026**. The application has been migrated to use the modern **Chat Completions API** instead.

## Breaking Changes

### Before (Assistants API - DEPRECATED)
```python
# Required an Assistant ID
assistant_id = st.secrets["ASSISTANT_ID"]

# Created threads and runs
thread = client.beta.threads.create()
client.beta.threads.messages.create(thread_id=thread.id, ...)
run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)
```

### After (Chat Completions API - CURRENT)
```python
# No Assistant ID needed
# Direct conversation with the model
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a Cigna assistant..."},
        {"role": "user", "content": "What is my coverage?"},
        {"role": "assistant", "content": "Your coverage includes..."}
    ]
)
```

## What You Need to Do

### ✅ Already Done in This Migration
- Removed `ASSISTANT_ID` from configuration
- Replaced Assistants API calls with Chat Completions API
- Simplified conversation flow
- Maintained conversation history in session state
- Kept all original features (video generation, UI, etc.)

### ⚠️ What You Need to Update

**No action required** - the app works out of the box! However:

1. **System Prompt**: The assistant behavior is now defined in code (line ~107 in app7.py). You can customize it:
   ```python
   system_message = {
       "role": "system",
       "content": """You are a helpful assistant for Cigna Health Insurance..."""
   }
   ```

2. **Model Selection**: Currently using `gpt-3.5-turbo`. You can upgrade to `gpt-4` if you have access:
   ```python
   model="gpt-4"  # More capable but more expensive
   ```

3. **Knowledge Base**: The old Assistants API allowed file uploads. With Chat Completions:
   - **Option A**: Embed knowledge in the system prompt (for small documents)
   - **Option B**: Use RAG (Retrieval Augmented Generation) with a vector database
   - **Option C**: Use OpenAI's File Search feature (if re-enabled in the future)

## Features Comparison

| Feature | Old (Assistants) | New (Chat Completions) | Status |
|---------|------------------|------------------------|--------|
| Basic Q&A | ✅ | ✅ | Working |
| Conversation context | ✅ | ✅ | Working |
| Video generation | ✅ | ✅ | Working |
| File citations | ✅ | ❌ | Removed (API limitation) |
| Document knowledge | ✅ | ⚠️ | Requires RAG setup |

## Cost Implications

Chat Completions API pricing (as of Sept 2026):
- **gpt-3.5-turbo**: ~$0.0015 per 1K tokens (input) + $0.002 per 1K tokens (output)
- **gpt-4**: ~$0.03 per 1K tokens (input) + $0.06 per 1K tokens (output)

A typical conversation turn costs:
- With gpt-3.5-turbo: ~$0.01 per message
- With gpt-4: ~$0.20 per message

## Future Enhancements

To restore document-based knowledge (like the old Cigna Healthguard Brochure PDF):

### Option 1: Simple - Embed in Prompt
For small documents, paste the content directly into the system message:
```python
system_content = f"""You are a Cigna assistant.

Here is the Cigna Healthguard documentation:
{document_text}

Answer questions based on this information."""
```

### Option 2: Advanced - RAG Pipeline
1. Use a vector database (Pinecone, Weaviate, ChromaDB)
2. Embed document chunks with OpenAI embeddings
3. Retrieve relevant chunks on each query
4. Include them in the context

### Option 3: File Search (if available)
Monitor OpenAI docs for re-release of file search capabilities in Chat Completions.

## Testing the Migration

1. Restart Streamlit: `streamlit run app7.py`
2. Ask: "What does Cigna Healthguard cover?"
3. Expected: General insurance answer (not document-specific until RAG is added)
4. Verify conversation context persists across multiple messages
5. Check video generation still works

## Rollback Plan

If you need the old Assistants API behavior and have an existing Assistant:

1. Check out git commit before this migration
2. Ensure your Assistant ID is still valid
3. Use an older OpenAI SDK: `pip install openai==1.14.3`
4. Note: Assistants API will eventually stop working entirely

## Questions?

- OpenAI Migration Guide: https://platform.openai.com/docs/assistants/migration
- Chat Completions Docs: https://platform.openai.com/docs/guides/chat
- Support: Check QUICKSTART.md and README.md

---

**Migration Date**: September 12, 2026  
**Migrated By**: Automated Migration Script  
**OpenAI SDK Version**: Compatible with openai>=1.0.0
