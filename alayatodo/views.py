from alayatodo import app
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    jsonify
    )
from config import todosPerPage

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

    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
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
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    myTodo = cur.fetchone()
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
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    return render_template('todo.html', todo=todo)



def getTodos(page):
    cur = g.db.execute("SELECT * FROM todos limit %s offset %s " % (todosPerPage, todosPerPage * int(page))")
    todos = cur.fetchall()
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
        g.db.execute(
            "INSERT INTO todos (user_id, description) VALUES ('%s', '%s')"
            % (session['user']['id'], request.form.get('description', ''))
        )
        g.db.commit()
        except:
        result = 'Error'
        page = 0
        return render_template('todos.html', todos=getTodos(page), result=result, page=page)
    return redirect('/todo')


@app.route('/todo/complete/<id>', methods=['POST'])
def todos_complete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute(
        "UPDATE todos SET is_complete = 1 WHERE id = '%s'" % id
    )
    g.db.commit()
    return redirect('/todo')

@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    result = 'Todo ' + id + ' deleted'
    try:
        g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)
        g.db.commit()
    except:
        result = 'Error'
    page = 0
    return render_template('todos.html', todos=getTodos(page), result=result, page=page)
