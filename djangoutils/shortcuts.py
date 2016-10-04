import os
from django.conf import settings
from django.core.files import File
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import Http404, HttpResponseServerError
from django.shortcuts import get_object_or_404, _get_queryset

import logging
logger = logging.getLogger(__name__)


def paginate(request, qs, rpp=20):
    # Make sure we have a valid results per page value.
    try:
        rpp = int(request.GET.get('rpp', rpp))
    except:
        rpp = 20;
    paginator = Paginator(qs, rpp)
    # Make sure we were given a valid page number.
    try:
        page_no = int(request.GET.get('page', '1'))
        if page_no < 1:
            page_no = 1
    except ValueError:
        page_no = 1
    # Make sure the page number is not too high.
    try:
        return paginator.page(page_no)
    except (EmptyPage, InvalidPage):
        return paginator.page(paginator.num_pages)


def redirect(request, tag='redirect', default=''):
    redirect = request.GET.get(tag, default)
    return HttpResponseRedirect(redirect)


def render(request, template=None, **kwargs):
    return render_to_response(template, kwargs, context_instance=RequestContext(request))


def get_object(request, klass, id_tag, query={}):
    klass = _get_queryset(klass)
    try:
        id = int(request.GET[tag])
    except:
        raise Http404
    return get_object_or_404(klass, pk=id, **query)


def filter_objects_by_form(request, klass, form_class,
                           form_fltr={}, def_fltr={}, com_fltr={},
                           pre_filter=None, method='POST'):
    klass = _get_queryset(klass)
    okay = False
    if request.method == method:
        form = form_class(request.POST if (method == 'POST') else request.GET)
        if form.is_valid():
            q_fltr = []
            fltr = {}
            for field, form_key in form_fltr.iteritems():
                val = form.cleaned_data[form_key]
                if val:
                    fltr[field] = val
            if pre_filter:
                pre_filter(form, fltr, q_fltr)
            if fltr or q_fltr:
                fltr.update(com_fltr)
                qs = klass.filter(*q_fltr, **fltr).distinct()
                okay = True
    else:
        form = form_class()
    if not okay:
        if def_fltr:
            fltr = dict(def_fltr) if com_fltr else def_fltr
            fltr.update(com_fltr)
            qs = klass.filter(**fltr).distinct()
        else:
            qs = klass.all(**com_fltr)
    return qs, form


def render_form_filter(request, tmpl, klass, form_class,
                       form_fltr={}, def_fltr={}, com_fltr={},
                       method='POST', order_by=None, objs_per_page=10):
    objs, form = filter_objects_by_form(request, klass, form_class, form_fltr, def_fltr, com_fltr, method)
    if order_by:
        objs = objs.order_by(order_by)
    if objs_per_page is not None and objs_per_page > 0:
        objs = paginate(request, objs, objs_per_page)
    return render(request, tmpl, form=form, objects=objs)


def render_object(request, id, template=None, model_class=None):
    if not template or not model_class:
        return HttpResponseServerError()
    return render(request, template, object=get_object_or_404(model_class, pk=id))


def edit_object_by_form(request, klass, form_class, id_tag='', query={}, form_sets={}):
    klass = _get_queryset(klass)
    obj = get_object(request, klass, id_tag, query)
    if request.method == 'POST':
        form = forms_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return obj, None
    else:
        form = form_class(instance=obj)
    for key, qs in form_sets.iteritems():
        form.fields[key].queryset = qs
    return (obj, form)


def new_object_by_form(request, form_class, form_sets):
    user = request.user
    if request.method == 'POST':
        form = forms.NewTaskForm(request.POST)
        if form.is_valid():
            if save:
                save(form)
            else:
                form.save()
            return None
    else:
        form = forms.NewTaskForm()
    for key, qs in form_sets.iteritems():
        form.fields[key].queryset = qs
    return form


def get_back_path(path):
    dirs = path.split('/')[:-1]
    dirs = [d for d in dirs if d != '']
    back = '/' + '/'.join(dirs[:-1])
    if back[-1] != '/':
        back += '/'
    return back


def get_week_dates(year=None, week=None):
    if year is None or week is None:
        year, week, day = date.today().isocalendar()
    else:
        year = int(year)
        week = int(week)
    start = date(year, 1, 1)
    week0 = start - timedelta(days=start.isoweekday())
    sun = week0 + timedelta(weeks=week)
    sat = sun + timedelta(days=6)
    return (sun, sat)


def get_week_bins(year=None, week=None):
    sun, sat = get_week_dates(year, week)
    bins = []
    day = sun
    for ii in range(7):
        day_begin = datetime(day.year, day.month, day.day, 0, 0, 0, 0)
        day = day + timedelta(days=1)
        day_end = datetime(day.year, day.month, day.day, 0, 0, 0, 0)
        bins.append((day_begin, day_end))
    return bins


def import_scrapy_image(file_field, image):
    filename = os.path.basename(image['path'])
    filepath = os.path.join(settings.SCRAPY_IMAGES_STORE, image['path'])
    file_field.save(filename, File(open(filepath)))
