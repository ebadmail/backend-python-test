from alayatodo.models import Todo, User
from alayatodo import connect_db as db
user = User('user1', 'user1')
db.session.add(user)

todo1 = Todo(1, 'Vivamus tempus')
todo2 = Todo(1, 'lorem ac odio')
todo3 = Todo(1, 'Ut congue odio')
todo3 = Todo(1, 'lorem ac odio')
todo4 = Todo(1, 'Lorem ipsum')

db.session.add(todo1)
db.session.add(todo2)
db.session.add(todo3)
db.session.add(todo4)
db.session.commit()
