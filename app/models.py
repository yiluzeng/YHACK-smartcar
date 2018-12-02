from werkzeug.security import generate_password_hash, check_password_hash
from app import login, firedata

@login.user_loader
def load_user(id):
    return User(id)

class User():
    def __init__(self, userid):
        self.userid = userid
        self.doc_ref = firedata.db.collection('users').document(userid)
    def set_name(self, name):
        d = self.doc_ref.get().to_dict()
        d['name'] = name
        self.doc_ref.set(d)
    def get_name(self):
        return self.doc_ref.get().to_dict()['name']
    def set_password(self, password):
        d = self.doc_ref.get().to_dict()
        d['pass_hash'] = generate_password_hash(password)
        self.doc_ref.set(d)
    def check_password(self, password):
        pass_hash = self.doc_ref.get().to_dict()['pass_hash']
        return check_password_hash(pass_hash, password)
    def get_rentals(self):
        return self.doc_ref.get().to_dict()['rentals']
    def set_rentals(self, rental):
        d = self.doc_ref.get().to_dict()
        d['rentals'].append(rental)
        self.doc_ref.set(d)
    def get_cars(self):
        return self.doc_ref.get().to_dict()['cars']
    def set_cars(self, car):
        d = self.doc_ref.get().to_dict()
        d['cars'].append(rental)
        self.doc_ref.set(d)
    def get_profile(self):
        try:
            return self.doc_ref.get().to_dict()['profile']
        except KeyError:
            return None
    def has_profile(self):
        return self.get_profile() is not None
    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.userid
