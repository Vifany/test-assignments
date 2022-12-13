import random
import math

TIMESTAMPS_COUNT = 50000

PROBABILITY_SCORE_CHANGED = 0.0001

PROBABILITY_HOME_SCORE = 0.45

OFFSET_MAX_STEP = 3

INITIAL_STAMP = {
    "offset": 0,
    "score": {
        "home": 0,
        "away": 0
    }
}


def generate_stamp(previous_value):
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED
    home_score_change = 1 if score_changed and random.random() > 1 - \
        PROBABILITY_HOME_SCORE else 0
    away_score_change = 1 if score_changed and not home_score_change else 0
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change
        }
    }


def generate_game():
    stamps = [INITIAL_STAMP, ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps


def get_score(game_stamps, offset):
    '''
        Takes list of game's stamps and time offset for which returns
        the scores for the home and away teams.
        Parameters:
            game_stamps (list[dict]): list of dicts with game's stamps
            offset (int): target offset
        Return:
            home (int): home score
            away (int): away score
    '''
    if offset<0:
        raise ValueError('Offset should be postive integer.')

    if offset >= game_stamps[-1]['offset']:
        #If offset is after or at the end of game
        home, away = (
            game_stamps[-1]['score']['home'],
            game_stamps[-1]['score']['away']
        )
    elif offset == 0:
        #If offset is at begining or before game
        home, away = (
            game_stamps[0]['score']['home'],
            game_stamps[0]['score']['away']
        )
    else:
        end = len(game_stamps)
        start = 0
        last = None
        while end >= start:
            #Simple binary search
            mid = int((end+start)/2)
            if game_stamps[mid]['offset'] < offset:
                start = mid + 1
                last = game_stamps[mid]
            elif game_stamps[mid]['offset'] > offset:
                end = mid - 1
            else:
                home, away = (
                    game_stamps[mid]['score']['home'],
                    game_stamps[mid]['score']['away']
                )
                break
        else:
            #In case nothing exact was found return closest lower
            home, away = (
                last['score']['home'],
                last['score']['away']
            )

    return home, away
