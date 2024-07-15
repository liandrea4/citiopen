from django.test import TestCase
from api.models.ballkid import *
from api.models.schedule import *
from api.views.ballkid import (
    recalc_captain_analytics,
    recalc_checkin_analytics,
    recalc_court_analytics,
)
from datetime import datetime, timedelta


class TestBallkidViewAnalytics(TestCase):
    def setUp(self):
        self.ballkid = Ballkid.objects.create(first_name="Lacy", last_name="Iosue")
        self.ballkid2 = Ballkid.objects.create(first_name="Joe", last_name="Iosue")
        self.captain = Ballkid.objects.create(
            first_name="Andrea", last_name="Iosue", is_captain=True
        )
        self.captain2 = Ballkid.objects.create(
            first_name="Bird", last_name="Iosue", is_captain=True
        )

    def test_recalc_checkin_analytics_doesnt_exist(self):
        self.assertEqual(0, len(CheckinAnalytics.objects.all()))

        CheckinHistory.objects.create(
            ballkid=self.ballkid,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 14, 29),
        )
        recalc_checkin_analytics(ballkid=self.ballkid, year=2022)

        analytics = CheckinAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        self.assertEqual(timedelta(hours=3, minutes=59), analytics.first().duration)

    def test_recalc_checkin_analytics_exists(self):
        self.assertEqual(0, len(CheckinAnalytics.objects.all()))

        CheckinHistory.objects.create(
            ballkid=self.ballkid,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 14, 29),
        )
        CheckinAnalytics.objects.create(
            ballkid=self.ballkid, duration=timedelta(), year=2022
        )
        recalc_checkin_analytics(ballkid=self.ballkid, year=2022)

        analytics = CheckinAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        self.assertEqual(timedelta(hours=3, minutes=59), analytics.first().duration)

    def test_recalc_checkin_analytics_one_history(self):
        CheckinHistory.objects.create(
            ballkid=self.ballkid,
            start=datetime(2022, 1, 1, 16, 30),
            end=datetime(2022, 1, 2, 0, 30),
        )
        recalc_checkin_analytics(ballkid=self.ballkid, year=2022)

        analytics = CheckinAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        self.assertEqual(timedelta(hours=8), analytics.first().duration)

    def test_recalc_checkin_analytics_mult_histories(self):
        CheckinHistory.objects.create(
            ballkid=self.ballkid,
            start=datetime(2022, 1, 1, 16, 30),
            end=datetime(2022, 1, 2, 0, 30),
        )
        CheckinHistory.objects.create(
            ballkid=self.ballkid,
            start=datetime(2022, 1, 2, 8, 15),
            end=datetime(2022, 1, 2, 18, 30),
        )
        recalc_checkin_analytics(ballkid=self.ballkid, year=2022)

        analytics = CheckinAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        self.assertEqual(timedelta(hours=18, minutes=15), analytics.first().duration)

    def test_recalc_checkin_analytics_mult_ballkids(self):
        CheckinHistory.objects.create(
            ballkid=self.ballkid,
            start=datetime(2022, 1, 1, 16, 30),
            end=datetime(2022, 1, 2, 0, 30),
        )
        CheckinHistory.objects.create(
            ballkid=self.ballkid,
            start=datetime(2022, 1, 2, 8, 15),
            end=datetime(2022, 1, 2, 18, 30),
        )
        CheckinHistory.objects.create(
            ballkid=self.ballkid2,
            start=datetime(2022, 1, 2, 8, 15),
            end=datetime(2022, 1, 2, 18, 30),
        )
        recalc_checkin_analytics(ballkid=self.ballkid, year=2022)
        recalc_checkin_analytics(ballkid=self.ballkid2, year=2022)

        analytics = CheckinAnalytics.objects.all()
        self.assertEqual(2, len(analytics))

        analytic1 = analytics.get(ballkid=self.ballkid)
        self.assertEqual(timedelta(hours=18, minutes=15), analytic1.duration)

        analytic2 = analytics.get(ballkid=self.ballkid2)
        self.assertEqual(timedelta(hours=10, minutes=15), analytic2.duration)

    def test_recalc_checkin_analytics_milliseconds(self):
        CheckinHistory.objects.create(
            ballkid=self.ballkid,
            start=datetime(2022, 1, 1, 16, 30, 2, 10),
            end=datetime(2022, 1, 2, 0, 30, 3, 11),
        )
        recalc_checkin_analytics(ballkid=self.ballkid, year=2022)

        analytics = CheckinAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(
            timedelta(hours=8, seconds=1, microseconds=1), analytic.duration
        )

    def test_recalc_checkin_analytics_empty_end(self):
        CheckinHistory.objects.create(
            ballkid=self.ballkid, start=datetime(2022, 1, 1, 16, 30, 2)
        )
        recalc_checkin_analytics(
            ballkid=self.ballkid, now=datetime(2022, 1, 2, 0, 30, 3), year=2022
        )

        analytics = CheckinAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(timedelta(hours=8, seconds=1), analytic.duration)

    def test_recalc_checkin_analytics_mult_ballkids_recalc_all(self):
        CheckinHistory.objects.create(
            ballkid=self.ballkid,
            start=datetime(2022, 1, 1, 16, 30),
            end=datetime(2022, 1, 2, 0, 30),
        )
        CheckinHistory.objects.create(
            ballkid=self.ballkid,
            start=datetime(2022, 1, 2, 8, 15),
            end=datetime(2022, 1, 2, 18, 30),
        )
        CheckinHistory.objects.create(
            ballkid=self.ballkid2,
            start=datetime(2022, 1, 2, 8, 15),
            end=datetime(2022, 1, 2, 18, 30),
        )
        recalc_checkin_analytics(year=2022)

        analytics = CheckinAnalytics.objects.all()
        self.assertEqual(4, len(analytics))

        analytic1 = analytics.get(ballkid=self.ballkid)
        self.assertEqual(timedelta(hours=18, minutes=15), analytic1.duration)

        analytic2 = analytics.get(ballkid=self.ballkid2)
        self.assertEqual(timedelta(hours=10, minutes=15), analytic2.duration)

    def test_recalc_captain_analytics_milliseconds(self):
        start = datetime(2022, 1, 1, 10, 30)
        end = datetime(2022, 1, 1, 14, 29, 1, 10)
        Schedule.objects.create(team=1, court=COURT.STADIUM, start=start, end=end)

        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=start,
            end=end,
            team=1,
        )
        recalc_captain_analytics(ballkid=self.ballkid, year=2022)

        analytics = CaptainAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(self.captain, analytic.captain)
        self.assertEqual(1, analytic.count)
        self.assertEqual(
            timedelta(hours=3, minutes=59, seconds=1, microseconds=10),
            analytic.duration,
        )

    def test_recalc_captain_analytics_doesnt_exist(self):
        start = datetime(2022, 1, 1, 10, 30)
        end = datetime(2022, 1, 1, 14, 29)
        Schedule.objects.create(team=1, court=COURT.STADIUM, start=start, end=end)

        self.assertEqual(0, len(CaptainAnalytics.objects.all()))
        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=start,
            end=end,
            team=1,
        )
        recalc_captain_analytics(ballkid=self.ballkid, year=2022)

        analytics = CaptainAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(self.captain, analytic.captain)
        self.assertEqual(1, analytic.count)
        self.assertEqual(timedelta(hours=3, minutes=59), analytic.duration)

    def test_recalc_captain_analytics_self_not_included(self):
        start = datetime(2022, 1, 1, 10, 30)
        end = datetime(2022, 1, 1, 14, 29)
        Schedule.objects.create(team=1, court=COURT.STADIUM, start=start, end=end)

        CaptainHistory.objects.create(
            ballkid=self.captain,
            captain=self.captain2,
            start=start,
            end=end,
            team=1,
        )
        CaptainHistory.objects.create(
            ballkid=self.captain2,
            captain=self.captain,
            start=start,
            end=end,
            team=1,
        )
        recalc_captain_analytics(ballkid=self.captain, year=2022)
        recalc_captain_analytics(ballkid=self.captain2, year=2022)

        self.assertFalse(
            CaptainAnalytics.objects.all().filter(
                ballkid_id=self.captain.id, captain_id=self.captain.id
            )
        )
        self.assertFalse(
            CaptainAnalytics.objects.all().filter(
                ballkid_id=self.captain2.id, captain_id=self.captain2.id
            )
        )
        self.assertTrue(
            CaptainAnalytics.objects.all().filter(
                ballkid_id=self.captain.id, captain_id=self.captain2.id
            )
        )
        self.assertTrue(
            CaptainAnalytics.objects.all().filter(
                ballkid_id=self.captain2.id, captain_id=self.captain.id
            )
        )

    def test_recalc_captain_analytics_ballkid_exists(self):
        start = datetime(2022, 1, 1, 10, 30)
        end = datetime(2022, 1, 1, 14, 29)
        Schedule.objects.create(team=1, court=COURT.STADIUM, start=start, end=end)

        analytic = CaptainAnalytics.objects.create(
            ballkid=self.ballkid, captain=self.captain, year=2022
        )
        self.assertEqual(1, len(CaptainAnalytics.objects.all()))

        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=start,
            end=end,
            team=1,
        )
        recalc_captain_analytics(ballkid=self.ballkid, year=2022)

        analytics = CaptainAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(self.captain, analytic.captain)
        self.assertEqual(1, analytic.count)
        self.assertEqual(end - start, analytic.duration)

    def test_recalc_captain_analytics_captain_exists(self):
        start = datetime(2022, 1, 1, 10, 30)
        end = datetime(2022, 1, 1, 14, 29)

        CaptainAnalytics.objects.create(
            ballkid=self.captain, captain=self.captain2, year=2022
        )
        CaptainAnalytics.objects.create(
            ballkid=self.captain2, captain=self.captain, year=2022
        )
        self.assertEqual(2, len(CaptainAnalytics.objects.all()))

        CaptainHistory.objects.create(
            ballkid=self.captain2,
            captain=self.captain,
            start=start,
            end=end,
            team=1,
        )
        CaptainHistory.objects.create(
            ballkid=self.captain,
            captain=self.captain2,
            start=start,
            end=end,
            team=1,
        )
        Schedule.objects.create(team=1, court=COURT.STADIUM, start=start, end=end)

        recalc_captain_analytics(ballkid=self.captain, year=2022)
        recalc_captain_analytics(ballkid=self.captain2, year=2022)

        analytics = CaptainAnalytics.objects.all().order_by("ballkid_id")
        self.assertEqual(2, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.captain, analytic.ballkid)
        self.assertEqual(self.captain2, analytic.captain)
        self.assertEqual(1, analytic.count)
        self.assertEqual(timedelta(hours=3, minutes=59), analytic.duration)

    def test_recalc_captain_analytics_one_history_one_captain(self):
        start = datetime(2022, 1, 1, 10, 30)
        end = datetime(2022, 1, 1, 14, 29)
        Schedule.objects.create(team=1, court=COURT.STADIUM, start=start, end=end)

        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=start,
            end=end,
            team=1,
        )
        recalc_captain_analytics(ballkid=self.ballkid, year=2022)

        analytics = CaptainAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(self.captain, analytic.captain)
        self.assertEqual(1, analytic.count)
        self.assertEqual(timedelta(hours=3, minutes=59), analytic.duration)

    def test_recalc_captain_analytics_mult_histories_one_captain(self):
        Schedule.objects.create(
            team=1,
            court=COURT.STADIUM,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 2, 14, 45),
        )

        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 14, 29),
            team=1,
        )
        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=datetime(2022, 1, 2, 13, 00),
            end=datetime(2022, 1, 2, 14, 45),
            team=1,
        )
        recalc_captain_analytics(ballkid=self.ballkid, year=2022)

        analytics = CaptainAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(self.captain, analytic.captain)
        self.assertEqual(2, analytic.count)
        self.assertEqual(timedelta(hours=5, minutes=44), analytic.duration)

    def test_recalc_captain_analytics_one_history_mult_captains(self):
        Schedule.objects.create(
            team=1,
            court=COURT.STADIUM,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 2, 14, 45),
        )

        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 14, 29),
            team=1,
        )
        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain2,
            start=datetime(2022, 1, 2, 13, 00),
            end=datetime(2022, 1, 2, 14, 45),
            team=1,
        )
        recalc_captain_analytics(ballkid=self.ballkid, year=2022)

        analytics = CaptainAnalytics.objects.all().order_by("captain_id")
        self.assertEqual(2, len(analytics))
        analytic1 = analytics.first()
        self.assertEqual(self.ballkid, analytic1.ballkid)
        self.assertEqual(self.captain, analytic1.captain)
        self.assertEqual(1, analytic1.count)
        self.assertEqual(timedelta(hours=3, minutes=59), analytic1.duration)

        analytic2 = analytics[1]
        self.assertEqual(self.ballkid, analytic2.ballkid)
        self.assertEqual(self.captain2, analytic2.captain)
        self.assertEqual(1, analytic2.count)
        self.assertEqual(timedelta(hours=1, minutes=45), analytic2.duration)

    def test_recalc_captain_analytics_mult_histories_mult_captains(self):
        Schedule.objects.create(
            team=1,
            court=COURT.STADIUM,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 4, 19, 0),
        )

        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 14, 29),
            team=1,
        )  # overlapping time is 3:59
        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=datetime(2022, 1, 2, 13, 00),
            end=datetime(2022, 1, 2, 14, 45),
            team=1,
        )  # overlapping time is 01:45

        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain2,
            start=datetime(2022, 1, 3, 15, 30),
            end=datetime(2022, 1, 3, 15, 39),
            team=1,
        )  # overlapping time is 00:09
        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain2,
            start=datetime(2022, 1, 4, 18, 30),
            end=datetime(2022, 1, 4, 19, 00),
            team=1,
        )  # overlapping time is 00:30
        recalc_captain_analytics(ballkid=self.ballkid, year=2022)

        analytics = CaptainAnalytics.objects.all().order_by("captain_id")
        self.assertEqual(2, len(analytics))
        analytic1 = analytics.first()
        self.assertEqual(self.ballkid, analytic1.ballkid)
        self.assertEqual(self.captain, analytic1.captain)
        self.assertEqual(2, analytic1.count)
        self.assertEqual(timedelta(hours=5, minutes=44), analytic1.duration)

        analytic2 = analytics[1]
        self.assertEqual(self.ballkid, analytic2.ballkid)
        self.assertEqual(self.captain2, analytic2.captain)
        self.assertEqual(2, analytic2.count)
        self.assertEqual(timedelta(minutes=39), analytic2.duration)

    def test_recalc_captain_analytics_many_hours(self):
        Schedule.objects.create(
            team=1,
            court=COURT.STADIUM,
            start=datetime(2022, 1, 1, 5, 30),
            end=datetime(2022, 1, 2, 18, 30),
        )

        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=datetime(2022, 1, 1, 5, 30),
            end=datetime(2022, 1, 1, 23, 30),
            team=1,
        )  # overlapping time is 18:00
        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=datetime(2022, 1, 2, 8, 00),
            end=datetime(2022, 1, 2, 18, 30),
            team=1,
        )  # overlapping time is 10:30
        recalc_captain_analytics(ballkid=self.ballkid, year=2022)

        analytics = CaptainAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(self.captain, analytic.captain)
        self.assertEqual(2, analytic.count)
        self.assertEqual(timedelta(hours=28, minutes=30), analytic.duration)

    def test_recalc_captain_analytics_past_midnight(self):
        start = datetime(2022, 1, 1, 20, 30)
        end = datetime(2022, 1, 2, 2, 30)
        Schedule.objects.create(team=1, court=COURT.STADIUM, start=start, end=end)

        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=start,
            end=end,
            team=1,
        )
        recalc_captain_analytics(ballkid=self.ballkid, year=2022)

        analytics = CaptainAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(self.captain, analytic.captain)
        self.assertEqual(1, analytic.count)
        self.assertEqual(timedelta(hours=6), analytic.duration)

    def test_recalc_captain_analytics_reciprocal_ballkid_captain(self):
        start = datetime(2022, 1, 1, 10, 30)
        end = datetime(2022, 1, 1, 14, 29)
        Schedule.objects.create(team=1, court=COURT.STADIUM, start=start, end=end)

        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=start,
            end=end,
            team=1,
        )
        recalc_captain_analytics(ballkid=self.captain, year=2022)

        analytics = CaptainAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(self.captain, analytic.captain)
        self.assertEqual(1, analytic.count)
        self.assertEqual(timedelta(hours=3, minutes=59), analytic.duration)

    def test_recalc_captain_analytics_reciprocal_two_captains(self):
        start = datetime(2022, 1, 1, 10, 30)
        end = datetime(2022, 1, 1, 14, 29)
        Schedule.objects.create(team=1, court=COURT.STADIUM, start=start, end=end)

        CaptainHistory.objects.create(
            ballkid=self.captain2,
            captain=self.captain,
            start=start,
            end=end,
            team=1,
        )
        CaptainHistory.objects.create(
            ballkid=self.captain,
            captain=self.captain2,
            start=start,
            end=end,
            team=1,
        )
        recalc_captain_analytics(ballkid=self.captain2, year=2022)

        analytics = CaptainAnalytics.objects.all().order_by("ballkid_id")
        self.assertEqual(2, len(analytics))

        analytic1 = analytics.first()
        self.assertEqual(self.captain, analytic1.ballkid)
        self.assertEqual(self.captain2, analytic1.captain)
        self.assertEqual(1, analytic1.count)
        self.assertEqual(timedelta(hours=3, minutes=59), analytic1.duration)

        analytic2 = analytics[1]
        self.assertEqual(self.captain2, analytic2.ballkid)
        self.assertEqual(self.captain, analytic2.captain)
        self.assertEqual(1, analytic2.count)
        self.assertEqual(timedelta(hours=3, minutes=59), analytic2.duration)

    def test_recalc_captain_analytics_reciprocal_ballkid_captain_mult_histories(self):
        Schedule.objects.create(
            team=1,
            court=COURT.STADIUM,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 2, 12, 31),
        )

        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 14, 29),
            team=1,
        )
        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=datetime(2022, 1, 2, 11, 30),
            end=datetime(2022, 1, 2, 12, 31),
            team=1,
        )
        recalc_captain_analytics(ballkid=self.captain, year=2022)

        analytics = CaptainAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(self.captain, analytic.captain)
        self.assertEqual(2, analytic.count)
        self.assertEqual(timedelta(hours=5), analytic.duration)

    def test_recalc_captain_analytics_one_history_one_captain_mult_shifts(self):
        Schedule.objects.create(
            team=1,
            court=COURT.STADIUM,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 11, 30),
        )
        Schedule.objects.create(
            team=1,
            court=COURT.STADIUM,
            start=datetime(2022, 1, 1, 12, 30),
            end=datetime(2022, 1, 1, 13, 30),
        )
        Schedule.objects.create(
            team=1,
            court=COURT.STADIUM,
            start=datetime(2022, 1, 1, 14, 30),
            end=datetime(2022, 1, 1, 15, 30),
        )

        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 14, 29),
            team=1,
        )
        recalc_captain_analytics(ballkid=self.ballkid, year=2022)

        analytics = CaptainAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(self.captain, analytic.captain)
        self.assertEqual(1, analytic.count)
        self.assertEqual(timedelta(hours=2), analytic.duration)

    def test_recalc_captain_analytics_no_overlap(self):
        Schedule.objects.create(
            team=1,
            court=COURT.STADIUM,
            start=datetime(2022, 1, 4, 10, 30),
            end=datetime(2022, 1, 4, 11, 30),
        )
        Schedule.objects.create(
            team=1,
            court=COURT.HARRIS,
            start=datetime(2022, 1, 4, 12, 30),
            end=datetime(2022, 1, 4, 13, 30),
        )

        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 14, 29),
            team=1,
        )
        recalc_captain_analytics(ballkid=self.ballkid, year=2022)

        self.assertEqual(0, len(CaptainAnalytics.objects.all()))

    def test_recalc_captain_analytics_mult_shifts_mult_courts(self):
        Schedule.objects.create(
            team=1,
            court=COURT.STADIUM,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 11, 30),
        )
        Schedule.objects.create(
            team=1,
            court=COURT.HARRIS,
            start=datetime(2022, 1, 1, 12, 30),
            end=datetime(2022, 1, 1, 13, 30),
        )
        Schedule.objects.create(
            team=1,
            court=COURT.GRANDSTAND,
            start=datetime(2022, 1, 1, 14, 30),
            end=datetime(2022, 1, 1, 15, 30),
        )

        CaptainHistory.objects.create(
            ballkid=self.ballkid,
            captain=self.captain,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 14, 29),
            team=1,
        )
        recalc_captain_analytics(ballkid=self.ballkid, year=2022)

        analytics = CaptainAnalytics.objects.all()
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(self.captain, analytic.captain)
        self.assertEqual(1, analytic.count)
        self.assertEqual(timedelta(hours=2), analytic.duration)

    def test_recalc_court_analytics_one_team_one_shift(self):
        TeamHistory.objects.create(
            ballkid=self.ballkid,
            team=1,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 14, 29),
        )
        Schedule.objects.create(
            team=1, court=COURT.STADIUM, start=datetime(2022, 1, 1, 10, 00)
        )
        recalc_court_analytics(ballkid=self.ballkid, year=2022)

        analytics = CourtAnalytics.objects.filter(duration__gt=timedelta())
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(1, analytic.count)
        self.assertEqual(COURT.STADIUM, analytic.court)
        self.assertEqual(timedelta(minutes=30), analytic.duration)

    def test_recalc_court_analytics_one_team_one_shift_recalc_all(self):
        TeamHistory.objects.create(
            ballkid=self.ballkid,
            team=1,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 14, 29),
        )
        Schedule.objects.create(
            team=1, court=COURT.STADIUM, start=datetime(2022, 1, 1, 10, 00)
        )
        recalc_court_analytics(year=2022)

        analytics = CourtAnalytics.objects.all()
        self.assertEqual(20, len(analytics))
        filtered = analytics.filter(duration__gt=timedelta())
        self.assertEqual(1, len(filtered))

    def test_recalc_court_analytics_one_team_one_shift_empty_end(self):
        TeamHistory.objects.create(
            ballkid=self.ballkid,
            team=1,
            start=datetime(2022, 1, 1, 10, 30),
        )
        Schedule.objects.create(
            team=1, court=COURT.STADIUM, start=datetime(2022, 1, 1, 10, 00)
        )
        recalc_court_analytics(
            ballkid=self.ballkid, now=datetime(2022, 1, 1, 15, 00), year=2022
        )

        analytics = CourtAnalytics.objects.filter(duration__gt=timedelta())
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(1, analytic.count)
        self.assertEqual(COURT.STADIUM, analytic.court)
        self.assertEqual(timedelta(minutes=30), analytic.duration)

    def test_recalc_court_analytics_one_team_mult_shifts(self):
        TeamHistory.objects.create(
            ballkid=self.ballkid,
            team=1,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 15, 30),
        )
        Schedule.objects.create(
            team=1, court=COURT.STADIUM, start=datetime(2022, 1, 1, 10, 00)
        )
        Schedule.objects.create(
            team=1, court=COURT.HARRIS, start=datetime(2022, 1, 1, 12, 00)
        )
        Schedule.objects.create(
            team=2, court=COURT.GRANDSTAND, start=datetime(2022, 1, 1, 11, 00)
        )
        recalc_court_analytics(ballkid=self.ballkid, year=2022)

        analytics = CourtAnalytics.objects.filter(duration__gt=timedelta())
        self.assertEqual(2, len(analytics))
        analytic, created = analytics.get_or_create(court=COURT.STADIUM)
        self.assertFalse(created)
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(1, analytic.count)
        self.assertEqual(timedelta(minutes=30), analytic.duration)

        analytic, created = analytics.get_or_create(court=COURT.HARRIS)
        self.assertFalse(created)
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(1, analytic.count)
        self.assertEqual(timedelta(minutes=60), analytic.duration)

    def test_recalc_court_analytics_one_team_mult_count(self):
        TeamHistory.objects.create(
            ballkid=self.ballkid,
            team=1,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 15, 30),
        )
        Schedule.objects.create(
            team=1, court=COURT.STADIUM, start=datetime(2022, 1, 1, 10, 00)
        )
        Schedule.objects.create(
            team=1, court=COURT.STADIUM, start=datetime(2022, 1, 1, 15, 00)
        )
        recalc_court_analytics(ballkid=self.ballkid, year=2022)

        analytics = CourtAnalytics.objects.filter(duration__gt=timedelta())
        self.assertEqual(1, len(analytics))
        analytic, created = analytics.get_or_create(court=COURT.STADIUM)
        self.assertFalse(created)
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(2, analytic.count)
        self.assertEqual(timedelta(hours=1), analytic.duration)

    def test_recalc_court_analytics_mult_team_mult_courts(self):
        TeamHistory.objects.create(
            ballkid=self.ballkid,
            team=1,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 15, 30),
        )
        TeamHistory.objects.create(
            ballkid=self.ballkid,
            team=2,
            start=datetime(2022, 1, 1, 15, 30),
            end=datetime(2022, 1, 1, 20, 00),
        )
        Schedule.objects.create(
            team=1, court=COURT.STADIUM, start=datetime(2022, 1, 1, 10, 00)
        )
        Schedule.objects.create(
            team=1, court=COURT.HARRIS, start=datetime(2022, 1, 1, 15, 00)
        )
        Schedule.objects.create(
            team=1, court=COURT.GRANDSTAND, start=datetime(2022, 1, 1, 18, 00)
        )
        Schedule.objects.create(
            team=2, court=COURT.FOUR, start=datetime(2022, 1, 1, 15, 00)
        )
        Schedule.objects.create(
            team=2, court=COURT.FIVE, start=datetime(2022, 1, 1, 19, 00)
        )
        recalc_court_analytics(ballkid=self.ballkid, year=2022)

        analytics = CourtAnalytics.objects.filter(duration__gt=timedelta())
        self.assertEqual(4, len(analytics))

        analytic, created = analytics.get_or_create(court=COURT.STADIUM)
        self.assertFalse(created)
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(1, analytic.count)
        self.assertEqual(timedelta(minutes=30), analytic.duration)

        analytic, created = analytics.get_or_create(court=COURT.HARRIS)
        self.assertFalse(created)
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(1, analytic.count)
        self.assertEqual(timedelta(minutes=30), analytic.duration)

        analytic, created = analytics.get_or_create(court=COURT.FOUR)
        self.assertFalse(created)
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(1, analytic.count)
        self.assertEqual(timedelta(minutes=30), analytic.duration)

        analytic, created = analytics.get_or_create(court=COURT.FIVE)
        self.assertFalse(created)
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(1, analytic.count)
        self.assertEqual(timedelta(hours=1), analytic.duration)

    def test_recalc_court_analytics_one_team_one_shift_not_yet_occurred(self):
        TeamHistory.objects.create(
            ballkid=self.ballkid,
            team=1,
            start=datetime(2022, 1, 1, 8, 30),
            end=datetime(2022, 1, 1, 9, 30),
        )
        Schedule.objects.create(
            team=1, court=COURT.STADIUM, start=datetime(2022, 1, 1, 10, 00)
        )
        recalc_court_analytics(ballkid=self.ballkid, year=2022)

        analytics = CourtAnalytics.objects.filter(duration__gt=timedelta())
        self.assertEqual(0, len(analytics))

    def test_recalc_court_analytics_one_team_one_shift_not_yet_occurred_empty_end(self):
        TeamHistory.objects.create(
            ballkid=self.ballkid,
            team=1,
            start=datetime(2022, 1, 1, 8, 30),
        )
        Schedule.objects.create(
            team=1, court=COURT.STADIUM, start=datetime(2022, 1, 1, 10, 00)
        )
        recalc_court_analytics(
            ballkid=self.ballkid, now=datetime(2022, 1, 1, 9, 30), year=2022
        )

        analytics = CourtAnalytics.objects.filter(duration__gt=timedelta())
        self.assertEqual(0, len(analytics))

    def test_recalc_court_analytics_one_team_one_shift_short_shifted(self):
        TeamHistory.objects.create(
            ballkid=self.ballkid,
            team=1,
            start=datetime(2022, 1, 1, 10, 30),
            end=datetime(2022, 1, 1, 14, 29),
        )
        Schedule.objects.create(
            team=1,
            court=COURT.STADIUM,
            start=datetime(2022, 1, 1, 10, 00),
            end=datetime(2022, 1, 1, 10, 45),
        )
        recalc_court_analytics(ballkid=self.ballkid, year=2022)

        analytics = CourtAnalytics.objects.filter(duration__gt=timedelta())
        self.assertEqual(1, len(analytics))
        analytic = analytics.first()
        self.assertEqual(self.ballkid, analytic.ballkid)
        self.assertEqual(1, analytic.count)
        self.assertEqual(COURT.STADIUM, analytic.court)
        self.assertEqual(timedelta(minutes=15), analytic.duration)
