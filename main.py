from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates')

todo = [{"task": "Sample ToDo", "done": False}]


@app.route('/')
def index():
    return render_template("index.html", todo=todo)


@app.route("/add", methods=["POST"])
def add():
    todos = request.form['todos']
    todo.append({"task": todos, "done": False})
    return redirect(url_for("index"))


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    todos = todo[index]
    if request.method == "POST":
        todos['task'] = request.form["todos"]
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todos=todos, index=index)
    

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