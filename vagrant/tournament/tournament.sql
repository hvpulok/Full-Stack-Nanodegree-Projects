-- code to create a tournament database
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create players table
DROP TABLE IF EXISTS players;
CREATE TABLE players(                                                                                                                             
        playerID SERIAL PRIMARY KEY NOT NULL,                                                                                                             
        NAME TEXT NOT NULL);

-- create matches table
DROP TABLE IF EXISTS matches;
CREATE TABLE matches(                                                                                                                             
        matchID SERIAL PRIMARY KEY NOT NULL,                                                                                                             
        winner INT NOT NULL REFERENCES players(playerID),
        loser INT NOT NULL REFERENCES players(playerID));


SELECT * FROM players;
SELECT * FROM matches;

