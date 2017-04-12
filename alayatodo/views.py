from alayatodo import app, connect_db as db
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    jsonify
    )

from config import todosPerPage
from models import User, Todo

@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')

@app.route('/todo/<id>/json', methods=['GET'])
@app.route('/todo/<id>/json/', methods=['GET'])
def todo_json(id):
    if not session.get('logged_in'):
        return redirect('/login')
    myTodo = Todo.query.filter_by(id=id).first()
    if myTodo:
        return jsonify(dict(myTodo))
    else:
        return redirect('/todo')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')



@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo = Todo.query.filter_by(id=id).first()
    return render_template('todo.html', todo=todo)



def getTodos(page):
    todos = Todo.query.limit(todosPerPage).offset(todosPerPage * int(page))
    return todos


@app.route('/todo', methods=['GET'])
@app.route('/todo/page/<page>', methods=['GET'])
def todos(page=0):
    if not session.get('logged_in'):
        return redirect('/login')
    todos = getTodos(page)
    return render_template('todos.html', todos=todos, page=page)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    if request.form.get('description'):
        result = 'Todo added'
        try:
            todo = Todo(session['user']['id'], request.form.get('description', ''))
            db.sessions.add(todo)
            db.sessions.commit()
        except:
            result = 'Error'
        page = 0
        return render_template('todos.html', todos=getTodos(page), result=result, page=page)
    return redirect('/todo')


@app.route('/todo/complete/<id>', methods=['POST'])
def todos_complete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    stmt = update(Todo).where(id=id).values(is_complete=1)
    db.execute(stmt).fetchall()
    return redirect('/todo')

@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    result = 'Todo ' + id + ' deleted'
    try:
        Todo.query.filter_by(id=id).delete()
    except:
        result = 'Error'
    page = 0
    return render_template('todos.html', todos=getTodos(page), result=result, page=page)
