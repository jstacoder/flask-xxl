from flask import session

def user_context():
    if 'email' in session:
        if 'user_id' in session:
            from auth.models import User
            return {
                'user':User.get_by_id(session.get('user_id',None)),
                'email':session.get('email',None)
            }
    return {'user':None}
# register this in settings.py to make it avialible in all templates
