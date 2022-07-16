import unittest
from datetime import datetime, timedelta, tzinfo

import windup

NO_DST = timedelta(0)


class Test(unittest.TestCase):

    def test_utcnow(self):
        dt_now = datetime.utcnow()
        wd_now = windup.utcnow()

        self.assertIsInstance(wd_now, datetime)

        self.assertEqual(wd_now.year, dt_now.year)
        self.assertEqual(wd_now.month, dt_now.month)
        self.assertEqual(wd_now.day, dt_now.day)

        self.assertEqual(wd_now.hour, dt_now.hour)
        self.assertEqual(wd_now.minute, dt_now.minute)
        self.assertEqual(wd_now.second, dt_now.second)

        self.assertEqual(wd_now.utcoffset(), timedelta(0))
        self.assertEqual(wd_now.dst(), NO_DST)

    def test_now(self):
        dt_now = datetime.now()
        wd_now = windup.now()

        self.assertIsInstance(wd_now, datetime)

        self.assertEqual(wd_now.year, dt_now.year)
        self.assertEqual(wd_now.month, dt_now.month)
        self.assertEqual(wd_now.day, dt_now.day)

        self.assertEqual(wd_now.hour, dt_now.hour)
        self.assertEqual(wd_now.minute, dt_now.minute)
        self.assertEqual(wd_now.second, dt_now.second)

    def test_from_and_to_string(self):
        rfc3339 = '2016-07-15T12:33:20.123000+01:30'
        dt = windup.from_string(rfc3339)

        self.assertIsInstance(dt, datetime)

        self.assertEqual(dt.year, 2016)
        self.assertEqual(dt.month, 7)
        self.assertEqual(dt.day, 15)

        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 33)
        self.assertEqual(dt.second, 20)
        self.assertEqual(dt.microsecond, 123000)

        self.assertEqual(dt.utcoffset(), timedelta(hours=1, minutes=30))
        self.assertEqual(dt.dst(), NO_DST)

        self.assertEqual(windup.to_string(dt), rfc3339)

        rfc3339 = '2016-07-18T12:58:26.485897-02:00'
        dt = windup.from_string(rfc3339)
        self.assertEqual(windup.to_string(dt), rfc3339)

    def test_fromtimestamp(self):
        DAY = 86400
        HOUR = 3600
        TZ_CEST = windup.TZFixedOffset(60 * 2)

        for t in range(0, DAY - (2 * HOUR), HOUR):
            dt = datetime.fromtimestamp(t)
            wdt = windup.from_timestamp(t)

            self.assertIsInstance(wdt, datetime)
            self.assertEqual(wdt.year, dt.year)
            self.assertEqual(wdt.month, dt.month)
            self.assertEqual(wdt.day, dt.day)

            self.assertEqual(wdt.hour, dt.hour)
            self.assertEqual(wdt.minute, dt.minute)
            self.assertEqual(wdt.second, dt.second)
            self.assertEqual(wdt.microsecond, dt.microsecond)

            self.assertEqual(wdt.utcoffset(), timedelta(0))
            self.assertEqual(wdt.dst(), NO_DST)

        for t in range(0, DAY, HOUR):
            dt = datetime.fromtimestamp(t, TZ_CEST)
            wdt = windup.from_timestamp(t, TZ_CEST)

            self.assertIsInstance(wdt, datetime)
            self.assertEqual(wdt.year, dt.year)
            self.assertEqual(wdt.month, dt.month)
            self.assertEqual(wdt.day, dt.day)

            self.assertEqual(wdt.hour, dt.hour)
            self.assertEqual(wdt.minute, dt.minute)
            self.assertEqual(wdt.second, dt.second)
            self.assertEqual(wdt.microsecond, dt.microsecond)

            self.assertEqual(wdt.utcoffset(), timedelta(hours=2))
            self.assertEqual(wdt.dst(), NO_DST)

        for t in range(0, DAY * -1, HOUR * -1):
            dt = datetime.fromtimestamp(t, TZ_CEST)
            wdt = windup.from_timestamp(t, TZ_CEST)

            self.assertIsInstance(wdt, datetime)
            self.assertEqual(wdt.year, dt.year)
            self.assertEqual(wdt.month, dt.month)
            self.assertEqual(wdt.day, dt.day)

            self.assertEqual(wdt.hour, dt.hour)
            self.assertEqual(wdt.minute, dt.minute)
            self.assertEqual(wdt.second, dt.second)
            self.assertEqual(wdt.microsecond, dt.microsecond)

            self.assertEqual(wdt.utcoffset(), timedelta(hours=2))
            self.assertEqual(wdt.dst(), NO_DST)

    def test_utcfromtimestamp(self):
        DAY = 86400
        HOUR = 3600

        for t in range(0, DAY, HOUR):
            dt = datetime.utcfromtimestamp(t)
            wdt = windup.from_utctimestamp(t)

            self.assertIsInstance(wdt, datetime)
            self.assertEqual(wdt.year, dt.year)
            self.assertEqual(wdt.month, dt.month)
            self.assertEqual(wdt.day, dt.day)
            self.assertEqual(wdt.hour, dt.hour)
            self.assertEqual(wdt.minute, dt.minute)
            self.assertEqual(wdt.second, dt.second)
            self.assertEqual(wdt.microsecond, dt.microsecond)

            self.assertEqual(wdt.utcoffset(), timedelta(0))
            self.assertEqual(wdt.dst(), NO_DST)

        for t in range(0, DAY * -1, HOUR * -1):
            dt = datetime.utcfromtimestamp(t)
            wdt = windup.from_utctimestamp(t)

            self.assertIsInstance(wdt, datetime)
            self.assertEqual(wdt.year, dt.year)
            self.assertEqual(wdt.month, dt.month)
            self.assertEqual(wdt.day, dt.day)
            self.assertEqual(wdt.hour, dt.hour)
            self.assertEqual(wdt.minute, dt.minute)
            self.assertEqual(wdt.second, dt.second)
            self.assertEqual(wdt.microsecond, dt.microsecond)

            self.assertEqual(wdt.utcoffset(), timedelta(0))
            self.assertEqual(wdt.dst(), NO_DST)

    def test_broken_from_string(self):
        invalid = [
            '2016-07-15 12:33:20.123000+01:30',
            '2016-13-15T12:33:20.123000+01:30',
            '20161315T12:33:20.123000+01:30',
            'Hello World',
            '2016-07-15 12:33:20.123000+01:302016-07-15 12:33:20.123000+01:30',
            '2016-07-15T12:33:20.1Z0',
            '2016-07-15T12:33:20.1 +01:30f',
        ]

        for r in invalid:
            with self.assertRaises(ValueError):
                windup.from_string(r)

    def test_ok_from_string(self):
        rfc3339s = [
            '2016-07-15 T 12:33:20.123000 +01:30',
            '2016-07-15 T 12:33:20.123000 +01:30',
            '2016-07-15T12:33:20.123 +01:30',
            '2016-07-15T12:33:20 +01:30',
            '2016-07-15T12:33:20 Z',
            '2016-07-15T12:33:20',
            '2016-07-15t12:33:20',
            '2016-07-15T12:33:20.1 +01:30',
        ]

        for r in rfc3339s:
            self.assertIsInstance(
                windup.from_string(r),
                datetime
            )

    def test_tzone(self):
        rfc3339 = '2016-07-15T12:33:20.123000+01:30'
        dt = windup.from_string(rfc3339)
        offset = dt.tzinfo.utcoffset()
        dst = dt.tzinfo.dst()

        self.assertIsInstance(offset, timedelta)
        self.assertEqual(offset.total_seconds() / 60, 90)
        self.assertEqual(dst, NO_DST)

        rfc3339 = '2016-07-15T12:33:20.123000Z'
        dt = windup.from_string(rfc3339)
        offset = dt.tzinfo.utcoffset()
        dst = dt.tzinfo.dst()

        self.assertIsInstance(offset, timedelta)
        self.assertEqual(offset.total_seconds(), 0)
        self.assertEqual(dst, NO_DST)

        rfc3339 = '2016-07-15T12:33:20.123000-02:00'
        dt = windup.from_string(rfc3339)
        offset = dt.tzinfo.utcoffset()
        dst = dt.tzinfo.dst()

        self.assertIsInstance(offset, timedelta)
        self.assertEqual(offset.total_seconds() / 60, -120)
        self.assertEqual(dst, NO_DST)

    def test_precision(self):
        t = 1469897308.549871
        dt = datetime.fromtimestamp(t)
        wdt = windup.from_timestamp(t)
        self.assertEqual(wdt.microsecond, dt.microsecond)

    def test_raise_on_not_TZFixedOffset(self):
        class TZInvalid(tzinfo):
            def utcoffset(self, dt=None):
                return timedelta(seconds=0)

            def dst(self, dt=None):
                return timedelta(seconds=0)

        dt = datetime.now(TZInvalid())

        with self.assertRaises(ValueError):
            windup.to_string(dt)

    def test_variable_fraction(self):
        rfc3339 = '2016-07-15T12:33:20.1'
        d1 = windup.from_string(rfc3339 + ('0' * 5) + 'Z')

        for x in range(0, 6):
            d2 = windup.from_string(rfc3339 + ('0' * x) + 'Z')
            self.assertEqual(d1, d2)

        self.assertEqual(
            windup.from_string('2016-07-15T12:33:20.123Z'),
            windup.from_string('2016-07-15T12:33:20.123000Z'),
        )

        self.assertEqual(
            windup.from_string('2016-07-15T12:33:20.0Z'),
            windup.from_string('2016-07-15T12:33:20Z'),
        )


if __name__ == '__main__':
    unittest.main()
