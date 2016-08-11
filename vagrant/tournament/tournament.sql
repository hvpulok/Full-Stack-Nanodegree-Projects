-- code to create a tournament database
DROP DATABASE IF EXISTS tournament;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;


CREATE DATABASE tournament;

-- create players table
CREATE TABLE players(                                                                                                                             
        playerid SERIAL PRIMARY KEY NOT NULL,                                                                                                             
        name TEXT NOT NULL);

-- create matches table
CREATE TABLE matches(                                                                                                                             
        matchID SERIAL PRIMARY KEY NOT NULL,                                                                                                             
        winner INT NOT NULL REFERENCES players(playerid),
        loser INT NOT NULL REFERENCES players(playerid));

-- sample players data
-- ==========================

INSERT INTO players (name) VALUES('Pulok');
INSERT INTO players (name) VALUES('Anika');
-- INSERT INTO players (name) VALUES('Akib');
-- INSERT INTO players (name) VALUES('Rajib');
-- INSERT INTO players (name) VALUES('Tony');
-- INSERT INTO players (name) VALUES('Mike');
-- INSERT INTO players (name) VALUES('Sara');
-- INSERT INTO players (name) VALUES('Jeny');


-- sample matches data
-- ==========================

-- INSERT INTO matches (winner, loser) VALUES(1, 2);
-- INSERT INTO matches (winner, loser) VALUES(3, 4);
-- INSERT INTO matches (winner, loser) VALUES(5, 6);
-- INSERT INTO matches (winner, loser) VALUES(7, 8);

-- 2nd round

-- INSERT INTO matches (winner, loser) VALUES(1, 3);
-- INSERT INTO matches (winner, loser) VALUES(5, 7);
-- INSERT INTO matches (winner, loser) VALUES(2, 4);
-- INSERT INTO matches (winner, loser) VALUES(6, 8);


-- SELECT * FROM players;
-- SELECT * FROM matches;

-- DELETE FROM players;
-- DELETE FROM matches;

    -- """Returns a list of the players and their win records, sorted by wins.

    -- The first entry in the list should be the player in first place, or a player
    -- tied for first place if there is currently a tie.

    -- Returns:
    --   A list of tuples, each of which contains (id, name, wins, matches):
    --     id: the player's unique id (assigned by the database)
    --     name: the player's full name (as registered)
    --     wins: the number of matches the player has won
    --     matches: the number of matches the player has played
    -- """
-- Code to get winner players id name and times won

SELECT * FROM players;
SELECT * FROM matches;


CREATE VIEW winnerTable AS 
    SELECT players.playerid, players.name, COUNT(players.playerid) AS number 
    FROM players, matches 
    WHERE players.playerid = matches.winner
    GROUP BY players.playerid, players.name 
    ORDER BY number DESC;

SELECT * FROM winnerTable;

-- Code to get loser players id name and times lost
CREATE VIEW loserTable AS 
    SELECT players.playerid, players.name, COUNT(players.playerid) AS number 
    FROM players, matches 
    WHERE players.playerid = matches.loser 
    GROUP BY players.playerid, players.name 
    ORDER BY number DESC;

SELECT * FROM loserTable;

-- Code to get total number of matches
-- combining winnerTable and loserTable
CREATE VIEW total_match_table AS 
    SELECT playerid, name, sum(number) AS total_matches 
    FROM (SELECT playerid, name, number FROM winnerTable 
            UNION ALL 
            SELECT playerid, name, number FROM loserTable) AS players
        GROUP BY playerid, name
        ORDER BY playerid;

SELECT * FROM total_match_table;

-- final code to get playerID | name | Win Count | Total Match count
-- by combining total_match_table and winnerTable

CREATE VIEW summury_table AS 
    SELECT total_match_table.playerid, total_match_table.name, total_match_table.total_matches, winnerTable.number AS win_count
        FROM total_match_table
        LEFT JOIN winnerTable
        ON total_match_table.playerid = winnerTable.playerid;

SELECT players.playerid, players.name, summury_table.win_count, summury_table.total_matches
    FROM players
    LEFT JOIN summury_table
    ON players.playerid = summury_table.playerid;


DROP VIEW IF EXISTS summury_table;
DROP VIEW IF EXISTS total_match_table;
DROP VIEW IF EXISTS winnerTable;
DROP VIEW IF EXISTS loserTable;