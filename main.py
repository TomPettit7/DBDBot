from connect import connect
from functions import link_post_remover, comment_monitor, dev_comments_collect
import time

paused = False
running = True


def main():
    global finished
    connect()
    link_post_remover()
    comment_monitor()
    finished = True

def dev_comment():
    dev_comments_collect()

main()
while running:
    counter = 0
    if finished == True:
        paused = True
        print('Bot is now sleeping for 1 minute')
        time.sleep(60)
        finished = False

    elif finished == False:
        print('Bot is performing its next check')
        main()
        finished = True
        counter += 1
        
    elif counter == 30:
        dev_comment()
