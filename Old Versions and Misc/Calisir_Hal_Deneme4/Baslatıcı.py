import psycopg2

def create_table():
    hostname = 'localhost'
    database = 'SeniorProject'
    username = 'postgres'
    pwd = '1234'
    port_id = 5432
    conn= psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id)

    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Log (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            datetime TIMESTAMP NOT NULL DEFAULT now(),
            action CHAR(1) NOT NULL CHECK (action IN ('i', 'o'))
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

create_table()