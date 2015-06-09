# NBA NLP - Senior Project - Spring 2015
# NBA Database
# Jacob Bustamante

import sqlite3
import os, sys
import data.data_globals as dg

db_filename = dg.db_filename
schema_filename = dg.schema_filename

def create_db(file_dir="./"):
    db_filepath = file_dir + db_filename
    schema_filepath = file_dir + schema_filename

    if not os.path.exists(db_filepath):
        with sqlite3.connect(db_filepath) as conn:
            sys.stdout.write("Creating db " + db_filepath + " from " + schema_filepath + "... ")
            with open(schema_filepath, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)
            print("done!")

if __name__ == '__main__':
    create_db()
