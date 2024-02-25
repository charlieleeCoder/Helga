import sqlite3


def start_db():
    """Creates a database called savefiles if one doesn't exist."""
    connect = sqlite3.connect("savefiles.db")
    db = connect.cursor()
    try:
        db.execute("CREATE TABLE saves (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, tile INTEGER NOT NULL, weapon INTEGER NOT NULL);")
    except:
        print("Save file database found.")


def find_saves():
    """Detects current save files."""
    connect = sqlite3.connect("savefiles.db")
    db = connect.cursor()
    try: 
        query = db.execute("SELECT * FROM saves;")
        saves = query.fetchall()
        print("Found saves function works.")
        return saves
    except:
        return False

def new_save():
    """Create new save data in slot 1."""
    connect = sqlite3.connect("savefiles.db")
    db = connect.cursor()
    try: 
        query = db.execute("INSERT INTO saves (name, tile, weapon) VALUES ('Join', 3, 1);")
        print("Save #1 successful.")
        connect.commit()
    except:
        print("Failed to save.")
        return False


def replace_save(savefile):
    """Replace save data in slot 1."""
    connect = sqlite3.connect("savefiles.db")
    db = connect.cursor()
    try: 
        query = db.execute("UPDATE saves SET name = 'Join', tile = 3, weapon = 1  WHERE id = ?", (savefile,))
        print(f"Save #{savefile} successful.")
        db.commit()
    except:
        print("Failed to save.")
        return False


def load_file(savefile):
    """Load data from slot X."""
    connect = sqlite3.connect("savefiles.db")
    db = connect.cursor()
    try: 
        query = db.execute("SELECT * FROM saves WHERE id = ?", (savefile,))
        print(f"Load #{savefile} successful.")
        saves = query.fetchall()
        return saves
    except:
        print("Failed to load.")
        return False

