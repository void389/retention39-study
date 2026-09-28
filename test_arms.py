import unittest
from arms import assign


class ArmTests(unittest.TestCase):
    def test_first_bind_global_gap_and_exclusive_cutoff(self):
        citizens = [{'citizen_id': i, 'handle': str(i), 'created_at': 100} for i in range(5)]
        citizens[4]['created_at'] = 200
        events = [{'citizen_id': i, 'kind': 'key-bind', 'created_at': t}
                  for i, t in [(0, 101), (0, 999), (1, 102), (2, 120), (4, 203)]]
        result = assign(citizens, events, 100, 200)
        self.assertEqual(result['boundary']['low_ms'], 3)
        self.assertEqual([r['arm'] for r in result['cohort']], ['door', 'door', 'sought', 'none'])
        self.assertEqual(result['cohort'][0]['first_bind'], 101)

    def test_insufficient_data_is_not_an_invented_threshold(self):
        with self.assertRaises(ValueError):
            assign([], [], 0, 100)


if __name__ == '__main__':
    unittest.main()
