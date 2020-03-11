import configparser
import psycopg2
import timeit

top_weekday_query = """select count(sp.songplay_id) as song_count, t.weekday
            from songplays sp
            join time t on sp.start_time = t.start_time
            group by t.weekday
            order by 1 desc"""

app_usage_query = """select count(sp.songplay_id) as song_count, t.hour
            from songplays sp
            join time t on sp.start_time = t.start_time
            group by t.hour
            order by t.hour"""

top_songs_query = """select count(*) song_count, s.title, a."name"
            from songplays sp
            join songs s on sp.song_id = s.song_id
            join artists a on sp.artist_id = a.artist_id
            group by s.title, a."name"
            order by 1 desc"""

top_locations_query = """select count(*), "location"
            from songplays sp
            group by "location"
            order by 1 desc"""


def execute_query(cur, conn, query):
    def _execute_query():
        cur.execute(query)
        conn.commit()
        pass
    return _execute_query


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
    
    time = timeit.timeit(execute_query(cur, conn, top_weekday_query), number=1)
    print(f"Executed top_weekday_query in {time} seconds")

    time = timeit.timeit(execute_query(cur, conn, app_usage_query), number=1)
    print(f"Executed app_usage_query in {time} seconds")

    time = timeit.timeit(execute_query(cur, conn, top_songs_query), number=1)
    print(f"Executed top_songs_query in {time} seconds")

    time = timeit.timeit(execute_query(cur, conn, top_locations_query), number=1)
    print(f"Executed top_locations_query in {time} seconds")

    print("Done")
    conn.close()


if __name__ == "__main__":
    main()