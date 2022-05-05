import psycopg2
from contextlib import contextmanager

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
    # Execute a command: this creates a new table
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

@contextmanager
def get_cursor():
  with psycopg2.connect(**connectionArgs) as conn:
    with conn.cursor() as cur:
      yield (conn, cur)


def other():

  # Pass data to fill a query placeholders and let Psycopg perform
  # the correct conversion (no more SQL injections!)
  cur.execute("INSERT INTO User (num, data) VALUES (%s, %s)", (101, "abc'def"))
  cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (102, "abc'def"))
  cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (103, "abc'def"))

  # Query the database and obtain data as Python objects
  cur.execute("SELECT * FROM test;")
  print(cur.fetchone())
  print(cur.fetchone())
  print(cur.fetchone())
  print(cur.fetchone())

  # Make the changes to the database persistent
  conn.commit()


if __name__ == '__main__':
  setup()