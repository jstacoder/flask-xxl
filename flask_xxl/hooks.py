from mrbob import bobexceptions as mbe

# post question hooks - takes (configurator,question,answer)


# pre question hooks - takes (configurator,question)
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



