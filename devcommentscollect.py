import praw
import time

paused = False
running = True


r = praw.Reddit(user_agent='The Official DeadByDaylight Bot',
                client_id='',
                client_secret='',
                username='TheDBDBot',
                password='')


print('Logged In')
paused = False
running = True
comment_ids = []
comment_exists = {}
link_comment = {}
is_visited = {}
post_counter = {}
counter = 0

def dev_comments_collect():
    global counter
    subreddit = r.subreddit('BotTestingGroundPlace')
    devs = ['tozzer7']
    
    for submission in subreddit.new():
        dev_comments = []
        post_counter.update({submission.shortlink:counter})

        if post_counter[submission.shortlink] > 0:
            is_visited.update({submission.shortlink:True})

        else:
            is_visited.update({submission.shortlink:False})

        if is_visited[submission.shortlink] == False:
            comment_exists[submission.shortlink] = False
        else:
            comment_exists[submission.shortlink] = True
            
        for comment in submission.comments:
            if comment.id not in comment_ids:
                comment_ids.append(comment.id)
                if comment.author in devs:
                    dev_comments.append([comment.author, comment.body.encode('utf-8')])

        if comment_exists[submission.shortlink] == False:
            if len(dev_comments) > 0:
                comment_body = 'Here is a list of BHVR comments in this thread: \n\n'
                for comment in dev_comments:
                    comment_body = comment_body + 'User: '+str(comment[0])+' said: '+str(comment[1])+'\n\n'
                comment_body = comment_body.replace("b'", "")
                comment_body = comment_body.replace("'", "")
                reddit_comment = submission.reply(comment_body)
                reddit_comment.mod.distinguish(how='yes', sticky=True)
                comment_exists.update({submission.shortlink:True})
                link_comment.update({submission.shortlink:reddit_comment})
                is_visited.update({submission.shortlink:True})
                print('Made a new comment for this thread')

            else:
                comment_exists.update({submission.shortlink:False})
                link_comment.update({submission.shortlink:None})

        elif comment_exists[submission.shortlink] == True:
            reddit_comment = link_comment[submission.shortlink]
            if reddit_comment is None:
                pass
            else:
                if len(dev_comments) > 0:
                    for comment in dev_comments:
                        comment_body = ''
                        comment_body = comment_body + '\n\n User: '+str(comment[0])+' said: '+str(comment[1])+'\n\n'
                    str(reddit_comment.body).replace("b'", "")
                    str(reddit_comment.body).replace("'", "")
                    comment_body = comment_body.replace("b'", "")
                    comment_body = comment_body.replace("'", "")
                    reddit_comment.edit(str(reddit_comment.body) + str(comment_body))
                    link_comment.update({submission.shortlink:reddit_comment})
                else:
                    pass

        print('One submission checked for dev comments')
    counter += 1
