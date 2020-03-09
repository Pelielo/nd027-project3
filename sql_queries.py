import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "drop table if exists stg_events"
staging_songs_table_drop = "drop table if exists stg_songs"
songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES

staging_events_table_create= ("""
    create table if not exists stg_events(
        artist varchar,
        auth varchar,
        firstName varchar
        gender char(1),
        itemInSession int,
        lastName varchar,
        length numeric,
        level varchar,
        location varchar,
        method varchar,
        page varchar,
        registration varchar,
        sessionId int,
        song varchar,
        status int,
        ts timestamp,
        userAgent varchar,
        userId int
    )
""")

staging_songs_table_create = ("""
    create table if not exists stg_songs(
        num_songs int,
        artist_id varchar,
        artist_latitude numeric,
        artist_longitude numeric,
        artist_location varchar,
        artist_name varchar,
        song_id varchar,
        title varchar,
        duration numeric
        year int
    )
""")

songplay_table_create = ("""
    create table if not exists songplays(
        songplay_id serial primary key, 
        user_id int references users(user_id), 
        song_id varchar references songs(song_id), 
        artist_id varchar references artists(artist_id), 
        start_time timestamp references time(start_time), 
        session_id int, 
        level varchar, 
        location varchar, 
        user_agent varchar
    )""")

user_table_create = ("""
    create table if not exists users(
        user_id int primary key, 
        first_name varchar, 
        last_name varchar, 
        gender varchar, 
        level varchar
    )""")

song_table_create = ("""
    create table if not exists songs(
        song_id varchar primary key, 
        title varchar, 
        artist_id varchar, 
        year int, 
        duration numeric
    )""")

artist_table_create = ("""
    create table if not exists artists(
        artist_id varchar primary key, 
        name varchar, 
        location varchar, 
        latitude numeric, 
        longitude numeric
    )""")


time_table_create = ("""
    create table if not exists time(
        start_time timestamp primary key, 
        hour int, 
        day int, 
        week int, 
        month int, 
        year int, 
        weekday int
    )""")

# STAGING TABLES

staging_events_copy = ("""
""").format()

staging_songs_copy = ("""
""").format()

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
