from core.models import Topic, User, Outcome, Course
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import csv


def import_topics(filename):
    with open(filename, 'rt', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        topic_list = list(reader)
    for i in topic_list:
        t = Topic(name=i[0],
                  descriptor=i[1])
        t.save()


def import_users(filename):
    with open(filename, 'rt', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        user_list = list(reader)
    for i in user_list:
        u = User(name=i[0],
                 descriptor=i[1])
        u.save()


def import_outcomes(filename):
    with open(filename, 'rt', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        outcome_list = list(reader)
    for i in outcome_list:
        t = Topic.objects.get(name=i[1])
        u = User.objects.get(name=i[2])
        o = Outcome(topic=t,
                    user=u,
                    code=i[0],
                    descriptor=i[3])
        o.save()


def import_course(filename):
    with open(filename, 'rt', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        course_list = list(reader)
    for i in course_list[1:]:
        try:
            c = Course(code=i[0],
                       title=i[1],
                       topic=i[2],
                       type=i[3],
                       opening=i[4],
                       duration=i[5],
                       venue=i[6],
                       fee=i[7],
                       grant=i[8],
                       wsa=i[9],
                       remark=i[10],
                       overview=i[11],
                       outline=i[12],
                       testimonial=i[13],
                       upcoming=i[14],
                       hyperlink=i[15])
            c.save()
            print('Added: {}'.format(i[0]))
        except IntegrityError as e:
            if 'UNIQUE constraint failed: core_course.code' in e.args:
                c = Course.objects.get(code=i[0])
                c.title = i[1]
                c.topic = i[2]
                c.type = i[3]
                c.opening = i[4]
                c.duration = i[5]
                c.venue = i[6]
                c.fee = i[7]
                c.grant = i[8]
                c.wsa = i[9]
                c.remark = i[10]
                c.overview = i[11]
                c.outline = i[12]
                c.testimonial = i[13]
                c.upcoming = i[14]
                c.hyperlink = i[15]
                c.save()
                print('Updated: {}'.format(i[0]))


def import_mappings(filename):
    with open(filename, 'rt', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        course_mappings = list(reader)
    for i in course_mappings:
        try:
            c = Course.objects.get(code=i[0])
            o = Outcome.objects.get(code=i[1])
            c.outcomes.add(o)
        except ObjectDoesNotExist:
            print('Either object does not exists: {} - {}'.format(i[0], i[1]))
        except MultipleObjectsReturned:
            print('Multiple objects returned: {} - {}'.format(i[0], i[1]))


