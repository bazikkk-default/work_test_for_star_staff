from argparse import ArgumentParser
from psycopg2 import connect, Error
from json import loads

parser = ArgumentParser(description='You must input host, port,database, table\n '
                                             'With format:\n|    id    |    log_message    |\n\n')

parser.add_argument('--host', help="Hostname or ip of data base", dest='host', default='localhost', type=str)
parser.add_argument('--port', help="Port to data base", dest='port', default=5432, type=int)
parser.add_argument('--password', help="Password for data base", dest='password',
                    default='postgesql', type=str)
parser.add_argument('--user', help="User for data base", dest='user', default='postgesql', type=str)
parser.add_argument('--db', help="Name of data base", dest='db_name', default='simple_test', type=str)
parser.add_argument('--table_name', help="Name table from database with logs", dest='tname', default='logs', type=str)

args = parser.parse_args()

try:
    connection = connect(
        user=args.user,
        password=args.password,
        host=args.host,
        port=args.port,
        database=args.db_name
    )

    cursor = connection.cursor()
    cursor.execute(f"SELECT DISTINCT {args.tname}.log -> 'client_id' AS client FROM {args.tname};")
    records = cursor.fetchall()
    clients = dict()
    for client in records:
        cursor.execute(f"SELECT log FROM {args.tname} WHERE {args.tname}.log -> 'client_id' = {client[0]};")
        client_history = cursor.fetchall()
        sorted_history = sorted([loads(step[0]) for step in client_history], key=lambda x: loads(x[0]).get('date'))
        if any([step.get('document.location') for step in sorted_history
                if "https://shop.com/checkout" == step.get('document.location')])\
            and any([step.get('document.location') for step in sorted_history
                     if step.get('document.referer').startswith("https://referal.ours.com/")]):
            ref_flag = False

            for step in sorted_history:
                if step.get('document.referer').startswith("https://referal.ours.com/"):
                    ref_flag = True
                elif step.get('document.referer').startswith("https://ad.theirs"):
                    ref_flag = False
                else:
                    pass

                if ref_flag and "https://shop.com/checkout" == step.get('document.location'):
                    ref_flag = False
                    clients.setdefault(step.get('client_id'), [])
                    client[step.get('client_id')].append(step)

    print("\n".join([f"{name}: {len(attempts)}" for name, attempts in clients.items()]))

except (Exception, Error) as error:
    print("Error while connecting", error)

finally:
    if(connection):
        cursor.close()
        connection.close()
        print("Connection is closed")



