from datetime import datetime as dt

class jj_players:

    def __init__(self) -> None:
            
        self.jj_players = [
            {
                'ign': 'Lenore',
                'b_mon':11,
                'b_day':9
            },
            {        
                'ign': 'LilsterP',
                'b_mon':5,
                'b_day':13
            },
            {
                'ign': 'Hapegolucke',
                'b_mon':10,
                'b_day':8
            },
            {
                'ign': 'ZerepNalyd',
                'b_mon':8,
                'b_day':19
            },
            {
                'ign': 'TheySeeMe',
                'b_mon':9,
                'b_day':23
            },
            {
                'ign': 'Annie',
                'b_mon':2,
                'b_day':21
            },
            {
                'ign': 'ghostboobster',
                'b_mon':5,
                'b_day':13
            },
            {
                'ign': 'Shoopuff',
                'b_mon':7,
                'b_day':25
            },
            {
                'ign': 'Happy Haggis',
                'b_mon':9,
                'b_day':4
            },
            {
                'ign': 'LindaG',
                'b_mon':2,
                'b_day':17
            },
            {
                'ign': 'Colin',
                'b_mon':9,
                'b_day':11
            },
            {
                'ign': 'Vickie Island',
                'b_mon':3,
                'b_day':7
            },
            {
                'ign': 'LouLou',
                'b_mon':7,
                'b_day':15
            },
            {
                'ign': 'MaladyRae',
                'b_mon':4,
                'b_day':4
            },
            {
                'ign': 'Jessica Jones',
                'b_mon':1,
                'b_day':20
            }
        ]

        self.purple_smokebush = self.jj_players[2]
        self.myself = self.jj_players[3]
        self.marmalade_bush = self.jj_players[4]
        self.spear_players = [i for i in self.jj_players \
            if i['ign'] != self.purple_smokebush['ign'] \
            and i['ign'] != self.myself['ign'] \
            and i['ign'] != self.marmalade_bush['ign']]

    def check_bday(self, test=False) -> dict:
        if test: now=dt(2022, 8, 19, 0, 0, 1)
        else: now = dt.now()
        mon = now.month
        day = now.day
        for player in self.jj_players:
            if player['b_mon'] == mon and player['b_day'] == day:
                return player
        return False

    def get_spear_grass(self, test_date:dt=False) -> list:
        one_day = 86400
        if test_date:
            today = int((test_date.timestamp()/one_day)%12)
        else:
            today = int((dt.now().timestamp()/one_day)%12)
        first = self.spear_players[today%12]['ign']
        second = self.spear_players[(today+1)%12]['ign']
        third = self.spear_players[(today+2)%12]['ign']

        return [first, second, third]

if __name__ == "__main__":
    from datetime import timedelta as td
    diff = td(days=1)
    one_day = 86400
    today = (dt.now()+diff)+diff
    tomm = today+diff
    print(dt.now())
    # two_day = today+2
    # print(jj_players[today])
    # print(jj_players[tomm])
    # print(jj_players[two_day])
    # print(check_bday(True))
    jjp = jj_players()
    print(f"realtime spear grass = {jjp.get_spear_grass()}")
    print(jjp.get_spear_grass(today))
    print(jjp.get_spear_grass(tomm))
