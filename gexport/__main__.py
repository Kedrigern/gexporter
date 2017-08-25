#!/usr/bin/env python3

import os
import sys
import csv
import sqlite3
import datetime
import argparse

from gexport import __doc__, __version__, __author__, __license__
from gexport import lines, parsing
from gexport.db import DB
from gexport.record import Record
from gexport.enums import LineType

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
        elif lines.month_start.match(line):   # 6/@
            schema += "\nM (%d)\n" % line_count
            previous_line_type = LineType.M
            res = lines.month_start.search(line)
            print('M', res.groups(), line_count)
        elif lines.record.match(line):        # G/@
            if previous_line_type == LineType.C:
                schema += "\n"
                doklad_count += 1
            schema += "R"
            previous_line_type = LineType.R
        elif lines.record_label.match(line):   # G/$
            if previous_line_type != LineType.R:
                print("Error: Record comment is no after Record", file=sys.stderr)
                break
            schema += "c"
            previous_line_type = LineType.c
        elif lines.global_label.match(line):   # G/#
            schema += "C"
            previous_line_type = LineType.C
        else:
            print("Error: Unknown type of line\n%s" % line, file=sys.stderr)
            sys.exit()
        previous_line_text = line

    print('Total count of lines:', line_count)
    print('Total count of records:', doklad_count)
    filename = 'schema.txt'
    print('Complete scheme in %s' % filename)
    with open(filename, 'w') as outfile:
        outfile.write(schema)

def parse_record(db, line, year, month, i, c):
    """
    Parse record into tuple
    Compose dati and dal into number
    Remove SU a AU
    """
    x = lines.record.search(line).groups()
    try:
        date = datetime.date(year, month, int(x[0]))
    except ValueError:
        db.log_it(i, 5, 'E', "Date: %s-%s-%s for line: %s" % (year, month, x[0], line))
        date = '0000-00-00'
    dati = int(x[11]) + (int(x[12]) * 0.01)
    dal  = int(x[14]) + (int(x[15]) * 0.01)
    return (i, date, int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]), int(x[6]), int(x[7]), int(x[8]), int(x[9]), int(x[10]), dati, dal, "")

def parse_into_db(infile, db, verbosity=0):
    """
    Parse input file into sqlite3 DB
    No changes to data, data are in same logic like in original file
    (for example long comment are in multiple line)
    """
    c = db.get_cursor()
    id, lastrowid, month, year, res = (None, None, None, None, None)
    i = 0

    db.log_it(0, 0, 'N', 'Start of parsing, in time: %s' % datetime.datetime.now())
    if verbosity > 0:
        print("Parsing (dot signs start of month):")
    for line in infile:
        i += 1
        if lines.file_start.match(line):
            pass
        elif lines.month_start.match(line):
            x = lines.month_start.search(line).groups()
            year = int(x[4])
            month = int(x[1])
            db.log_it(i, 0, 'L', "Month %d start" % month)
            if verbosity > 0:
                sys.stdout.write('.')
                sys.stdout.flush()
        elif lines.record.match(line):
            x = parse_record(db, line, year, month, i, c)
            res = db.insert_raw_record(x)
            lastrowid = res.lastrowid
        elif lines.record_label.match(line):
            x = lines.record_label.search(line).groups()
            db.update_rec_comment(lastrowid, x[2])
        elif lines.global_label.match(line):
            x = lines.global_label.search(line).groups()
            db.insert_raw_comment(i, x)
        else:
            db.log_it(i, 5, 'E', "Can't parser line: %s" % line)
    if verbosity > 0:
        print()
    db.create_rozpocet_view()
    db.log_it(0, 0, 'N', 'End of parsing, parsed %d lines' % i)
    db.conn.commit()

def post_process(db, csvfile, verbosity=0):
    """
    db: DB
    hide: dict -- what hide in output
    verbosity: num -- verbosity level
    Parse long comment
    Hide some items (personal data, for example pol 6399)
    """
    db.log_it(0, 0, 'N', 'Start of post processing')
    lines = db.conn.execute("SELECT * FROM raw_rozpocet")
    for line in lines:
        record = Record(line)
        db.insert_rozpocet(record)

    with open(csvfile, 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['DATUM', 'MODUL', 'PARAGRAF', 'POLOZKA', 'CASTKA', 'AKCE', 'SUBJEKT_IC', 'SUBJEKT_NAZEV', 'POPIS'])
        for line in db.conn.execute("SELECT * FROM csv"):
            writer.writerow(line)

    if verbosity > 0:
        print()
    db.log_it(0, 0, 'N', 'End of post processing')
    db.conn.commit()

def summary(db, args):
    c = db.get_cursor()
    raws = c.execute("SELECT count(*) FROM raw_record").fetchone()[0]
    items = c.execute("SELECT count(*) FROM raw_rozpocet").fetchone()[0]
    logs = c.execute("SELECT count(*) FROM log").fetchone()[0]

    print("%d\t\tnaparsovaných záznamů" % raws)
    print("%d\t\tpoložek" % items)
    print("%d\t\tlogů" % logs)
    print('Show logs:\nsqlite3 -column -header %s "select * from log;"' % args.db)
    print('Export csv:\nsqlite3 -header -csv %s "select * from csv;" > %s'% (args.db, args.csv))
    print('CSV: %s, podrobná data: %s' % (args.csv, args.db))


def main():
    epilog = 'Version: ' + __version__ + ' Author: ' + __author__ + ' Licence: ' + __license__
    parser = argparse.ArgumentParser(description=__doc__, epilog=epilog)
    meg = parser.add_mutually_exclusive_group()
    meg.add_argument('--validate', action='store_true', help='Analyze and validate input file. This option is for debuging.')
    meg.add_argument('--db', help='Fílename for sqlite (overide if exists) for storing of parsed data (from raw data to clean data)')
    meg.add_argument('-e', '--csv', help='Fílename for csv (overide if exists)')
    parser.add_argument('--verbose', '-v', action='count', help='Verbosity')
    parser.add_argument('infile', help='Input file in kxx')
    args = parser.parse_args()

    if not args.verbose:
        args.verbose = 1

    if not os.path.isdir('export'):
        os.path.mkdir('export')

    basename = os.path.basename(args.infile)
    filename = os.path.splitext(basename)[0]

    if not args.db:
        args.db =  os.path.join('export', filename + '.db')

    if not args.csv:
        args.csv = os.path.join('export', filename + '.csv')

    with open(args.infile, encoding="cp1250") as infile:
        if args.validate:
            loop_validate(infile)
        else:
            if os.path.isfile(args.db):
                os.remove(args.db)
            with sqlite3.connect(args.db) as conn:
                db = DB(conn, True)
                db.log_it(0, 0, 'I', 'Infile: %s, DBfile: %s, CSVfile: %s' % (args.infile, args.db, args.csv))
                parse_into_db(infile, db, args.verbose)
                post_process(db, args.csv, args.verbose)
                if args.verbose > 0:
                    summary(db, args)


if __name__ == '__main__':
    sys.exit(main())
