# Memory System

This module handles the agent's persistent memory, preventing duplicate job applications.

## Key Functions

### `load_memory()`
Loads the agent's memory from `data/applied_jobs.json`

### `save_memory(memory)`
Saves the agent's memory to disk

### `job_already_applied(job_url)`
Check if a job has already been applied to

### `mark_job_applied(job_url)`
Mark a job as applied (prevents re-application)

### `get_applied_count()`
Get total number of jobs applied to

### `clear_memory()`
⚠️ **WARNING**: Clears all memory. Use with caution!

## Memory Structure

```json
{
  "applied_jobs": [
    "https://indeed.com/job/123",
    "https://indeed.com/job/456"
  ]
}
```

## Usage Example

```python
from memory.memory import job_already_applied, mark_job_applied

job_url = "https://indeed.com/job/123"

if not job_already_applied(job_url):
    # Apply to job
    mark_job_applied(job_url)
    print("Applied to job")
else:
    print("Already applied, skipping")
```

## Benefits

- ✅ Prevents duplicate applications
- ✅ Enables safe stop/resume
- ✅ Tracks application history
- ✅ Persists across sessions
