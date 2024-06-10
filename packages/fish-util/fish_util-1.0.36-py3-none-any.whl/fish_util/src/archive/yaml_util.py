import yaml

with open('data/example.yaml', 'r') as f:
    doc = yaml.safe_load(f)
    name=doc['name']
    count=doc['count']
    print(f"name: {name}")
    print(f"count: {count}")
    doc["link"]="https://www.fishyer.com"
    yaml.dump(doc, open('data/example.yaml', 'w'))