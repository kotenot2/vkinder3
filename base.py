import psycopg2

conn = psycopg2.connect(database="postgres", user="postgres", password="38621964")

class Baseclass:

    def delete_tables(self, conn):
        with conn.cursor() as cur:
            cur.execute("""Drop table if exists profiles;""")
            conn.commit()
        # print('Таблицы успешно удалены')

    def create_db(self, conn):
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS profiles(
            
            id serial primary key unique,
            user_search_id integer UNIQUE,
            name VARCHAR NOT NULL
            );
            """)
            # print('Таблица profiles создана')
            conn.commit()



    def insert_profiles(self, conn,user_search_id, name):
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO profiles (user_search_id, name)
                VALUES (%s, %s);
            """,
            (user_search_id, name)
            )
            # print('Внесены данные в тблицу')
            conn.commit()

    def delete_db(self, conn):
        with conn.cursor() as cur:
            cur.execute("""
            DELETE from profiles;
            """)
            # print('Таблица profiles очищена')
            conn.commit()

    def select_profiles(self, conn, user_search_id):
        with conn.cursor() as cur:
            cur.execute(""" 
            SELECT user_search_id, name FROM profiles
            """, )
            list_profiles = cur.fetchall()


        # print(list_profiles)
        return list_profiles



base = Baseclass()
# base.select_profiles(conn, 131810384)