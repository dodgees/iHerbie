import unittest
from iHerbieReplacement import cleanStatusText

class TestHerbieMethods(unittest.TestCase):
    def test_cleanStatus_Text(self):
        status = "RT @ProFootballHOF: The order of #PFHOF15 enshrinement is ... http://t.co/bsT6CXYVHW"
        self.assertEqual(cleanStatusText(status), "The order of PFHOF15 enshrinement is ...")
        status2 = "How cool is that! Last guy didn't even want the #Blackshirts ,this ones down to #ThrowTheBones !  #Huskers #GBR"
        self.assertEqual(cleanStatusText(status2), "How cool is that! Last guy didn't even want the Blackshirts ,this ones down to ThrowTheBones !  Huskers GBR")
        status3 = "@Huskers got a great one in @PhilBeckner ... A huge part of my success and progress as a man. He's a handful but he's  worth it lol"
        self.assertEqual(cleanStatusText(status3), "Huskers got a great one in PhilBeckner ... A huge part of my success and progress as a man. He's a handful but he's  worth it lol")
        status4 = "Welcome our new Assistant Coach @PhilBeckner  http://go.unl.edu/beckner080115 ."
        self.assertEqual(cleanStatusText(status4), "Welcome our new Assistant Coach PhilBeckner   .")

suite = unittest.TestLoader().loadTestsFromTestCase(TestHerbieMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
# if __name__ == '__main__':
#     unittest.main()
