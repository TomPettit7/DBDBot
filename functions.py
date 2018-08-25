import praw

r = praw.Reddit(user_agent='The Official DeadByDaylight Bot',
                client_id='*************',
                client_secret='****************',
                username='TheDBDBot',
                password='***********')

post_links = []
def link_post_remover():
    global post_links
    bad_words = ['porn']
    bad_users = []
    subreddit = r.subreddit('deadbydaylight')
    counter = 1
    for submission in subreddit.new():
        print('Post: '+str(counter))
        counter += 1
        if submission.shortlink not in post_links:
            post_links.append(submission.shortlink)
            for word in bad_words:
                if str(word) in str(submission.url):
                    print('Found a URL that is bad')
                    print(submission.shortlink)
                    submission.report('Post link looks to contain a pornographic website')

                    with open('bad_users.txt', 'a') as users_file:
                        users_file.write(str(submission.author) + ': Posting a bad link: ' + str(submission.shortlink) + '\n')
                        users_file.close()

                    bad_users.append(submission.author)
                    print('Reported and lists appended')
                    try:
                        submission.reply('The URL of this post looks like it contains explicit content, which is banned under this subs rules, sorry :)    *If you feel this has been removed incorrectly, message the moderator team*')
                        #submission.delete()
                    except:
                        submission.hide()
                        print('Submission hidden as the reddit rate limit restricted me. The post has been reported.')
                    else:
                        pass
                else:
                    print('Link fine')
                    pass

    print(post_links)


comment_links = []
def comment_monitor():
    global comment_links
    bad_words = ['shit', 'faggot', 'nigger', 'gay', 'wanker', 'moron', 'kys'] #examples of bad words
    bad_people = []

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
                            users_file.write(str(submission.author) + ': Bad Language: ' + str(submission.shortlink) + '\n')
                            users_file.close()

                        print('*************** Comment has been reported for inappropriate language ***************')
                    else:
                        print('Comment acceptable')
    print(comment_links)

dev_comment_links = []
def dev_comments_collect():
    devs = [list of the BHVR devs]
    dev_comments = []
    subreddit = r.subreddit('deadbydaylight')
    for submission in subreddit.new():
        if submission.shortlink not in dev_comment_links:
            dev_comment_links.append(submission.shortlink)
            for comment in submission.comments:
                if str(comment.author) in devs:
                    print('Found a dev comment')
                    comment_body = comment.body.encode('utf-8')
                    comment_author = comment.author
                    dev_comments.append([comment_author, comment_body])
                else:
                    print('Comment not from Dev')
                    pass


        if len(dev_comments) == 0:
            pass
        else:
            for comment in dev_comments:
                with open('my_comment.txt', 'a') as comment_file:
                    comment_file.write(str(comment[0]) + ' said: ' + str(comment[1]) + '\n\n')

            with open('my_comment.txt', 'r') as comment_file:
                my_comment_body = comment_file.read()
                my_comment = ' ------ Here is a list of BHVR comments in this thread ------  \n\n' + str(my_comment_body)
                my_comment = my_comment.replace("b'", "'")

            reddit_comment = submission.reply(my_comment)
            reddit_comment.mod.distinguish(how='yes', sticky=True)

        with open('my_comment.txt', 'w') as rewrite_file:
            rewrite_file.write('')

        dev_comments.clear()
