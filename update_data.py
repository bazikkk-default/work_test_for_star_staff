from argparse import ArgumentParser
from psycopg2 import connect, Error
from json import load, dumps

parser = ArgumentParser(description='You must input host, port,database, table\n '
                                             'With format:\n|    id    |    log_message    |\n\n')

parser.add_argument('--host', help="Hostname or ip of data base", dest='host', default='localhost', type=str)
parser.add_argument('--port', help="Port to data base", dest='port', default=5432, type=int)
parser.add_argument('--password', help="Password for data base", dest='password',
                    default='postgesql', type=str)
parser.add_argument('--user', help="User for data base", dest='user', default='postgesql', type=str)
parser.add_argument('--db', help="Name of data base", dest='db_name', default='simple_test', type=str)
parser.add_argument('--table_name', help="Name table from database with logs", dest='tname', default='logs', type=str)
parser.add_argument('--dumped_logs', help="Dump path", dest='logs', default='./logs.json', type=str)

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
    cursor.execute(f"CREATE TABLE logs("
                   f"id serial PRIMARY KEY,"
                   f"log jsonb);")

    with open(args.logs) as f:
        data_set = load(f)

    for step in data_set:
        cursor.execute(f"INSERT INTO {args.tname}(log) VALUES({dumps(step)});")

except (Exception, Error) as error:
    print("Error while connecting", error)

finally:
    if(connection):
        cursor.close()
        connection.close()
        print("Connection is closed")
