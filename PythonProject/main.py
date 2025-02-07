from dominate.tags import progress
from flask import Flask,render_template,request,url_for,redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
import os
from dotenv import load_dotenv
load_dotenv()
app=Flask(__name__)
app.config['SECRET_KEY'] =os.environ.get('FLASK_KEY')
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("DB_URI","sqlite:///to_do_list.db")




class Base(DeclarativeBase):
     pass
db=SQLAlchemy(model_class=Base)
db.init_app(app)
class Task(db.Model):
    id:Mapped[int]=mapped_column(primary_key=True)
    task:Mapped[str]=mapped_column(nullable=False)
    status:Mapped[str]=mapped_column(nullable=False)
with app.app_context():
    db.create_all()
@app.route("/")
def home():
    all_tasks = db.session.execute(db.select(Task)).scalars().all()
    return render_template("index.html", tasks=all_tasks, enumerate=enumerate)
@app.route("/Add_Task",methods=["GET","POST"])
def add():
    if request.method=="POST":
        name=request.form.get("todo")
        new_task=Task(
            task=name,
            status='In progress'
        )
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('home'))
@app.route("/home<int:id>")
def delete(id):
    deleted=db.get_or_404(Task,id)
    db.session.delete(deleted)
    db.session.commit()
    return redirect(url_for('home'))
@app.route("/finish<int:id>")
def finish(id):
    finish_task=db.get_or_404(Task,id)
    finish_task.status="Finished"
    db.session.commit()
    return  redirect(url_for('home'))
if __name__=="__main__":
    app.run(debug=True)
