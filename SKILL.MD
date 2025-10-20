---
name: meeting_to_tasks_converter
description: Transforms meeting transcripts and notes into a structured, tab-separated CSV of tasks with assignees, deadlines, and priorities for easy import into project management tools.
metadata:
  version: 1.1.0
  author: Homemade Meals Team
  dependencies: python>=3.8, pandas>=2.0.0
---

# Meeting to Tasks Converter

This skill transforms meeting transcripts, standup notes, and team discussions into structured, tab-separated CSV files.

## When to Use This Skill
This skill should be used when a user provides meeting notes or a transcript and asks to extract action items or create a task list.

## How It Works
The skill uses a Python script to analyze the text and extract key details for each task.

### Step 1: Execute the Python Script
Run the `scripts/converter.py` script, passing the full meeting transcript as an argument. The script will handle the logic of identifying tasks, assignees, priorities, and deadlines.

**Usage:**
```bash
python scripts/converter.py "<full_meeting_transcript_text>"
