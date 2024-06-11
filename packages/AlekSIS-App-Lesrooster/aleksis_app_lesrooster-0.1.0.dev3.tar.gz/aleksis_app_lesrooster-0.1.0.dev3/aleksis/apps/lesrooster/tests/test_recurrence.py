from datetime import date, datetime, time
from pprint import pprint

from django.utils.timezone import get_current_timezone

import pytest
import recurrence

from aleksis.apps.lesrooster.models import (
    BreakSlot,
    Lesson,
    Slot,
    Supervision,
    TimeGrid,
    ValidityRange,
)
from aleksis.core.models import SchoolTerm

pytestmark = pytest.mark.django_db


@pytest.fixture
def school_term():
    date_start = date(2024, 1, 1)
    date_end = date(2024, 6, 1)
    school_term = SchoolTerm.objects.create(name="Test", date_start=date_start, date_end=date_end)
    return school_term


@pytest.fixture
def validity_range(school_term):
    validity_range = ValidityRange.objects.create(
        school_term=school_term, date_start=school_term.date_start, date_end=school_term.date_end
    )
    return validity_range


@pytest.fixture
def time_grid(validity_range):
    return TimeGrid.objects.get(validity_range=validity_range, group=None)


def test_slot_build_recurrence(time_grid):
    slot = Slot.objects.create(
        time_grid=time_grid, weekday=0, period=1, time_start=time(8, 0), time_end=time(9, 0)
    )
    rec = slot.build_recurrence(recurrence.WEEKLY)

    pprint(rec.rrules[0].__dict__)

    assert rec.dtstart == datetime(2024, 1, 1, 8, 0, tzinfo=get_current_timezone())
    assert len(rec.rrules) == 1

    rrule = rec.rrules[0]
    assert rrule.until == datetime(2024, 6, 1, 9, 0, tzinfo=get_current_timezone())
    assert rrule.freq == 2
    assert rrule.interval == 1


def test_lesson_recurrence(time_grid):
    slot = Slot.objects.create(
        time_grid=time_grid, weekday=0, period=1, time_start=time(8, 0), time_end=time(9, 0)
    )
    break_slot = BreakSlot.objects.create(
        time_grid=time_grid, weekday=0, time_start=time(9, 0), time_end=time(9, 15)
    )

    lesson = Lesson.objects.create(
        slot_start=slot,
        slot_end=slot,
    )

    assert lesson.build_recurrence(recurrence.WEEKLY) == slot.build_recurrence(recurrence.WEEKLY)

    supervision = Supervision.objects.create(break_slot=break_slot)

    assert supervision.build_recurrence(recurrence.WEEKLY) == break_slot.build_recurrence(
        recurrence.WEEKLY
    )
