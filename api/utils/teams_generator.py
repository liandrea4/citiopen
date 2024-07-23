from api.models.ballkid import *
from api.utils.consts import *

from django.db.models import Q

import math


class Team:
    def __init__(self, num):
        self.number = num
        self.ballkids = {position: [] for position in [POSITION.N, POSITION.B]}
        self.experienced = {position: [] for position in [POSITION.N, POSITION.B]}

    def get_number(self):
        return self.number

    def get_ballkids(self):
        return self.ballkids[POSITION.N] + self.ballkids[POSITION.B]

    def size(self, position=None):
        if position is None:
            return len(self.get_ballkids())
        else:
            return len(self.ballkids[position])

    def has_experienced(self, position):
        return len(self.experienced[position]) > 0

    def add_ballkid(self, ballkid):
        position = ballkid.position

        self.ballkids[position].append(ballkid)

        if (
            ballkid.is_captain
            or ballkid.is_chairperson
            or ballkid.num_years_experience > SUPERVET_THRESHOLD
        ):
            self.experienced[position].append(ballkid)

    def __repr__(self):
        return str(
            [
                f"{ballkid.first_name} {ballkid.last_name}"
                for ballkid in self.get_ballkids()
            ]
        )


class TeamsGenerator:
    def __init__(self, num_teams):
        # If number of teams is less than 10, then naively create an order
        if num_teams < len(TEAMS_STRENGTH_ORDER):
            self.teams = [Team(i + 1) for i in range(num_teams)]

        # Otherwise if number of teams is >= 10, then use predefined strength order
        # and tack on extra teams at the end
        else:
            self.teams = [
                Team(i)
                for i in TEAMS_STRENGTH_ORDER
                + [
                    i + len(TEAMS_STRENGTH_ORDER) + 1
                    for i in range(num_teams - len(TEAMS_STRENGTH_ORDER))
                ]
            ]

    """
    Returns the smallest team in the list of teams. 

    Arguments: 
    position(str): If position is not None, then returns the team with the fewest 
    number of ballkids at that position
    max_size(int): if max_size is not None, then will not return a team which already 
    has the max number of ballkids 
    """

    def get_smallest_team(self, position=None, max_size=None):
        # Keep track of both the smallest team and the team with the fewest ballkids at
        # the position of interest
        smallest_team = self.teams[0]
        smallest_position_team = self.teams[0]

        for team in self.teams:
            # Update smallest team
            if team.size() < smallest_team.size():
                smallest_team = team

            # Update team with the fewest ballkids at position of interest
            if team.size(position) < smallest_position_team.size(position):
                smallest_position_team = team

        # If the smallest position team is already too large, then return the
        # smallest team instead
        if max_size and smallest_position_team.size() >= max_size:
            return smallest_team

        return smallest_position_team

    def get_team_without_experienced_position(self, position):
        eligible_teams = [
            team for team in self.teams if not team.has_experienced(position)
        ]
        return eligible_teams[0] if len(eligible_teams) > 0 else None

    def create_teams(self):
        all = Ballkid.objects.filter(is_checked_in=True)
        max_ballkids_per_team = math.ceil(len(all) / len(self.teams))

        captains = all.filter(Q(is_chairperson=True) | Q(is_captain=True))
        supervets = (
            all.exclude(id__in=captains)
            .filter(num_years_experience__gt=0)
            .filter(
                Q(num_years_experience__gt=SUPERVET_THRESHOLD) | Q(is_out_of_town=True)
            )
            .order_by("?")
        )

        ballkids = list(
            all.exclude(id__in=captains)
            .exclude(id__in=supervets)
            .order_by("-num_years_experience")
        )

        team_counter = 0

        for pos in [POSITION.N, POSITION.B]:
            # Get all captains at that position and shuffle them
            position_captains = captains.filter(position=pos).order_by("?")

            # For each captain, assign them to a team
            for captain in position_captains:
                team = self.teams[team_counter]
                team.add_ballkid(captain)

                # Increment team counter
                team_counter = (team_counter + 1) % len(self.teams)

        for supervet in supervets:
            team = self.get_team_without_experienced_position(supervet.position)
            if team is None:
                team = self.get_smallest_team(supervet.position)

            team.add_ballkid(supervet)

        for ballkid in ballkids:
            team = self.get_smallest_team(
                ballkid.position, max_size=max_ballkids_per_team
            )
            team.add_ballkid(ballkid)

        return self.teams

    def __repr__(self):
        return str([team for team in self.teams])
