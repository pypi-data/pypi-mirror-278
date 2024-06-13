import re
import datetime
import scipy.stats as ss



# code below may not be the most readable but it's certainly not clear 



class CA:

    def __init__(self, plik, name, token=None):

        self.plik = plik
        self.name = name
        self.token = token                # for integration with lichess API, not yet done but will add soon tho




###########                                       FUNCTIONS RELATED TO SIMPLE GAME-MANIPULATION OPERATIONS             ###########



# best and only way to get all games from the file
    def pure_moves(self) -> list:

        """"

        Returns all games from file in pure move format.
        
        """

        if True:


            with open(self.plik, 'r') as plik:
                zawartosc = plik.read()


            partie = re.findall(r'\n\n.*?(?=\[Event|\Z)', zawartosc, re.DOTALL)
            partie = [partia.strip() for partia in partie]


            for i in range(len(partie)):
                partie[i] = re.sub(r'\{[^}]*\}', '', partie[i])


            for i in range(len(partie)):
                elements = partie[i].split()
                cleaned_elements = [
                    el.replace('...', '') if el.endswith('...') else el.replace('...', '.')
                    for el in elements
                ]
                partie[i] = ' '.join(cleaned_elements)
                partie[i] = CA.game_without_movechars(self,partie[i])
                partie[i] = re.sub(r'\b\d+\b', '', partie[i])
                partie[i] = re.sub(r'\s+', ' ', partie[i]).strip()



            partie = [re.sub(r'\.\s', '.', partia) for partia in partie]

            return partie
        


    def game_without_movechars(self,game) -> list:
        '''
        Returns game without movechars.

        Params:

        game (str): game from which you want to strip of movechars.
        '''

        gra = ' '.join([el for el in game.split() if not el.endswith('.')])

        gra = gra.replace('1-0', '').replace('0-1', '').replace('1/2-1/2', '') 

        return gra
    
    

    

    def whitepc_games(self) -> list:

        """
        Returns games played by player with white pieces.
        
        """

        l = []

        with open(self.plik,'r') as plik:

            for line in plik:

                if f'[White "{self.name}"' in line:

                    while '1. ' not in line:
                        line = next(plik)

                    l.append(line)

        return l
    

    def blackpc_games(self) -> list:

        """
        Returns games played by player with black pieces.
        
        """

        l = []

        with open(self.plik,'r') as plik:

            for line in plik:

                if f'[Black "{self.name}"' in line:

                    while '1. ' not in line:
                        line = next(plik)

                    l.append(line)

        return l
    

    def games_opening(self, opening) -> list:
        """
        Returns games played by player after certain opening.

        Args:

            opening:

                Name of the certain opening.
        
        """

        l = []

        with open (self.plik, 'r') as plik:

            for line in plik:

                if '[Opening ' in line and opening in line:

                    while '1. ' not in line:
                        line = next(plik)

                    l.append(line)

        return l
    

    def games_date(self, data) -> list:
        """
        Returns games played by player on certain date.

        Args:

            data:

                Exact date you want to get games from, must be passed in yyyy/mm/dd [ISO 8601 standard].
        
        """

        l = []

        with open(self.plik, 'r') as plik:

            for line in plik:

                if '[UTCDate' in line:

                    if line.split('"')[1] == data:

                        while '1. ' not in line:
                            line = next(plik)

                        l.append(line)

        return l






###############                        FUNCTIONS RELATED TO OPENINGS                       #############


    def detailed_openings(self) -> dict:
        """
        Returns dictionary with names of openings as keys and their frequency in file as values. Different variants of the same opening
        are treated distincly.

        """

        d = {}

        with open(self.plik, 'r') as plik:

            for line in plik:

                if '[Opening ' in line:

                    opn = line.split('"')[1]

                    if opn not in d:
                        d[opn] = 0

                    d[opn] += 1

        if len(d) == 0:
            return 'No opening was found :('
        
        return d



    def notso_detailedOpenings(self) -> dict:
        """
        Returns frequency of not detailed openings. 'Nimzo-Larsen Attack: XYZ variation' is treated same as 'Nimzo-Larsen Attack' and 
        'Nimzo-Larsen Attack: WZK'.

        """

        d = {}

        with open(self.plik,'r') as plik:

            for line in plik:

                if '[Opening' in line:

                    op = line.split('"')[1]

                    if ':' in op:

                        idx = op.index(':')

                        op = op[:idx]

                    if op not in d:
                        d[op] = 0

                    d[op] += 1

        if len(d) == 0:
            return 'No opening was found :( )'

        return d
    

    def starting_squares(self) -> dict:
        """
        Returns board coordinates of first moves.

        """

        d = {}

        gry = CA.pure_moves(self)

        gry = [' '.join([el for el in gra.split() if not el.endswith('.')]) for gra in gry]

        gry = [gra.replace('1-0', '').replace('0-1', '').replace('1/2-1/2', '') for gra in gry]


        for el in gry:

            if len(el.split()) > 0:

                pierszy = el.split()[0]

            if pierszy not in d:
                d[pierszy] = 0

            d[pierszy] += 1


        if len(d) == 0:
            return 'No starting square was found :('

        return d
    

    def openings_by_ECO(self) -> dict:
        """
        Returns dictionary containing ECO codes and their frequencies.
        """

        d = {}


        with open(self.plik,'r') as plik:

            for line in plik:

                if '[ECO ' in line:

                    eco = line.split('"')[1][0]

                    if eco not in d:
                        d[eco] = 0

                    d[eco] += 1

        if len(d) == 0:
            return 'No ECO was found in file :( '

        return d
    

    def openings_with_white(self) -> dict:
        """
        Returns count of openings played by player with white pieces.
        """
        
        d = {}

        with open(self.plik, 'r') as plik:

            for line in plik:

                if f'[White "{self.name}"' in line:

                    while '[Opening ' not in line:
                        line = next(plik)

                    opn = line.split('"')[1]

                    if opn not in d:
                        d[opn] = 0

                    d[opn] += 1
        
        return d


    def openings_with_black(self) -> dict:
        """
        Returns count of openings played by player with white pieces.
        """
        
        d = {}

        with open(self.plik, 'r') as plik:

            for line in plik:

                if f'[Black "{self.name}"' in line:

                    while '[Opening ' not in line:
                        line = next(plik)

                    opn = line.split('"')[1]

                    if opn not in d:
                        d[opn] = 0

                    d[opn] += 1
        
        return d




##################                            WIN / DRAW / LOSS RELATED FUNCTIONS                             #############






    def WDL_stats(self) -> dict:
        """
        Returns player's Win/Draw/Loss stats.
        """


        win,loss,draw = 0,0,0

        with open(self.plik, 'r') as plik:

            for line in plik:

                if f'[White "{self.name}"' in line:

                    while '[Result' not in line:
                        line = next(plik)

                    if '[Result "1-0"]' in line:

                        win += 1

                    elif '[Result "0-1"]' in line:

                        loss += 1

                    elif '[Result "1/2-1/2"]' in line:
                        draw += 1


                elif f'[Black "{self.name}"' in line:

                    while '[Result' not in line:
                        line = next(plik)

                    if '[Result "1-0"]' in line:

                        loss += 1

                    elif '[Result "0-1"]' in line:
                        win += 1

                    elif '[Result "1/2-1/2"]' in line:
                        draw += 1
                        

            return win,draw,loss


# detailed set to False treats Nimzo-Larssen Attack and Nimzo-Larssen Attack : Classical Variation like 2 different openings, while detailed=True thinks that they're the same :)

    def WDL_Opening(self, detailed: bool =True) -> dict:

        """
        Returns player's Win/Draw/Loss statistics by opening.

        Parameters:
            detailed (bool): Specifies the level of detail for the statistics.
            - If True, different variants of the same opening are treated as separate entries.
            - If False, all variants of the same opening are aggregated into one entry..
        """

        d = {}

        with open(self.plik,'r') as plik:

            for line in plik:

                if f'[White "{self.name}"' in line:

                    res = 0

                    while '[Result ' not in line:
                        line = next(plik)

                    if '1-0' in line:

                        res = 1

                    elif '0-1' in line:

                        res = -1

                    elif '1/2-1/2' in line:

                        res = 2

                    while '[Opening ' not in line:
                        line = next(plik)

                    opn = line.split('"')[1]

                    if detailed:

                        if ':' in opn:
                            x = opn.index(':')
                            opn = opn[:x]


                    if opn not in d:
                        d[opn] = [0,0,0]

                    if res == 1:
                        d[opn][0] += 1

                    elif res == -1:
                        d[opn][2] +=1

                    elif res == 2:

                        d[opn][1] += 1


                elif f'[White ' in line and self.name not in line:

                    res = 0

                    while '[Result ' not in line:
                        line = next(plik)

                    if '1-0' in line:

                        res = -1

                    elif '0-1' in line:

                        res = 1

                    elif '1/2-1/2' in line:

                        res = 2

                    while '[Opening ' not in line:
                        line = next(plik)

                    opn = line.split('"')[1]

                    if detailed:

                        if ':' in opn:
                            x = opn.index(':')
                            opn = opn[:x]


                    if opn not in d:
                        d[opn] = [0,0,0]

                    if res == 1:
                        d[opn][0] += 1

                    elif res == -1:
                        d[opn][2] +=1

                    elif res == 2:

                        d[opn][1] += 1

        return d
    

    def WDL_Day(self) -> dict:

        """
        Returns player's Win/Draw/Loss statistics by day.
        """

        d = {}

        with open(self.plik,'r') as plik:

            for line in plik:

                if f'White "{self.name}"' in line:

                    res = 0

                    while '[Result ' not in line:
                        line = next(plik)

                    if '1-0' in line:
                        res = 1

                    elif '0-1' in line:
                        res = -1
                    
                    elif '1/2-1/2' in line:

                        res = 2

                    while '[UTCDate' not in line:
                        line = next(plik)

                    dat = line.split('"')[1]

                    dob = datetime.datetime.strptime(dat, "%Y.%m.%d")

                    day_of_week = dob.strftime("%A")

                    if day_of_week not in d:
                        d[day_of_week] = [0,0,0]

                    if res == 1:
                        d[day_of_week][0] += 1

                    elif res == 2:
                        d[day_of_week][1] += 1

                    elif res == -1:
                        d[day_of_week][2] += 1

                elif f'White ' in line and self.name not in line:

                    res = 0

                    while '[Result ' not in line:
                        line = next(plik)

                    if '1-0' in line:
                        res = -1

                    elif '0-1' in line:
                        res = 1
                    
                    elif '1/2-1/2' in line:

                        res = 2

                    while '[UTCDate' not in line:
                        line = next(plik)

                    dat = line.split('"')[1]

                    date_obj = datetime.datetime.strptime(dat, "%Y.%m.%d")

                    day_of_week = date_obj.strftime("%A")

                    if day_of_week not in d:
                        d[day_of_week] = [0,0,0]

                    if res == 1:
                        d[day_of_week][0] += 1

                    elif res == 2:
                        d[day_of_week][1] += 1

                    elif res == -1:
                        d[day_of_week][2] += 1

        return d


    def WDL_Time(self) -> dict:

        """
        Returns player's Win/Draw/Loss statistics by hour.

        """

        d = {}

        with open(self.plik,'r') as plik:

            for line in plik:

                if f'[White "{self.name}"' in line:

                    scr = 0

                    while '[Result' not in line:
                        line = next(plik)

                    if '1-0' in line:
                        scr = 1

                    elif '0-1' in line:
                        scr = -1

                    elif '1/2-1/2' in line:
                        scr = 2

                    while '[UTCTime ' not in line:
                        line = next(plik)

                    godz = line.split('"')[1][:2]

                    if godz not in d:
                        d[godz] = [0,0,0]

                    if scr == 1:
                        d[godz][0] += 1

                    elif scr == -1:
                        d[godz][2] += 1

                    elif scr == 2:
                        d[godz][1] += 1



                elif f'[White ' in line and self.name not in line:

                    scr = 0

                    while '[Result' not in line:
                        line = next(plik)

                    if '1-0' in line:
                        scr = -1

                    elif '0-1' in line:
                        scr = 1

                    elif '1/2-1/2' in line:
                        scr = 2

                    while '[UTCTime ' not in line:
                        line = next(plik)

                    godz = line.split('"')[1][:2]

                    if godz not in d:
                        d[godz] = [0,0,0]

                    if scr == 1:
                        d[godz][0] += 1

                    elif scr == -1:
                        d[godz][2] += 1

                    elif scr == 2:
                        d[godz][1] += 1
                    

        return d
    

    # day is split to 4 parts 

    def WDL_Part(self) -> dict:

        """
        Returns player's Win/Draw/Loss statistics by time of day.

        Returns:
            dict: A dictionary containing Win/Draw/Loss statistics for each day.
        """

        morn = ['6','7','8', '9', '10', '11','12']
        aft = ['13','14', '15', '16', '17','18']
        eve = ['19','20','21','22','23']
        noon = ['00','01', '02', '03', '04', '05']

        d = {'Morning'  : [0,0,0], 'Afternoon' : [0,0,0], 'Evening' : [0,0,0], 'Noon' : [0,0,0]}


        with open(self.plik, 'r') as plik:

            for line in plik:

                if f'[White "{self.name}' in line:

                    res = 0

                    while '[Result ' not in line:
                        line=next(plik)

                    if line[8:].strip().strip('[]"') == '1-0':

                        res = 1

                    elif line[8:].strip().strip('[]"') == '1-0' == '0-1':

                        res = -1


                    while '[UTCTime ' not in line:

                        line = next(plik)

                    if line.split('"')[1][:2] in morn:

                        if res == 1:

                            d['Morning'][0] += 1

                        elif res == -1:

                            d['Morning'][2] += 1

                        elif res == 0:

                            d['Morning'][1] += 1


                    elif line.split('"')[1][:2] in aft:

                        if res == 1:

                            d['Afternoon'][0] += 1

                        elif res == -1:

                            d['Afternoon'][2] += 1

                        elif res == 0:

                            d['Afternoon'][1] += 1


                    elif line.split('"')[1][:2] in eve:

                        if res == 1:

                            d['Evening'][0] += 1

                        elif res == -1:

                            d['Evening'][2] += 1

                        elif res == 0:

                            d['Evening'][1] += 1
    

                    elif line.split('"')[1][:2] in noon:

                        if res == 1:

                            d['Noon'][0] += 1

                        elif res == -1:

                            d['Noon'][2] += 1

                        elif res == 0:

                            d['Noon'][1] += 1



                if f'[Black "{self.name}' in line:

                    res = 0

                    while '[Result ' not in line:
                        line=next(plik)

                    if line[8:].strip().strip('[]"') == '0-1':

                        res = 1

                    elif line[8:].strip().strip('[]"') == '1-0':

                        res = -1


                    while '[UTCTime ' not in line:

                        line = next(plik)

                    if line.split('"')[1][:2] in morn:

                        if res == 1:

                            d['Morning'][0] += 1

                        elif res == -1:

                            d['Morning'][2] += 1

                        elif res == 0:

                            d['Morning'][1] += 1


                    elif line.split('"')[1][:2] in aft:

                        if res == 1:

                            d['Afternoon'][0] += 1

                        elif res == -1:

                            d['Afternoon'][2] += 1

                        elif res == 0:

                            d['Afternoon'][1] += 1


                    elif line.split('"')[1][:2] in eve:

                        if res == 1:

                            d['Evening'][0] += 1

                        elif res == -1:

                            d['Evening'][2] += 1

                        elif res == 0:

                            d['Evening'][1] += 1
    

                    elif line.split('"')[1][:2] in noon:

                        if res == 1:

                            d['Noon'][0] += 1

                        elif res == -1:

                            d['Noon'][2] += 1

                        elif res == 0:

                            d['Noon'][1] += 1
                    

                    
        return d





    def WDL_Date(self) -> dict:

        """
        Returns player's Win/Draw/Loss statistics by date.

        """


        d = {}

        if True:

            with open(self.plik,'r') as plik:

                for line in plik:

                    if f'[White "{self.name}' in line:

                        res = 0

                        while '[Result ' not in line:
                            line=next(plik)

                        if line.split('"')[1] == '1-0':

                            res = 1

                        elif line.split('"')[1] == '0-1':

                            res = -1

                        elif line.split('"')[1] == '1/2-1/2':
                            res = 0

                        
                        while '[UTCDate ' not in line:
                            line = next(plik)

                        cho = line.split('"')[1]

                        if cho not in d:
                            d[cho] = [0, 0, 0]

                        if res == 1:
                            d[cho][0] += 1
                        elif res == -1:
                            d[cho][2] += 1
                        elif res == 0:
                            d[cho][1] += 1

                    elif f'[Black "{self.name}' in line:

                        res = 0

                        while '[Result ' not in line:
                            line=next(plik)

                        if line.split('"')[1] == '1-0':

                            res = -1

                        elif line.split('"')[1] == '0-1':

                            res = 1

                        elif line.split('"')[1] == '1/2/-1/2':
                            res = 0


                        
                        while '[UTCDate ' not in line:
                            line = next(plik)

                        cho = line.split('"')[1]

                        if cho not in d:
                            d[cho] = [0, 0, 0]

                        if res == 1:
                            d[cho][0] += 1
                        elif res == -1:
                            d[cho][2] += 1
                        elif res == 0:
                            d[cho][1] += 1


        return d



    def WDL_accurate_elo(self, elo : int, roundz : bool =True) -> list:

        """
        Returns player's Win/Draw/Loss statistics against opponents with specific elo ratings.

        Params:
            elo (int): A integer specifying range of the elo. Range is set by default to (elo, elo+99).
                           
            roundz (bool): Declaration of rounding elo to nearest 100. If set to True, f.e if elo var is 1630, the range becomes
            (1600,1699). If set to False, range becomes (1630,1729)

        """

    

        if True:

            if roundz:

                elo1 = round(elo, -2)

            if not roundz:

                elo1 = elo

            elo2 = elo1 + 99

            l = [0,0,0]

            with open (self.plik, 'r') as plik:

                for line in plik:

                    if f'[White "{self.name}"' in line:

                        while '[Result ' not in line:
                            line = next(plik)

                        res = 0

                        if '1-0' in line:
                            res = 1

                        elif '0-1' in line:
                            res = -1

                        elif '1/2-1/2' in line:
                            res = 2

                        while '[BlackElo ' not in line:
                            line = next(plik)

                        if '?' not in line:

                            if int(line.split('"')[1]) >= elo1 and int(line.split('"')[1]) < elo2:

                                if res == 1:
                                    l[0] += 1

                                elif res == -1:
                                    l[2] += 1

                                elif res == 2:
                                    l[1] += 1

                    elif f'[Black "{self.name}"' in line:

                        while '[Result ' not in line:
                            line = next(plik)

                        res = 0

                        if '0-1' in line:
                            res = 1

                        elif '1-0' in line:
                            res = -1

                        elif '1/2-1/2' in line:
                            res = 2

                        while '[WhiteElo ' not in line:
                            line = next(plik)

                        if '?' not in line:

                            if int(line.split('"')[1]) >= elo1 and int(line.split('"')[1]) < elo2:

                                if res == 1:
                                    l[0] += 1

                                elif res == -1:
                                    l[2] += 1

                                elif res == 2:
                                    l[1] += 1


            return elo1,l




    def WDL_opponent(self, amount : int =None) -> dict:

        """
        Returns player's Win/Draw/Loss statistics against opponents.

        Params:
        amount (int, optional): The number of opponents to display in the dictionary. 
        If None, all opponents are included. This helps to limit the length of the dictionary.
        """

        d = {}

        with open(self.plik, 'r') as plik:

            for line in plik:

                if f'[White "{self.name}"' in line:
                    
                    while '[Black "' not in line:
                        line = next(plik)

                    op, wyn = line.split('"')[1], 0

                    while '[Result ' not in line:
                        line = next(plik)

                    if '1-0' in line:
                        wyn = 1

                    elif '0-1' in line:
                        wyn = -1

                    elif '1/2-1/2' in line:
                        wyn = 2

                    if op not in d:
                        d[op] = [0,0,0]

                    if wyn ==1:
                        d[op][0] += 1

                    elif wyn == -1:
                        d[op][2] +=1

                    elif wyn == 2:
                        d[op][1] += 1


                elif f'[White "' in line and self.name not in line:

                    op, wyn = line.split('"')[1], 0

                    while '[Result ' not in line:
                        line = next(plik)

                    if '0-1' in line:
                        wyn = 1

                    elif '1-0' in line:
                        wyn = -1

                    elif '1/2-1/2' in line:
                        wyn = 2

                    if op not in d:
                        d[op] = [0,0,0]

                    if wyn ==1:
                        d[op][0] += 1

                    elif wyn == -1:
                        d[op][2] +=1

                    elif wyn == 2:
                        d[op][1] += 1


        return dict(sorted(d.items(), key=lambda item: item[1][0], reverse=True)[:amount]) if amount else d




    def WDL_elo(self) -> dict:

        """
        Returns player's Win/Draw/Loss statistics in 100-point Elo ranges.

        """

        d = {}

        with open (self.plik, 'r') as plik:

            for line in plik:

                if f'[White "{self.name}' in line:

                    while '[Result ' not in line:
                        line = next(plik)

                    res = 0

                    if '1-0' in line:
                        res = 1

                    elif '0-1' in line:
                        res = -1

                    elif '1/2-1/2' in line:
                        res = 2

                    while '[BlackElo ' not in line:
                        line = next(plik)

                    if '?' not in line:

                        elo = round(int(line.split('"')[1]),-2)

                    if elo not in d:
                        d[elo] = [0,0,0]

                    if res == 1:
                        d[elo][0] += 1

                    elif res == 2:
                        d[elo][1] += 1

                    elif res == -1:
                        d[elo][2] += 1

                elif f'[White "' in line and self.name not in line:

                    while '[Result ' not in line:
                        line = next(plik)

                    res = 0

                    if '0-1' in line:
                        res = 1

                    elif '1-0' in line:
                        res = -1

                    elif '1/2-1/2' in line:
                        res = 2

                    while '[WhiteElo ' not in line:
                        line = next(plik)

                    if '?' not in line:

                        elo = round(int(line.split('"')[1]),-2)

                    if elo not in d:
                        d[elo] = [0,0,0]

                    if res == 1:
                        d[elo][0] += 1

                    elif res == 2:
                        d[elo][1] += 1

                    elif res == -1:
                        d[elo][2] += 1


        return d




                    
    def WDL_time_control(self) -> dict:

        '''
        Returns player's Win/Draw/Loss based on time control.
        '''

        d = {}

        with open(self.plik, 'r') as plik:

            for line in plik:

                if f'[White "{self.name}"' in line:

                    while '[Result ' not in line:
                        line = next(plik)

                    res = 0

                    if line.split('"')[1] == '1-0':
                        res += 1

                    elif line.split('"')[1] == '0-1':
                        res -= 1

                    elif line.split('"')[1] == '1/2-1/2':
                        res = 69

                    while '[TimeControl ' not in line:
                        line = next(plik)

                    czas =  line.split('"')[1] 

                    if czas not in d:
                        d[czas] = [0,0,0]

                    if res == 1:
                        d[czas][0] += 1

                    elif res == -1:
                        d[czas][2] += 1

                    elif res == 69:
                        d[czas][1] += 1

                if f'[White "' in line and self.name not in line:

                    while '[Result ' not in line:
                        line = next(plik)

                    res = 0

                    if line.split('"')[1] == '1-0':
                        res -= 1

                    elif line.split('"')[1] == '0-1':
                        res += 1

                    elif line.split('"')[1] == '1/2-1/2':
                        res = 69

                    while '[TimeControl ' not in line:
                        line = next(plik)

                    czas =  line.split('"')[1] 

                    if czas not in d:
                        d[czas] = [0,0,0]

                    if res == 1:
                        d[czas][0] += 1

                    elif res == -1:
                        d[czas][2] += 1

                    elif res == 69:
                        d[czas][1] += 1



        return d
    


    def WDL_variant(self) -> dict:

        '''
        Returns player's Win/Draw/Loss based on variant.
        '''

        d = {}

        with open(self.plik, 'r') as plik:

            for line in plik:

                if f'[White "{self.name}"' in line:

                    while '[Result ' not in line:
                        line = next(plik)

                    res = 0

                    if line.split('"')[1] == '1-0':
                        res += 1

                    elif line.split('"')[1] == '0-1':
                        res -= 1

                    elif line.split('"')[1] == '1/2-1/2':
                        res = 69

                    while '[Variant ' not in line:
                        line = next(plik)

                    war =  line.split('"')[1] 

                    if war not in d:
                        d[war] = [0,0,0]

                    if res == 1:
                        d[war][0] += 1

                    elif res == -1:
                        d[war][2] += 1

                    elif res == 69:
                        d[war][1] += 1

                if f'[White "' in line and self.name not in line:

                    while '[Result ' not in line:
                        line = next(plik)

                    res = 0

                    if line.split('"')[1] == '1-0':
                        res -= 1

                    elif line.split('"')[1] == '0-1':
                        res += 1

                    elif line.split('"')[1] == '1/2-1/2':
                        res = 69

                    while '[Variant ' not in line:
                        line = next(plik)

                    war =  line.split('"')[1] 

                    if war not in d:
                        d[war] = [0,0,0]

                    if res == 1:
                        d[war][0] += 1

                    elif res == -1:
                        d[war][2] += 1

                    elif res == 69:
                        d[war][1] += 1



        return d


    def WDL_gametype(self) -> dict:
        '''
        Returns player's Win/Draw/Loss based on time gamr type [blitz, bullet, rapid].
        '''


        d = {}

        with open(self.plik, 'r') as plik:

            for line in plik:
                
                if '[Event ' in line:

                    lin = line.split('"')[1]                       #zloty lin wita krola

                    gt = 0

                    if 'blitz' in lin:
                        gt = 'blitz'

                    elif 'bullet' in lin:
                        gt = 'bullet'

                    elif 'rapid' in lin:
                        gt = 'rapid'

                    while '[White "' not in line:
                        line = next(plik)

                    if self.name in line:

                        while '[Result ' not in line:
                            line = next(plik)

                        res = 0

                        ln = line.split('"')[1]

                        if ln == '1-0':
                            res += 1

                        elif ln == '0-1':
                            res -=1

                        elif ln == '1/2-1/2':
                            res = 1738

                        if gt not in d:
                            d[gt] = [0,0,0]

                        if res==1:
                            d[gt][0] += 1

                        elif res == -1:
                            d[gt][2] += 1

                        elif res == 1738:
                            d[gt][1] += 1

                    elif self.name not in line:

                        while '[Result ' not in line:
                            line = next(plik)

                        res = 0

                        ln = line.split('"')[1]

                        if ln == '0-1':
                            res += 1

                        elif ln == '1-0':
                            res -=1

                        elif ln == '1/2-1/2':
                            res = 1738

                        if gt not in d:
                            d[gt] = [0,0,0]

                        if res==1:
                            d[gt][0] += 1

                        elif res == -1:
                            d[gt][2] += 1

                        elif res == 1738:
                            d[gt][1] += 1
                        
 
        return d




##############                                         FUNCTIONS RELATED TO PLAYER STATS        #############





    def blitz_progress(self, reverse : bool = True) -> list:

        """
        Returns player's progress in blitz games.

        Params:

            reverse (bool): Indicates if list of elo scores should be returned in reverse. By default set to True.

        """


        l = []

        with open (self.plik, 'r') as plik:

            for line in plik:

                if '[Event ' in line:

                    if line.split(" ")[2] == 'blitz':

                        while '[White ' not in line:
                            line = next(plik)

                        if f'"{self.name}' in line:

                            while '[WhiteElo' not in line:
                                line = next(plik)

                            l.append(line.split('"')[1])



                        elif f'"{self.name}' in next(plik):

                            while '[BlackElo' not in line:
                                line=next(plik)

                            l.append(line.split('"')[1])

        return l[::-1] if reverse else l
        

    def blitz_progress_date(self) -> dict:
        """
        Returns player's gained/lost elo by date in blitz games.
        """

        d = {}

        with open (self.plik, 'r') as plik:

            for line in plik:

                if '[Event ' in line:

                    if 'blitz' in line:

                        while '[White ' not in line:
                            line = next(plik)

                        if self.name in line:

                            while '[UTCDate ' not in line:
                                line = next(plik)

                            cho = line.split('"')[1]

                            if cho not in d:
                                d[cho] = 0

                            while '[WhiteRatingDiff' not in line:
                                line = next(plik)
            

                            d[cho] += int(line.split('"')[1])

                        elif self.name not in line:

                            while '[UTCDate ' not in line:
                                line = next(plik)

                            cho = line.split('"')[1]

                            if cho not in d:
                                d[cho] = 0

                            while '[BlackRatingDiff' not in line:
                                line = next(plik)
            

                            d[cho] += int(line.split('"')[1])


        return d


    def blitz_progress_hour(self) -> dict:
        """
        Returns player's gained/lost elo determined by hour in blitz games.
        """


        d = {}

        with open (self.plik, 'r') as plik:

            for line in plik:

               if '[Event ' in line:

                    if 'blitz' in line:

                        while '[White ' not in line:
                            line = next(plik)

                        if self.name in line:

                            while '[UTCTime ' not in line:
                                line = next(plik)

                            cho = line.split('"')[1][:2]

                            if cho not in d:
                                d[cho] = 0

                            while '[WhiteRatingDiff' not in line:
                                line = next(plik)
            

                            d[cho] += int(line.split('"')[1])

                        elif self.name not in line:

                            while '[UTCTime ' not in line:
                                line = next(plik)

                            cho = line.split('"')[1][:2]

                            if cho not in d:
                                d[cho] = 0

                            while '[BlackRatingDiff' not in line:
                                line = next(plik)
            

                            d[cho] += int(line.split('"')[1])

        return d
    


    def bullet_progress(self, reverse=True) -> list:

        """
        Returns player's progress in bullet games.

        Params:

            reverse (bool): Indicates if list of elo scores should be returned in reverse. By default set to True.

        """


        l = []

        with open (self.plik, 'r') as plik:

            for line in plik:

                if '[Event ' in line:

                    if 'bullet' in line:

                        while '[White ' not in line:
                            line = next(plik)

                        if f'"{self.name}' in line:

                            while '[WhiteElo' not in line:
                                line = next(plik)

                            l.append(line[10:].strip().strip('[]"'))



                        elif f'"{self.name}' in next(plik):

                            while '[BlackElo' not in line:
                                line=next(plik)

                            l.append(line[10:].strip().strip('[]"'))

        return l[::-1] if reverse else l
        



    def bullet_progress_date(self) -> dict:
        """
        Returns player's gained/lost elo by date in bullet games.
        """


        d = {}

        with open (self.plik, 'r') as plik:

            for line in plik:

                if '[Event ' in line:

                    if 'bullet' in line:

                        while '[White ' not in line:
                            line = next(plik)

                        if self.name in line:

                            while '[UTCDate ' not in line:
                                line = next(plik)

                            cho = line.split('"')[1]

                            if cho not in d:
                                d[cho] = 0

                            while '[WhiteRatingDiff' not in line:
                                line = next(plik)
            

                            d[cho] += int(line.split('"')[1])

                        elif self.name not in line:

                            while '[UTCDate ' not in line:
                                line = next(plik)

                            cho = line.split('"')[1]

                            if cho not in d:
                                d[cho] = 0

                            while '[BlackRatingDiff' not in line:
                                line = next(plik)
            

                            d[cho] += int(line.split('"')[1])


        return d


    def bullet_progress_hour(self) -> dict:
        """
        Returns player's gained/lost elo determined by hour in bullet games.
        """

        d = {}

        with open (self.plik, 'r') as plik:

            for line in plik:

               if '[Event ' in line:

                    if 'bullet' in line:

                        while '[White ' not in line:
                            line = next(plik)

                        if self.name in line:

                            while '[UTCTime ' not in line:
                                line = next(plik)

                            cho = line.split('"')[1][:2]

                            if cho not in d:
                                d[cho] = 0

                            while '[WhiteRatingDiff' not in line:
                                line = next(plik)
            

                            d[cho] += int(line.split('"')[1])

                        elif self.name not in line:

                            while '[UTCTime ' not in line:
                                line = next(plik)

                            cho = line.split('"')[1][:2]

                            if cho not in d:
                                d[cho] = 0

                            while '[BlackRatingDiff' not in line:
                                line = next(plik)
            

                            d[cho] += int(line.split('"')[1])

        return d
        




    def rapid_progress(self, reverse=True) -> list:

        """
        Returns player's progress in blitz games.

        Params:

            reverse (bool): Indicates if list of elo scores should be returned in reverse. By default set to True.

        """


        l = []

        with open (plik, 'r') as plik:

            for line in plik:

                if '[Event ' in line:

                    if line.split(" ")[2] == 'rapid':

                        while '[White ' not in line:
                            line = next(plik)

                        if f'"{self.name}' in line:

                            while '[WhiteElo' not in line:
                                line = next(plik)

                            l.append(line[10:].strip().strip('[]"'))



                        elif f'"{self.name}' in next(plik):

                            while '[BlackElo' not in line:
                                line=next(plik)

                            l.append(line[10:].strip().strip('[]"'))


        return l[::-1] if reverse else l



    def rapid_progress_date(self) -> dict:

        """
        Returns player's gained/lost elo by date in rapid games.
        """


        d = {}

        with open (self.plik, 'r') as plik:

            for line in plik:

                if '[Event ' in line:

                    if 'rapid' in line:

                        while '[White ' not in line:
                            line = next(plik)

                        if self.name in line:

                            while '[UTCDate ' not in line:
                                line = next(plik)

                            cho = line.split('"')[1]

                            if cho not in d:
                                d[cho] = 0

                            while '[WhiteRatingDiff' not in line:
                                line = next(plik)
            

                            d[cho] += int(line.split('"')[1])

                        elif self.name not in line:

                            while '[UTCDate ' not in line:
                                line = next(plik)

                            cho = line.split('"')[1]

                            if cho not in d:
                                d[cho] = 0

                            while '[BlackRatingDiff' not in line:
                                line = next(plik)
            

                            d[cho] += int(line.split('"')[1])


        return d


    def rapid_progress_hour(self) -> dict:
        """
        Returns player's gained/lost elo determined by hour in rapid games.
        """

        d = {}

        with open (self.plik, 'r') as plik:

            for line in plik:

               if '[Event ' in line:

                    if 'rapid' in line:

                        while '[White ' not in line:
                            line = next(plik)

                        if self.name in line:

                            while '[UTCTime ' not in line:
                                line = next(plik)

                            cho = line.split('"')[1][:2]

                            if cho not in d:
                                d[cho] = 0

                            while '[WhiteRatingDiff' not in line:
                                line = next(plik)
            

                            d[cho] += int(line.split('"')[1])

                        elif self.name not in line:

                            while '[UTCTime ' not in line:
                                line = next(plik)

                            cho = line.split('"')[1][:2]

                            if cho not in d:
                                d[cho] = 0

                            while '[BlackRatingDiff' not in line:
                                line = next(plik)
            

                            d[cho] += int(line.split('"')[1])

        return d


    def Win_percentage_white(self):
        '''
        Returns player's win percentage when playing with white pieces.
        '''

        win,total = 0,0

        with open(self.plik,'r') as plik:

            for line in plik:

                if f'[White "{self.name}"' in line:

                    while '[Result ' not in line:
                        line = next(plik)

                    if '1-0' in line:
                        win += 1
                        total += 1

                    elif '0-1' in line or '1/2-1/2' in line:
                        total += 1

        if total == 0:

            return 0.00

        return round(win/total,3)




    def Win_percentage_black(self) -> int:
        '''
        Returns player's win percentage when playing with black pieces.
        '''

        win,total = 0,0

        with open(self.plik,'r') as plik:

            for line in plik:
                    
                if f'[White ' in line and self.name not in line:
                        
                    while '[Result ' not in line:
                        line = next(plik)

                    if '1-0' in line:
                        win += 1
                        total += 1

                    elif '0-1' in line or '1/2-1/2' in line:
                        total += 1

        if total == 0:
            return 0.00


        return round(win/total,3)


    def win_percentage_opponent(self, opponents_name) -> int:
        '''
        Returns player's win percentage determined by oponnent.

        Params:

        opponents_name (str): 
        '''
        w,t = 0,0

        with open(self.plik, 'r') as plik:

            for line in plik:

                if f'[White "{opponents_name}' in line:

                    res = 0

                    while '[Result ' not in line:
                        line = next(plik)

                    if '1-0' in line:
                        t += 1

                    elif '1/2-1/2' in line:
                        t += 1

                    elif '0-1' in line:
                        w += 1
                        t += 1

                elif f'[Black "{opponents_name}' in line:

                    res = 0

                    while '[Result ' not in line:
                        line = next(plik)

                    if '1-0' in line:
                        w += 1
                        t += 1

                    elif '1/2-1/2' in line:
                        t += 1

                    elif '0-1' in line:
                        t += 1

        return round(w/t, 3)


    def avg_opponent_elo(self) -> int:
        '''
        Returns average oponnent's elo.
        '''

        elo, total = 0,0

        with open(self.plik, 'r') as plik:

            for line in plik:

                if f'[White "{self.name}' in line:

                    while '[BlackElo' not in line:
                        line = next(plik)

                    if '?' not in line:
                        elo += int(line.split('"')[1])
                        total += 1

                elif f'[Black "{self.name}' in line:

                    while '[WhiteElo' not in line:
                        line = next(plik)


                    if '?' not in line:
                        elo += int(line.split('"')[1])
                        total += 1

        return round(elo/total, 3)
    

    def white_black_total(self) -> list:
        '''
        Returns player's number of games with white, black pieces and total amount of games.
        '''

        w,b,t = 0,0,0

        with open(self.plik, 'r') as plik:

            for line in plik:

                if f'[White "{self.name}"' in line:
                    w += 1
                    t += 1

                elif f'[Black "{self.name}"' in line:
                    b += 1
                    t += 1

        return [w,b,t]


    def common_opponents(self, amount : int=None) -> dict:
        '''
        Returns player's opponents in decreasing order.

        Params:

        amount (int) : amount of opponents to be returned.
        '''

        d = {}

        with open(self.plik, 'r') as plik:

            for line in plik:

                if f'[White "{self.name}"' in line:

                    while '[Black ' not in line:
                        line = next(plik)

                    if line.split('"')[1] not in d:
                        d[line.split('"')[1]] = 0

                    d[line.split('"')[1]] += 1

                elif f'[White "' in line and self.name not in line:

                    if line.split('"')[1] not in d:
                        d[line.split('"')[1]] = 0

                    d[line.split('"')[1]] += 1

        return dict(sorted(d.items(), key=lambda item: item[1], reverse=True)[:amount]) if amount else d

        
    

    


#######################                                 OVERALL FUNCTIONS                                         ############


    def game_types(self) -> dict:
        '''
        Returns variants of games played by player.
        '''

        d = {}

        with open(self.plik, 'r') as plik:
            
            for line in plik:

                if '[Variant ' in line:

                    war = line.split('"')[1]

                    if war not in d:
                        d[war] = 0

                    d[war] += 1


        return d



    def time_control(self) -> dict:
        '''
        Returns time controls of games played by player.
        '''

        d = {}

        with open(self.plik, 'r') as plik:

            for line in plik:

                if '[TimeControl ' in line:

                    tc = line.split('"')[1]

                    if tc not in d:
                        d[tc] = 0

                    d[tc] += 1  

        return d         



    def count_ofGames_Date(self) -> dict:
        '''
        Returns number of games played by player in exact date.
        '''

        d = {}

        with open(self.plik, 'r') as plik:

            for line in plik:

                if '[UTCDate ' in line:

                    dzien = line.split('"')[1]
                    
                    if dzien not in d:
                        d[dzien] = 0

                    d[dzien] += 1

        return d




    def count_ofGames_Time(self) -> dict:
        '''
        Returns number of games played by player in exact hour.
        '''


        d = {}

        with open(self.plik, 'r') as plik:

            for line in plik:

                if '[UTCTime ' in line:

                    dzien = line.split('"')[1][:2]
                    
                    if dzien not in d:
                        d[dzien] = 0

                    d[dzien] += 1

        return d
    


    def termination_stats(self) -> dict:
        '''
        Returns way in which games has ended.
        '''

        d = {}

        with open(self.plik,'r') as plik:

            for line in plik:

                if '[Termination ' in line:

                    wyb = line.split('"')[1]

                    if wyb not in d:
                        d[wyb] = 0

                    d[wyb] += 1

        return d
    


    def ranked_unranked(self) -> dict:
        '''
        Returns num of ranked and unranked games.
        '''

        d = {'Ranked' : 0, 'Unranked' : 0}

        with open(self.plik, 'r') as plik:

            for line in plik:

                if '[Event ' in line:

                    line = line.split('"')[1]

                    if 'Rated' in line:

                        d['Ranked'] += 1

                    elif 'Rated' not in line:

                        d['Unranked'] += 1

        return d





 




#########################                   STATISTICAL // AVERAGE  RELATED FUNCTIONS              #############################


    def avg_gameLength(self) -> int:
        '''
        Returns average game length. e4 e5 Nf3 Nf6 are treated as 4 moves.
        '''

        moves,total = 0,0

        gry = CA.pure_moves(self)

        for el in gry:
            moves += len(el.split())
            total += 1

        if total == 0:
            return 'No games were played'
        
        moves = moves/2

        return round(moves/total,3)
    


    def xth_move(self, move:int) -> dict:
        '''
        Returns dictionary with frequencies of x'th move.

        Params:

        move(int) : num of move 
        '''

        d = {}

        gry = CA.pure_moves(self)

        for partia in gry:

            if len(partia.split())-1 >= move:

                ruch = partia.split()[move]

                if ruch not in d:
                    d[ruch] = 0

                d[ruch] += 1

        return d

    def xth_move_square(self, move:int) -> dict:
        '''
        Returns dictionary with frequencies of x'th move square. 

        Params:

        move (int): num of move
        '''

        d = {}

        pchars = 'QNBRK'

        gry = CA.pure_moves(self)

        for partia in gry:

            if len(partia.split())-1 >= move:

                ruch = partia.split()[move]

                ruch = ruch.replace('#', '').replace('+', '')

                if ruch[0] in pchars and len(ruch) == 3:
                    ruch = ruch[1:]

                elif ruch[0] in pchars and len(ruch) == 4:
                    ruch = ruch[2:]

                if '=' in ruch:
                    ruch = ruch[:-2]

                if 'x' in ruch:
                    ruch = ruch[-2:]

                if ruch not in d:
                    d[ruch] = 0

                d[ruch] += 1

        return d
    

    def xth_move_opening(self, move: int, opening:str) -> dict:
        '''
        Returns dictionary with frequencies of x'th move determined by opening.

        Params:

        move (int): num of move
        opening (str): distinct opening


        '''
        move = move -1

        d, l = {}, []

        with open(self.plik, 'r') as plik:

            for line in plik:

                if '[Opening' in line and opening in line:

                    while '1. ' not in line:
                        line = next(plik)

                    line = line.replace('\n', '')

                    l.append(line)

        if l is not None:

            for partia in l:

                partia = CA.game_without_movechars(self,partia)

                if len(partia.split()) - 1 >= move:

                    ruch = partia.split()[move]

                    if ruch not in d:
                        d[ruch] = 0

                    d[ruch] += 1

        return d


    def spearman_elo_winrate(self) -> list:
        '''
        Returns spearman correlation between elo and winrate.
        '''

        z = CA.WDL_elo(self)

        d = {}

        for k,v in z.items():
            d[k] = round(v[0] / (v[0]+v[1]+v[2]),4)

        x,y  = list(d.keys()) , list(d.values())

        spearman_corr, p_value = ss.spearmanr(x, y)

        return [spearman_corr, p_value]




                                    ######            BOARD / PIECE RELATED FUNCS               ######################




    def bishop_moves(self, only_player_games : bool =True) -> dict:
        '''
        Returns frequencies of each square that bishop has gone to.

        Params:

            only_player_games (bool): Determines if only moves played by player are counted. By default set to True.
            If set to False, moves made by opponent count as well.
        '''

        d = {}

        if only_player_games:

            wg, bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for partia in wg:

                for i, ruch in enumerate(partia.split()):

                    if i % 2 == 0:

                        if ruch[0] == 'B':

                            hmhm = ''

                            ruch = ruch.replace('+', '').replace('#', '')

                            if len(ruch) == 3:

                                hmhm = ruch[1:]

                            else:
                                
                                hmhm = ruch[-2:]

                            if hmhm not in d:

                                d[hmhm] = 0

                            d[hmhm] += 1


            for partia in bg:

                for i, ruch in enumerate(partia.split()):

                    if i % 2 != 0:

                        if ruch[0] == 'B':

                            hmhm = ''

                            ruch = ruch.replace('+', '').replace('#', '')

                            if len(ruch) == 3:

                                hmhm = ruch[1:]

                            else:
                                
                                hmhm = ruch[-2:]

                            if hmhm not in d:

                                d[hmhm] = 0

                            d[hmhm] += 1




        else:

            gierki = CA.pure_moves(self)

            for partia in gierki:

                for ruch in partia.split():

                    if ruch[0] == 'B':

                        hm = 0

                        ruch = ruch.replace('#', '').replace('+', '')

                        if len(ruch) == 3:
                            hm = ruch[1:]

                        else:
                            hm = ruch[-2:]

                        if hm not in d:
                            d[hm] = 0

                        d[hm] += 1


        return d
    


    ### nothing interesting down there, just same func repeated x times for dif piece 



    def queen_moves(self, only_player_games : bool =True) -> dict:
        '''
        Returns frequencies of each square that queen has gone to.

        Params:

            only_player_games (bool): Determines if only moves played by player are counted. By default set to True.
            If set to False, moves made by opponent count as well.
        '''

        d = {}

        if only_player_games:

            wg, bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for partia in wg:

                for i, ruch in enumerate(partia.split()):

                    if i % 2 == 0:

                        if ruch[0] == 'Q':

                            hmhm = ''

                            ruch = ruch.replace('+', '').replace('#', '')

                            if len(ruch) == 3:

                                hmhm = ruch[1:]

                            else:
                                
                                hmhm = ruch[-2:]

                            if hmhm not in d:

                                d[hmhm] = 0

                            d[hmhm] += 1


            for partia in bg:

                for i, ruch in enumerate(partia.split()):

                    if i % 2 != 0:

                        if ruch[0] == 'Q':

                            hmhm = ''

                            ruch = ruch.replace('+', '').replace('#', '')

                            if len(ruch) == 3:

                                hmhm = ruch[1:]

                            else:
                                
                                hmhm = ruch[-2:]

                            if hmhm not in d:

                                d[hmhm] = 0

                            d[hmhm] += 1




        else:

            gierki = CA.pure_moves(self)

            for partia in gierki:

                for ruch in partia.split():

                    if ruch[0] == 'Q':

                        hm = 0

                        ruch = ruch.replace('#', '').replace('+', '')

                        if len(ruch) == 3:
                            hm = ruch[1:]

                        else:
                            hm = ruch[-2:]

                        if hm not in d:
                            d[hm] = 0

                        d[hm] += 1


        return d



                            

    def rook_moves(self, only_player_games : bool =True) -> dict:
        '''
        Returns frequencies of each square that rook has gone to.

        Params:

            only_player_games (bool): Determines if only moves played by player are counted. By default set to True.
            If set to False, moves made by opponent count as well.
        '''

        d = {}

        if only_player_games:

            wg, bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for partia in wg:

                for i, ruch in enumerate(partia.split()):

                    if i % 2 == 0:

                        if ruch[0] == 'R':

                            hmhm = ''

                            ruch = ruch.replace('+', '').replace('#', '')

                            if len(ruch) == 3:

                                hmhm = ruch[1:]

                            else:
                                
                                hmhm = ruch[-2:]

                            if hmhm not in d:

                                d[hmhm] = 0

                            d[hmhm] += 1


            for partia in bg:

                for i, ruch in enumerate(partia.split()):

                    if i % 2 != 0:

                        if ruch[0] == 'R':

                            hmhm = ''

                            ruch = ruch.replace('+', '').replace('#', '')

                            if len(ruch) == 3:

                                hmhm = ruch[1:]

                            else:
                                
                                hmhm = ruch[-2:]

                            if hmhm not in d:

                                d[hmhm] = 0

                            d[hmhm] += 1




        else:

            gierki = CA.pure_moves(self)

            for partia in gierki:

                for ruch in partia.split():

                    if ruch[0] == 'R':

                        hm = 0

                        ruch = ruch.replace('#', '').replace('+', '')

                        if len(ruch) == 3:
                            hm = ruch[1:]

                        else:
                            hm = ruch[-2:]

                        if hm not in d:
                            d[hm] = 0

                        d[hm] += 1


        return d




    def knight_moves(self, only_player_games : bool =True) -> dict:
        '''
        Returns frequencies of each square that bishop has gone to.

        Params:

            only_player_games (bool): Determines if only moves played by player are counted. By default set to True.
            If set to False, moves made by opponent count as well.
        '''

        d = {}

        if only_player_games:

            wg, bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for partia in wg:

                for i, ruch in enumerate(partia.split()):

                    if i % 2 == 0:

                        if ruch[0] == 'N':

                            hmhm = ''

                            ruch = ruch.replace('+', '').replace('#', '')

                            if len(ruch) == 3:

                                hmhm = ruch[1:]

                            else:
                                
                                hmhm = ruch[-2:]

                            if hmhm not in d:

                                d[hmhm] = 0

                            d[hmhm] += 1


            for partia in bg:

                for i, ruch in enumerate(partia.split()):

                    if i % 2 != 0:

                        if ruch[0] == 'N':

                            hmhm = ''

                            ruch = ruch.replace('+', '').replace('#', '')

                            if len(ruch) == 3:

                                hmhm = ruch[1:]

                            else:
                                
                                hmhm = ruch[-2:]

                            if hmhm not in d:

                                d[hmhm] = 0

                            d[hmhm] += 1




        else:

            gierki = CA.pure_moves(self)

            for partia in gierki:

                for ruch in partia.split():

                    if ruch[0] == 'N':

                        hm = 0

                        ruch = ruch.replace('#', '').replace('+', '')

                        if len(ruch) == 3:
                            hm = ruch[1:]

                        else:
                            hm = ruch[-2:]

                        if hm not in d:
                            d[hm] = 0

                        d[hm] += 1


        return d



    def king_moves(self, only_player_games : bool =True) -> dict:
        '''
        Returns frequencies of each square that bishop has gone to.

        Params:

            only_player_games (bool): Determines if only moves played by player are counted. By default set to True.
            If set to False, moves made by opponent count as well.
        '''

        d = {}

        if only_player_games:

            wg, bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for partia in wg:

                for i, ruch in enumerate(partia.split()):

                    if i % 2 == 0:

                        if ruch[0] == 'K':

                            hmhm = ''

                            ruch = ruch.replace('+', '').replace('#', '')

                            if len(ruch) == 3:

                                hmhm = ruch[1:]

                            else:
                                
                                hmhm = ruch[-2:]

                            if hmhm not in d:

                                d[hmhm] = 0

                            d[hmhm] += 1


            for partia in bg:

                for i, ruch in enumerate(partia.split()):

                    if i % 2 != 0:

                        if ruch[0] == 'K':

                            hmhm = ''

                            ruch = ruch.replace('+', '').replace('#', '')

                            if len(ruch) == 3:

                                hmhm = ruch[1:]

                            else:
                                
                                hmhm = ruch[-2:]

                            if hmhm not in d:

                                d[hmhm] = 0

                            d[hmhm] += 1




        else:

            gierki = CA.pure_moves(self)

            for partia in gierki:

                for ruch in partia.split():

                    if ruch[0] == 'K':

                        hm = 0

                        ruch = ruch.replace('#', '').replace('+', '')

                        if len(ruch) == 3:
                            hm = ruch[1:]

                        else:
                            hm = ruch[-2:]

                        if hm not in d:
                            d[hm] = 0

                        d[hm] += 1


        return d



    def squares_with_captures(self, only_player_games : bool =  True) -> dict:
        '''
        Returns squares with captures.

        Params:

            only_player_games (bool): Determines if only moves played by player are counted. By default set to True.
            If set to False, moves made by opponent count as well.
        '''

        d = {}


        if not only_player_games:

            partie = CA.pure_moves(self)

            for partia in partie:
                for el in partia.split():
                    if 'x' in el:

                        if '=' in el:
                            el = el[:2]

                        el = el.replace("#", '').replace('+', '')

                        el = el[2:]

                        if el not in d:
                            d[el] = 0

                        d[el] += 1
        
        else:

            wg, bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for partia in wg:

                for i,ruch in enumerate(partia.split()):

                    if i % 2 == 0 and 'x' in ruch:

                        ruch = ruch.replace('#', '').replace('+', '')

                        if '=' in ruch:
                            ruch = ruch[:-2]

                        g = ruch.index('x')

                        ruch = ruch[g+1:]

                        if ruch not in d:
                            d[ruch] = 0

                        d[ruch] += 1

            for gierka in bg:

                for i,ruch in enumerate(gierka.split()):

                    if i % 2 != 0 and 'x' in ruch:

                        ruch = ruch.replace('#', '').replace('+', '')

                        if '=' in ruch:
                            ruch = ruch[:-2]

                        g = ruch.index('x')

                        ruch = ruch[g+1:]

                        if ruch not in d:
                            d[ruch] = 0

                        d[ruch] += 1



        return d
    

    def squares_with_Bishopcaptures(self, only_player_games : bool=True) -> dict:
        '''
        Returns squares with bishop captures (square on which bishop made a capture, not bishop being captured :)     ).

        Params:

            only_player_games (bool): Determines if only moves played by player are counted. By default set to True.
            If set to False, moves made by opponent count as well.
        '''

        if not only_player_games:

            d = {}

            partie = CA.pure_moves(self)

            for partia in partie:
                for el in partia.split():
                    if el [0] == 'B' and 'x' in el:

                        el = el.replace("#", '').replace('+', '')

                        el = el[2:]

                        if el not in d:
                            d[el] = 0

                        d[el] += 1


        else:

            d = {}

            wg, bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for partia in wg:
                for i,ruch in enumerate(partia.split()):
                    if i % 2 == 0:

                        if ruch[0] == 'B':

                            ruch = ruch.replace('+', '').replace('x','').replace('#', '')

                            if '=' in ruch:
                                ruch = ruch[:-2]   
                            
                            if len(ruch) == 3:
                                ruch = ruch[1:]

                            if ruch not in d:
                                d[ruch] = 0

                            d[ruch] += 1


            for gierka in bg:

                for i,ruch in enumerate(gierka.split()):
                    if i % 2 != 0:

                        if ruch[0] == 'B':

                            ruch = ruch.replace('+', '').replace('x','').replace('#', '') 

                            if '=' in ruch:
                                ruch = ruch[:-2]         
                            
                            if len(ruch) == 3:
                                ruch = ruch[1:]

                            if ruch not in d:
                                d[ruch] = 0

                            d[ruch] += 1

        
        return d


    def squares_with_Queencaptures(self, only_player_games : bool = True) -> dict:
        '''
        Returns squares with queen captures (square on which queen made a capture, not queen being captured :)     ).

        Params:

            only_player_games (bool): Determines if only moves played by player are counted. By default set to True.
            If set to False, moves made by opponent count as well.
        '''

        if not only_player_games:

            d = {}

            partie = CA.pure_moves(self)

            for partia in partie:
                for el in partia.split():
                    if el [0] == 'Q' and 'x' in el:

                        el = el.replace("#", '').replace('+', '')

                        el = el[2:]

                        if el not in d:
                            d[el] = 0

                        d[el] += 1

        else:

            d = {}

            wg, bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for partia in wg:
                for i,ruch in enumerate(partia.split()):
                    if i % 2 == 0:

                        if ruch[0] == 'Q':

                            ruch = ruch.replace('+', '').replace('x','').replace('#', '')

                            if '=' in ruch:
                                ruch = ruch[:-2]   
                            
                            if len(ruch) == 3:
                                ruch = ruch[1:]

                            if ruch not in d:
                                d[ruch] = 0

                            d[ruch] += 1


            for gierka in bg:

                for i,ruch in enumerate(gierka.split()):
                    if i % 2 != 0:

                        if ruch[0] == 'Q':

                            ruch = ruch.replace('+', '').replace('x','').replace('#', '') 

                            if '=' in ruch:
                                ruch = ruch[:-2]         
                            
                            if len(ruch) == 3:
                                ruch = ruch[1:]

                            if ruch not in d:
                                d[ruch] = 0

                            d[ruch] += 1

        
        return d
    

    def squares_with_Rookcaptures(self, only_player_moves : bool = True) -> dict:
        '''
        Returns squares with rook captures (square on which rook made a capture, not rook being captured :)     ).

        Params:

            only_player_games (bool): Determines if only moves played by player are counted. By default set to True.
            If set to False, moves made by opponent count as well.
        '''

        if not only_player_moves:

            d = {}

            partie = CA.pure_moves(self)

            for partia in partie:
                for el in partia.split():
                    if el [0] == 'R' and 'x' in el:

                        el = el.replace("#", '').replace('+', '')

                        el = el[2:]

                        if el not in d:
                            d[el] = 0

                        d[el] += 1

        else:

            d = {}

            wg, bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for partia in wg:
                for i,ruch in enumerate(partia.split()):
                    if i % 2 == 0:

                        if ruch[0] =='R':

                            ruch = ruch.replace('+', '').replace('x','').replace('#', '')

                            if '=' in ruch:
                                ruch = ruch[:-2]   
                            
                            if len(ruch) == 3:
                                ruch = ruch[1:]

                            if ruch not in d:
                                d[ruch] = 0

                            d[ruch] += 1


            for gierka in bg:

                for i,ruch in enumerate(gierka.split()):
                    if i % 2 != 0:

                        if ruch[0] == 'R':

                            ruch = ruch.replace('+', '').replace('x','').replace('#', '') 

                            if '=' in ruch:
                                ruch = ruch[:-2]         
                            
                            if len(ruch) == 3:
                                ruch = ruch[1:]

                            if ruch not in d:
                                d[ruch] = 0

                            d[ruch] += 1

        
        return d
    

    def squares_with_Knightcaptures(self, only_player_games : bool = True) -> dict:
        '''
        Returns squares with knight captures (square on which knight made a capture, not knight being captured :)     ).

        Params:

            only_player_games (bool): Determines if only moves played by player are counted. By default set to True.
            If set to False, moves made by opponent count as well.
        '''

        if not only_player_games:


            d = {}

            partie = CA.pure_moves(self)

            for partia in partie:
                for el in partia.split():
                    if el [0] == 'N' and 'x' in el:

                        el = el.replace("#", '').replace('+', '')

                        el = el[2:]

                        if el not in d:
                            d[el] = 0

                        d[el] += 1
            

        else:

            d = {}

            wg, bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for partia in wg:
                for i,ruch in enumerate(partia.split()):
                    if i % 2 == 0:

                        if ruch[0] == 'N':

                            ruch = ruch.replace('+', '').replace('x','').replace('#', '')

                            if '=' in ruch:
                                ruch = ruch[:-2]   
                            
                            if len(ruch) == 3:
                                ruch = ruch[1:]

                            if ruch not in d:
                                d[ruch] = 0

                            d[ruch] += 1


            for gierka in bg:

                for i,ruch in enumerate(gierka.split()):
                    if i % 2 != 0:

                        if ruch[0] == 'N':

                            ruch = ruch.replace('+', '').replace('x','').replace('#', '') 

                            if '=' in ruch:
                                ruch = ruch[:-2]         
                            
                            if len(ruch) == 3:
                                ruch = ruch[1:]

                            if ruch not in d:
                                d[ruch] = 0

                            d[ruch] += 1

        return d

    

    def squares_with_Kingcaptures(self, only_player_games : bool = True) -> dict:
        '''
        Returns squares with king captures (square on which king made a capture, not king being captured :)     ).

        Params:

            only_player_games (bool): Determines if only moves played by player are counted. By default set to True.
            If set to False, moves made by opponent count as well.
        '''

        if not only_player_games:

            d = {}

            partie = CA.pure_moves(self)

            for partia in partie:
                for el in partia.split():
                    if el [0] == 'B' and 'x' in el:

                        el = el.replace("K", '').replace('+', '')

                        el = el[2:]

                        if el not in d:
                            d[el] = 0

                        d[el] += 1

        else:

            d = {}

            wg, bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for partia in wg:
                for i,ruch in enumerate(partia.split()):
                    if i % 2 == 0:

                        if ruch[0] == 'K':

                            ruch = ruch.replace('+', '').replace('x','')                   # no need to replace '#' as u cant give checkmate with king
                            
                            if len(ruch) == 3:
                                ruch = ruch[1:]

                            if ruch not in d:
                                d[ruch] = 0

                            d[ruch] += 1
                        
        return d
    

    def squares_with_Pawncaptures(self, only_player_games : bool = True) -> dict:
        '''
        Returns squares with pawn captures (square on which pawn made a capture, not pawn being captured :)     ).

        Params:

            only_player_games (bool): Determines if only moves played by player are counted. By default set to True.
            If set to False, moves made by opponent count as well.
        '''

        pawnlet = ['a','b','c','d','e','f','g','h']

        if not only_player_games:

            d = {}

            partie = CA.pure_moves(self)

            for partia in partie:

                for el in partia.split():

                    if el [0] in pawnlet and 'x' in el:

                        el = el.replace("#", '').replace('+', '')

                        if '=' in el:
                            el = el[:-2]


                        el = el[2:]

                        if el not in d:
                            d[el] = 0

                        d[el] += 1
            

        else:

            d = {}

            wg, bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for partia in wg:
                for i,ruch in enumerate(partia.split()):
                    if i % 2 == 0:

                        if ruch[0] in pawnlet:

                            ruch = ruch.replace('+', '').replace('x','').replace('#', '')

                            if '=' in ruch:
                                ruch = ruch[:-2]   
                            
                            if len(ruch) == 3:
                                ruch = ruch[1:]

                            if ruch not in d:
                                d[ruch] = 0

                            d[ruch] += 1


            for gierka in bg:

                for i,ruch in enumerate(gierka.split()):
                    if i % 2 != 0:

                        if ruch[0] in pawnlet:

                            ruch = ruch.replace('+', '').replace('x','').replace('#', '') 

                            if '=' in ruch:
                                ruch = ruch[:-2]         
                            
                            if len(ruch) == 3:
                                ruch = ruch[1:]

                            if ruch not in d:
                                d[ruch] = 0

                            d[ruch] += 1

        return d
    
                    
    def squares_with_promotions(self, only_player_games : bool = True) -> dict:

        d = {}

        if not only_player_games:

            partie = CA.pure_moves(self)

            for partia in partie:

                for el in partia.split():

                    if '=' in el:

                        if 'x' in el:
                            el = el[2:4]
                            if el not in d:
                                d[el] = 0

                            d[el] += 1

                        el = el[:2]

                        if el not in d:
                            d[el] = 0

                        d[el] += 1

        else:

            wg, bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for gra in wg:
                for i,el in enumerate(gra.split()):
                    if i % 2 == 0 and '=' in el:

                        if 'x' in el:
                            el = el[2:4]
                            if el not in d:
                                d[el] = 0

                            d[el] += 1

                        el = el[:2]

                        if el not in d:
                            d[el] = 0

                        d[el] += 1

            for gierka in bg:

                for i,el in enumerate(gierka.split()):
                    if i % 2 != 0 and '=' in el:

                        if 'x' in el:
                            el = el[2:4]
                            if el not in d:
                                d[el] = 0

                            d[el] += 1

                        el = el[:2]

                        if el not in d:
                            d[el] = 0

                        d[el] += 1

        return d


    def squares_with_checks(self, only_player_games : bool = True) -> dict:

        d = {}

        if not only_player_games:

            partie = CA.pure_moves(self)

            for partia in partie:

                for el in partia.split():

                    if '+' in el:

                        el =el[:-1]

                        if len(el) == 3:

                            el = el[1:]

                            if el not in d:
                                d[el] = 0

                            d[el] += 1

                        elif 'x' in el and '=' not in el:
                            el = el[-2:]
                            if el not in d:
                                d[el] = 0

                            d[el] += 1

                        elif '=' in el:
                            el = el[-4:-2]
                            if el not in d:
                                d[el] = 0

                            d[el] += 1

        else:


            wg,bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for gra in wg:
                for i, el in enumerate(gra.split()):
                    if i % 2 == 0 and '+' in el:

                        el = el[:-1]

                        if len(el) == 3:

                            el = el[1:]

                            if el not in d:
                                d[el] = 0

                            d[el] += 1

                        elif 'x' in el and '=' not in el:
                            el = el[-2:]
                            if el not in d:
                                d[el] = 0

                            d[el] += 1

                        elif '=' in el:
                            el = el[-4:-2]
                            if el not in d:
                                d[el] = 0

                            d[el] += 1

            for gierka in bg:
                for i, el in enumerate(gierka.split()):
                    if i % 2 != 0 and '+' in el:

                        el = el[:-1]

                        if len(el) == 3:

                            el = el[1:]

                            if el not in d:
                                d[el] = 0

                            d[el] += 1

                        elif 'x' in el and '=' not in el:
                            el = el[-2:]
                            if el not in d:
                                d[el] = 0

                            d[el] += 1

                        elif '=' in el:
                            el = el[-4:-2]
                            if el not in d:
                                d[el] = 0

                            d[el] += 1

        return d
        



    def squares_with_mates(self, only_player_games : bool = True) -> dict:

        d = {}

        if not only_player_games:

            partie = CA.pure_moves(self)

            for partia in partie:
                    
                    for el in partia.split():
        
                        if '#' in el:
        
                            el =el[:-1]
        
                            if len(el) == 3:
        
                                el = el[1:]
        
                                if el not in d:
                                    d[el] = 0
        
                                d[el] += 1
        
                            elif 'x' in el and '=' not in el:
                                el = el[-2:]
                                if el not in d:
                                    d[el] = 0
        
                                d[el] += 1
        
                            elif '=' in el:
                                el = el[-4:-2]
                                if el not in d:
                                    d[el] = 0
        
                                d[el] += 1

        else:

            wg,bg = CA.whitepc_games(self), CA.blackpc_games(self)

            for gra in wg:
                for i,el in enumerate(gra.split()):
                    if i % 2 == 0 and '#' in el:

                        el = el[:-1]

                        if len(el) == 3:

                            el = el[1:]

                            if el not in d:
                                d[el] = 0

                            d[el] += 1

                        elif 'x' in el and '=' not in el:
                            el = el[-2:]
                            if el not in d:
                                d[el] = 0

                            d[el] += 1

                        elif '=' in el:
                            el = el[-4:-2]
                            if el not in d:
                                d[el] = 0

                            d[el] += 1
            
            for gierka in bg:
                for i, el in enumerate(gierka.split()):
                    if i % 2 != 0 and '#' in el:

                        el = el[:-1]

                        if len(el) == 3:

                            el = el[1:]

                            if el not in d:
                                d[el] = 0

                            d[el] += 1

                        elif 'x' in el and '=' not in el:
                            el = el[-2:]
                            if el not in d:
                                d[el] = 0

                            d[el] += 1

                        elif '=' in el:
                            el = el[-4:-2]
                            if el not in d:
                                d[el] = 0

                            d[el] += 1 

        return d

