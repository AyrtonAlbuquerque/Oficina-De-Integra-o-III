import psycopg2
from contextlib import contextmanager
from src.config import LOAD_TEST_DATA

DB_PASSWORD = 'admin'

connectionArgs = {
  'user': "admin",
  'password': DB_PASSWORD,
  'host': "127.0.0.1",
  'port': "5432",
  'database': "SmartRecyclerDb"
}

def setup():
  with get_cursor() as (conn, cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
      username varchar PRIMARY KEY,
      pwd_hash varchar,
      is_admin boolean,
      balance float(4));""")

    cur.execute("""
      CREATE TABLE IF NOT EXISTS transactions (
        ID serial PRIMARY KEY,
        to_account varchar,
        from_account varchar,
        amount float(4),
        created_at date);""")
    
    cur.execute("""
      CREATE TABLE IF NOT EXISTS recyclers (
        ID serial PRIMARY KEY,
        name varchar,
        description varchar);""")

    cur.execute("""
      CREATE TABLE IF NOT EXISTS classifications (
        ID serial PRIMARY KEY,
        recycler_id int,
        label int,
        redeem_code varchar,
        is_redeemed boolean,
        image_path varchar,
        CONSTRAINT recycler_cons FOREIGN KEY(recycler_id)  REFERENCES recyclers(ID));""")

    if LOAD_TEST_DATA:
      cur.execute("SELECT * FROM recyclers WHERE name='TestRecycler'")
      if not cur.fetchone():
        cur.execute("""
          INSERT INTO recyclers (name, description)
            VALUES (%s, %s);
          """, ('TestRecycler', 'Recycler to test'))
        conn.commit()
      

@contextmanager
def get_cursor():
  """Returns database connection and cursor as a tuple"""
  with psycopg2.connect(**connectionArgs) as conn:
    with conn.cursor() as cur:
      yield (conn, cur)

if __name__ == '__main__':
  setup()