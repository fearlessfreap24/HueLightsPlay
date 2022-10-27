import sqlite3
from traceback import format_exc
from dataclasses import dataclass
from threading import Lock
from datetime import datetime as dt

@dataclass
class JJ_Player:
    index: int
    name: str
    ign: str
    location: str
    b_mo: int = 0
    b_day: int = 0


@dataclass
class Bush:
    bush_type: str
    sender: str
    date: float
    diamonds: int
    ribbons: int = 0

    def __iter__(self):
        attribs = ["bush_type", "sender", "date", "diamonds", "ribbons"]
        for i in range(len(attribs)):
            yield self.__dict__[attribs[i]]


class JJ_DB:

    # TEST = True
    TEST = False

    def __init__(self) -> None:
        if JJ_DB.TEST:
            self.__conn = sqlite3.connect(":memory:", check_same_thread=False)
        else:
            self.__conn = sqlite3.connect("jj_db.db", check_same_thread=False)

        self.__c = self.__conn.cursor()
        self.__lock = Lock()
        self.__main()

    def __main(self):
        with self.__conn:
            self.__c.execute(
                """
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY Key,
                    name TEXT NOT NULL,
                    ign TEXT NOT NULL,
                    location TEXT,
                    birth_mo INTEGER,
                    birth_d INTEGER
                )
                """
            )
        with self.__conn:
            try:
                self.__lock.acquire(True)
                self.__c.execute(
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

    def add_player(self, player: JJ_Player) -> None:
        with self.__conn:
            self.__c.execute(
                """
                INSERT INTO players
                VALUES (
                    :id, :name, :ign, :loc, :b_mo, :b_day
                )
                """,
                {
                    "id": player.index,
                    "name": player.name,
                    "ign": player.ign,
                    "loc": player.location,
                    "b_mo": player.b_mo,
                    "b_day": player.b_day
                }
            )

    def get_player_from_index(self, index: int) -> JJ_Player:

        with self.__conn:
            self.__c.execute(
                """
                SELECT *
                FROM players
                WHERE id=?
                """, (index,)
            )
            player = self.__c.fetchone()        

        return JJ_Player(
            player[0],
            player[1],
            player[2],
            player[3],
            player[4],
            player[5]
            )

    def get_player_from_name(self, name: str) -> JJ_Player:

        with self.__conn:
            self.__c.execute(
                """
                SELECT *
                FROM players
                WHERE name=?
                """, (name,)
            )
            player = self.__c.fetchone()        

        return JJ_Player(
            player[0],
            player[1],
            player[2],
            player[3],
            player[4],
            player[5]
            )

    def get_player_from_ign(self, ign: str) -> JJ_Player:
        with self.__conn:
            self.__c.execute(
                """
                SELECT *
                FROM players
                WHERE ign=?
                """, (ign,)
            )
            player = self.__c.fetchone()        

        return JJ_Player(
            player[0],
            player[1],
            player[2],
            player[3],
            player[4],
            player[5]
            )

    def get_spear_grass_players(self) -> list:
        with self.__conn:
            self.__c.execute(
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
                i[5])
                for i in self.__c.fetchall()]

        return s_g

    def get_birthday_player(self, b_mo:int, b_day:int) -> JJ_Player:
        with self.__conn:
            self.__c.execute(
                '''
                SELECT *
                FROM players
                WHERE birth_mo = ?
                AND birth_d = ?
                ''',
                (b_mo, b_day)
            )
            bday_players = self.__c.fetchall()
            if bday_players:
                bday_players = [
                    JJ_Player(
                        i[0],
                        i[1],
                        i[2],
                        i[3],
                        i[4],
                        i[5]
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
                self.__c.execute(
                    """
                    SELECT bush_name, SUM(diamonds)
                    FROM bush_data bd
                    GROUP BY bush_name 
                    """
                )
                dc = self.__c.fetchall()
        finally:
            self.__lock.release()
        return [list(i) for i in dc]

    def get_bush_count(self) -> list:
        bc = []
        try:
            self.__lock.acquire(True)
            with self.__conn:
                self.__c.execute(
                    """
                    SELECT bush_name, COUNT(sender) 
                    FROM bush_data bd 
                    GROUP BY bush_name 
                    """
                )
                bc = self.__c.fetchall()
        finally:
            self.__lock.release()
        return [list(i) for i in bc]

    def add_bush(self, bush:Bush):
        with self.__conn:
            self.__c.execute(
                """
                INSERT INTO bush_data VALUES(
                    ?,?,?,?,?
                )
                """, tuple(bush)
            )

    def get_all_bush_data(self):
        with self.__conn:
            self.__c.execute(
                """
                SELECT * FROM bush_data
                """
            )
            data = self.__c.fetchall()

        return [list(i) for i in data]


    
if __name__ == "__main__":
    db = JJ_DB()
    # # with open("./test_data.csv", 'r') as f:
    # #     lines = f.readlines()

    # # line_arr = [tuple(i.split(',')[:4]) for i in lines]
    # # db.load_data(line_arr)
    # print(db.get_diamonds_by_bush())
    # print(db.get_bush_count())
    

    bush = Bush("purple", dt.now().timestamp(), "dylan", 10)
    print(tuple(bush))
    db.add_bush(bush)
    print(db.get_all_bush_data())

    db.close()
