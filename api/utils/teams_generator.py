from api.models.ballkid import *
from api.utils.consts import *

from django.db.models import Q

import random

# import math


# def get_smallest_team(all_teams, court=None):
#     if court is None:
#         teams = {key: val for key, val in all_teams.items()}
#     else:
#         teams = {key: val for key, val in all_teams.items() if key[0] == court}

#     min_key = None
#     min_val = None

#     for key, val in teams.items():
#         if min_val is None or len(val) < len(min_val):
#             min_key = key
#             min_val = val

#     return {"court": min_key[0], "rotation": min_key[1], "count": len(min_val)}


# def get_ballkids_order(ballkids):
#     """
#     Generate order of checked in, unassigned ballkids
#     (random descending years experience with top xx% or
#     xx people randomized)
#     """
#     ballkids = ballkids.order_by("?").order_by("-num_years_experience")
#     num_top = max(NUM_TOP_TO_RANDOMIZE, int(ballkids.count() * PERCENT_TOP_TO_RANDOMIZE))
#     top_ballkids = list(ballkids)[:num_top]
#     random.shuffle(top_ballkids)
#     bottom_ballkids = list(ballkids)[num_top:]

#     ballkids = top_ballkids + bottom_ballkids
#     return ballkids


# def assign_max_experience_courts(teams, max_experience, rotations, avg_ballkids_per_team):
#     # Get order of courts by reverse sort of max experience
#     courts = sorted(max_experience, key=max_experience.get)

#     # For each court with a max experience provided
#     for court in courts:
#         for rotation in rotations:
#             # If team is already full, then continue
#             if len(teams[(court, rotation)]) >= avg_ballkids_per_team - 1:
#                 continue

#             # Get all ballkids already assigned in teams
#             assigned = set(sum(teams.values(), []))

#             # Greedily and randomly assign ballkids with this max experience.
#             # Filter to ballkids with <= max experience who are not yet assigned
#             max_experience_ballkids = list(
#                 set(
#                     Ballkid.objects.filter(
#                         is_checked_in=True,
#                         num_years_experience__lte=max_experience[court],
#                     )
#                 )
#                 - assigned
#             )

#             # If not enough ballkids, then assign as many as possible
#             if len(max_experience_ballkids) < avg_ballkids_per_team:
#                 sampled = max_experience_ballkids

#             # If enough ballkids, randomly choose ballkids
#             else:
#                 sampled = random.sample(max_experience_ballkids, avg_ballkids_per_team)

#             # Assign ballkids to team (court and rotation)
#             teams[(court, rotation)] = sampled

#     return teams


# def assign_remaining_ballkids(teams, ballkids_order, courts_order, avg_ballkids_per_team):
#     # Court index for courts order
#     index = 0

#     for ballkid in ballkids_order:
#         # If ballkid already has a court assigned, continue
#         if any(ballkid in val for val in teams.values()):
#             continue

#         # Keep track of the court index that we start with to break if we
#         # do a full loop
#         start_index = index
#         should_continue = False

#         # While the current court is full, continue on to the next court
#         while (
#             get_smallest_team(teams, courts_order[index])["count"]
#             >= avg_ballkids_per_team
#         ):
#             # Continue to the next court
#             index = (index + 1) % len(courts_order)

#             if index == start_index:
#                 if (
#                     get_smallest_team(teams, courts_order[index])["count"]
#                     >= MAX_BALLKIDS_PER_TEAM
#                 ):
#                     should_continue = True
#                 break

#         if should_continue:
#             continue

#         # Assign court and rotation to the current ballkid
#         court = courts_order[index]
#         rotation = get_smallest_team(teams, court)["rotation"]
#         teams[(court, rotation)].append(ballkid)

#         # Update court index
#         index = (index + 1) % len(courts_order)

#     return teams


# def create_teams(courts, should_recreate, balance_coeff, max_experience):
#     ballkids = Ballkid.objects.filter(is_checked_in=True)
#     rotations = get_rotations(ballkids, courts)
#     avg_ballkids_per_team = math.ceil(ballkids.count() / len(rotations) / len(courts))

#     ballkids_order = get_ballkids_order(ballkids)
#     courts_order = get_courts_order(courts, balance_coeff, max_experience)

#     # Start with empty teams
#     teams = {(court, rotation): [] for court in courts for rotation in rotations}

#     # If not recreating teams, then seed teams with the current
#     # teams for which courts are still active
#     if not should_recreate:
#         for ballkid in Ballkid.objects.exclude(court=""):
#             key = (ballkid.court, ballkid.rotation)
#             if key in teams and len(teams[key]) < avg_ballkids_per_team:
#                 teams[key].append(ballkid)

#     # Assign ballkids to courts with max experience provided
#     teams = assign_max_experience_courts(
#         teams, max_experience, rotations, avg_ballkids_per_team
#     )

#     teams = assign_remaining_ballkids(
#         teams, ballkids_order, courts_order, avg_ballkids_per_team
#     )

#     return teams


# def assign_unassigned():
#     ballkids = Ballkid.objects.filter(is_checked_in=True, current_team=0).order_by(
#         "is_chairperson", "is_captain", "-num_years_experience"
#     )


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
        self.teams = [Team(i + 1) for i in range(num_teams)]

    def get_smallest_team(self, position=None):
        smallest_team = self.teams[0]
        for team in self.teams:
            if team.size(position) < smallest_team.size(position):
                smallest_team = team

        return smallest_team

    def get_team_without_experienced_position(self, position):
        eligible_teams = [
            team for team in self.teams if not team.has_experienced(position)
        ]
        return eligible_teams[0] if len(eligible_teams) > 0 else None

    def create_teams(self):
        all = Ballkid.objects.filter(is_checked_in=True)
        captains = all.filter(Q(is_chairperson=True) | Q(is_captain=True))
        supervets = list(
            all.exclude(Q(is_chairperson=True) | Q(is_captain=True)).filter(
                num_years_experience__gt=SUPERVET_THRESHOLD
            )
        )
        ballkids = list(
            all.exclude(Q(is_chairperson=True) | Q(is_captain=True))
            .filter(num_years_experience__lte=SUPERVET_THRESHOLD)
            .order_by("-num_years_experience")
        )

        team_counter = 0

        for pos in [POSITION.N, POSITION.B]:
            # Get all captains at that position and shuffle them
            position_captains = list(captains.filter(position=pos))
            random.shuffle(position_captains)

            # For each captain, assign them to a team
            for captain in position_captains:
                team = self.teams[team_counter]
                team.add_ballkid(captain)

                # Increment team counter
                team_counter = (team_counter + 1) % len(self.teams)

        random.shuffle(supervets)
        for supervet in supervets:
            team = self.get_team_without_experienced_position(supervet.position)
            if team is None:
                team = self.get_smallest_team()

            team.add_ballkid(supervet)

        for ballkid in ballkids:
            team = self.get_smallest_team()
            team.add_ballkid(ballkid)

        return self.teams

    def __repr__(self):
        return str([team for team in self.teams])
