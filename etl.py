import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """Loads tables in "copy_table_queries" list 
    from a S3 bucket defined in config file"""
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """Inserts data from the staging tables into
    the star-schema tables defined in the 
    "insert_table_queries" list"""
    for query in insert_table_queries:
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
    
    print("Loading staging tables")
    load_staging_tables(cur, conn)

    print("Inserting from staging tables to star schema")
    insert_tables(cur, conn)

    print("Done")
    conn.close()


if __name__ == "__main__":
    main()