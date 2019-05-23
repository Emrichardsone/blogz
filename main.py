from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:locker@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "123"


class Blog(db.Model): #Blog class

    id = db.Column(db.Integer, primary_key=True)
    blogpost = db.Column(db.String(5000))
    blogtitle = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __init__(self, blogpost, blogtitle, owner):
        self.blogpost = blogpost
        self.blogtitle = blogtitle
        self.owner = owner

class User(db.Model):#User class

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blog = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', "static", 'allposts', 'usersblogs','root']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route("/") 
def root():
    #somevariable = request.args.get("id")
    return render_template("index.html", users=User.query.all())

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and password == user.password:
            session['email'] = email
            flash("Logged in")
            return redirect("/")
        else:
            flash('User password incorrect, or user does not exist', 'error')
            return render_template("login.html")
    else:
        return render_template ('login.html')
  
@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        password = request.form['password']
        verify = request.form ['verify']
        email = request.form ['email']
        existing_user = User.query.filter_by(email=email).first()
        has_error = False
        if not is_email(email):
            flash ("Please enter a valid email")
            has_error = True
        if password != verify:
            flash ('Please enter matching passwords')
            has_error = True
        if " " in password:
            flash ('Please exclude spaces from password')
            has_error = True
        if existing_user:
            flash('This email is already in use')
            has_error=True
        if has_error:
            return redirect ("/signup")
        else:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return render_template('/Blog-it.html')
    else:
        return render_template("signup.html")
def is_email(string):
    string = request.form["email"]
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    length =len(string) 
    
    if not atsign_present:
        return False
    if length < 3 or length > 20 :
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present
    

    if length < 3 or length > 20:
        return False
    
    else:
        return True
    return render_template("signup.html")

def is_email(string):
    string = request.form["email"]
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    length =len(string) 
    
    if not atsign_present:
        return False
    if length < 3 or length > 20 :
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present   

@app.route("/Blog-it", methods = ['GET', 'POST']) 
def blog():   
    if request.method == "POST":
        owner = User.query.filter_by(email = session ['email']).first()
        blog_title = request.form["blogtitle"]
        blogpost = request.form["textarea"]
        blogsubmit = Blog(blogpost, blog_title, owner )
        error_present = False

        if not blog_title:
            flash("You left the Blog title blank! Give your entry a title :)")
            error_present = True
        if not blogpost:
            flash("You left Blog Content blank! Give us your thoughts :)")
            error_present = True
        if error_present:
            return redirect ("/Blog-it")

        else:
            db.session.add(blogsubmit)
            db.session.commit()
            blogid = blogsubmit.id
            return redirect("/allposts?id="+str(blogid))

    else:
        return render_template("Blog-it.html")

@app.route("/showblogs")
def usersblogs():
    user_id = request.args.get("user_id")
    blogs = Blog.query.filter_by(owner_id=int(user_id))
    
    return render_template("showblogs.html", blogs=blogs)

@app.route("/allposts")
def allposts():
    somevariable = request.args.get("id")
    theblog = Blog.query.filter_by(id=somevariable).first()
    return render_template("allposts.html", allblogs = Blog.query.all(), 
    theblog=theblog, somevariable=somevariable)

@app.route("/logout")
def logout():
    session.clear()
    return render_template ("logout.html")




    
if __name__=="__main__":
    app.run()
