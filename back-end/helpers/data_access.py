import mysql.connector

def run(query, params=None):
    cnx = None
    try:
        cnx = mysql.connector.connect(database='social_book', password = 'Bb1258998521??', user='root' )
        cursor = cnx.cursor(buffered=True, dictionary=True)
        cursor.execute(query, params)
        row = cursor.fetchall()
        return row
    except Exception as ex:
        print('Run err', ex)
    finally:
        cursor.close()
        cnx.close()
    return None


def run_non_query(query, params=None):
    cnx = None
    res = None
    try:
        cnx = mysql.connector.connect(database='social_book', password = 'Bb1258998521??', user='root' )
        cursor = cnx.cursor(buffered=True)
        res = cursor.execute(query,params)
        cnx.commit()
        return res.rowcount
    except:
        print('post err')
    finally:
        cursor.close()
        cnx.close()
    return None
