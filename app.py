from flask import Flask, render_template, request, redirect, url_for
from models import db, Post, Goga,Category, Otziv
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from form import RegisterForm, LoginForm, ArticleForm,OtzivForm
import locale


locale.setlocale(locale.LC_ALL, '')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///identifier.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
db.init_app(app)
migarte = Migrate(app, db)
login = LoginManager(app)


@login.user_loader
def load_user(user_id):
    return Goga.query.get(int(user_id))



@app.route('/')
def index():
    return render_template("index.html", articles=Post.query.all())



@app.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = Goga.query.filter_by(email=email).first()
        login_user(user, remember=True)
        return redirect('/')
    return render_template('login.html', form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route("/about")
def about():
    return render_template("about.html")




@app.route('/add', methods=['GET', 'POST'])
@login_required
def create_article():
    article_form = ArticleForm()
    if article_form.validate_on_submit():
        title = article_form.title.data
        body = article_form.body.data
        address = article_form.address.data
        category_id = article_form.category_id.data
        author_id = current_user.name
        post_id = article_form.post_id.data
        article = Post(title=title, body=body,address=address,category_id=category_id,author_id=author_id, post_id=post_id )
        db.session.add(article)
        db.session.commit()
        return redirect('/')
    return render_template('add.html', form=article_form)


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route('/index/<int:id>')
def post(id):
    item = Post.query.get(id)
    lol = Otziv.query.query.get_or_404(post)
    return render_template("post_detail.html", item = item, lol=lol)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        name = register_form.name.data
        password = register_form.password.data
        user = Goga(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect('/')
    return render_template('register.html', form=register_form)


@app.route('/search')
def search():
    text = request.args['text']
    result = Post.query.filter(db.or_(
        Post.title.like(f'%{text}%'),
        Post.body.like(f'%{text}%')
    )).all()

    if len(result) == 1:
        return redirect(url_for('/index/<int:article_id>', article_id=result[0].id))

    return render_template('index.html', header=f'Поиск по слову "{text}"', articles=result)


@app.route('/category/<int:category_id>')
def category_articles(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template('category.html', category=category)


@app.context_processor
def inject_categories():
    return {'categories': Category.query.all()}


@app.route('/add_otziv', methods=['GET', 'POST'])
def otziv():
    add_otziv = OtzivForm()
    if add_otziv.validate_on_submit():
        title = add_otziv.about.data
        bode = add_otziv.lol.data
        star = add_otziv.star.data
        athor= current_user.name
        otziv = Otziv(title=title,bode=bode,star=star, athor=athor)
        db.session.add(otziv)
        db.session.commit()
        return redirect('/')
    return render_template('add_otziv.html', form=add_otziv)


@app.route('/home_id')
def home():
    status = Post.query.all()
    status[current_user]
    return render_template('home_id.html', status = status)


if __name__ == '__main__':
    app.run()