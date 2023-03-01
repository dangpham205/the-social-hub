import json
from pathlib import Path
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from fastapi import HTTPException, status
from cores.databases.connection import get_db
from cores.rabbitmq.rpc_client import FibonacciRpcClient
from cores.rabbitmq.rpc_server import FibonacciRpcServer
from enums.workers.worker_enum import MYSQL_QUEUE, EXCHANGE_API, ES_QUEUE, LOG_QUEUE
from repositories.services import SchoolService, SchoolAddressService, SchoolStaffService, SchoolNewsService, SchoolCategoryService, SchoolEnrollmentInformationService, SchoolInfrastructureService, SchoolPostService, SchoolLinkService
from v1.di import init_di
from enums.db import table_enum
from db import Address, Link
import datetime
from cores.activity_logs import activity_log
from cores.enums import activity_log_enum
from workers.crawler import LinkCrawler
init_di()
db = next(get_db())

class MySQLWorker():
    def __init__(self, table):
        self.table = table
    
    def process_done(self, message=''):
        print(f" [.] Reported message done to Rabbitmq")

    def get_service(self):
        if self.table == table_enum.TABLE_SCHOOL:
            return SchoolService()
        elif self.table == table_enum.TABLE_SCHOOL_ADDRESS:
            return SchoolAddressService()
        elif self.table == table_enum.TABLE_SCHOOL_STAFF:
            return SchoolStaffService()
        elif self.table == table_enum.TABLE_SCHOOL_ENROLL_INFORMATION:
            return SchoolEnrollmentInformationService()
        elif self.table == table_enum.TABLE_SCHOOL_INFRASTRUCTURE:
            return SchoolInfrastructureService()
        elif self.table == table_enum.TABLE_SCHOOL_CATEGORY:
            return SchoolCategoryService()
        elif self.table == table_enum.TABLE_SCHOOL_POST:
            return SchoolPostService()
        elif self.table == table_enum.TABLE_SCHOOL_NEWS:
            return SchoolNewsService() 
        elif self.table == table_enum.TABLE_SCHOOL_LINK:
            return SchoolLinkService() 
        else:
            return None

    def to_ES_message_queue(self, method, body):
        FibonacciRpcClient().send_message(
            method=method, 
            header={
                "table": self.table
            },
            routing_key=ES_QUEUE, 
            body=body
        )
        
def handle(ch, method, props, body):
    try:
        obj = event = None
        print(f" [.] Processing queue: {MYSQL_QUEUE}")
        operation = props.type
        table = props.headers['table'] if 'table' in props.headers else None
        current_user_id = None
        if 'request_state' in props.headers:
            request_state = props.headers['request_state']['_state']
            if 'current_user_id' in request_state:
                current_user_id = request_state['current_user_id']

        worker = MySQLWorker(table = table)
        service = worker.get_service()
        if not service:
            print(f'    [O] Received unknown table: {table}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unknow table: {table}")
        if operation == 'post':
            print(f'    [O] Writing to table {table} in DB')
            body = body.decode('utf-8')
            # body = body.decode('utf-8').replace("'", '"').replace('False', 'false').replace('True', 'true').replace('None', 'null')
            # thay các datetime format thành string format
            body = eval(body)
            for key, value in body.items():
                if isinstance(value, datetime.datetime):
                    body[key] = value.isoformat()
            body = str(body)
            body = body.replace("'", '"').replace('False', 'false').replace('True', 'true').replace('None', 'null')
            body = json.loads(body)
            
            if table == table_enum.TABLE_SCHOOL_ADDRESS:
                # điều kiện để write address: mỗi trường chỉ có 1 dịa chỉ chính (is_default = True)
                df_address = db.query(Address).filter(
                    Address.school_id == body['school_id'], Address.is_default == True, Address.deleted_at == None).first()
                if df_address and body['is_default'] == True:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"School {body['school_id']} already have a default address")
            if table == table_enum.TABLE_SCHOOL_LINK:
                additional_data = LinkCrawler(url=body['link']).get_info()
                if not additional_data['type'] or not additional_data['thumb'] or not additional_data['title']:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Can't get thumb and type from {body['link']}")
                else:
                    body['type'] = additional_data['type']
                    body['thumb'] = additional_data['thumb']
                    body['title'] = additional_data['title']
                    
            result = service.repo.create(db, body)
            if result:
                print('    [O] Succeed, Sending message to ES')
                obj = dict(result.__dict__)
                del obj['_sa_instance_state']
                worker.to_ES_message_queue(method=operation, body=obj)
                event = activity_log_enum.EVENT_CREATED
        if operation == 'put':
            body = body.decode('utf-8').replace("'", '"').replace('False', 'false').replace('True', 'true').replace('None', 'null')
            body = json.loads(body)
            if table == table_enum.TABLE_SCHOOL_ADDRESS:
                # điều kiện để write address: mỗi trường chỉ có 1 dịa chỉ chính (is_default = True)
                df_address = db.query(Address).filter(
                    Address.school_id == body['school_id'], Address.is_default == True , Address.deleted_at == None).first()
                if df_address and body['is_default'] == True and df_address.id != body['id']:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"School {body['school_id']} already have a default address")
            if table == table_enum.TABLE_SCHOOL_LINK:
                additional_data = LinkCrawler(url=body['link']).get_info()
                if not additional_data['type'] or not additional_data['thumb'] or not additional_data['title']:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Can't get thumb and type from {body['link']}")
                else:
                    body['type'] = additional_data['type']
                    body['thumb'] = additional_data['thumb']
                    body['title'] = additional_data['title']
                    
            print(f'    [O] Updating to table {table} in DB, row with ID={body["id"]}')
            result = service.repo.update(db, body['id'], body)
            if result:
                print('    [O] Succeed, Send message to ES')
                obj = dict(result.__dict__)
                del obj['_sa_instance_state']
                worker.to_ES_message_queue(method=operation, body=obj)
                event = activity_log_enum.EVENT_UPDATED
        if operation == 'delete':
            print(f'    [O] Deleting to table {table} in DB, row with ID={body}')
            body = int(body)
            result = service.repo.delete(db, body)
            if result:
                obj = {
                    'id': body
                }
                print('    [O] Succeed, Send message to ES')
                worker.to_ES_message_queue(method=operation, body=int(result.id))
                event = activity_log_enum.EVENT_DELETED
        if event and obj:
            activity_log.send_queue_to_write_activity_log(current_user_id, event, obj, table)

        worker.process_done()
    except Exception as e:
        print(f" [.] Process queue: {MYSQL_QUEUE} failed")
        error = str(sys.exc_info())
        FibonacciRpcClient().send_message(
            method=operation, 
            header={
                "from": MYSQL_QUEUE,
                "table": table,
                "details": error
            },
            routing_key=LOG_QUEUE, 
            body=body
        )

if __name__ == '__main__':
    FibonacciRpcServer().consume_messages(MYSQL_QUEUE, EXCHANGE_API, MYSQL_QUEUE, handle)
