# windup: A fast date-time library

`windup` is a library extends from [udatetime](https://pypi.org/project/udatetime/) 
and offers an faster `datetime` object instantiation, serialization and 
deserialization of date-time strings. `windup` is using Python's `datetime class` 
under the hood and code already using `datetime` should be able to easily switch 
to `windup`. All `datetime` objects created by `windup` are timezone-aware. 
The timezones that `windup` uses are fixed-offset timezones, meaning that they 
don't observe daylight savings time (DST), and thus return a fixed offset from 
UTC all year round.

`windup` extends some optional formatting options, all the options are in 
`windup.fmt` and `windup.sep`. 

* windup.fmt
  * fmt.date: formatting date string, like '`2022-07-17`'
  * fmt.time: formatting time string, like '`12:12:12`'
  * fmt.msec: formatting milisecond string, like '12:12:12.`123`'
  * fmt.usec: formatting microsecond string, like '12:12:12.`2123456`'
  * fmt.tz: formatting timezone string, like '2022-07-17T12:12:12.123`+08:00`'
  * fmt.utc_z: formatting timezone string as `Z` if `UTC`, like '2022-07-17T12:12:12.123`Z`'


* windup.sep
  * sep.T: set the separator '`T`' between date-string and time-string
  * sep.space: set the separator '` `' between date-string and time-string
  * sep.underscore: set the separator '`_`' between date-string and time-string



Just see the examples below.

```python
>>> windup.from_string("2021-07-15T12:12:12.123456+08:00")
datetime.datetime(2021, 7, 15, 12, 12, 12, 123456, tzinfo=+08:00)

>>> dt = windup.from_string("2021-07-15T12:12:12.123456+08:00")
>>> windup.to_string(dt)
"2021-07-15T12:12:12.123456+08:00"

>>> windup.now()
datetime.datetime(2021, 7, 15, 12, 12, 12, 472467, tzinfo=+08:00)

>>> windup.utcnow()
datetime.datetime(2021, 7, 15, 4, 12, 12, 472467, tzinfo=+00:00)

>>> windup.now_to_string(option=windup.fmt.date | windup.fmt.time | windup.fmt.usec)
"2021-07-15T12:12:12.123456"

>>> windup.utcnow_to_string(option=windup.fmt.date | windup.fmt.time, sep=windup.sep.space)
"2021-07-15 12:12:12"

>>> windup.fromtimestamp(time.time())
datetime.datetime(2021, 7, 15, 17, 45, 1, 536586, tzinfo=+08:00)

>>> windup.utcfromtimestamp(time.time())
datetime.datetime(2021, 7, 15, 10, 14, 53, tzinfo=+00:00)
```

## Installation

Currently only **POSIX** compliant systems are supported.
Working on cross-platform support.

```
$ pip install windup
```

You might need to install the header files of your Python installation and
some essential tools to execute the build like a C compiler.

```
$ sudo apt-get install python3-dev build-essential
```

or

```
$ sudo yum install python3-devel gcc
```

## Benchmark

```
$ python scripts/bench_windup.py
Executing benchmarks ...

============ benchmark_parse ============
datetime_strptime 2.7934684499996365
windup_parse 0.20049594300053286
windup is 13.9 times faster

============ benchmark_format ============
datetime_strftime 0.6035372909973375
windup_format 0.31113305999315344
windup is 1.9 times faster

============ benchmark_utcnow ============
datetime_utcnow 0.09793541399994865
windup_utcnow 0.04310180398169905
windup is 2.3 times faster

============ benchmark_now ============
datetime_now 0.14119137199941179
windup_now 0.04639216099985788
windup is 3.0 times faster

============ benchmark_utcnow_to_string ============
datetime_utcnow_to_string 0.6921647540002596
windup_utcnow_to_string 0.29203156699077226
windup is 2.4 times faster

============ benchmark_now_to_string ============
datetime_now_to_string 1.2531362709996756
windup_now_to_string 0.49691468400033045
windup is 2.5 times faster

============ benchmark_fromtimestamp ============
datetime_fromtimestamp 0.09680619402206503
windup_fromtimestamp 0.0611271969974041
windup is 1.6 times faster

============ benchmark_utcfromtimestamp ============
datetime_utcfromtimestamp 0.08515822299523279
windup_utcfromtimestamp 0.04857380600878969
windup is 1.8 times faster
```
