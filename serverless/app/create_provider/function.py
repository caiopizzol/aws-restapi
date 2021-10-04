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
    body = json.loads(event['body'])
    try:
        RESPONSE['body'] = json.dumps({
            'message': 'Provider successfully created with id {}!'.format(create_provider(body))
        })
    except Exception as error:
        RESPONSE['statusCode'] = 400
        RESPONSE['body'] = json.dumps({
            'message': error
        })
    finally:
        print(RESPONSE)
        return RESPONSE

def create_provider(body):
    con = get_db_connection()
    cur = con.cursor()
    query = '''
    INSERT INTO
        providers ({})
    VALUES 
        {}
    RETURNING id;
    '''.format(
        ', '.join(body.keys()),
        tuple(list(body.values()))
    )
    cur.execute(query)
    provider_id = cur.fetchone()[0]
    con.commit()      
    cur.close()
    if con is not None:
        con.close()
    return provider_id

def get_db_connection():         
    dbname = os.environ["DBNAME"]
    dbuser = os.environ["DBUSER"]
    dbpass = os.environ["DBPASS"]
    dbhost = os.environ["DBHOST"]
    dbport = os.environ["DBPORT"]
    con = connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass, port=dbport)
    return con  

# event = {
#     'name': 'Transport ABC',
#     'email': 'contact@transportabc.com',
#     'phone': '+5541996749101',
#     'language_id': 5,
#     'currency_id': 4
# }
# handler(event, {})
