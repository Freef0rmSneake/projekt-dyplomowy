from flask import Flask, render_template, request, redirect, url_for, session
import secrets

from db.database import init_db, close_db
from db.todo_repository import (
    get_all_todos,
    get_todo,
    create_todo,
    update_todo,
    toggle_todo_done,
    delete_todo,
)

app = Flask(__name__, template_folder='templates')
app.secret_key = secrets.token_hex(16)


def get_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']


def validate_csrf_token(token):
    return token and token == session.get('csrf_token')


@app.before_request
def setup_db():
    init_db()


@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)


@app.route('/')
def index():
    todos = get_all_todos()
    return render_template("index.html", todo=todos, csrf_token=get_csrf_token())


@app.route("/add", methods=["POST"])
def add():
    if not validate_csrf_token(request.form.get('csrf_token')):
        return redirect(url_for("index"))
    todos = request.form['todos']
    create_todo(todos)
    return redirect(url_for("index"))


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    todo_item = get_todo(index)
    if todo_item is None:
        return redirect(url_for("index"))

    if request.method == "POST":
        if not validate_csrf_token(request.form.get('csrf_token')):
            return redirect(url_for("index"))
        new_task = request.form["todos"]
        update_todo(index, new_task)
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todos=todo_item, index=index, csrf_token=get_csrf_token())
    

@app.route("/check/<int:index>")
def check(index):
    toggle_todo_done(index)
    return redirect(url_for("index"))


@app.route("/delete/<int:index>")
def delete(index):
    delete_todo(index)
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)