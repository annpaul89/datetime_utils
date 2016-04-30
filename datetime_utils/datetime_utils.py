from datetime import datetime, timedelta

import pytz


def parse_period(period):
    """
    Parse a 'period' out to it's two parts

    >>> parse_period('minute-15')
    ('minute', 15)
    >>> parse_period('day')
    ('day', 1)
    """
    unit = period.split('-')[0]
    quantity = int((period.split('-') + ['1'])[1])
    return (unit, quantity)


def period_to_timedelta(period):
    """
    Valid periods are:
        minute, minute-15, hour, day, week
    'month' is not supported - months are varrying lengths of time
    """
    unit, quantity = parse_period(period)
    return timedelta(**{unit+'s': quantity})


def get_isoweek_monday(dt):
    # if it's a week we want to find the iso-week's monday
    return dt - timedelta(days=dt.weekday())


def round_datetime_to_15min(dt, tzinfo=None, force=False):
    """
    Round the given datetime to a 15-minute period.

    If a timezone is specified, the rounding is done in that timezone.
    Else it is done in the timezone of the datetime.

    Specify force=True to cause pre-rounded values to jump another step anyway.
    """
    if dt.minute % 15 <= 7:
        return round_datetime_down(dt, 'minute-15', tzinfo, force)
    else:
        return round_datetime_up(dt, 'minute-15', tzinfo, force)


def round_datetime_down(dt, period, tzinfo=None, force=False):
    """
    Round the given datetime down by 'snapping' it to the period.

    Valid periods are:
        minute, minute-15, hour, day, week

    If a timezone is specified, the rounding is done in that timezone.
    Else it is done in the timezone of the datetime.

    Specify force=True to cause pre-rounded values to jump another step anyway.
    """
    if force:
        dt = dt - timedelta.resolution

    org_tz = dt.tzinfo
    if not org_tz:
        dt = pytz.UTC.localize(dt)

    if tzinfo:
        dt = tzinfo.normalize(dt)

    rounded = None

    if period == 'week':
        monday = get_isoweek_monday(dt)
        args = [monday.year, monday.month, monday.day]
        rounded = datetime(*args)

    args = [dt.year, dt.month, dt.day]
    if period == 'day':
        rounded = datetime(*args)

    args.append(dt.hour)
    if period == 'hour':
        rounded = datetime(*args)
    if period == 'minute-15':
        args.append(dt.minute/15*15)
        rounded = datetime(*args)

    args.append(dt.minute)
    if period == 'minute':
        rounded = datetime(*args)

    args.append(dt.second)
    if period == 'second':
        rounded = datetime(*args)

    if rounded is None:
        raise Exception('Unrecognized period')

    rounded = dt.tzinfo.localize(rounded)

    if org_tz:
        rounded = org_tz.normalize(rounded)
    else:
        rounded = pytz.UTC.normalize(rounded).replace(tzinfo=None)

    return rounded


def round_datetime_up(dt, period, tzinfo=None, force=False):
    """
    Anologue of 'round_datetime_down', but in the 'up' direction.

    Valid periods are:
        minute, minute-15, hour, day, week
    """
    if force:
        dt = dt + timedelta.resolution

    # we're already 'snapped' to the period
    previous = round_datetime_down(dt, period, tzinfo=tzinfo)

    if previous == dt:
        return previous

    # add the period, then round down.
    ahead = dt + period_to_timedelta(period)
    return round_datetime_down(ahead, period, tzinfo=tzinfo)



def is_snapped_to_15min(dt, tz=None):
    """
    Checks if the datetime is 'snapped' to the period.

    Valid periods are:
        minute, minute-15, hour, day, week

    If a timezone is specified, the check is done in that timezone.
    Else it is done in the timezone of the datetime.
    """
    return is_snapped_to(dt, 'minute-15', tz)


def is_snapped_to(dt, period, tz=None):
    tz = tz or dt.tzinfo
    dt_local = tz.normalize(dt) if tz else dt

    dt_less = dt - timedelta.resolution
    dt_less = tz.normalize(dt_less) if tz else dt_less

    if period == 'minute':
        return dt_less.minute != dt_local.minute

    if period == 'minute-15':
        return dt_less.minute / 15 != dt_local.minute / 15

    if period == 'hour':
        if dt_less.hour != dt_local.hour:
            return True

        # handling the case where there's a 'double hour' DST transition
        if (    dt_less.tzinfo != dt_local.tzinfo and
                dt_less.minute > dt_local.minute):
            return True

        return False

    if period == 'day':
        return dt_less.day != dt_local.day

    raise Exception('Unrecognized period: %s' % period)
