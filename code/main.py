from parser import parse_log
from itertools import batched
from db import insert_logs_bulk

with open('router.log') as f:
    lines = f.read().splitlines()

for batch in batched(lines, 100):
    logs = [parse_log(log) for log in batch]
    insert_logs_bulk(logs)
