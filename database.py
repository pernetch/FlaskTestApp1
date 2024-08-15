from app import db, Role, User

admin_role = Role(name ='Admin')
mod_role = Role(name ='Moderator')
user_role = Role(name ='User')

user1 = User(username ='john', role = admin_role)
user2 = User(username ='susan', role = user_role)
user3 = User(username ='david', role = user_role)

db.session.add_all([admin_role, mod_role, user_role, user1, user2, user3])

db.session.commit()

User.query.all()
