import logging
import os
import json
from datetime import datetime
class AMQPLogger(logging.Logger):
    def info(self, msg, project_id=None, test_image_id=None, application_name=None, checkpoint_name=None, *args, **kwargs):
        #make the query here
        data = {'created_at':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'project_id': project_id,
        'test_image_id': test_image_id,'application_name': application_name,'checkpoint_name': checkpoint_name,
        'logs': json.dumps(msg)}
        query = """INSERT INTO pdlogger_logs (created_at,project_id, test_image_id, application_name, checkpoint_name, logs)
        VALUES (%s,%s, %s, %s, %s, %s);"""
        input_json = {}
        input_json['insert_query'] = query
        input_json['insert_values'] = tuple(data.values())
        super().info(self,input_json)
