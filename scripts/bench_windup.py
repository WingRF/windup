from time import time
from datetime import datetime

import windup


RFC3339_DATE = '2016-07-18'
RFC3339_TIME = '12:58:26.485897+02:00'
RFC3339_DATE_TIME = RFC3339_DATE + 'T' + RFC3339_TIME
RFC3339_DATE_TIME_DTLIB = RFC3339_DATE_TIME[:-6]
DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
DATETIME_OBJ = datetime.strptime(RFC3339_DATE_TIME_DTLIB, DATE_TIME_FORMAT)
TIME = time()
WINDUP_OPT = windup.fmt.date | windup.fmt.time | windup.fmt.usec


def benchmark_parse():
    def datetime_strptime():
        datetime.strptime(RFC3339_DATE_TIME_DTLIB, DATE_TIME_FORMAT)

    def windup_parse():
        windup.from_string(RFC3339_DATE_TIME)

    return datetime_strptime, windup_parse


def benchmark_format():
    def datetime_strftime():
        DATETIME_OBJ.strftime(DATE_TIME_FORMAT)

    def windup_format():
        windup.to_string(DATETIME_OBJ, option=WINDUP_OPT)

    return datetime_strftime, windup_format


def benchmark_utcnow():
    def datetime_utcnow():
        datetime.utcnow()

    def windup_utcnow():
        windup.utcnow()

    return datetime_utcnow, windup_utcnow


def benchmark_now():
    def datetime_now():
        datetime.now()

    def windup_now():
        windup.now()

    return datetime_now, windup_now


def benchmark_utcnow_to_string():
    def datetime_utcnow_to_string():
        datetime.utcnow().strftime(DATE_TIME_FORMAT)

    def windup_utcnow_to_string():
        windup.utcnow_to_string(option=WINDUP_OPT)

    return datetime_utcnow_to_string, windup_utcnow_to_string


def benchmark_now_to_string():
    def datetime_now_to_string():
        datetime.now().strftime(DATE_TIME_FORMAT)

    def windup_now_to_string():
        windup.now_to_string(option=WINDUP_OPT)

    return datetime_now_to_string, windup_now_to_string


def benchmark_fromtimestamp():
    def datetime_fromtimestamp():
        datetime.fromtimestamp(TIME)

    def windup_fromtimestamp():
        windup.from_timestamp(TIME)

    return datetime_fromtimestamp, windup_fromtimestamp


def benchmark_utcfromtimestamp():
    def datetime_utcfromtimestamp():
        datetime.utcfromtimestamp(TIME)

    def windup_utcfromtimestamp():
        windup.from_utctimestamp(TIME)

    return datetime_utcfromtimestamp, windup_utcfromtimestamp


if __name__ == '__main__':
    from timeit import repeat

    benchmarks = [
        benchmark_parse,
        benchmark_format,

        benchmark_utcnow,
        benchmark_now,

        benchmark_utcnow_to_string,
        benchmark_now_to_string,

        benchmark_fromtimestamp,
        benchmark_utcfromtimestamp,
    ]

    print('Executing benchmarks ...')

    for k in benchmarks:
        print('\n============ %s ============' % k.__name__)
        mins = []

        for func in k():
            times = repeat(stmt='func()',
                           setup='from __main__ import func',
                           number=100000)
            t = min(times)
            mins.append(t)
            print(func.__name__, t)

        win = False
        if mins[0] > mins[1]:
            win = True

        mins = sorted(mins)
        diff = mins[1] / mins[0]

        if win:
            print('windup is %.01f times faster' % diff)
        else:
            print('windup is %.01f times slower' % diff)
