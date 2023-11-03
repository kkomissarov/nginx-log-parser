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

def get_response_time():
    url = 'https://api.waveservice.ru/v3/healthcheck'
    start = time.monotonic()
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('Bad request from the server')
    stop = time.monotonic()
    return stop - start


def write_results(la, response_time):
    sql = '''
        INSERT INTO load_average(created, load_average, response_time) 
        VALUES (
            now(), 
            %(la)s, 
            %(response_time)s
        );
    '''
    with db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, {'la': la, 'response_time': response_time})
        conn.commit()


if __name__ == '__main__':
    la = get_la()
    response_time = get_response_time()
    write_results(la, response_time)
