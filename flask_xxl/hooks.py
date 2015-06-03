from mrbob import bobexceptions as mbe

# post question hooks - takes (configurator,question,answer)
def skip_next_if(c,q,a):
    if a:
        c.questions.pop(c.questions.index(q)+1)
    return a

def skip_next_if_not(c,q,a):
    if not a:
        c.questions.pop(c.questions.index(q)+1)
    return a

def to_list(c,q,a):
    return a.split(',')

def choose_app_template(c):
    if c.variables['app.language'].startswith('c'):
        c.template_dir = '{}_coffee'.format(c.template_dir)

# pre question hooks - takes (configurator,question)
def only_if_type(c,q):
    print c.variables['service.service_type']
    print q.extra.get('check_type')
    if c.variables['service.service_type'] != q.extra.get('check_type'):
        raise mbe.SkipQuestion

def add_apps(c,q):
    if not c.variables['project.add_apps']:
        raise mbe.SkipQuestion

def check_for_captcha(c,q):
    if not c.variables['local_settings.use_captcha']:
        raise mbe.SkipQuestion

def db_related_skip(c,q):
    if not c.variables['project.use_database']:
        raise mbe.SkipQuestion

# pre render hooks - takes nothing - maybe configurator

def get_service_type(c):
    c.template_dir = '{}/{}'.format(c.template_dir,c.variables['service.service_type'])    

def make_db_uri(c):
    if c.variables['project.use_database']:
        fmt = '%s://%s:%s@%s:%d/%s' 
        c.variables['project.db_uri'] = fmt % (c.variables['project.db-driver'],
                                               c.variables['project.db-username'],
                                               c.variables['project.db-password'],
                                               c.variables['project.db-host'],
                                               c.variables['project.db-port'],
                                               c.variables['project.db-name'])
# post render hooks - takes (configurator)



