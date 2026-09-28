import unittest
from analyze import DAY, newcombe, retained, summarize, wilson


class AnalysisTests(unittest.TestCase):
    def test_wilson_extreme_and_balanced_known_intervals(self):
        lo,hi=wilson(0,10)
        self.assertAlmostEqual(lo,0)
        self.assertAlmostEqual(hi,0.2775328,places=6)
        lo,hi=wilson(50,100)
        self.assertAlmostEqual(lo,0.4038315,places=6)
        self.assertAlmostEqual(hi,0.5961685,places=6)
        with self.assertRaises(ValueError): wilson(0,0)

    def test_newcombe_antisymmetry_and_zero_difference(self):
        a=newcombe(3,10,7,20); b=newcombe(7,20,3,10)
        self.assertAlmostEqual(a[0],-b[1])
        self.assertAlmostEqual(a[1],-b[0])
        lo,hi=newcombe(5,10,5,10)
        self.assertLess(lo,0); self.assertGreater(hi,0)

    def test_outcome_is_half_open_and_not_ever_active(self):
        self.assertFalse(retained([6*DAY,14*DAY],0))
        self.assertTrue(retained([7*DAY],0))
        self.assertTrue(retained([14*DAY-1],0))

    def test_late_bind_moves_to_none_in_prespecified_sensitivity(self):
        cohort = [dict(handle=str(i), registered=0, first_bind=bind, arm=arm)
                  for i, (bind, arm) in enumerate([(1,'door'), (5000,'sought'),
                                                   (None,'none'), (8*DAY,'sought')])]
        activity = {'3':[9*DAY]}
        primary=summarize(cohort,activity)
        sensitivity=summarize(cohort,activity,censor=True)
        self.assertEqual(primary['arms']['sought']['retained'],1)
        self.assertEqual(sensitivity['arms']['sought']['retained'],0)
        self.assertEqual(sensitivity['arms']['none']['n'],2)
        self.assertEqual(sensitivity['arms']['none']['retained'],1)
