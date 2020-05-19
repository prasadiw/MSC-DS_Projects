#! /bin/env python

import argparse
import config
import psaw

# TODO: import and use praw to handle comment updates/deletions

import threading
import time
from collections import deque

import whoosh
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.analysis import StemmingAnalyzer, RegexTokenizer, LowercaseFilter, StopFilter, StemFilter
import os, os.path
from whoosh import index

BATCH_SIZE = 1000

def main(args):
    ''' Index Reddit comments '''

    comment_queue = deque()
    comment_index = make_index()
    thread_indexing = threading.Thread(
        target=index_thread,
        args=[comment_queue, comment_index]
        )
    thread_indexing.start()

    start_time = int(time.time() - args.time_back)

    api = psaw.PushshiftAPI()

    last_comment = None
    # Initial query for previous comments
    gen = api.search_comments(
        after= start_time,
        sort='asc',
        sort_type='created_utc',
        filter=['id','parent_id','link_id','subreddit_id', 'body','permalink']
    )
    for comment in gen:
        last_comment = comment
        comment_queue.append(comment)
    # If this returned no result, grab the most recent comment
    if not last_comment:
        gen = api.search_comments(
            limit =1,
            sort='desc',
            sort_type='created_utc',
            filter=['id','parent_id','link_id','subreddit_id', 'body','permalink']
        )
        for comment in gen:
            last_comment = comment
            comment_queue.append(comment)
            #print("Grabbing most recent")
            #print(comment)

    while True:
        gen = api.search_comments(
            #after_id= last_comment.id,
            # Sometimes PSAW's paging with after_id get's tripped up
            after= last_comment.created_utc,
            sort='asc',
            sort_type='created_utc',
            filter=['id','parent_id','link_id','subreddit_id', 'body','permalink']
        )
        for comment in gen:
            last_comment = comment
            comment_queue.append(comment)
        time.sleep(2)



def index_thread(comment_queue, comment_index):
    ''' Index comments '''

    while True:
        if len(comment_queue) > BATCH_SIZE:
            write_to_index(comment_index,comment_queue)
        time.sleep(0.5)

def make_index():

    analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter() | StemFilter()

    schema = Schema(
        comment_id=ID(stored=True),
        parent_id=ID(stored=True),
        submission_id=ID(stored=True),
        subreddit_id=ID(stored=True),
        content=TEXT(analyzer=analyzer)
    )

    if not os.path.exists(config.indexdir):
        os.mkdir(config.indexdir)
    ix = index.create_in(config.indexdir, schema)

    return ix

def write_to_index(ix,q):

    with ix.writer() as writer:
        for _ in range(BATCH_SIZE):
            comment = q.popleft()
            '''
            print(comment)
            print({
                'comment_id' : comment.id,
                'parent_id' : comment.parent_id,
                'submission_id' : comment.link_id,
                'subreddit_id' : comment.subreddit_id,
                'permalink' : comment.permalink
            })
            '''
            writer.add_document(
                comment_id = comment.id,
                parent_id = comment.parent_id,
                submission_id = comment.link_id,
                subreddit_id = comment.subreddit_id,
                content = comment.body
            )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Index Reddit comments')
    parser.add_argument('--time_back',
        type=int,
        help='Time in past where to start indexing (in seconds)',
        default=600
    )
    args = parser.parse_args()

    main(args)
