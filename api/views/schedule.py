from datetime import timedelta, datetime
from django.shortcuts import render
from django.db.models import Max
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import *
from rest_framework.permissions import IsAuthenticated
from api.permissions import *


class GetSchedule(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        param = self.request.query_params.get("day")
        if param == "":
            day = datetime.now()
        else:
            day = datetime.strptime(param, "%m/%d/%Y")
        start_hour = datetime(year=day.year, month=day.month, day=day.day, hour=8)
        end_hour = start_hour + timedelta(days=1)

        return Schedule.objects.filter(
            day_hour__gte=start_hour, day_hour__lt=end_hour
        ).order_by("id")


class CreateSchedule(APIView):
    permission_classes = [IsChairperson]

    def post(self, request, format=None):
        start_hour = datetime.strptime(
            f"{request.data['day']} {request.data['start_hour']}",
            "%m/%d/%Y %H:%M",
        )
        num_teams = request.data["num_teams"]
        num_hours = request.data["num_hours"]
        num_courts = request.data["num_courts"]
        courts = [x[0] for x in Court.choices][:num_courts]

        team_index = 0
        for hour_index in range(num_hours):
            hour = start_hour + timedelta(hours=hour_index)
            for court in courts:
                shift = Schedule(
                    day_hour=hour,
                    team=(team_index % num_teams) + 1,
                    court=court,
                )
                shift.save()

                team_index += 1
            if team_index % num_teams == 0:
                courts = courts[-1:] + courts[:-1]

        return Response(
            {"Success": f"Created schedule starting at {start_hour}"},
            status=status.HTTP_200_OK,
        )


class AddHour(APIView):
    permission_classes = [IsChairperson]

    def post(self, request, format=None):
        day = datetime.strptime(request.data["day"], "%m/%d/%Y")
        start_hour = datetime(year=day.year, month=day.month, day=day.day, hour=8)
        end_hour = start_hour + timedelta(days=1)
        shifts = Schedule.objects.filter(day_hour__gte=start_hour, day_hour__lt=end_hour)

        max_hour = shifts.aggregate(max=Max("day_hour"))["max"]
        next_hour = max_hour + timedelta(hours=1)

        for court in Court.choices:
            shift = Schedule(
                day_hour=next_hour,
                court=court[0],
            )
            shift.save()

        return Response(
            {"Success": f"Added hour at {next_hour}"}, status=status.HTTP_200_OK
        )


class UpdateSchedule(APIView):
    permission_classes = [IsChairperson]

    def patch(self, request, format=None):
        try:
            day = request.data["day"]
            hour = request.data["hour"]
            day_hour = datetime.strptime(f"{day} {hour}", "%m/%d/%Y %I%p")
            if "am" in hour.lower():
                day_hour += timedelta(days=1)

            court = request.data["court"]
            team = 0 if request.data["team"] == "" else int(request.data["team"])

            shift = Schedule.objects.get(day_hour=day_hour, court=court)
            shift.team = team
            shift.save()

            return Response(
                {"Success": f"Updated team to {team} at {day_hour} on {court}"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"Invalid schedule update": f"Error: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ShowTeams(APIView):
    permission_classes = [IsChairpersonOrAuthenticatedReadOnly]

    def get(self, request, format=None):
        tournament = Tournament.objects.get(year=2023)
        return Response({"show_teams": tournament.show_teams}, status=status.HTTP_200_OK)

    def patch(self, request, format=None):
        show_teams = request.data["show_teams"]

        tournament = Tournament.objects.get(year=2023)
        tournament.show_teams = show_teams
        tournament.save()

        return Response(
            {"Success": f"Updated show teams status to {show_teams}"},
            status=status.HTTP_200_OK,
        )


class ShowFinalsTeams(APIView):
    permission_classes = [IsChairpersonOrAuthenticatedReadOnly]

    def get(self, request, format=None):
        tournament = Tournament.objects.get(year=2023)
        return Response(
            {"show_finals_teams": tournament.show_finals_teams}, status=status.HTTP_200_OK
        )

    def patch(self, request, format=None):
        show_finals_teams = request.data["show_finals_teams"]

        tournament = Tournament.objects.get(year=2023)
        tournament.show_finals_teams = show_finals_teams
        tournament.save()

        return Response(
            {"Success": f"Updated show finals teams status to {show_finals_teams}"},
            status=status.HTTP_200_OK,
        )
