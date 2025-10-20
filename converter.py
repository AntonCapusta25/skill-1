---

### 2. The Python Script

This script contains the logic to parse the meeting notes and convert them into a structured CSV format. Create a `scripts` subfolder and save this file inside it.

#### 📁 `scripts/converter.py`
```python
import pandas as pd
import re
import sys
from datetime import date, timedelta

# --- MAPPING USER NAMES TO EMAILS ---
# For the script to assign tasks correctly, add the names and emails of your team members here.
USER_EMAIL_MAP = {
    "nash": "nash@example.com",
    "menna": "mennatyehiaz@gmail.com",
    "tia": "tiayahyaa@gmail.com",
    "alex": "apersaud878@gmail.com",
    "alexandr": "bangalexf@gmail.com"
}

def parse_meeting_notes(text):
    """Analyzes text to extract tasks, assignees, and other details."""
    tasks = []
    
    # Split text into sentences for individual analysis
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    for sentence in sentences:
        if not sentence.strip():
            continue

        # --- Rule-based Information Extraction ---
        title = sentence.strip()
        description = f"Task identified from the statement: \"{title}\""
        status = "todo"
        
        # Priority Detection
        if re.search(r'\basap\b|urgent|immediately', sentence, re.IGNORECASE):
            priority = "high"
        elif "this week" in sentence.lower():
            priority = "medium"
        else:
            priority = "medium" # Default

        # Due Date Inference
        today = date.today()
        if "today" in sentence.lower() or "end of day" in sentence.lower():
            due_date = today.strftime("%Y-%m-%d")
        elif "this week" in sentence.lower():
            due_date = (today + timedelta(days=4-today.weekday())).strftime("%Y-%m-%d") # End of this week (Friday)
        elif "next week" in sentence.lower():
            due_date = (today + timedelta(weeks=1, days=4-today.weekday())).strftime("%Y-%m-%d")
        else:
            due_date = (today + timedelta(days=1)).strftime("%Y-%m-%d") # Default to tomorrow for high priority

        # Assignee Extraction
        assignees = []
        for name, email in USER_EMAIL_MAP.items():
            if re.search(r'\b' + name + r'\b', sentence, re.IGNORECASE):
                assignees.append(email)
        
        # Simple Tagging Logic
        tags = set()
        if "launch" in sentence.lower(): tags.add("launch")
        if "website" in sentence.lower(): tags.add("website")
        if "social media" in sentence.lower() or "reels" in sentence.lower(): tags.add("social-media")
        if "email" in sentence.lower() or "campaign" in sentence.lower(): tags.add("marketing")
        if priority == "high": tags.add("urgent")

        # Only create a task if an assignee is found
        if assignees:
            tasks.append({
                "Title": title,
                "Description": description,
                "Status": status,
                "Priority": priority,
                "Due Date": due_date,
                "Assignees (emails)": ";".join(assignees),
                "Tags": ";".join(list(tags)) if tags else ""
            })

    return tasks

def main():
    """Main function to run the script from the command line."""
    if len(sys.argv) < 2:
        print("Usage: python converter.py \"<meeting_transcript>\"")
        return

    transcript = sys.argv[1]
    tasks = parse_meeting_notes(transcript)

    if not tasks:
        print("No actionable tasks with clear assignees were identified.")
        return

    # Create a DataFrame and convert to tab-separated CSV string
    df = pd.DataFrame(tasks)
    csv_output = df.to_csv(sep='\t', index=False)
    
    print(csv_output)

if __name__ == "__main__":
    main()
