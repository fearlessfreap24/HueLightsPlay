import sqlite3
from traceback import format_exc
from dataclasses import dataclass

@dataclass
class JJ_Player:
    index: int
    name: str
    ign: str
    location: str
    b_mo: int = 0
    b_day: int = 0


class JJ_DB:

    # TEST = True
    TEST = False

    def __init__(self) -> None:
        if JJ_DB.TEST:
            self.__conn = sqlite3.connect(":memory:", check_same_thread=False)
        else:
            self.__conn = sqlite3.connect("jj_db.db", check_same_thread=False)

        self.__c = self.__conn.cursor()
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


    
if __name__ == "__main__":
    db = JJ_DB()
    # with open("jj_players.txt", 'r') as f:
    #     lines = f.readlines()

    # for line in lines:
    #     line = line.split(',')
    #     db.add_player(
    #         JJ_Player(
    #             int(line[0]),
    #             line[1],
    #             line[2],
    #             line[3],
    #             int(line[4]),
    #             int(line[5])
    #         )
    #     )
    print(
        db.get_player_from_index(
            db.get_player_from_name("Dylan").index+1
        )
    )
    
    db.close()

