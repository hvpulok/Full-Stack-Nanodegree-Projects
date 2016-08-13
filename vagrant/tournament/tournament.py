#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    query = "DELETE FROM matches;"
    c.execute(query)
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    query = "DELETE FROM players;"
    c.execute(query)
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    query = "SELECT COUNT(name) AS num FROM players;"
    c.execute(query)
    results = c.fetchone()
    # print results[0]
    DB.commit()
    DB.close()
    return results[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s) ", (name,))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    query = '''
    -- Code to get winner players id name and times won  
    CREATE VIEW winnerTable AS 
    SELECT players.playerid, players.name, COUNT(players.playerid) AS number 
    FROM players, matches 
    WHERE players.playerid = matches.winner
    GROUP BY players.playerid, players.name 
    ORDER BY number DESC;

    -- Code to get loser players id name and times lost
    CREATE VIEW loserTable AS 
    SELECT players.playerid, players.name, COUNT(players.playerid) AS number 
    FROM players, matches 
    WHERE players.playerid = matches.loser 
    GROUP BY players.playerid, players.name 
    ORDER BY number DESC;

    -- Code to get total number of matches
    -- combining winnerTable and loserTable
    CREATE VIEW total_match_table AS 
        SELECT playerid, name, sum(number) AS total_matches 
        FROM (SELECT playerid, name, number FROM winnerTable 
                UNION ALL 
                SELECT playerid, name, number FROM loserTable) AS players
            GROUP BY playerid, name
            ORDER BY playerid;
    
    -- final code to get playerID | name | Win Count | Total Match count
    -- by combining total_match_table and winnerTable
    CREATE VIEW summury_table AS 
        SELECT total_match_table.playerid, total_match_table.name, total_match_table.total_matches, winnerTable.number AS win_count
            FROM total_match_table
            LEFT JOIN winnerTable
            ON total_match_table.playerid = winnerTable.playerid;

    CREATE VIEW player_standings AS 
        SELECT players.playerid, players.name,
            CASE summury_table.win_count WHEN summury_table.win_count THEN summury_table.win_count
                ELSE 0
                END AS win_count,    
            CASE summury_table.total_matches WHEN summury_table.total_matches THEN summury_table.total_matches
                ELSE 0
                END AS total_matches
            FROM players
            LEFT JOIN summury_table
            ON players.playerid = summury_table.playerid;

    SELECT * FROM player_standings;

    '''

    c.execute(query)
    results = c.fetchall()   
    DB.close()
    return results

# results = playerStandings()
# for item in results:
#     print item
#     print "\n"

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    query = "INSERT INTO matches (winner, loser) VALUES(%s, %s);" %(winner, loser)
    c.execute(query)
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    DB = connect()
    c = DB.cursor()
    query = '''
    -- Code to get winner players id name and times won  
    CREATE VIEW winnerTable AS 
    SELECT players.playerid, players.name, COUNT(players.playerid) AS number 
    FROM players, matches 
    WHERE players.playerid = matches.winner
    GROUP BY players.playerid, players.name 
    ORDER BY number DESC;

    -- Code to get loser players id name and times lost
    CREATE VIEW loserTable AS 
    SELECT players.playerid, players.name, COUNT(players.playerid) AS number 
    FROM players, matches 
    WHERE players.playerid = matches.loser 
    GROUP BY players.playerid, players.name 
    ORDER BY number DESC;

    -- Code to get total number of matches
    -- combining winnerTable and loserTable
    CREATE VIEW total_match_table AS 
        SELECT playerid, name, sum(number) AS total_matches 
        FROM (SELECT playerid, name, number FROM winnerTable 
                UNION ALL 
                SELECT playerid, name, number FROM loserTable) AS players
            GROUP BY playerid, name
            ORDER BY playerid;
    
    -- final code to get playerID | name | Win Count | Total Match count
    -- by combining total_match_table and winnerTable
    CREATE VIEW summury_table AS 
        SELECT total_match_table.playerid, total_match_table.name, total_match_table.total_matches, winnerTable.number AS win_count
            FROM total_match_table
            LEFT JOIN winnerTable
            ON total_match_table.playerid = winnerTable.playerid;

    CREATE VIEW player_standings AS 
        SELECT players.playerid, players.name,
            CASE summury_table.win_count WHEN summury_table.win_count THEN summury_table.win_count
                ELSE 0
                END AS win_count,    
            CASE summury_table.total_matches WHEN summury_table.total_matches THEN summury_table.total_matches
                ELSE 0
                END AS total_matches
            FROM players
            LEFT JOIN summury_table
            ON players.playerid = summury_table.playerid;


    -- code to create a player group based on their standings: odd number standings    
    CREATE VIEW player_group_odd AS 
        SELECT ROW_NUMBER() OVER(ORDER BY win_count DESC) AS serial_no, id1, name1, win_count, standings FROM( 
        SELECT playerid AS id1, name as name1, win_count, ROW_NUMBER() OVER(ORDER BY win_count DESC) AS standings 
        FROM player_standings
        ) d where (standings % 2) = 1;

    -- code to create a player group based on their standings: Even number standings    
    CREATE VIEW player_group_even AS 
        SELECT ROW_NUMBER() OVER(ORDER BY win_count DESC) AS serial_no, id2, name2, win_count, standings FROM( 
        SELECT playerid AS id2, name as name2, win_count, ROW_NUMBER() OVER(ORDER BY win_count DESC) AS standings 
        FROM player_standings
        ) d where (standings % 2) = 0;

    -- code to create pairs combining odd group and even group
    CREATE VIEW swiss_pairs AS
        SELECT player_group_odd.id1, player_group_odd.name1, player_group_even.id2, player_group_even.name2
            FROM player_group_odd, player_group_even
            WHERE player_group_odd.serial_no = player_group_even.serial_no;

    SELECT * FROM swiss_pairs;
    '''

    c.execute(query)
    results = c.fetchall()   
    DB.close()
    return results
