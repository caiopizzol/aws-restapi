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
            'message': 'Service area successfully created with id {}!'.format(create_service_area(body))
        })
    except Exception as error:
        RESPONSE['statusCode'] = 400
        RESPONSE['body'] = json.dumps({
            'message': error
        })
    finally:
        print(RESPONSE)
        return RESPONSE

def create_service_area(data):
    con = get_db_connection()
    cur = con.cursor()
    query = '''
    INSERT INTO
        providers_service_areas (
            name,
            price,
            polygon,
            provider_id
        )
    VALUES (
        %s,
        %s,   
        ST_GeomFromGeoJSON('{}'),
        %s
    )
    RETURNING id;
    '''.format(json.dumps(data['polygon']))
    cur.execute(query, (
        data['name'],
        data['price'],
        data['provider_id']
        )
    )
    service_area_id = cur.fetchone()[0]
    con.commit()       
    cur.close()
    if con is not None:
        con.close()
    return service_area_id

def get_db_connection():         
    dbname = os.environ["DBNAME"]
    dbuser = os.environ["DBUSER"]
    dbpass = os.environ["DBPASS"]
    dbhost = os.environ["DBHOST"]
    dbport = os.environ["DBPORT"]
    con = connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass, port=dbport)
    return con


# event = {
#     'name': 'Curitiba Area 2',
#     'price': 55.20,
#     'provider_id': 2,
    # 'polygon': {
    #     "type": "Polygon",
    #     "coordinates": [
    #       [
    #         [
    #           -49.251708984375,
    #           -25.449164928922198
    #         ],
    #         [
    #           -49.17274475097656,
    #           -25.449164928922198
    #         ],
    #         [
    #           -49.17274475097656,
    #           -25.389938642388444
    #         ],
    #         [
    #           -49.251708984375,
    #           -25.389938642388444
    #         ],
    #         [
    #           -49.251708984375,
    #           -25.449164928922198
    #         ]
    #       ]
    #     ]
    #   }
# }
# handler(event, {})
