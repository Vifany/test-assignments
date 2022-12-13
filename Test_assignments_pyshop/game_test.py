'''
Test module
'''


import unittest
import game


TEST_GAME = (
    {
    "offset": 0,
    "score": {
        "home": 0,
        "away": 0
    }
    },
    {
    "offset": 150,
        "score": {
            "home": 1,
            "away": 2
        }
    },
    {
    "offset": 1550,
        "score": {
            "home": 7,
            "away": 40
        }
    }
)

class TestGameGetScore(unittest.TestCase):
    'Test class'

    def test_game_get_score_existing(self):
        '''
        Test existing offsets in game case
        '''
        for test_case in TEST_GAME:
            actual = game.get_score(TEST_GAME, test_case['offset'])
            expected = (
            test_case['score']['home'],
            test_case['score']['away']
            )
            self.assertEqual(actual, expected)

    def test_game_get_score_offset(self):
        '''
        Test offset values with offset from existing
        '''
        for test_case in TEST_GAME:
            actual = game.get_score(TEST_GAME, test_case['offset']+5)
            expected = (
            test_case['score']['home'],
            test_case['score']['away']
            )
            self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
