# from opensearchpy import OpenSearch
from decouple import config
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, RequestError
import warnings
warnings.filterwarnings('ignore')
class ElasticSearch:
    def __init__(self):
        self.host = config('ELASTICSEARCH_HOST')
        self.port = config('ELASTICSEARCH_PORT')
        self.client = Elasticsearch([f"{self.host}:{self.port}"])

    def search(self, index_name, query):
        rs = self.client.search(
            body=query,
            index=index_name
        )

    def paginate(self, index_name, query, page=1, page_size=15, sort_by='id', order='desc'):
        offset = 0
        if page != 1 and page_size != 0:
            offset = (page - 1) * page_size

        try:
            body = {
                "from": offset,
                "size": page_size,
                "sort": [{sort_by: order}]
            }
            if query:
                body['query'] = query
            rs = self.client.search(
                body=body,
                index=index_name,
            )
        except RequestError as e: # TH field đó khổng thể sort/ mapping chưa có field đó
            try:
                body = {
                    # "query": query,
                    "from": offset,
                    "size": page_size,
                    "sort": [{f'{sort_by}.keyword': order}]
                }
                if query:
                    body["query"] = query
                rs = self.client.search(
                    body=body,
                    index=index_name,
                )
            except:
                return {
                    'data': [],
                    'metadata': {
                        "current_page": 0,
                        "page_size": 0,
                        "total_items": 0,
                        "total_page": 0
                    }   
                }
        data = []
        for item in rs['hits']['hits']:
            data.append(item['_source'])
        # data = rs
        total = rs['hits']['total']['value']
        total_page = int((total + page_size - 1) / page_size)
        metadata = {
            "current_page": page,
            "page_size": page_size,
            "total_items": total,
            "total_page": total_page
        }
        response = dict()
        response['data'] = data
        response['metadata'] = metadata
        return response

    def get_a_document(self, index_name, id):
        return self.client.get(index=index_name, id=id, ignore=[404])

    def create_index(self, index_name, index_body=None):
        # if not settings:
        #     settings = {
        #         'index': {
        #             'number_of_shards': 4
        #         }
        #     }
        #
        # index_body = {
        #     'settings': settings
        # }

        response = self.client.indices.create(index_name, body=index_body)
        return response

    def delete_index(self, index_name):
        return self.client.indices.delete(
            index=index_name
        )

    def add_document_to_index(self, index_name, document):
        return self.client.index(
            index=index_name,
            body=document,
            id=document['id'],
            refresh=True
        )

    def update_a_document(self, index_name, id, document):
        return self.client.update(
            index=index_name,
            body=document,
            id=id,
            refresh=True
        )

    def delete_document(self, index_name, id):
        return self.client.delete(
            index=index_name,
            id=id
        )
# # Successful response!
# # {'name': 'instance-0000000000', 'cluster_name': ...}
