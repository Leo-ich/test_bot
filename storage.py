from contextlib import closing

import psycopg2
from psycopg2 import sql


def db_connect(func):
    def wrapper(self, *args, **kwargs):
        result = self.execute(func, *args, **kwargs)
        return result
    return wrapper


class PgStorage:

    def __init__(self, config=None, **kwargs):
        self._conn_params = {}
        if config:
            self._conn_params = {
                "database": config.DB_NAME,
                "user": config.DB_USER_NAME,
                "password": getattr(config, 'DB_PASS', ''),
                "host": config.DB_HOST,
                "port": config.DB_PORT,
                "sslmode": 'prefer',
            }
        self._conn_params.update(kwargs)
        self.create_table()

    def execute(self, func, *args, **kwargs):
        with closing(psycopg2.connect(**self._conn_params)) as db_conn:
            db_conn.autocommit = True
            with db_conn.cursor() as db_cursor:
                result = func(self, db_cursor, *args, **kwargs)
        return result

    @db_connect
    def create_table(self, cursor):
        # 1-1
        query = """
        CREATE TABLE IF NOT EXISTS  users
        (
            id  BIGINT NOT NULL PRIMARY KEY,
            name VARCHAR(256),
            last_name VARCHAR(256),
            step SMALLINT
        );
        CREATE TABLE IF NOT EXISTS car
        (
            id SERIAL NOT NULL PRIMARY KEY,
            model VARCHAR(256),
            year SMALLINT,
            power SMALLINT,
            user_id INTEGER NOT NULL UNIQUE 
        );
        """
        cursor.execute(query)

    @db_connect
    def get_known_users(self, cursor):
        query = """
        SELECT id FROM users ;
        """
        cursor.execute(query)
        known_users = cursor.fetchall()
        known_users = [t[0] for t in known_users]
        return known_users

    @db_connect
    def add_user(self, cursor, uid, step):
        query = """
        INSERT INTO users
         (id, step)
         VALUES
          (%s, %s)
          ON CONFLICT (id) DO UPDATE SET step = 0;
        """
        cursor.execute(query, (uid, step))
        return

    @db_connect
    def update_data(self, cursor, table, data_key, val, pkey, pval):
        query = sql.SQL("UPDATE {tab_name}"
                        " SET {field} = %s"
                        " WHERE {pkey} = %s;").format(
            tab_name=sql.Identifier(table),
            field=sql.Identifier(data_key),
            pkey=sql.Identifier(pkey),
        )
        cursor.execute(query, (val, pval))
        return

    @db_connect
    def get_step(self, cursor, uid):
        query = """
        SELECT step FROM users WHERE id = %s;
        """
        cursor.execute(query, (uid,))
        step = cursor.fetchone()
        return step[0]

    @db_connect
    def add_car(self, cursor, uid):
        # 1 user - 1 car
        query = """
        INSERT INTO car
         (user_id)
         VALUES
          (%s)
          ON CONFLICT (user_id) DO NOTHING ;
        """
        cursor.execute(query, (uid,))
        return

    @db_connect
    def get_version(self, cursor=None):
        # ver = 12
        query = 'SELECT version()'
        cursor.execute(query)
        print(cursor.fetchall())

    @db_connect
    def get_users(self, cursor, params):
        query = """
            SELECT name, last_name, model, year, power
            FROM users AS u, car AS c
            WHERE u.name LIKE %s
              AND u.last_name LIKE %s
              AND c.model LIKE %s
              AND c.year::VARCHAR(15) LIKE %s
              AND c.power::VARCHAR(15) LIKE %s
              AND u.id = c.user_id;
        """
        sql_param = [params['user_name'],
                     params['last_name'],
                     params['car_model'],
                     params['year'],
                     params['power']]
        cursor.execute(query, sql_param)
        result = cursor.fetchall()
        return {'result': result}

