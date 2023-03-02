mapping = {
    "properties": {
        "id": {
            "type": "long"
        },
        "code": {
            "type": "keyword",
        },
        "name": {
            "type": "text",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            },
            "analyzer": "ngram_analyzer"
        },
        "targets": {
            "type": "long"
        },
        "phone": {
            "type": "text",
        },
        "email": {
            "type": "text",
            "analyzer": "my_standard"
        },
        "avatar": {
            "type": "keyword",
        },
        "logo": {
            "type": "keyword",
        },
        "website": {
            "type": "keyword",
        },
        "description": {
            "type": "text",
            "analyzer": "my_standard"
        },
        "seo_description": {
            "type": "text",
            "analyzer": "my_standard"
        },
        "vision": {
            "type": "text",
            "analyzer": "my_standard"
        },
        "mission": {
            "type": "text",
            "analyzer": "my_standard"
        },
        "enrollment_targets": {
            "type": "long"
        },
        "method_content": {
            "type": "keyword",
        },
        "is_outstanding": {
            "type": "boolean"
        },
        "order": {
            "type": "long"
        },
        "state": {
            "type": "keyword",
        },
    }
}
