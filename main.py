from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:locker@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = "123"
#gotta have a secret key when using flash

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blogpost = db.Column(db.String(5000))
    blogtitle = db.Column(db.String(500))
    def __init__(self, blogpost, blogtitle):
        self.blogpost = blogpost
        self.blogtitle = blogtitle
#The above is defining a class and setting up a database-to make a database work you have
#to drop and create in python while MAMP is running

@app.route("/")
def root():
    somevariable = request.args.get("id")
    instanceofblogobject = Blog.query.filter_by(id = somevariable).first()
#This is not totally great because there is no route--HOWEVER! It works. this pulls out the specific id
    return render_template("index.html", displayblog = Blog.query.all(), somevariable=somevariable, instanceofblogobject=instanceofblogobject)

@app.route("/Blog-it", methods = ['GET', 'POST'])
def blog():   
    if request.method == "POST":
        blog_title = request.form["blogtitle"]
        blogpost = request.form["textarea"]
        blogsubmit = Blog(blogpost,blog_title )
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
            return redirect("/?id="+str(blogid))

    else:
        return render_template("Blog-it.html")




    
if __name__=="__main__":
    app.run()
