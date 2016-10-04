from .conv import to_list


class AttrDict(dict):

    def __init__(self, defaults={}, updates={}, mergers=[]):
        super(AttrDict, self).__init__(defaults)
        self._mergers = set(mergers)
        self.update(updates)

    def update(self, other):
        if other is None:
            return
        for key, val in other.iteritems():
            if key in self._mergers:
                self._merge(key, val)
            else:
                self[key] = val

    def _merge(self, key, val):
        if key in self:
            existing = self[key]
            if not isinstance(existing, list):
                existing = [existing]
                self[key] = existing
            if isinstance(val, list):
                existing.extend(val)
            else:
                existing.append(val)
        else:
            self[key] = val

    def __unicode__(self):
        result = u''
        for key, val in self.iteritems():
            result += ' %s="%s"'%(key, u' '.join(to_list(val)))
        return result
