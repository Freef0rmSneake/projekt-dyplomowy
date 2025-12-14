from flask import Flask, render_template, request, redirect, url_for, session
import secrets

app = Flask(__name__, template_folder='templates')
app.secret_key = secrets.token_hex(16)

todo = [{"task": "Sample ToDo", "done": False}]


def get_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']


def validate_csrf_token(token):
    return token and token == session.get('csrf_token')


@app.route('/')
def index():
    return render_template("index.html", todo=todo, csrf_token=get_csrf_token())


@app.route("/add", methods=["POST"])
def add():
    if not validate_csrf_token(request.form.get('csrf_token')):
        return redirect(url_for("index"))
    todos = request.form['todos']
    todo.append({"task": todos, "done": False})
    return redirect(url_for("index"))


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    todos = todo[index]
    if request.method == "POST":
        if not validate_csrf_token(request.form.get('csrf_token')):
            return redirect(url_for("index"))
        todos['task'] = request.form["todos"]
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todos=todos, index=index, csrf_token=get_csrf_token())
    

@app.route("/check/<int:index>")
def check(index):
    todo[index]['done'] = not todo[index]['done']
    return redirect(url_for("index"))


@app.route("/delete/<int:index>")
def delete(index):
    del todo[index]
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)