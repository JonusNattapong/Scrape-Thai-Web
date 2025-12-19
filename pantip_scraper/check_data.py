import json

# Load all data from JSONL file
topics = []
with open('data/pantip_dataset.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            topics.append(json.loads(line.strip()))

print(f"Total topics scraped: {len(topics)}")
print()

# Print each topic
for i, data in enumerate(topics, 1):
    print(f"Topic {i}:")
    print(f"  Title: {data['title']}")
    print(f"  Comments: {len(data['comments'])}")
    print(f"  URL: https://pantip.com/topic/{data['topic_id']}")
    
    # Print first 2 comments
    print("  First 2 comments:")
    for j, comment in enumerate(data['comments'][:2]):
        print(f"    - {comment}")
    print()