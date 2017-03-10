#!/usr/bin/env python3

import os
import sys
import sqlite3
import datetime
import argparse

from .enums import LineType
from . import lines
from . import record


def loop_validate(infile):
    """
    Validate file and generate schema, for debuging puporse
    """
    line_count = 0
    doklad_count = 0
    schema = ""
    previous_line_text = ""
    previous_line_type = LineType.N

    for line in infile:
        line_count += 1
        if lines.file_start.match(line):
            schema += "S\n"
            previous_line_type = LineType.S
            res = lines.file_start.search(line)
            print('S', res.groups(), line_count)
        elif lines.month_start.match(line):
            # 6/@
            schema += "\nM (%d)\n" % line_count
            previous_line_type = LineType.M
            res = lines.month_start.search(line)
            print('M', res.groups(), line_count)
        elif lines.record.match(line):
            # G/@
            if previous_line_type == LineType.C:
                schema += "\n"
                doklad_count += 1
            schema += "R"
            previous_line_type = LineType.R
        elif lines.record_label.match(line):
            # G/$
            if previous_line_type != LineType.R:
                print("Error: Record comment is no after Record", file=sys.stderr)
                break
            schema += "c"
            previous_line_type = LineType.c
        elif lines.global_label.match(line):
            # G/#
            schema += "C"
            previous_line_type = LineType.C
        else:
            print("Error: Unknown type of line\n%s" % line, file=sys.stderr)
            sys.exit()
        previous_line_text = line

    print('Řádků celkem:', line_count)
    print('Dokladů celkem:', doklad_count)
    filename = 'schema.txt'
    print('Kompletní schéma v: %s' % filename)
    with open(filename, 'w') as outfile:
        outfile.write(schema)

def create_records_table(c):
    c.execute(''' CREATE TABLE record (
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

def create_log_table(c):
    c.execute(''' CREATE TABLE log (
        line  int NOT NULL,             -- line in original file
        level int NOT NULL,
        type varchar(1) NOT NULL,
        message varchar(255) NOT NULL
    ) ''')

def create_comment_table(c):
    c.execute(''' CREATE TABLE comment (
        line  int NOT NULL,   -- line in original file
        fline int NOT NULL,   -- line as in record (original value)
        gid   int NOT NULL,   -- číslo dokladu
        text text NOT NULL    -- text poznámky
    ) ''')

def create_rozpocet_view(c):
    c.execute(''' CREATE VIEW rozpocet AS
    SELECT kap, odpa, pol, gid, date, orj, org, dati, dal, comment FROM record
    WHERE odpa <> 0 AND pol <> 0;
    ''')

def log_it(c, line, level, error, message):
    c.execute('INSERT INTO log VALUES (?, ?, ?, ?)', (line, level, error, message))

def parse_record(line, year, month, i, c):
    """
    Parse record into tuple
    Compose dati and dal into number
    Remove SU a AU
    """
    x = lines.record.search(line).groups()
    try:
        date = datetime.date(year, month, int(x[0]))
    except ValueError:
        log_it(c, i, 5, 'E', "Date: %s-%s-%s for line: %s" % (year, month, x[0], line))
        date = '0000-00-00'
    dati = int(x[11]) + (int(x[12]) * 0.01)
    dal  = int(x[14]) + (int(x[15]) * 0.01)
    return (i, date, int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]), int(x[6]), int(x[7]), int(x[8]), int(x[9]), int(x[10]), dati, dal, "")

def parse_into_db(infile, conn):
    """
    Parse input file into sqlite3 DB
    """
    c = conn.cursor()
    create_records_table(c)
    create_comment_table(c)
    create_log_table(c)
    id, lastrowid, month, year, res = (None, None, None, None, None)
    i = 0

    log_it(c, 0, 0, 'S', 'Start of parsing, in time: %s' % datetime.datetime.now())
    for line in infile:
        i += 1
        if lines.file_start.match(line):
            pass
        elif lines.month_start.match(line):
            x = lines.month_start.search(line).groups()
            year = int(x[4])
            month = int(x[1])
            log_it(c, i, 0, 'L', "Month %d start" % month)
            sys.stdout.write('.')
            sys.stdout.flush()
        elif lines.record.match(line):
            x = parse_record(line, year, month, i, c)
            res = c.execute('INSERT INTO record VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', x)
            lastrowid = res.lastrowid
        elif lines.record_label.match(line):
            x = lines.record_label.search(line).groups()
            c.execute('UPDATE record SET comment = ? WHERE rowid = ?', (x[2], lastrowid))
        elif lines.global_label.match(line):
            x = lines.global_label.search(line).groups()
            c.execute('INSERT INTO comment VALUES (?, ?, ?, ?)', (i, int(x[0]), int(x[1]), x[2]))
        else:
            log_it(c, i, 5, 'E', "Can't parser line: %s" % line)

    create_rozpocet_view(c)
    log_it(c, 0, 0, 'S', 'End of parsing, in time: %s' % datetime.datetime.now())
    conn.commit()

    count = c.execute("SELECT count(*) FROM record").fetchone()
    log = c.execute("SELECT count(*) FROM log").fetchone()
    print()
    print("%d\t\tzáznamů" % count)
    print("%d\t\třádek" % i)
    print("%d\t\tlogů" % log)

def main():
    database = 'data.db'
    filename = 'test/data.kxx'
    #filename = 'data/2016_uct.kxx'
    if os.path.isfile(database):
        os.remove(database)
    conn = sqlite3.connect(database)
    with open(filename, encoding="cp1250") as infile:
        parse_into_db(infile, conn)
        #loop_validate(infile)
    conn.close()
    print('Uloženo v %s' % database)

if __name__ == '__main__':
    sys.exit(main())
