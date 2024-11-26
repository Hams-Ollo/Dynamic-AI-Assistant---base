import os
from pathlib import Path

# Define the directories to create
directories = [
    'data/memory',
    'data/vector_store',
    'logs/feedback'
]

# Create each directory
for dir_path in directories:
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    print(f"Created directory: {dir_path}")
