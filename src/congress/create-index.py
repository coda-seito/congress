from elasticsearch import Elasticsearch

# Elasticsearch client
client = Elasticsearch(['https://elastic:iloveoranges@localhost:9200'], verify_certs=False)

# Index name
index_name = "congress-full"

# Mapping for the index
mapping = {
    "mappings": {
        "properties": {
            "date": {"type": "date"},
            "content": {"type": "text"},
            "document_id":{"type": "keyword"}
        }
    }
}

# Create the index with the specified mapping
response = client.indices.create(index=index_name, body=mapping)

# Check if the index creation was successful
if response["acknowledged"]:
    print(f"Index '{index_name}' with mapping created successfully.")
else:
    print("Failed to create index.")