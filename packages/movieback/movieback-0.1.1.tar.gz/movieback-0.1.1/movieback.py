import sqlite3


class movieback:
    def __init__(self, filename: str, columns=(), dbname: str = "movies"):
        self._filename = filename
        self._columns = columns
        self._dbname = dbname

        self._create_database()

    def _connect(self):
        con = sqlite3.connect(f"{self._filename}")
        cur = con.cursor()
        return con, cur

    def _create_database(self):
        self._query(
            f"CREATE TABLE IF NOT EXISTS {self._dbname}(id INTEGER PRIMARY KEY)"
        )

        for column_name, column_type in self._columns:
            self._add_column(column_name, column_type)

    def _query(self, query, parameters=()):
        con, cur = self._connect()
        cur.execute(query, parameters)
        result = cur.fetchall()
        con.commit()
        con.close()
        return result

    def _add_column(self, column_name: str, column_type: str):
        existing_columns = [col[1] for col in self._query(f"PRAGMA table_info({self._dbname})")]
        if column_name not in existing_columns:
            query = (
                f"ALTER TABLE {self._dbname} ADD COLUMN {column_name} {column_type}"
            )
            self._query(query)


    def _remove_column(self, column_name: str):
        query = f"ALTER TABLE {self._dbname} DROP COLUMN {column_name}"
        self._query(query)

    def add_movie(self, **kwargs):
        columns = ", ".join(kwargs.keys())
        values = tuple(kwargs.values())
        placeholders = ", ".join(["?" for _ in range(len(kwargs))])
        query = (
            f"INSERT INTO {self._dbname} ({columns}) VALUES ({placeholders})"
        )
        self._query(query, values)

    def remove_movie(self, movie_id: int):
        query = f"DELETE FROM {self._dbname} WHERE id = ?"
        self._query(query, (movie_id,))

    def list_movies(self):
        query = f"SELECT * FROM {self._dbname}"
        return self._query(query)

    def search_movies(self, search_term: str, column: str = None):
        if search_term == "":
            return []

        if column and column in [col[0] for col in self._columns]:
            query = f"SELECT * FROM {self._dbname} WHERE {column} LIKE ?"
            return self._query(query, ("%" + search_term + "%",))
        else:
            placeholders = " OR ".join(
                [f"{col[0]} LIKE ?" for col in self._columns]
            )
            query = f"SELECT * FROM {self._dbname} WHERE {placeholders}"
            parameters = ["%" + search_term + "%" for _ in self._columns]
            return self._query(query, parameters)

    def edit_movie(self, movie_id: int, **kwargs):
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        parameters = list(kwargs.values())
        parameters.append(movie_id)
        query = f"UPDATE {self._dbname} SET {set_clause} WHERE id = ?"
        self._query(query, tuple(parameters))
