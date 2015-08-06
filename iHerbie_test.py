import unittest
from iHerbieReplacement import cleanStatusText

class TestHerbieMethods(unittest.TestCase):
    def test_cleanStatus_Text(self):
        status = "RT @ProFootballHOF: The order of #PFHOF15 enshrinement is ... http://t.co/bsT6CXYVHW"
        self.assertEqual(cleanStatusText(status), "The order of PFHOF15 enshrinement is ...")


suite = unittest.TestLoader().loadTestsFromTestCase(TestHerbieMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
# if __name__ == '__main__':
#     unittest.main()
