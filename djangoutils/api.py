import json
from django.http import HttpResponse
from django.db.models import Q

import logging
logger = logging.getLogger(__name__)


def follow(obj, field):
    parts = field.split('__')
    for part in parts:
        obj = getattr(obj, part)
    return obj


def autocomplete(request, model=None, fields=None, limit=10):
    if isinstance(fields, str):
        fields = [fields]
    data = ''
    if request.is_ajax():
        term = request.GET.get('term', '')
        limit = request.GET.get('limit', limit)
        fltr = []
        for field in fields:
            fltr.append(Q(**{field + '__icontains': term}))
        fltr = reduce(lambda x,y: x|y, fltr)
        try:
            objs = model.objects.filter(fltr)[:limit]
            data = json.dumps([', '.join([follow(o, f) for f in fields if follow(o, f)]) for o in objs])
        except:
            pass
    return HttpResponse(data, mimetype='application/javascript')


def get_record_field(request, id, field, model=None):
    data = ''
    if request.is_ajax():
        try:
            obj = model.objects.get(pk=id)
            data = json.dumps(getattr(obj, field))
        except:
            pass
    return HttpResponse(data, mimetype='application/javascript')
