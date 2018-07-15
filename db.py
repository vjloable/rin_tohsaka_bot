import psycopg2

conn = psycopg2.connect("dbname=test user=postgres")
cur = conn.cursor()

cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))

conn.commit()

cur.close()
conn.close()
