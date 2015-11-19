from unittest import TestCase

from . import logs

class TestSteinacherParser(TestCase):
    card_string_key = 'card_string'

    valid_game = {
        "schupf":[[0,33,43,21],[13,0,32,50],[52,29,0,41],[15,53,4,0]],
        'card_string':{
            "1":"Hu","2":"Ma","3":"R2","4":"B2","5":"G2","6":"S2","7":"R3",
            "8":"B3","9":"G3","10":"S3","11":"R4","12":"B4","13":"G4","14":"S4",
            "15":"R5","16":"B5","17":"G5","18":"S5","19":"R6","20":"B6",
            "21":"G6","22":"S6","23":"R7","24":"B7","25":"G7","26":"S7",
            "27":"R8","28":"B8","29":"G8","30":"S8","31":"R9","32":"B9",
            "33":"G9","34":"S9","35":"R10","36":"B10","37":"G10","38":"S10",
            "39":"RB","40":"BB","41":"GB","42":"SB","43":"RD","44":"BD",
            "45":"GD","46":"SD","47":"RK","48":"BK","49":"GK","50":"SK",
            "51":"RA","52":"BA","53":"GA","54":"SA","55":"Ph","56":"Dr"
            },
        "views":[
            {
                "state":"1",
                "hand":[
                    [52,38,28,30,17,14,2,1,36,35,26,22,15,13],
                    [48,47,33,23,18,11,9,8,53,46,39,29,16,10],
                    [55,54,43,42,32,34,24,7,49,44,20,12,5,4],
                    [51,50,41,40,27,21,19,3,56,45,37,31,25,6]
                    ],
                "tisch":[[],[],[],[]],
                "tichu":[],
                "tichu_gross":["2"],
                "mitteilung":"LucyBotwin sagt GROSSES Tichu! "}],
        "nsteps":1
        }

    int_keys_valid_card_string = {
        1:"Hu",2:"Ma",3:"R2",4:"B2",5:"G2",6:"S2",7:"R3",
        8:"B3",9:"G3",10:"S3",11:"R4",12:"B4",13:"G4",14:"S4",
        15:"R5",16:"B5",17:"G5",18:"S5",19:"R6",20:"B6",
        21:"G6",22:"S6",23:"R7",24:"B7",25:"G7",26:"S7",
        27:"R8",28:"B8",29:"G8",30:"S8",31:"R9",32:"B9",
        33:"G9",34:"S9",35:"R10",36:"B10",37:"G10",38:"S10",
        39:"RB",40:"BB",41:"GB",42:"SB",43:"RD",44:"BD",
        45:"GD",46:"SD",47:"RK",48:"BK",49:"GK",50:"SK",
        51:"RA",52:"BA",53:"GA",54:"SA",55:"Ph",56:"Dr"
        }

    translated_valid_card_string = {
        1:"D", 2:"1",
        3:"2T", 4:"2P", 5:"2E", 6:"2S", 7:"3T", 8:"3P", 9:"3E", 10:"3S",
        11:"4T", 12:"4P", 13:"4E", 14:"4S", 15:"5T", 16:"5P", 17:"5E", 18:"5S",
        19:"6T", 20:"6P", 21:"6E", 22:"6S", 23:"7T", 24:"7P", 25:"7E", 26:"7S",
        27:"8T", 28:"8P", 29:"8E", 30:"8S", 31:"9T", 32:"9P", 33:"9E", 34:"9S",
        35:"0T", 36:"0P", 37:"0E", 38:"0S", 39:"JT", 40:"JP", 41:"JE", 42:"JS",
        43:"QT", 44:"QP", 45:"QE", 46:"QS", 47:"KT", 48:"KP", 49:"KE", 50:"KS",
        51:"AT", 52:"AP", 53:"AE", 54:"AS",
        55:"P", 56:"R",
        }

    replaced_valid_hands = [
        ["AP","0S","8P","8S","SE","4S","1", "D", "0P","0T","7S","6S","5T","4E"],
        ["KP","KT","9E","7T","5S","4T","3E","3P","AE","QS","JT","8E","5P","3S"],
        ["P", "AS","QT","JS","9P","9S","7P","3T","KE","QP","6P","4P","2E","2P"],
        ["AT","KS","JE","JP","8T","6E","6T","2T","R", "QE","0E","9T","7E","2S"],
        ]

    def test_valid_input(self):
        self.parser = logs.SteinacherParser(self.valid_game)
        game = self.parser.game
        self.parser.pre_translate_card_string()
        self.assertEqual(
            self.int_keys_valid_card_string,
            game[self.card_string_key]
            )
        self.parser.translate_card_string()
        self.assertEqual(
            self.translated_valid_card_string,
            game[self.parser.card_string_key]
            )
        self.parser.replace_cards()
        self.assertEqual(
            self.replaced_valid_hands,
            game[self.parser.states_key][self.parser.hands_key]
            )
