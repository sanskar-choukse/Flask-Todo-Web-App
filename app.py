from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy   # when we create database so we use SQLAlchemy
from datetime import datetime             #use of this when defeaut set =datetime
from flask import flash                   #use of flash when return a message
from sqlalchemy import or_                #use for check value ASC & DESC



app=Flask(__name__)
app.secret_key = "mysecretkey"         #we use app.secret  when we use of flash for message write


# Here are some example connection database if you want to create SQLitedatabase so enter SQLite URL:

# # SQLite, relative to Flask instance path
# sqlite:///project.db

# # PostgreSQL
# postgresql://scott:tiger@localhost/project

# # MySQL / MariaDB
# mysql://scott:tiger@localhost/project

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///./Shukvimla.db"    # when we create database so we use config & now we are create Sqlite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

# Create table that'swhy we use class 
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"  # <-- here


@app.route('/', methods=['GET','POST'])
def create():
    if request.method == "POST":   # iska use actual me form me data load kerane ke liye 
        title=request.form.get('title')
        desc=request.form.get('desc')
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
        flash("Todo added successfully!", "success")

    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo) #data show in index.html by using for loop in index.html


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/search')
def search():
    query = request.args.get('q')

    if not query:
        return redirect('/')

    results = Todo.query.filter(
        or_(
            Todo.title.ilike(f"%{query}%"),
            Todo.desc.ilike(f"%{query}%")
        )
    ).all()

    return render_template('index.html', allTodo=results)

# @app.route('/show')  
# def product():
#     allTodo = Todo.query.all()  #that show the all data title in a terminal
#     print(allTodo)
#     return render_template('index.html')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.get_or_404(sno)

    if request.method == "POST":
        todo.title = request.form.get('title')
        todo.desc = request.form.get('desc')
        db.session.commit()
        flash("Todo updated successfully!", "info")
        return redirect('/')

    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')  
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    flash("Todo deleted!", "danger")
    return redirect("/")


@app.context_processor
def inject_datetime():
    return {'datetime':datetime}


# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()    # ✅ THIS CREATES DB
    app.run(debug=True, port=8000)    