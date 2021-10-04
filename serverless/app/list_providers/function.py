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
    try:
        RESPONSE['body'] = json.dumps({
            'message': 'Providers list successfully retrieved!',
            'data': list_providers()
        })
    except Exception as error:
        RESPONSE['statusCode'] = 400
        RESPONSE['body'] = json.dumps({
            'message': error
        })
    finally:
        print(RESPONSE)
        return RESPONSE

def list_providers():
    con = get_db_connection()
    cur = con.cursor()
    query = '''
    SELECT
        json_build_object(
            'name', providers.name,
            'email', providers.email,
            'phone', providers.phone,
            'language_code', languages.code,
            'language', languages.language,
            'currency_code', currencies.code,
            'currency', currencies.currency
        )
    FROM 
        providers
    JOIN 
        languages
        ON providers.language_id = languages.id
    JOIN
        currencies
        ON providers.currency_id = currencies.id;
    '''
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    if con is not None:
        con.close()
    return list(list(zip(*result))[0])
    
def get_db_connection():         
    dbname = os.environ["DBNAME"]
    dbuser = os.environ["DBUSER"]
    dbpass = os.environ["DBPASS"]
    dbhost = os.environ["DBHOST"]
    dbport = os.environ["DBPORT"]
    con = connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass)
    return con

# handler({}, {})
