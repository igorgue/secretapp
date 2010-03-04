import csv
import datetime

class Request(object):
    META = {}

def import_csv(f):
    return csv.reader(open(f), delimiter=',', quotechar='"')

def clean(text):
    return text.decode('utf-8','ignore')


def create_facebook(uid, name):
    fuid = uid.replace('http://www.facebook.com/profile.php?id=', '')
    
    from facebook import Facebook
    from django.contrib.auth.models import User
    fb_user, is_new = User.objects.get_or_create(username='FB:%s' % fuid)
    fb_user.first_name = name
    fb_user.save()
    return fb_user


def discussion_import(file_name):
    from discussion.models import Discussion
    
    # imports data
    data = import_csv(file_name)

    count = 0
    # creates for each data point
    for row in data:
        try:
            d = Discussion()
            d.id = row[0]
            d.title = row[1]
            d.text = row[2]
            d.tags = row[3]
            d.created_by = create_facebook(row[4], row[5])
            d.created_at = datetime.datetime.now()
            d.updated_at = datetime.datetime.now()
            d.save()
        except:
            print count
        count += 1


def comment_import(file_name):
    from comment.models import DiscussionComment
    data = import_csv(file_name)
    
    count = 0
    
    for row in data:
        #try:
            dc = DiscussionComment()
            dc.id = clean(row[0])
            dc.discussion_id = clean(row[1])
            dc.created_by = create_facebook(clean(row[3]), clean(row[4]))
            dc.text = clean(row[5])
            dc.created_at = datetime.datetime.now()
            dc.updated_at = datetime.datetime.now()
            dc.save()
        #except:
        #    print count
        #count += 1


def secret_import(file_name):
    from secret.models import Secret
    from comment.models import DiscussionComment, Proposal
    # imports data
    data = import_csv(file_name)
    
    count = 0
    # creates for each data point
    for row in data:
        #try:
        if len(row) > 1:
            try:
                s = Secret()
                s.id = clean(row[0])
                # data item 2 need to load into comments
                s.title = clean(row[2])
                s.location = clean(row[3])
                s.url = clean(row[4])
                
                comment = DiscussionComment.objects.get(pk=clean(row[1]))
                
                s.created_by = comment.created_by
                s.created_at = datetime.datetime.now()
                s.updated_at = datetime.datetime.now()
                s.save()
                
                p = Proposal()
                p.discussion_comment = comment
                p.secret = s
                p.save()
            except:
                print row[0]

        #except:
        #    print count
        #count += 1


def import_data():
    from settings import CWD
    discussion_import('%s/utilz/csv/discussions-4txt.csv' % CWD)
    comment_import('%s/utilz/csv/comments-4txt.csv' % CWD)
    secret_import('%s/utilz/csv/secrets-4txt.csv' % CWD)


