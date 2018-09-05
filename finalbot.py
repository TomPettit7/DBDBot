import praw
import time

r = praw.Reddit(user_agent='The Official DeadByDaylight Bot',
                client_id='',
                client_secret='',
                username='TheDBDBot',
                password='')

checked_posts = []
def ensure_flaired_post():

    subreddit = r.subreddit('deadbydaylight')
    for submission in subreddit.new():
        redditor_replied = False
        flair_choices = submission.flair.choices()
        if submission.shortlink not in checked_posts:
            checked_posts.append(submission.shortlink)
            if submission.link_flair_text is None:
                print('This post does not have a flair')
                submission.hide()
                author = submission.author
                redditor = r.redditor(str(author))
                message = 'Dear: '+str(author)+', \n\n'+'It appears that you have not flaired your submission to r/deadbydaylight.' + '\n\n *Your submission will be hidden unless you add a flair to it*'+'\n\n'+'If you want me to flair the submission, message me with the flair you want your submission to have and I will do it for you. \n\n Here is a list of the flair choices: '+str(flair_choices)+'\n\n Thanks, \n\n ~TheDBDBot'
                my_reddit_msg = redditor.message('Flairing Your Submission', message)

                while redditor_replied == False:
                    for message in r.inbox.stream():
                        if message.author == author:
                            if message.body in flair_choices:
                                flair_template_id = message.body
                                submission.flair.select(flair_template_id)
                                redditor_replied = True
                                submission.unhide()
                                message.delete()
                                break
                            else:
                                redditor = r.redditor(str(message.author))
                                redditor.message('The flair you sent me', 'The flair you sent me was not an optional flair. Therefore I was unable to flair your post. Please try resubmitting your post with a new flair :)')
                                message.delete()
                                submission.mod.remove()
                                redditor_replied = True
                                break
            else:
                print('Submission has a flair')
        else:
            print('Already seen this post')


comment_ids = []
comment_exists = {}
link_comment = {}
is_visited = {}
post_counter = {}
counter = 0


def dev_comments_collect():
    global counter
    subreddit = r.subreddit('deadbydaylight')
    devs = ['tozzer7']

    for submission in subreddit.new():
        dev_comments = []
        post_counter.update({submission.shortlink: counter})

        if post_counter[submission.shortlink] > 0:
            is_visited.update({submission.shortlink: True})

        else:
            is_visited.update({submission.shortlink: False})

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
                    comment_body = comment_body + 'User: ' + str(comment[0]) + ' said: ' + str(comment[1]) + '\n\n'
                comment_body = comment_body.replace("b'", "")
                comment_body = comment_body.replace("'", "")
                reddit_comment = submission.reply(comment_body)
                reddit_comment.mod.distinguish(how='yes', sticky=True)
                comment_exists.update({submission.shortlink: True})
                link_comment.update({submission.shortlink: reddit_comment})
                is_visited.update({submission.shortlink: True})
                print('Made a new comment for this thread')

            else:
                comment_exists.update({submission.shortlink: False})
                link_comment.update({submission.shortlink: None})

        elif comment_exists[submission.shortlink] == True:
            reddit_comment = link_comment[submission.shortlink]
            if reddit_comment is None:
                pass
            else:
                if len(dev_comments) > 0:
                    for comment in dev_comments:
                        comment_body = ''
                        comment_body = comment_body + '\n\n User: ' + str(comment[0]) + ' said: ' + str(
                            comment[1]) + '\n\n'
                    str(reddit_comment.body).replace("b'", "")
                    str(reddit_comment.body).replace("'", "")
                    comment_body = comment_body.replace("b'", "")
                    comment_body = comment_body.replace("'", "")
                    reddit_comment.edit(str(reddit_comment.body) + str(comment_body))
                    link_comment.update({submission.shortlink: reddit_comment})
                else:
                    pass

        print('One submission checked for dev comments')
    counter += 1


comment_links = []


def comment_monitor():
    global comment_links
    bad_words = ['shit', 'faggot', 'nigger', 'gay', 'wanker', 'moron', 'kys'] #examples of bad words

    subreddit = r.subreddit('deadbydaylight')
    counter = 1
    for submission in subreddit.new():
        print('Checking comments in Post: '+str(counter))
        counter += 1
        if submission.shortlink not in comment_links:
            comment_links.append(submission.shortlink)
            for comment in submission.comments:
                for word in bad_words:
                    if word in (str(comment.body.encode('utf-8')).split()):
                        comment.report('Inappropriate language')

                        with open('bad_users.txt', 'a') as users_file:
                            users_file.write(str(comment.author) + ': Bad Language: ' + str(submission.shortlink) + '\n\n')
                            users_file.close()

                        redditor = r.redditor('tozzer7')
                        redditor.message('Users Using Bad Language', 'Here is a list of users using bad language: '+users_file.read())

                        print('*************** Comment has been reported for inappropriate language ***************')
                    else:
                        print('Comment acceptable')


running = False


def main():
    global finished
    global running
    running = True
    ensure_flaired_post()
    dev_comments_collect()
    comment_monitor()
    finished = True


main()
while running:
    if finished == True:
        print('Bot is now sleeping for 3 minute')
        time.sleep(180)
        finished = False

    elif finished == False:
        print('Bot is performing its next check')
        main()
