import datetime as dt

from dto import LogData
import hashlib


def _get_hash(log: str) -> str:
    return hashlib.sha256(log.encode()).hexdigest()


def _get_created(log: str) -> dt.datetime:
    parts = log.split()
    dt_string = parts[3].strip('[').strip(']')
    return dt.datetime.strptime(dt_string, '%d/%b/%Y:%H:%M:%S')


def _get_ip(log: str) -> str:
    return log.split()[0]


def _get_method(log: str) -> str:
    return log.split()[5].strip('"')


def _get_url(log: str) -> str:
    return log.split()[6].strip('"')


def _get_response_code(log: str) -> int:
    response_code_str = log.split()[8]
    return int(response_code_str) if response_code_str.isdigit() else 0


def _get_response_size(log: str) -> int:
    response_size_str = log.split()[9]
    return int(response_size_str) if response_size_str.isdigit() else 0


def _get_referer(log: str) -> str | None:
    referer_str = log.split()[10].strip('"')
    return referer_str if referer_str != '-' else None


def _get_user_agent(log: str) -> str:
    return log.split(' "')[-2].strip('"')


def parse_log(log: str) -> LogData:
    result = LogData(
        hash=_get_hash(log),
        created=_get_created(log),
        ip=_get_ip(log),
        method=_get_method(log),
        url=_get_url(log),
        response_code=_get_response_code(log),
        response_size=_get_response_size(log),
        referer=_get_referer(log),
        user_agent=_get_user_agent(log),
    )
    return result
