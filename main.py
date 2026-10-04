import os
from flask import Flask, render_template, request, redirect, url_for
from database import db
from models import Task

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///tasks.db").replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    active = Task.query.filter_by(deleted=False, completed=False).all()
    completed = Task.query.filter_by(deleted=False, completed=True).all()
    deleted = Task.query.filter_by(deleted=True).all()
    return render_template("index.html", active_tasks=active, completed_tasks=completed, deleted_tasks=deleted)


@app.route("/add", methods=["POST"])
def add_task():
    content = request.form.get("content", "").strip()
    if content:
        db.session.add(Task(content=content))
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.deleted = True
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/restore/<int:task_id>", methods=["POST"])
def restore_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.deleted = False
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/hard_delete/<int:task_id>", methods=["POST"])
def hard_delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
