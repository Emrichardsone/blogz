from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:locker@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = "123"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blogpost = db.Column(db.String(5000))
    blogtitle = db.Column(db.String(500))
    def __init__(self, blogpost, blogtitle):
        self.blogpost = blogpost
        self.blogtitle = blogtitle

@app.route("/blog")
def root():
    somevariable = request.args.get("id")
    instanceofblogobject = Blog.query.filter_by(id = somevariable).first()
    
    return render_template("index.html", displayblog = Blog.query.all(), somevariable=somevariable, instanceofblogobject=instanceofblogobject)

@app.route("/Blog-it", methods = ['GET', 'POST'])
def blog():   
    if request.method == "POST":
        blog_title = request.form["blogtitle"]
        blogpost = request.form["textarea"]
        blogsubmit = Blog(blogpost,blog_title )
        db.session.add(blogsubmit)
        db.session.commit()
        blogid = blogsubmit.id
        
        #if is_complete == True:
        return redirect("/blog?id="+str(blogid))

    else:
        return render_template("Blog-it.html")

    
if __name__=="__main__":
    app.run()
