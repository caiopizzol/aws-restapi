import os
import json
from psycopg2 import connect

RESPONSE = {
    'statusCode': 200,
    'headers': { 'Access-Control-Allow-Origin' : '*' },
    'body': {},
    'isBase64Encoded': False
}


## Lambda handler
def handler(event, context):
    print('event:',event)
    service_area_id = event['pathParameters']['id']
    try:
        delete_service_area(service_area_id)
        RESPONSE['body'] = json.dumps({
            'message': 'Service area id {} deleted successfully!'.format(service_area_id)
        })
    except Exception as error:
        RESPONSE['statusCode'] = 400
        RESPONSE['body'] = {
            'message': error
        }
    finally:
        print(RESPONSE)
        return RESPONSE

def delete_service_area(service_area_id):
    con = get_db_connection()
    cur = con.cursor()
    query = '''
    DELETE FROM
        providers_service_areas
    WHERE
        id = %s;
    '''
    cur.execute(query, (service_area_id,))
    con.commit()
    cur.close()
    if con is not None:
        con.close()

def get_db_connection():         
    dbname = os.environ["DBNAME"]
    dbuser = os.environ["DBUSER"]
    dbpass = os.environ["DBPASS"]
    dbhost = os.environ["DBHOST"]
    dbport = os.environ["DBPORT"]
    con = connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass)
    return con
   

# event = {
#     'id': 1
# }
# handler(event, {})
