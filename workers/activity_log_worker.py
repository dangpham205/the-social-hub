import json
from pathlib import Path
import sys

from fastapi import HTTPException
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from cores.databases.connection import get_db
from cores.rabbitmq.rpc_client import FibonacciRpcClient
from cores.rabbitmq.rpc_server import FibonacciRpcServer
from enums.workers.worker_enum import EXCHANGE_API, ACTIVITY_LOG_QUEUE, LOG_QUEUE
from repositories.services import SchoolService, SchoolAddressService, SchoolStaffService, SchoolNewsService, SchoolCategoryService, SchoolEnrollmentInformationService, SchoolInfrastructureService, SchoolPostService
from v1.di import init_di
from enums.db import table_enum
from db import Address
import datetime
init_di()
db = next(get_db())
from cores.enums import activity_log_enum
from cores.activity_logs import activity_log

def handle(ch, method, props, body):
    try:
        print(f" [.] Processing queue: {ACTIVITY_LOG_QUEUE}")
        operation = props.type
        table = props.headers['table'] if 'table' in props.headers else None
        body = body.decode()
        body = eval(body)
        activity_log.write_activity_log(**body)
        # activity_log.write_activity_log(body['current_user_id'], body['event'], body['subject'], body['subject_type'])

        print(f" [.] Reported message done to Rabbitmq")
    except Exception as e:
        print(e)
        print(f" [.] Process queue: {ACTIVITY_LOG_QUEUE} failed")
        error = str(sys.exc_info())
        FibonacciRpcClient().send_message(
            method=operation, 
            header={
                "table": table,
                "details": error
            },
            routing_key=LOG_QUEUE, 
            body=body
        )

if __name__ == '__main__':
    FibonacciRpcServer().consume_messages(ACTIVITY_LOG_QUEUE, EXCHANGE_API, ACTIVITY_LOG_QUEUE, handle)
