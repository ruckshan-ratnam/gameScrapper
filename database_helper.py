from configparser import ConfigParser
import psycopg2

def config(filename='database.ini',section='postgresql'):
    # Make the parser
    parser = ConfigParser()

    # read the file
    parser.read(filename)

    # goto postgres section
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        issue = 'Section {0} not found in the file: {1}'.format(section, filename)
        raise Exception(issue)

    return db

def connect():
    conn = None
    try:
        # read the connection params, hostname, user, port... etc.
        params = config()

        # connect to digital ocean db
        print('Connecting to games db...')
        conn = psycopg2.connect(**params)

        # make the cursor
        cur = conn.cursor()

        print("DB Version:")
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        # close the cursor
        cur.close

        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

def insert(conn=None,game_name=None, gog_price=None, gog_link=None, mac_price=None, mac_link=None, billet_price=None, billet_link=None, humble_price=None, humble_link=None, steam_price=None, steam_link=None):
    if conn is None:
        raise Exception('No Connection was given')
    else:
        try:
            cur = conn.cursor()
            insert_statement = ("INSERT INTO games (game_name, gog_price, billet_price, humble_price, mac_price, steam_price, gog_link, billet_link, humble_link, mac_link, steam_link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            try:
                cur.execute(insert_statement,(game_name, gog_price, billet_price, humble_price, mac_price, steam_price, gog_link, billet_link, humble_link, mac_link, steam_link))
                conn.commit()
            except:
                conn.rollback()
                issue = 'last transaction of game {0} was rolled back due to an error. Passing {0}'.format(game_name)
                raise Warning(issue)
            finally:
                curr.close()
                pass
        except:
            raise Exception('Error with Connection')

def delete(conn=None, game_name=None):
    rows_deleted = 0
    if conn is None or game_name is None:
        raise Exception('No Connection and game name given')
    else:
        try:
            cur = conn.cursor()
            delete_statement = ("DELETE FROM games WHERE game_name = %s")
            cur.execute(delete_statement,(game_name,))
            rows_deleted = cur.rowcount
            conn.commit()
        except:
            conn.rollback()
            curr.close()
            issue = 'issue when deleting {0}, rolled back transaction'.format(game_name)
            raise Exception(issue)
    return rows_deleted

def update(conn=None,game_name=None, game_price=None, game_link=None):
    if conn is None:
        raise Exception('No Connection was given')
    else:
        try:
            cur = conn.cursor()
            update_statement = ("UPDATE gamesdb SET game_name = %s game_price = %s game_link = %s WHERE game_name=%s")
            try:
                cur.execute(update_statement,(game_name,game_price,game_link,game_name))
                conn.commit()
            except:
                conn.rollback()
                raise Warning('last transaction of game {0} was rolled back due to an error. Passing {0}'.format(game_name))
            finally:
                pass
        except:
            raise Exception('Error with Connection')
