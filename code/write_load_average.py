import datetime
import datetime as dt
import sys
import time
import requests
from db import db_connection


def get_la():
    if len(sys.argv) == 2:
        try:
            la = float(sys.argv[1])
        except ValueError:
            raise Exception("Argument should be a number")

    else:
        raise Exception("This command requires 1 number argument")

    return la

def get_healthcheck_data():
    url = 'https://api.waveservice.ru/v3/healthcheck'
    start = time.monotonic()

    request_started_at = dt.datetime.now(datetime.UTC)
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('Bad request from the server')

    data = r.json()


    stop = time.monotonic()

    return {
        'request_started_at': request_started_at,
        'response_time': stop - start,
        'db_ping': data['db_ping'],
        'total_business_logic_exec': data['total'],
    }


def write_results(la, response_time, request_started_at, db_ping, total_business_logic_exec):
    sql = '''
        INSERT INTO load_average(
            created, 
            load_average, 
            response_time, 
            request_started_at, 
            db_ping,
            total_business_logic_exec
        ) 
        VALUES (
            now(), 
            %(la)s, 
            %(response_time)s,
            %(request_started_at)s,
            %(db_ping)s,
            %(total_business_logic_exec)s
        );
    '''
    with db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, {
                'la': la,
                'response_time': response_time,
                'request_started_at': request_started_at,
                'db_ping': db_ping,
                'total_business_logic_exec': total_business_logic_exec,
            })
        conn.commit()


if __name__ == '__main__':
    la = get_la()
    healthcheck_data = get_healthcheck_data()
    write_results(
        la=la,
        response_time=healthcheck_data['response_time'],
        request_started_at=healthcheck_data['request_started_at'],
        db_ping=healthcheck_data['db_ping'],
        total_business_logic_exec=healthcheck_data['total_business_logic_exec'],
    )
