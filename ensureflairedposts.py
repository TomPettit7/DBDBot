import praw
import time

r = praw.Reddit(user_agent='The Official DeadByDaylight Bot',
                client_id='',
                client_secret='',
                username='TheDBDBot',
                password='')

checked_posts = []
def ensure_flaired_post():
    print('Running function')

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

ensure_flaired_post()
