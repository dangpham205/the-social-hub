
from pathlib import Path
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
import json
from cores.elasticsearch.es_helper import ElasticSearch
from cores.rabbitmq.rpc_client import FibonacciRpcClient
from cores.rabbitmq.rpc_server import FibonacciRpcServer
from enums.workers.worker_enum import ES_QUEUE, EXCHANGE_API, LOG_QUEUE
from enums.db import table_enum

class ESWorker():
    def __init__(self, table):
        self.table = table
        
    def process_done(self, message=''):
        print(f" [.] Reported message done to Rabbitmq")

    def build_es(self, type, index_name, obj):
        if type == 'delete':
            print(f'    [O] Deleting to index {index_name} in ES, with ID={obj}')
            rs = ElasticSearch().delete_document(index_name, obj)
            print('    [O] ',rs)
        elif type == 'post' or type == 'put':
            import datetime 
            # body = obj.decode('utf-8').replace("'", '"').replace('False', 'false').replace('True', 'true').replace('None', 'null')
            body = obj.decode()

            res = eval(body)
            if index_name == table_enum.TABLE_SCHOOL_ADDRESS:
                province_file = open('../location/tinh_tp.json')
                province_data = json.load(province_file)
                district_file = open('../location/quan_huyen.json')
                district_data = json.load(district_file)
                ward_file = open('../location/xa_phuong.json')
                ward_data = json.load(ward_file)

                province_id = str(res['province_id'])
                district_id = str(res['district_id'])
                ward_id = str(res['ward_id'])
                
                if len(province_id) < 2:
                    province_id = '0' * (2- len(province_id)) + province_id
                if len(district_id) < 3:
                    district_id = '0' * (3- len(district_id)) + district_id
                if len(ward_id) < 5:
                    ward_id = '0' * (5- len(ward_id)) + ward_id

                province = province_data[province_id] if province_id in province_data else None
                district = district_data[district_id] if district_id in district_data else None
                ward = ward_data[ward_id] if ward_id in ward_data else None

                res['province_name'] = province['name'] if province else None
                res['district_name'] = district['name'] if district else None
                res['ward_name'] = ward['name'] if ward else None

            print(f'    [O] {type} to index {index_name} in ES, with ID={res["id"]}')
            rs = ElasticSearch().add_document_to_index(index_name, res)
            print('    [O] ',rs)
        else:
            rs = None
        return rs
    
    def get_index(self):
        supported_tables = [
            table_enum.TABLE_SCHOOL, 
            table_enum.TABLE_SCHOOL_ADDRESS, 
            table_enum.TABLE_SCHOOL_STAFF, 
            table_enum.TABLE_SCHOOL_INFRASTRUCTURE,
            table_enum.TABLE_SCHOOL_ENROLL_INFORMATION,
            table_enum.TABLE_SCHOOL_CATEGORY,
            table_enum.TABLE_SCHOOL_POST,
            table_enum.TABLE_SCHOOL_NEWS,
            table_enum.TABLE_SCHOOL_LINK
        ]
        if self.table in supported_tables:
            return str(self.table)
        else:
            return None
        
def handle(ch, method, props, body):
    try:
        print(f" [.] Processing queue: {ES_QUEUE}")
        operation = props.type
        table = props.headers['table'] if 'table' in props.headers else None
        worker = ESWorker(table = table)
        index = worker.get_index()
        if not index:
            print(f'    [O] Received unknown table: {table}')
            raise
        result = worker.build_es(
            type=operation,
            index_name=index,
            obj=body
        )
        worker.process_done()
    except Exception as e:
        print(f" [.] Process queue: {ES_QUEUE} failed")
        error = str(sys.exc_info())
        FibonacciRpcClient().send_message(
            method=operation, 
            header={
                "from": ES_QUEUE,
                "table": table,
                "details": error
            },
            routing_key=LOG_QUEUE, 
            body=body
        )
        
if __name__ == '__main__':
    FibonacciRpcServer().consume_messages(ES_QUEUE, EXCHANGE_API, ES_QUEUE, handle)