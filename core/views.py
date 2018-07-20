from django.shortcuts import render, redirect
from core.models import Topic, User, Outcome, Course
from core.data_import import import_users, import_topics, import_course, import_outcomes, import_mappings
from itertools import chain, combinations
import ast


def all(outcomes_list):
    query_all = Course.objects.filter(outcomes__code__in=outcomes_list)
    relevant_all = [i.code for i in query_all]
    return list(set(relevant_all))


def up(outcomes_list):
    query_up = Course.objects.filter(outcomes__code__in=outcomes_list).exclude(upcoming='NO AVAILABLE DATES')
    relevant_up = [i.code for i in query_up]
    return list(set(relevant_up))


def powerset(relevant_list, max_length):
    s = list(relevant_list)
    return chain.from_iterable(combinations(s, r) for r in range(max_length+1))


def curate(outcomes_selected, max_length):
    relevant = up(outcomes_list=outcomes_selected)
    combi = powerset(relevant_list=relevant, max_length=max_length)
    results_table = []
    for x in combi:
        html = []
        covered_bymodel = []
        duration_bymodel = float(0)
        if x == () or x == []:
            continue
        for y in x:
            [covered_bymodel.append(i.code) for i in Outcome.objects.filter(course__code=y)]
            duration_bymodel += float(str(Course.objects.get(code=y).duration)[:-5])
            html.append("<a href='{}'>{}</a>".format(Course.objects.get(code=y).hyperlink, y))
        results_table.append([html, duration_bymodel,
                              len([x for x in outcomes_selected if x in covered_bymodel]) / len(outcomes_selected)])
    results_table = sorted(results_table, key=lambda x: (x[1]))
    results_table = sorted(results_table, key=lambda x: (len(x[0])))
    results_table = sorted(results_table, key=lambda x: (x[2]), reverse=True)
    for i in results_table:
        i[0] = ' + '.join(i[0])
        i[1] = "{} hours".format(i[1])
        i[2] = "{:.2%}".format(i[2])
    return results_table


def index(request):
    return redirect('step1')


def step1(request):
    topics = Topic.objects.all()
    return render(request, 'core/base_step1.html', {'topics': topics})


def step2(request):
    if request.method == 'POST':
        topic_selected = request.POST['topic_selection']
        learning_outcomes = Outcome.objects.filter(topic__name=topic_selected)
        return render(request, 'core/base_step2.html', {'topic_selected': topic_selected,
                                                   'learning_outcomes': learning_outcomes})
    return redirect('index')


def step3(request):
    if request.method == 'POST':
        if request.META['HTTP_REFERER'][-2:-1] == '2':
            outcomes_selected = request.POST.getlist('curator')
            model_limit = 3
            display_limit = 10
        elif request.META['HTTP_REFERER'][-2:-1] == '3':
            outcomes_selected = ast.literal_eval(request.POST['curator'])
            model_limit = int(request.POST['model_limit'])
            display_limit = int(request.POST['display_limit'])
        if model_limit > 6:
            model_limit = 5
        elif model_limit < 1:
            model_limit = 1
        results_table = curate(outcomes_selected=outcomes_selected, max_length=model_limit)
        combi_limit = len(results_table)
        if display_limit < 1:
            display_limit = 1
        elif display_limit > combi_limit:
            display_limit = combi_limit
        return render(request, 'core/base_step3.html', {'outcomes_selected': outcomes_selected,
                                                   'models': results_table[:display_limit],
                                                   'max_display': display_limit,
                                                   'max_model': model_limit,
                                                   'max_combi': combi_limit})
    return redirect('index')