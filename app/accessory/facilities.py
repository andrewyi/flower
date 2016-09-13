
def app_func():
    def avalue(t):
        return ('avalue converted input: %s' % (t.v,))
    return dict(avalue_r=avalue)
