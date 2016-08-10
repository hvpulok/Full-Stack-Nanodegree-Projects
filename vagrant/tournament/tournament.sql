-- code to create a tournament database
DROP DATABASE IF EXISTS tournament;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;


CREATE DATABASE tournament;

-- create players table
CREATE TABLE players(                                                                                                                             
        playerID SERIAL PRIMARY KEY NOT NULL,                                                                                                             
        name TEXT NOT NULL);

-- create matches table
CREATE TABLE matches(                                                                                                                             
        matchID SERIAL PRIMARY KEY NOT NULL,                                                                                                             
        winner INT NOT NULL REFERENCES players(playerID),
        loser INT NOT NULL REFERENCES players(playerID));

-- sample players data
-- ==========================

INSERT INTO players (name) VALUES('Pulok');
INSERT INTO players (name) VALUES('Anika');
INSERT INTO players (name) VALUES('Akib');
INSERT INTO players (name) VALUES('Rajib');
INSERT INTO players (name) VALUES('Tony');
INSERT INTO players (name) VALUES('Mike');
INSERT INTO players (name) VALUES('Sara');
INSERT INTO players (name) VALUES('Jeny');


-- sample matches data
-- ==========================
INSERT INTO matches (winner, loser) VALUES(1, 2);
INSERT INTO matches (winner, loser) VALUES(3, 4);
INSERT INTO matches (winner, loser) VALUES(5, 6);
INSERT INTO matches (winner, loser) VALUES(7, 8);



SELECT * FROM players;
SELECT * FROM matches;

-- DELETE FROM players;
-- DELETE FROM matches;
