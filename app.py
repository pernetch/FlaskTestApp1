import os
from flask import Flask, render_template, url_for, session, redirect, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))


from forms import NameForm




app = Flask(__name__)

app.config['SECRET_KEY'] = 'fsadjkl fsaléf jsadf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

#tables de la DB en SQLALCHEMY
class Role (db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User (db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username   

# point d'entrée de l'application. Equivalent (att. bugs de Flask run)
if __name__ == '__main__':
   app.run(debug=True)

#shell context pour DB
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

#routes de l'application
@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    
    if form.validate_on_submit():
        #on teste si l'utilisateur existe
        user = User.query.filter_by(username=form.name.data).first()

        if user is None:
            #par défaut, un utilisateur est un User
            user_role = Role.query.filter_by(name='User').first()
            #print(user_role, user_role.id, user_role.name)
            new_user= User(username=form.name.data, role = user_role)
            db.session.add(new_user)
            db.session.commit()
            session['known'] = False
        else: 
            session['known'] = True

        #on teste si l'utilisateur est le même ou pas
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Il semble que vous ayez changé votre nom!')

        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form = form, name = session.get('name'), known = session.get('known', False))

@app.route('/<user>')
def user(user):
    user_exist = User.query.filter_by(username=user).first()

    if user_exist is None:
        return render_template('404.html')
    else:
        user_role=Role.query.filter_by(id=user_exist.role_id).first()
        return render_template('user.html', user=user, role=user_role.name)

@app.route('/about/')
def about():
    return render_template('about.html')

#test
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html',error=error), 404