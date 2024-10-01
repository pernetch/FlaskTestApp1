import os
from flask import Flask, render_template, url_for, session, redirect, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))


from forms import NameForm
from models import *

app = Flask(__name__)

app.config.from_pyfile(os.path.join(basedir, 'config.py'))

bootstrap = Bootstrap(app)
#db = SQLAlchemy(app)
db.init_app(app)

 



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
        #return render_template('user.html', user=user, role=user_role.name)
        return render_template('user.html',user=user_exist)
    
@app.route('/users/')
def users():
    users = User.query.order_by(User.username.desc())
    return render_template('users.html',users=users)

@app.route('/about/')
def about():
    return render_template('about.html')

# on ajoute un commentaire ici...
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html',error=error), 404

# point d'entrée de l'application. Equivalent (att. bugs de Flask run)
if __name__ == '__main__':
   app.run(debug=True)