class User:
    ...

class Ad:
    user_id = ...
    
    @property
    def user(self):
        User.query.filter_by(id=self.user_id).first()
        
        
Ad.user.name = "Felipe"

db.session.commit()

