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
        firstName varchar,
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
        ts varchar,
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
        duration numeric,
        year int
    )
""")

songplay_table_create = ("""
    create table if not exists songplays(
        songplay_id int identity(1,1) primary key sortkey distkey, 
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
        user_id int primary key sortkey, 
        first_name varchar, 
        last_name varchar, 
        gender varchar, 
        level varchar
    )""")

song_table_create = ("""
    create table if not exists songs(
        song_id varchar primary key sortkey, 
        title varchar, 
        artist_id varchar, 
        year int, 
        duration numeric
    )""")

artist_table_create = ("""
    create table if not exists artists(
        artist_id varchar primary key sortkey, 
        name varchar, 
        location varchar, 
        latitude numeric, 
        longitude numeric
    )""")


time_table_create = ("""
    create table if not exists time(
        start_time timestamp primary key sortkey, 
        hour int, 
        day int, 
        week int, 
        month int, 
        year int, 
        weekday int
    )""")

# STAGING TABLES

# USE CONF VARIABLES FOR S3 BUCKETS
staging_events_copy = ("""
    copy stg_events from {}
    credentials 'aws_iam_role={}'
    JSON {};
""").format(
    config.get("S3", "LOG_DATA"),
    config.get("IAM_ROLE", "ARN"),
    config.get("S3", "LOG_JSONPATH"))

staging_songs_copy = ("""
    copy stg_songs from {}
    timeformat 'auto'
    credentials 'aws_iam_role={}'
    JSON 'auto';
""").format(
    config.get("S3", "SONG_DATA"),
    config.get("IAM_ROLE", "ARN"))

# FINAL TABLES

songplay_table_insert = ("""
    insert into songplays (user_id, song_id, artist_id, start_time,
                            session_id, level, location, user_agent)
    select 
        e.userId,
        s.song_id,
        s.artist_id,
        timestamp 'epoch' + CAST(e.ts AS BIGINT)/1000 * interval '1 second',
        e.sessionId,
        e.level,
        e.location,
        e.userAgent
    from stg_events e
    join stg_songs s on e.artist = s.artist_name 
    and e.song = s.title  
""")

user_table_insert = ("""
    insert into users (user_id, first_name, last_name, gender, level)
    select 
        e.userId,
        e.firstName,
        e.lastName,
        e.gender,
        e.level
    from stg_events e
""")

song_table_insert = ("""
    insert into songs (song_id, title, artist_id, year, duration)
    select
        s.song_id,
        s.title,
        s.artist_id,
        s.year,
        s.duration
    from stg_songs s
""")

artist_table_insert = ("""
    insert into artists (artist_id, name, location, latitude, longitude)
    select
        s.artist_id,
        s.artist_name,
        s.artist_location,
        s.artist_latitude,
        s.artist_longitude
    from stg_songs s    
""")

time_table_insert = ("""
    insert into time (start_time, hour, day, week, month, year, weekday)
    select
        timestamp 'epoch' + CAST(e.ts AS BIGINT)/1000 * interval '1 second' as start_time,
        extract(hour from e.ts) as hour,
        extract(day from e.ts) as day,
        extract(week from e.ts) as week,
        extract(month from e.ts) as month,
        extract(year from e.ts) as year,
        extract(dow from e.ts) as weekday
    from stg_events e
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert, songplay_table_insert]
