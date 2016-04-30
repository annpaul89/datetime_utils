"""
Tests for datetime helpers.
"""
from datetime import datetime
from unittest import TestCase

import pytz

from datetime_utils import datetime_utils

class TestIsSnappedTo(TestCase):

    # UTC/GMT -2:30 hours
    tz = pytz.timezone('Canada/Newfoundland')

    # UTC/GMT -3 hours
    # Transition from 2015-02-22 24:00:00 -> 23:00:00
    # Transition from 2015-10-18 00:00:00 -> 01:00:00 (midnight doesn't exist)
    tz_AmericaSaoPaulo = pytz.timezone('America/Sao_Paulo')

    # UTC/GMT +2 hours
    # Transition from 2015-03-27 00:00:00 -> 01:00:00 (midnight doesn't exist)
    # Transition from 2015-10-30 01:00:00 -> 00:00:00 (midnight exists twice)
    tz_AsiaAmman = pytz.timezone('Asia/Amman')

    def test_naive_dt(self):
        period = 'minute'

        # success
        dt_success = datetime(2015, 3, 1, 4, 1)
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # failure
        dt_fail = datetime(2015, 3, 1, 4, 1, 35)
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        period = 'minute-15'

        # success
        dt_success = datetime(2015, 3, 1, 4, 15)
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # failure
        dt_fail = datetime(2015, 3, 1, 4, 25)
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        period = 'hour'

        # success
        dt_success = datetime(2015, 3, 1, 4)
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # failure
        dt_fail = datetime(2015, 3, 1, 4, 1)
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        period = 'day'

        # success
        dt_success = datetime(2015, 3, 1 )
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # failure
        dt_fail = datetime(2015, 3, 1, 4, 1)
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

    def test_min(self):
        period = 'minute'

        # same TZ, success
        dt_success = self.tz.localize(datetime(2015, 3, 1, 4, 1))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz))

        # same TZ, failure
        dt_fail = self.tz.localize(datetime(2015, 3, 1, 4, 1, 35))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        # different TZ, failure
        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz))

    def test_15_min(self):
        period = 'minute-15'

        # same TZ, success
        dt_success = self.tz.localize(datetime(2015, 3, 1, 4, 45))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz))

        # same TZ, failure
        dt_fail = self.tz.localize(datetime(2015, 3, 1, 4, 35))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        # different TZ, failure
        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz))

    def test_hour(self):
        period = 'hour'

        # same TZ, success
        dt_success = self.tz.localize(datetime(2015, 3, 1, 4))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz))

        # same TZ, failure
        dt_fail = self.tz.localize(datetime(2015, 3, 1, 4, 35))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        # different TZ, failure
        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz))

        # different TZ, would be success if TZ parameter not respected
        # depends on tz being a half-hour tz
        dt_should_fail = pytz.UTC.localize(datetime(2015, 3, 1))
        self.assertFalse(datetime_utils.is_snapped_to(dt_should_fail, period, self.tz))

    def test_day(self):
        period = 'day'

        # same TZ, success
        dt_success = self.tz.localize(datetime(2015, 3, 1))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz))

        # same TZ, failure
        dt_fail = self.tz.localize(datetime(2015, 3, 1, 4, 35))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        # different TZ, failure
        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz))

        # different TZ, would be success if TZ parameter not respected
        # depends on tz being a half-hour tz
        dt_should_fail = pytz.UTC.localize(datetime(2015, 3, 1))
        self.assertFalse(datetime_utils.is_snapped_to(dt_should_fail, period, self.tz))

    def test_day_dst_transition_at_midnight_midnight_doesnt_exist(self):
        period = 'day'

        # America/Sao_Paulo Timezone
        # Transition from 2015-02-22 24:00:00 -> 23:00:00
        # same TZ, success
        dt_success = self.tz_AmericaSaoPaulo.localize(datetime(2015, 2, 22))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz_AmericaSaoPaulo))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz_AmericaSaoPaulo))

        # America/Sao_Paulo Timezone
        # Transition from 2015-10-18 00:00:00 -> 01:00:00 (midnight doesn't exist)
        # same TZ, success
        dt_success = self.tz_AmericaSaoPaulo.localize(datetime(2015, 10, 18))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz_AmericaSaoPaulo))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz_AmericaSaoPaulo))

        # same TZ, failure
        dt_fail = self.tz_AmericaSaoPaulo.localize(datetime(2015, 10, 18, 0, 35))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz_AmericaSaoPaulo))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        # different TZ, failure
        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz_AmericaSaoPaulo))

    def test_day_dst_transition_at_midnight_midnight_exists_twice(self):
        period = 'day'

        # Asia/Amman Timezone
        # Transition from 2015-03-27 00:00:00 -> 01:00:00 (midnight doesn't exist)
        # same TZ, success
        dt_success = self.tz_AsiaAmman.localize(datetime(2015, 3, 27))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz_AsiaAmman))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # # different TZ, success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz_AsiaAmman))

        # Transition from 2015-10-30 01:00:00 -> 00:00:00 (midnight exists twice)
        # same TZ, success
        # this midnight should succeed - it's the first one
        dt_success = self.tz_AsiaAmman.localize(datetime(2015, 10, 30), is_dst=True)
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz_AsiaAmman))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # # different TZ, same success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz_AsiaAmman))

        # this midnight should fail - it's the second one
        dt_success = self.tz_AsiaAmman.localize(datetime(2015, 10, 30), is_dst=False)
        self.assertFalse(datetime_utils.is_snapped_to(dt_success, period, self.tz_AsiaAmman))
        self.assertFalse(datetime_utils.is_snapped_to(dt_success, period))

        # # different TZ, same failure
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz_AsiaAmman))

        # same TZ, failure
        dt_fail = self.tz_AsiaAmman.localize(datetime(2015, 10, 30, 0, 35))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz_AsiaAmman))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        # different TZ, failure
        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz_AsiaAmman))

    def test_hour_dst_transition_time_exists_twice(self):
        period = 'hour'

        # Transition from 2015-10-30 01:00:00 -> 00:00:00 (midnight exists twice)
        # first midnight
        dt_success = self.tz_AsiaAmman.localize(datetime(2015, 10, 30), is_dst=True)
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz_AsiaAmman))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # different TZ, same success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz_AsiaAmman))

        # second midnight
        dt_success = self.tz_AsiaAmman.localize(datetime(2015, 10, 30), is_dst=False)
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period, self.tz_AsiaAmman))
        self.assertTrue(datetime_utils.is_snapped_to(dt_success, period))

        # # different TZ, same success
        dt_utc_success = pytz.UTC.normalize(dt_success)
        self.assertTrue(datetime_utils.is_snapped_to(dt_utc_success, period, self.tz_AsiaAmman))

        # make sure we're not passing other times that happen twice
        dt_fail = self.tz_AsiaAmman.localize(datetime(2015, 10, 30, 0, 5), is_dst=True)
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz_AsiaAmman))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz_AsiaAmman))

        dt_fail = self.tz_AsiaAmman.localize(datetime(2015, 10, 30, 0, 5), is_dst=False)
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period, self.tz_AsiaAmman))
        self.assertFalse(datetime_utils.is_snapped_to(dt_fail, period))

        dt_utc_fail = pytz.UTC.normalize(dt_fail)
        self.assertFalse(datetime_utils.is_snapped_to(dt_utc_fail, period, self.tz_AsiaAmman))