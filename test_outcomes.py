import unittest
from outcomes import advance


class CursorTests(unittest.TestCase):
    def test_finished_stream_is_silenced_without_reinitializing_other(self):
        page = {'has_more_streams':['comments'], 'continuation_covers':['posts','comments'],
                'next_posts_since':'id:123', 'next_comments_since':'snapi:900:500'}
        self.assertEqual(advance(page, {'posts':'snapi:123:100','comments':'init'}),
                         {'posts':'done','comments':'snapi:900:500'})

    def test_incomplete_coverage_and_stalled_cursor_fail(self):
        page = {'has_more_streams':['comments'], 'continuation_covers':[],
                'next_posts_since':'done','next_comments_since':'snapi:900:500'}
        with self.assertRaises(ValueError):
            advance(page, {'posts':'done','comments':'snapi:900:500'})
        page['continuation_covers'] = ['comments']
        with self.assertRaises(ValueError):
            advance(page, {'posts':'done','comments':'snapi:900:500'})
