#! /bin/env python

import argparse
import config
import praw
import prawcore
import time
import subprocess

SLEEP_TIME = 5

def main(args):
    ''' Watch for a query '''

    robot = bot_login()

    mark_read = []
    while True:
        try:
            if mark_read:   # Needed to clear after a Reddit disconnection error
                robot.inbox.mark_read(mark_read)
                mark_read.clear()
            # for all unread messages
            for message in robot.inbox.unread():
                # for all unread comments
                if message.was_comment:
                    # username mentions are simple
                    if message.subject == "username mention":
                        process_query(robot.comment(message.id))
                    # if it was a reply, check to see if it contained a summon
                    elif message.subject == "comment reply" or message.subject == "post reply":
                        # Not implemented yet
                        pass
                mark_read.append(message)

            robot.inbox.mark_read(mark_read)
            mark_read.clear()

            time.sleep(SLEEP_TIME)

        except prawcore.exceptions.ResponseException as e:   # Something funky happened
            print("Did a comment go missing?", e, vars(e))
            time.sleep(SLEEP_TIME)

        except prawcore.exceptions.RequestException:    # Unable to connect to Reddit
            print("Unable to connect to Reddit, is the internet down?")
            time.sleep(SLEEP_TIME)

        except KeyboardInterrupt:
            robot.inbox.mark_read(mark_read)
            print("Exiting...")
            break

        except ConnectionError:
            print('A connection was unable to be established')
            time.sleep(SLEEP_TIME)

        except Exception as e:
            robot.inbox.mark_read(mark_read)
            raise

def process_query(comment):
    ''' Process a query '''

    print(f"Responding to a query in comment {comment.id}")
    subprocess.run(['python', 'src/responder.py', comment.id])


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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Watch for a query')
    args = parser.parse_args()

    main(args)
