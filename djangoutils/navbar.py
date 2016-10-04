from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class NavbarMetaclass(type):

    def __new__(cls, name, bases, attrs):

        # Parse all the entries.
        new_entries = []
        for entry in attrs.get('entries', []):
            try:
                tag, url = entry
            except:
                raise TypeError('Each entry must be a tuple of length 2.')
            new_entries.append((tag, reverse(url)))
        attrs['entries'] = new_entries

        # Continue as usual.
        return super(NavbarMetaclass, cls).__new__(cls, name, bases, attrs)


class Entry(object):

    def __init__(self, tag, url):
        self.tag = tag
        self.url = url


class BoundEntry(object):

    def __init__(self, entry, selected):
        self.entry = entry
        self.selected = selected

    def __unicode__(self):
        if self.selected:
            html = u'<li class="selected"><span>%s</span></li>'%self.entry.tag
        else:
            html = u'<li><a href="%s">%s</a></li>'%(reverse(self.entry.url), self.entry.tag)
        return mark_safe(html)

    @property
    def url(self):
        return self.entry.url

    @property
    def tag(self):
        return self.entry.tag

    def open(self):
        if self.selected:
            html = u'<li class="selected">'
        else:
            html = u'<li>'
        return mark_safe(html)

    def link(self):
        if self.selected:
            html = u'<span>%s</span>'%self.tag
        else:
            html = u'<a href="%s">%s</a>'%(reverse(self.url), self.tag)
        return mark_safe(html)

    def close(self):
        return mark_safe(u'</li>')


class Navbar(object):

    def __init__(self, selected=None):
        self.selected = selected

    def __unicode__(self):
        html = ['<ol id="navbar">']
        for ii, entry in enumerate(self.entries):
            if ii == self.selected:
                html.append(u'<li class="selected"><span>%s</span></li>'%entry[0])
            else:
                html.append(u'<li><a href="%s">%s</a></li>'%(reverse(entry[0]), entry[1]))
        html.append('</ol>')
        return mark_safe(u'\n'.join(html))

    def open(self):
        return mark_safe(u'<ol id="navbar">')

    def iter_entries(self):
        for ii, entry in enumerate(self.entries):
            yield BoundEntry(entry, ii == self.selected)

    def close(self):
        return mark_safe(u'</ol>')
