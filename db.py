import sqlite3, json
from traceback import format_exc
from dataclasses import dataclass
from threading import Lock
from datetime import datetime as dt
from datetime import timedelta as td

@dataclass
class JJ_Player:
    index: int
    name: str
    ign: str
    location: str
    b_mo: int = 0
    b_day: int = 0
    is_spear: int = 1

    def __eq__(self, __value: object) -> bool:
        return self.index == __value.index \
            and self.name == __value.name \
            and self.ign == __value.ign

    def __iter__(self):
        attribs = [
            "index",
            "name",
            "ign",
            "location",
            "b_mo",
            "b_day",
            "is_spear"
        ]
        for i in range(len(attribs)):
            yield self.__dict__[attribs[i]]


@dataclass
class Bush:
    bush_type: str
    sender: str
    date: float
    diamonds: int
    ribbons: int = 0

    def __iter__(self):
        attribs = [
            "bush_type",
            "sender",
            "date",
            "diamonds",
            "ribbons"
        ]
        for i in range(len(attribs)):
            yield self.__dict__[attribs[i]]


class JJ_DB:

    # TEST = True
    # TEST = False

    def __init__(self, test=False) -> None:
        if test:
            # self.__conn = sqlite3.connect(":memory:", check_same_thread=False)
            self.__conn = sqlite3.connect(
                "db/03142023_jj_db.db",
                check_same_thread=False
            )
        else:
            # self.__conn = sqlite3.connect("/mnt/jj/jj_db.db", check_same_thread=False)
            self.__conn = sqlite3.connect(
                "/mnt/db/03142023_jj_db.db",
                check_same_thread=False
            )

        # self.__c = self.__conn.cursor()
        self.__lock = Lock()
        self.__main()

    def __main(self):
        with self.__conn:
            self.__conn.cursor().execute(
                """
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY Key,
                    name TEXT NOT NULL,
                    ign TEXT NOT NULL,
                    location TEXT,
                    birth_mo INTEGER,
                    birth_d INTEGER,
                    is_spear INTEGER
                )
                """
            )
        with self.__conn:
            try:
                self.__lock.acquire(True)
                self.__conn.cursor().execute(
                    """
                    CREATE TABLE IF NOT EXISTS bush_data(
                        bush_name TEXT,
                        sender TEXT,
                        date TEXT,
                        diamonds INTEGER,
                        ribbons INTEGER
                    )
                    """
                )
            finally:
                self.__lock.release()
        with self.__conn:
            try:
                self.__lock.acquire(True)
                self.__conn.cursor().execute(
                    """
                    CREATE VIEW IF NOT EXISTS v_bush_list AS
                    SELECT * FROM players p 
                    WHERE is_spear = 1;
                    """
                )
            finally:
                self.__lock.release()

    def add_player(self, player: JJ_Player) -> None:
        try:
            with self.__conn:
                self.__lock.acquire(True)
                self.__conn.cursor().execute(
                    """
                    INSERT INTO players
                    VALUES (
                        ?, ?, ?, ?, ?, ?, ?
                    )
                    """, tuple(player)
                )
        finally:
            self.__lock.release()

    def add_many_players(self, players: list) -> None:
        try:
            with self.__conn:
                self.__lock.acquire(True)
                self.__conn.cursor().executemany(
                    """
                    INSERT INTO players
                    VALUES (
                        ?, ?, ?, ?, ?, ?, ?
                    )
                    """, players
                )
        finally:
            self.__lock.release()

    def get_all_players(self) -> list:
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    """
                    SELECT *
                    FROM players
                    """
                )
                players = __c.fetchall()
        finally:
            self.__lock.release()

        return players

    def get_all_players_obj(self) -> list:
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    """
                    SELECT *
                    FROM players
                    """
                )
                players = __c.fetchall()
                players = [
                    JJ_Player(
                        i[0],
                        i[1],
                        i[2],
                        i[3],
                        i[4],
                        i[5],
                        i[6]
                ) for i in players]
        finally:
            self.__lock.release()

        return players

    def get_player_from_index(self, index: int) -> JJ_Player:
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    """
                    SELECT *
                    FROM players
                    WHERE id=?
                    """, (index,)
                )
                player = __c.fetchone()
        finally:
            self.__lock.release()

        return JJ_Player(
            player[0],
            player[1],
            player[2],
            player[3],
            player[4],
            player[5],
            player[6]
            )

    def get_player_from_name(self, name: str) -> JJ_Player:
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    """
                    SELECT *
                    FROM players
                    WHERE name=?
                    """, (name,)
                )
                player = __c.fetchone()
        finally:
            self.__lock.release()

        return JJ_Player(
            player[0],
            player[1],
            player[2],
            player[3],
            player[4],
            player[5],
            player[6]
            )

    def get_player_from_ign(self, ign: str) -> JJ_Player:
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    """
                    SELECT *
                    FROM players
                    WHERE ign=?
                    """, (ign,)
                )
                player = __c.fetchone()
        finally:
            self.__lock.release()

        return JJ_Player(
            player[0],
            player[1],
            player[2],
            player[3],
            player[4],
            player[5],
            player[6]
            )

    def get_spear_grass_players(self) -> list:
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    '''
                    SELECT *
                    FROM v_bush_list
                    '''
                )
                s_g = [JJ_Player(
                    i[0],
                    i[1],
                    i[2],
                    i[3],
                    i[4],
                    i[5],
                    i[6])
                    for i in __c.fetchall()]
        finally:
            self.__lock.release()

        return s_g

    def get_birthday_player(self, b_mo:int, b_day:int) -> JJ_Player:
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    '''
                    SELECT *
                    FROM players
                    WHERE birth_mo = ?
                    AND birth_d = ?
                    ''',
                    (b_mo, b_day)
                )
                bday_players = __c.fetchall()
        finally:
            self.__lock.release()
        if bday_players:
            bday_players = [
                JJ_Player(
                    i[0],
                    i[1],
                    i[2],
                    i[3],
                    i[4],
                    i[5],
                    i[6]
                ) for i in bday_players
            ]
        return bday_players

    def close(self):
        self.__conn.close()

    def load_data(self, data: list[tuple]) -> None:
        with self.__conn:
            self.__c.executemany(
                """
                INSERT INTO bush_data VALUES(?,?,?,?)
                """, data
            )

    def get_diamonds_by_bush(self) -> list:
        dc = []
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    """
                    SELECT bush_name, SUM(diamonds)
                    FROM bush_data bd
                    GROUP BY bush_name 
                    """
                )
                dc = __c.fetchall()
        finally:
            self.__lock.release()
        return [list(i) for i in dc]

    def get_bush_count(self) -> list:
        bc = []
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    """
                    SELECT bush_name, COUNT(sender) 
                    FROM bush_data bd 
                    GROUP BY bush_name 
                    """
                )
                bc = __c.fetchall()
        finally:
            self.__lock.release()
        return [list(i) for i in bc]

    def add_bush(self, bush:Bush):
        try:
            self.__lock.acquire(True)
            with self.__conn:
                self.__conn.cursor().execute(
                    """
                    INSERT INTO bush_data VALUES(
                        ?,?,?,?,?
                    )
                    """, tuple(bush)
                )
        finally:
            self.__lock.release()

    def get_all_bush_data(self):
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    """
                    SELECT * FROM bush_data
                    """
                )
                data = __c.fetchall()
        finally:
            self.__lock.release()

        return [list(i) for i in data]

    def get_bushes_gave_diamonds(self) -> list:
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    """
                    SELECT bd.bush_name ,COUNT(*) 
                    FROM bush_data bd 
                    WHERE bd.diamonds != 0
                    GROUP BY bd.bush_name ;
                    """
                )
                bc = __c.fetchall()
        finally:
            self.__lock.release()
        return [list(i) for i in bc]
        
    def get_spear_grass_data(self) -> dict:
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    """
                    SELECT COUNT(bd.ribbons)
                    FROM bush_data bd;
                    """
                )
                ribbons = __c.fetchall()[0][0]

                __c.execute(
                    """
                    SELECT COUNT(*)
                    FROM bush_data bd
                    WHERE bush_name = 'Spear Grass'
                    AND bd.diamonds > 0;
                    """
                )

                diamonds = __c.fetchall()[0][0]

                __c.execute(
                    """
                    SELECT COUNT(*)
                    FROM bush_data bd
                    WHERE bush_name = 'Spear Grass';
                    """
                )
                all_spear_grass = __c.fetchall()[0][0]
        finally:
            self.__lock.release()

        all_spear_grass = float(all_spear_grass)
        diamonds = float(diamonds)/all_spear_grass
        ribbons = float(ribbons)/all_spear_grass
        no_ribbons_no_diamonds = (1-(ribbons+diamonds))
        return {
            "spear_grass_none": no_ribbons_no_diamonds,
            "spear_grass_diamonds" : diamonds,
            "spear_grass_ribbons" : ribbons
        }
    
    def last_7_data(self):
        now = dt.now()
        now_ts = now.timestamp()
        seven_days = (now - td(days=7)).timestamp()
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    """
                    SELECT bush_name,
                    COUNT(bush_name) as "Total Bushes",
                    SUM(diamonds) as "Total Diamonds",
                    SUM(ribbons) as "Total Ribbons" 
                    FROM bush_data bd 
                    WHERE date < ?
                    AND date > ?
                    GROUP BY bush_name ;
                    """, (now_ts, seven_days)
                )
                data = __c.fetchall()
        finally:
            self.__lock.release()
        return [list(i) for i in data]
    
    def last_24_data(self):
        now = dt.now()
        now_ts = now.timestamp()
        seven_days = (now - td(hours=24)).timestamp()
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    """
                    SELECT bush_name,
                    COUNT(bush_name) as "Total Bushes",
                    SUM(diamonds) as "Total Diamonds",
                    SUM(ribbons) as "Total Ribbons" 
                    FROM bush_data bd 
                    WHERE date < ?
                    AND date > ?
                    GROUP BY bush_name ;
                    """, (now_ts, seven_days)
                )
                data = __c.fetchall()
        finally:
            self.__lock.release()
        return [list(i) for i in data]
    
    def update_jj_ids(self, num:int):
        max_id = max([i.index for i in self.get_all_players_obj()])
        id_list = [(i-1, i) for i in range(num, max_id+1)]
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.executemany(
                    """
                    UPDATE PLAYERS
                    SET id = ?
                    WHERE id = ?;
                    """,
                    id_list
                )
        finally:
            self.__lock.release()
        # for i in id_list:
        #     print(i)
    
    def update_jj_ids_plus(self, num:int):
        max_id = max([i.index for i in self.get_all_players_obj()])
        id_list = [(i+1, i) for i in range(num, max_id+1)]
        try:
            self.__lock.acquire(True)
            with self.__conn:
                __c = self.__conn.cursor()
                __c.executemany(
                    """
                    UPDATE PLAYERS
                    SET id = ?
                    WHERE id = ?;
                    """,
                    id_list[::-1]
                )
        finally:
            self.__lock.release()

    def remove_player_by_id(self, id: int) -> bool:
        del_player = self.get_player_from_index(id)
        print(del_player)
        try:
            self.__lock.acquire()
            with self.__conn:
                __c = self.__conn.cursor()
                __c.execute(
                    """
                    DELETE FROM players
                    where id = ?;
                    """,
                    (id,)
                )
        finally:
            self.__lock.release()
        self.update_jj_ids(id+1)
        try:
            new_player = self.get_player_from_index(id)
            print(new_player)
        except: return True
        return del_player != new_player
        

if __name__ == "__main__":
    import json
    player = [
        "MeerkatOverlord",
        "Detective Ivik",
        "SherLynn",
        "ZerepNalyd",
        "Pandora",
        "Bullet",
        "Joana",
        "Miss Nona",
        "Found_Myself",
        "JR",
        "Feather&Pearls",
        "Morrigan",
        "Expelliarmus",
        "Keith 2"
    ]

    player_list = [tuple([i[0]+1, i[1], i[1], None, None, None, None]) for i in enumerate(player)]
    print(json.dumps(player_list, indent=4))

    # player_list = [
    #     (5, "Cheri", "Juniper Berry", None, None, None, None),
    #     (6, "Cynthia", "Cynthiaisbummed", None, None, None, None),
    #     (7, "Jim", "Finders", None, None, None, None),
    #     (8, "Cammy", "Cammie", None, None, None, None),
    #     (9, "Bobbi", "Cupcake", None, None, None, None),
    #     (10, "AMC", "AMC", None, None, None, None),
    #     (11, "Stephanie", "Epiphany", None, None, None, None),
    #     (12, "Rhonda", "Minne", None, None, None, None),
    #     (13, "Dylan", "Zerep Nalyd", None, None, None, None),
    #     (14, "", "Rov ostrov", None, None, None, None),
    #     (15, "", "Gonnfindityay", None, None, None, None)
    # ]

    # print(json.dumps(player_list, indent=4))


    db = JJ_DB(True)
    # # all_players = db.get_all_players_obj()
    # # dylan = [i for i in all_players if i.name == "Dylan"][0]
    # # bushes = [
    # #     i for i in all_players if i.index == (dylan.index+1)%len(all_players)
    # #     or i.index == (dylan.index+2)%len(all_players)
    # # ]
    # # for i in bushes: print(i)
    # db.add_many_players(player_list)
    # db.update_jj_ids_plus(3)
    # db.update_jj_ids(3)
    # print(db.remove_player_by_id(9))
    # print(db.get_all_players())
    # print(json.dumps(db.update_jj_ids(2),indent=4))
    # # with open("./test_data.csv", 'r') as f:
    # #     lines = f.readlines()

    # # line_arr = [tuple(i.split(',')[:4]) for i in lines]
    # # db.load_data(line_arr)
    # print(db.get_diamonds_by_bush())
    # print(db.get_bush_count())
    
    # bush = Bush("purple", dt.now().timestamp(), "dylan", 10)
    # print(tuple(bush))
    # db.update_jj_ids_plus(3)
    player = JJ_Player(
        15,
        "Lotvia",
        "Lotvia",
        None,
        None,
        None
    )
    print(tuple(player))
    db.add_player(player)
    # print(db.get_all_players())
    # db.remove_player_by_id(11)
    # db.add_bush(bush)
    # print(db.get_all_bush_data())
    # print(db.get_spear_grass_data())
    # print(len(db.get_all_players()))
    # print(db.last_7_data())
    # print(db.last_24_data())
    db.close()
    # arr = [1, 2]
    # print(arr)
    # print(arr[::-1])
