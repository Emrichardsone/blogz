from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:locker@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blogpost = db.Column(db.String(5000))
    blogtitle = db.Column(db.String(500))
    def __init__(self, blogpost, blogtitle):
        self.blogpost = blogpost
        self.blogtitle = blogtitle

def get_blog_posts():
    return Blog.query.get()

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
        return render_template ("entry.html", blogsubmit = blogsubmit, )

    else:
        return redirect("/Blog-it")

    
#def is_complete():
     #   error = ""
        #blog_title = request.form["blogtitle"]
        
        #blogpost = request.form["textarea"]
        #title_entered = len(blog_title)
        #content_entered = len(blogpost)
        #if title_entered < 0:
         #   return True
        #else:
         #   error = error +"please enter a title"
          #  return redirect ("/Blog-it", error = error)
        
       # if content_entered <0:
        #    return True
        #else:
         #   error = error + "please enter text"
          #  return redirect ("/Blog-it", error = error)





    
if __name__=="__main__":
    app.run()
