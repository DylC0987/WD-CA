DROP TABLE IF EXISTS albums;


CREATE TABLE albums (
  album_id INTEGER PRIMARY KEY AUTOINCREMENT,
  album_name TEXT NOT NULL,
  artist TEXT NOT NULL,
  release_year INTEGER NOT NULL,
  genre TEXT NOT NULL,
  avg_rating REAL DEFAULT 0.0,
  image_url TEXT
  );


INSERT INTO albums (album_name, artist, release_year, genre, avg_rating, image_url)
VALUES
  ('Thriller', 'Michael Jackson', 1982, 'Pop', 0,'Thriller_image.jpg' ),
  ('Abbey Road', 'The Beatles', 1969, 'Rock', 0, 'Abbey_Road_image.jpg'),
  ('Nevermind', 'Nirvana', 1991, 'Grunge',0,'Nevermind_image.jpg'),
  ('Kind of Blue', 'Miles Davis', 1959, 'Jazz',0,'Kind_of_Blue_image.jpeg'),
  ('Rumours', 'Fleetwood Mac', 1977, 'Rock', 0, 'Rumours_image.jpg'),
  ('Franz Ferdinand', 'Franz Ferdinand', 2004, 'Indie Rock',0,'Franz_Ferdinand_image.jpg'),
  ('Hot Fuss', 'The Killers', 2004, 'Indie Rock', 0,'Hot_Fuss_image.jpeg'),
  ('American Idiot', 'Green Day', 2004, 'Pop Punk',0,'American_Idiot_image.jpeg'),
  ('Demon Days', 'Gorillaz', 2005, 'Alternative',0,'Demon_Days_image.jpg'),
  ('Currents', 'Tame Impala', 2015, 'Alternative',0,'Currents_image.jpg'),
  ('More Life', 'Drake', 2017, 'Hip Hop', 0,'More_Life_image.jpg'),
  ('Dawn FM', 'The Weeknd', 2022, 'Pop',0,'Dawn_FM_image.jpg'),
  ('Gloria', 'Sam Smith', 2023, 'Pop',0,'Gloria_image.jpg');





DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    bio TEXT DEFAULT '',
    followers_amount INTEGER DEFAULT 0,
    following_amount INTEGER DEFAULT 0
);


DROP TABLE IF EXISTS followers;

CREATE TABLE followers (
    user_id TEXT NOT NULL,
    follower_id TEXT NOT NULL
);






DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    review TEXT,
    likes INTEGER DEFAULT 0,
    dislikes INTEGER DEFAULT 0,
    date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(album_id) REFERENCES albums(album_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);



DROP TABLE IF EXISTS likes_dislikes;

CREATE TABLE likes_dislikes (
like_dislike_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
review_id INTEGER NOT NULL,
like_or_dislike TEXT NOT NULL);







