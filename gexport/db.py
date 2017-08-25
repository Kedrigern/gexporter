#!/usr/bin/env python3
import sys
import sqlite3
import datetime

class DB:
    """ DB scheme
+------------+  +-------------+  +-----+
| raw_record |  | raw_comment |  | log |
+------------+  +-------------+  +-----+
       |           |
       v           v
+---------------------+
| raw_rozpocet (view) |
+---------------------+
          |
          v
     +----------+
     | rozpocet |
     +----------+
          |
          v
    +------------+
    | csv (view) |
    +------------+
    """

    def __init__(self, conn, create=True):
        self.conn = conn
        if create:
            self.create_schema()

    def create_schema(self):
        self._create_records_table()
        self._create_comment_table()
        self._create_log_table()
        self._create_rozpocet_table()

    def _create_records_table(self):
        self.conn.execute(''' CREATE TABLE IF NOT EXISTS raw_record (
            line int NOT NULL,   -- line in original file
            date date NOT NULL,  -- datum zaúčtování
            gid  int NOT NULL,   -- číslo dokladu
            su   int NOT NULL,   -- syntetika
            au   int NOT NULL,   -- analytika
            kap  int NOT NULL,   -- kapitola
            odpa int NOT NULL,   -- oddíl,paragraf
            pol  int NOT NULL,   -- položka
            zj   int NOT NULL,   -- záznamová jednotka
            uz   int NOT NULL,   -- účelový znak
            orj  int NOT NULL,   -- organizační jednotka
            org  int NOT NULL,   -- organizace (projekt)
            dati int NOT NULL,   -- má dáti
            dal  int NOT NULL,   -- dal
            comment text
        ) ''')

    def _create_comment_table(self):
        self.conn.execute(''' CREATE TABLE IF NOT EXISTS raw_comment (
            line  int NOT NULL,   -- line in original file
            fline int NOT NULL,   -- line as in record (original value)
            gid   int NOT NULL,   -- číslo dokladu
            text text NOT NULL    -- text poznámky
        ) ''')

    def _create_log_table(self):
        self.conn.execute(''' CREATE TABLE IF NOT EXISTS log (
            line  int NOT NULL,             -- line in original file
            level int NOT NULL,             -- log level
            type varchar(1) NOT NULL,       -- E: error, L: line, N: notice
            date date NOT NULL,             -- time
            message varchar(255) NOT NULL
        ) ''')

    def _create_rozpocet_table(self):
        self.conn.execute(''' CREATE TABLE IF NOT EXISTS rozpocet (
            modul text,             -- modul
            date date NOT NULL,     -- date
            odpa int NOT NULL,      -- oddíl, paragraf
            pol  int NOT NULL,      -- položka
            orj  int NOT NULL,      -- organizační jednotka
            org  int NOT NULL,      -- organizace (projekt)
            castka int NOT NULL,    -- částka (dati-dal)
            ic int,                 -- ic
            gid int NOT NULL,       -- unique identifier, gordic ID
            partner text,           -- druhá smluvní strana
            pid text,               -- id smlouvy
            description text,       -- from long comment
            evk text,               -- evk
            evkt text,              -- evkt
            comment text,           -- inline comment
            kap text                -- kapitola
        ) ''')
        self.conn.execute('''CREATE VIEW IF NOT EXISTS csv AS
        select date as DATUM, modul as MODUL, odpa as PARAGRAF, pol as POLOZKA, castka as CASTKA, org as AKCE, ic as SUBJEKT_IC, partner as SUBJEKT_NAZEV, evkt as POPIS from rozpocet''')

    def create_rozpocet_view(self):
        """
        Create view which join comments with record and filter irelevant data
        """
        self.conn.execute('''
        CREATE view IF NOT EXISTS raw_rozpocet as
        select r.gid, r.date, r.odpa, r.pol, r.orj, r.org, r.dati, r.dal, r.comment, c.text, r.kap from
          raw_record r left join
          (select gid, group_concat(text, '') as text from raw_comment group by gid) c
          on r.gid = c.gid
         where (r.odpa <> 0 AND r.odpa is not NULL) and (r.pol > 5000 AND r.pol < 9000)
        ''')

    def log_it(self, line, level, error, message):
        now = datetime.datetime.now()
        self.conn.execute('INSERT INTO log VALUES (?, ?, ?, ?, ?)', (line, level, error, now, message))

    def insert_rozpocet(self, rec):
        t = (rec.modul, rec.date, rec.odpa, rec.pol, rec.orj, rec.org, rec.castka, rec.ic, rec.gid, rec.partner, rec.pid, rec.desc, rec.evk, rec.evkt, rec.comment, rec.kap)
        self.conn.execute('INSERT INTO rozpocet VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );', t )

    def insert_raw_record(self, x):
        return self.conn.execute('INSERT INTO raw_record VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', x)

    def insert_raw_comment(self, i, x):
        self.conn.execute('INSERT INTO raw_comment VALUES (?, ?, ?, ?)', (i, int(x[0]), int(x[1]), x[2]))

    def update_rec_comment(self, id, text):
        self.conn.execute('UPDATE raw_record SET comment = ? WHERE rowid = ?', (text, id))

    def insert_complete_record(self, records):
        """Insert tuple:
        (gid, date, odpa, pol, orj, org, dati, dal, partner, comment, description, evk, evkt, pid)
        """
        i = 0
        for r in records:
            i += 1
            try:
                self.conn.execute('INSERT INTO rozpocet VALUES (?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?)', r)
            except sqlite3.ProgrammingError as e:
                # TODO: into db
                print(records[i])
                print(e)
                sys.exit()

    def rozpocet_count(self):
        return int(self.conn.execute("SELECT count(*) FROM rozpocet").fetchone()[0])

    def get_cursor(self):
        return self.conn.cursor()

    def fetch_comment_for(self, gid, c):
        """
        Return comment as string
        conn    -- DB connection (sqlite3)
        gid     -- global id
        """
        comments = c.execute("SELECT text FROM raw_comment WHERE gid=%s" % gid).fetchall()
        result = ""
        for c in comments:
            result += c[0]
        return result
