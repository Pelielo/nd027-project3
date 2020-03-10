import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    print("Connecting to Redshift cluster")
    conn = psycopg2.connect(
        f"""host={config.get("CLUSTER", "HOST")} 
            dbname={config.get("CLUSTER", "DB_NAME")} 
            user={config.get("CLUSTER", "DB_USER")} 
            password={config.get("CLUSTER", "DB_PASSWORD")} 
            port={config.get("CLUSTER", "DB_PORT")}"""
    )
    cur = conn.cursor()

    print("Dropping tables if they exist")
    drop_tables(cur, conn)

    print("Creating tables if they don't exist")
    create_tables(cur, conn)

    print("Done")
    conn.close()


if __name__ == "__main__":
    main()