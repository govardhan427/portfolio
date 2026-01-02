import json

# List of apps we actually care about (The core portfolio content)
KEEP_APPS = ['auth', 'core', 'blog', 'vault', 'features']

print("🧹 Cleaning data...")

with open('initial_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter: Keep only items where the 'model' starts with our safe apps
clean_data = [
    item for item in data 
    if item['model'].split('.')[0] in KEEP_APPS
]

# Write to a new file
with open('clean_data.json', 'w', encoding='utf-8') as f:
    json.dump(clean_data, f, indent=2)

print(f"✨ Done! Reduced items from {len(data)} to {len(clean_data)}")
print("✅ Created 'clean_data.json'")