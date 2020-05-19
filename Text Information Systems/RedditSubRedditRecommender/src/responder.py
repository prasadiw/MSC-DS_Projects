#! /bin/env python

import argparse
import config
import praw

from collections import deque

import whoosh
from whoosh.qparser import QueryParser

from scipy.stats.mstats import hmean
import math
import pandas as pd


def main(comment_id):
    ''' Respond to a given query '''

    robot = bot_login()

    # Get the comment
    try:
        comment = robot.comment(comment_id)
        comment.refresh()
    except praw.exceptions.ClientException:
        print ("Comment not found!\n")
        raise

    query = prepare_query(robot, comment)
    result = execute_query(robot, query)
    post_reply(robot, comment, result)

def bot_login():
    ''' Login to Reddit '''

    robot = praw.Reddit(
        username      = config.username,
        password      = config.password,
        client_id     = config.client_id,
        client_secret = config.client_secret,
        user_agent    = config.user_agent
    )
    return robot

def prepare_query(robot, comment):
    ''' Prepare the query text '''

    MAX_RADIUS = 2

    # Find your center
    center_id = comment.parent_id \
        if not args.no_query \
        else comment


    # Prepare
    seen = set([center_id])
    growth = deque()
    growth.append((0,center_id))
    query_text = ""

    # Spread out
    while growth:
        (r,c) = growth.popleft()

        # NOTE: At the moment, ignore MoreComments
        #       If we're getting that, we've likely got enough to use.
        #       If it seems prudent, instead we could expand them.
        if type(c) == praw.models.MoreComments:
            continue
        if type(c) == str:
            # Submission
            if c[:2] == 't3':
                seen.add(c)
                if r < MAX_RADIUS:
                    s = robot.submission(c[3:])
                    growth.extend(
                        map(lambda x: (r+1,x),s.comments)
                    )
                continue
            # Comment
            c = robot.comment(c[3:])
            c.refresh()
        query_text += "\n" + c.body
        seen.add(c.id)
        if r == MAX_RADIUS:
            continue
        if c.parent_id not in seen:
            growth.append((r+1,c.parent_id))
        for child in c.replies:
            if child.id not in seen:
                growth.append((r+1,child))

    print(query_text)
    return query_text

def execute_query(robot,query):
    ''' Query with the query text '''

    # The following analysis is to use the query text and
    # select one or more submissions to return.
    # The general approach as as follows:
    #   * Use the inverted index and Okapi BM25 to score the documents
    #   * Select the top 10%
    #   * Group by submission
    #   * Take the harmonic mean within each submission
    #   * Multiply by the log of the count of matched documents per submission
    #   * Rank with this score per submission


    inverted_index = whoosh.index.open_dir(config.indexdir)
    # Beware!!  We need as simple a query parser as possible.
    # Specifically, we cannot permit any "interpretation" of the query text.
    query_parser = QueryParser(
        'content', 
        inverted_index.schema, 
        plugins=[],
        group=whoosh.qparser.syntax.OrGroup
    )
    parsed_query = query_parser.parse(query) 
    with inverted_index.searcher() as searcher:
        results = searcher.search(parsed_query)             # Okapi scoring
        df = pd.DataFrame([
            [hit['submission_id'], hit.score]
            for hit in results[:int(len(results)/10)]],     # Top 10%
            columns=['submission', 'score'])
    topN = df.groupby('submission')\
        .score\
        .apply(
            lambda group: \
                # Mean of scores of matching comments per submission
                hmean(group) \
                # Log of count of matching comments per submission
                * math.log(1+len(group))
        )\
        .sort_values(ascending=False)\
        .reset_index()\
        [:20]

    return topN

def post_reply(robot, comment, result):
    ''' Reply with the results '''

    print("Replying to the Request")
    submission_id = result.iloc[0].submission[3:]
    if submission_id == comment.submission.id:
        submission_id = result.iloc[1].submission
    if submission_id[:3] == 't3_':
        submission_id = submission_id[3:]

    print("Suggesting submission ", submission_id)

    submission = robot.submission(submission_id)

    link = f"https://reddit.com{submission.permalink}"
    if args.no_query:
        print(link)
    else:
        comment.reply(link)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Respond to a query')
    parser.add_argument('--no_query',
        action='store_true',
        help='An optional flag to use the provided message as "center" and respond to STDOUT',
        default=False
    )
    parser.add_argument('comment_id', help='The comment id of the query')
    args = parser.parse_args()

    main(args.comment_id)
