import psycopg2

def connect():
    c = psycopg2.connect("dbname=flask-toys")
    return c

def get_all_toys():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM toys;")
    toys = cur.fetchall()
    cur.close()
    conn.close()
    return toys

def get_toy_by_id(id):
	conn = connect()
	cur = conn.cursor()
	cur.execute("SELECT * FROM toys WHERE id=%s", [id])
	toys = cur.fetchall()
	cur.close()
	conn.close()
	return toys

def edit_toy(id, name):
	conn = connect()
	cur = conn.cursor()
	cur.execute("UPDATE toys SET name=%s WHERE id=%s;", [name, id])
	conn.commit()
	cur.close()
	conn.close()

def add_toy(name):
	conn = connect()
	cur = conn.cursor()
	cur.execute("INSERT INTO toys (name) VALUES (%s);", (name,))
	conn.commit()
	cur.close()
	conn.close()

def delete_toy(id):
	conn = connect()
	cur = conn.cursor()
	cur.execute("DELETE FROM toys WHERE id=%s", (id,))
	conn.commit()
	cur.close()
	conn.close()
