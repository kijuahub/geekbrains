from flask import Flask, render_template, request, jsonify
from database import db
from models import Task

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def index():
    active_tasks = Task.query.filter_by(deleted=False, completed=False).all()
    completed_tasks = Task.query.filter_by(deleted=False, completed=True).all()
    deleted_tasks = Task.query.filter_by(deleted=True).all()

    return render_template("index.html", active_tasks=active_tasks, completed_tasks=completed_tasks,
                           deleted_tasks=deleted_tasks)


@app.route("/add", methods=["POST"])
def add_task():
    content = request.form.get("content")
    if content:
        task = Task(content=content)
        db.session.add(task)
        db.session.commit()
        return jsonify({'success': True, 'id': task.id, 'content': task.content})
    return jsonify({'success': False}), 400


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return jsonify({'success': True, 'completed': task.completed})


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.deleted = True
    db.session.commit()
    return jsonify({'success': True, 'content': task.content})


@app.route("/restore/<int:task_id>", methods=["POST"])
def restore_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.deleted = False
    db.session.commit()
    return jsonify({'success': True, 'content': task.content})


@app.route("/hard_delete/<int:task_id>", methods=["POST"])
def hard_delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'success': True})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)