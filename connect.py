import praw
import time

def connect():
    r = praw.Reddit(user_agent='The Official DeadByDaylight Bot',
                    client_id='**********',
                    client_secret='*************',
                    username='TheDBDBot',
                    password='****************')


    print('Logged In')
