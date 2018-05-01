import MySQLdb
import pickle

def load_db():
    with open('../data/private/pw_db.p', 'rb') as f:
        pw = pickle.load(f) # 단 한줄씩 읽어옴

    db = MySQLdb.connect(
        "127.0.0.1",
        "root",
        pw,
        "twitchdb",
        charset='utf8',
    )

    return db

def get_id_by_name(db, name):
    QUERY = '''
    SELECT id
    FROM stream_info
    WHERE name = "{}";
    '''.format(name)

    curs = db.cursor()
    curs.execute(QUERY)
    id = curs.fetchone()

    return id[0]

def exist_by_name(db, name):
    QUERY = '''
    SELECT EXISTS(
    SELECT *
    FROM stream_info
    WHERE name = "{}");
    '''.format(name)

    curs = db.cursor()
    curs.execute(QUERY)
    isName = curs.fetchone()

    return isName[0]
