# create_index.py

from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

index_name = "research_papers"

index_mapping = {
    "settings": {"number_of_shards": 1, "number_of_replicas": 0},
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "abstract": {"type": "text"},
            "content": {"type": "text"},
            "authors": {"type": "text"},
            "publication_date": {"type": "date"}
        }
    }
}

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_mapping)
    print(f"Index '{index_name}' created successfully.")
else:
    print(f"Index '{index_name}' already exists.")