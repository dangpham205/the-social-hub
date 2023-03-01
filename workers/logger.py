from pathlib import Path
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
import logging
from cores.rabbitmq.rpc_server import FibonacciRpcServer
from enums.workers.worker_enum import EXCHANGE_API, LOG_QUEUE, ES_QUEUE, MYSQL_QUEUE


class Logger():
    def __init__(self, logger_name= 'error_logger'):
        self.logger_name = logger_name
    
    def get_logger(self, for_queue):
        if for_queue == MYSQL_QUEUE:
            file_name = "workers/sql_err_log.txt"
        if for_queue == ES_QUEUE:
            file_name = "workers/es_err_log.txt"
        
        logging.basicConfig(
            filename=file_name,
            filemode="a",
            format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
            level=logging.INFO,
        )
        self.stderrLogger = logging.StreamHandler()
        logging.getLogger().addHandler(self.stderrLogger)
        self.logger = logging.getLogger(self.logger_name)
        return self.logger
     
    def done(self):
        print('     [O] Done')
    
def handle(ch, method, props, body):
    try:
        print(f" [.] Processing queue: {LOG_QUEUE}")
        from_queue = props.headers['from'] if 'from' in props.headers else None
        table = props.headers['table'] if 'table' in props.headers else None
        operation = props.type
        body = body.decode()
        body = eval(body)
        details = props.headers['details'] if 'details' in props.headers else None

        logger = Logger().get_logger( for_queue= from_queue)
        logger.error({
            "from": from_queue,
            "table": table,
            "operation": operation,
            "body": body,
            "details": details
        })
        
    except Exception as e:
        print('-'*50)
        print(e)
        error = str(sys.exc_info())
        print(error)
        print('-'*50)

if __name__ == '__main__':
    FibonacciRpcServer().consume_messages(LOG_QUEUE, EXCHANGE_API, LOG_QUEUE, handle)