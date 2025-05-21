#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector as mysqld
import argparse, time
import logging, traceback


__title__ = 'load_vector_data'
__version__ = '1.0.0-DEV'
__author__ = 'khkwon01'
__license__ = 'MIT'
__copyright__ = 'Copyright 2025'

def get_args_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-f", "--file",
        default="data.csv",
        nargs='?',
        type=str,
        required=True,
        help="File which was included test data")
    parser.add_argument("--help",
        default=False,
        action='store_true',
        help="Show this help message and exit.")
    parser.add_argument("-h", "--host",
        type=str, action="store",
        default="127.0.0.1", nargs="?",
        help="heatwave database ip address.")
    parser.add_argument("-P", "--port", 
        type=int, action="store",
        default=3306, nargs="?",
        help="heatwave database port number.")
    parser.add_argument("-d", "--database",
        type=str, action="store",
        default="test", nargs="?",
        help="heatwave database")
    parser.add_argument("-u", "--user",
        type=str, action="store",
        default="admin", nargs="?", 
        help="database user")
    parser.add_argument("-p", "--password",
        type=str, action="store",
        default="Welcome#1", nargs="?",
        help="database user password")

    return parser

def load_to_db(options):

    s_embeding_query='select sys.ML_EMBED_ROW("%s", JSON_OBJECT("model_id","cohere.embed-multilingual-v3.0")) into @text_embedding'
    s_insert_embed_data='insert into customer_qa (question, question_vector, answer) values ("%s", @text_embedding, "%s")'

    try:

        s_datafile = options.file
        s_host = options.host
        s_port = options.port
        s_db = options.database
        s_user = options.user
        s_pass = options.password
    
        #print(s_datafile, s_host, s_port, s_db, s_user, s_pass)

        o_db = mysqld.connect(
                    host=s_host,
                    port=s_port,
                    user=s_user,
                    passwd=s_pass,
                    db=s_db,
                    connection_timeout=10,
                    autocommit=True
               )

        with open(options.file, "r") as file:
            for s_line in file:
                o_qa = s_line.strip().split('|')
                print(f"question : { o_qa[0] }")
                print(f"answer: { o_qa[1] }\n")

                o_cursor = o_db.cursor()
                o_init_time = time.time()
                o_cursor.execute(s_embeding_query % (o_qa[0]))
                o_after_time = time.time()
                print("Embedding time of text : %s" % round((o_after_time - o_init_time),3))

                o_init_time = time.time()
                o_cursor.execute(s_insert_embed_data % (o_qa[0], o_qa[1]))
                o_after_time = time.time()
                i_count = o_cursor.rowcount
                print("Insert time and count : %s %i" % (round((o_after_time - o_init_time),3), i_count))
                o_cursor.close()

        if o_db is not None: o_db.close()

    except Exception as e:
        s_trackmsg = traceback.format_exc()
        print("Err :" + str(e) + "\n" + s_trackmsg)


if __name__ == '__main__':
    parser = get_args_parser()
    options = parser.parse_args()
    if options.help:
        parser.print_help()
        parser.exit()

    load_to_db(options=options)
