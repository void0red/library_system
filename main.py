from config import *
from Database import *
from flask_security import login_user, login_required, logout_user, current_user
from flask import jsonify, request
import datetime
from sqlalchemy import and_, or_


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return '', 400
    user = User.query.filter_by(email=data['email']).first()
    if user is None:
        return '', 202
    elif not user.password == data['password']:
        return '', 203
    elif user.has_role('User'):
        login_user(user, remember=data['remember'])
        return '', 200
    elif user.has_role('Admin'):
        login_user(user, remember=data['remember'])
        return '', 201
    else:
        return '', 400


@app.route('/api/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return '', 200


@app.route('/api/user/register', methods=['POST'])
def user_register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password') or not data.get('username'):
        return '', 400
    user = User.query.filter_by(email=data['email']).first()
    if user is not None:
        return '', 201
    else:
        user = user_datastore.create_user(email=data['email'], password=data['password'], username=data['username'])
        user_datastore.add_role_to_user(user, user_datastore.find_role('User'))
        db.session.add(user)
        db.session.commit()
        return '', 200


@app.route('/api/user/modify', methods=['POST'])
@login_required
def user_modify():
    if not current_user.has_role('User'):
        return '', 400
    data = request.get_json()
    if not data:
        return '', 400
    if data.get('new_email') and data.get('new_email') is not '':
        x = User.query.filter_by(email=data['new_email']).first()
        if not x or x.email == data['new_email']:
            current_user.email = data['new_email']
        else:
            return '', 202
    if data.get('new_password') and data.get('new_password') is not '':
        current_user.password = data['new_password']
    if data.get('new_username') and data.get('new_username') is not '':
        current_user.username = data['new_username']
    db.session.commit()
    logout_user()
    return '', 201


@app.route('/api/user/query', methods=['GET'])
@login_required
def user_query():
    if not current_user.has_role('User'):
        return '', 400
    borrow = Borrow.query.filter_by(user_id=current_user.id).all()
    re = []
    for i in borrow:
        book = Book.query.filter_by(id=i.book_id).first()
        re.append({'book_id': i.book_id, 'name': book.name, 'start_time': i.start_time, 'end_time': i.end_time})
    return jsonify(re), 201


@app.route('/api/admin/modify', methods=['POST'])
@login_required
def admin_modify():
    if not current_user.has_role('Admin'):
        return '', 400
    data = request.get_json()
    if not data:
        return '', 201
    if data.get('new_email'):
        x = User.query.filter_by(email=data['new_email']).first()
        if not x:
            current_user.email = data['new_email']
        else:
            return '', 201
    if data.get('new_password'):
        current_user.password = data['new_password']
    if data.get('new_username'):
        current_user.username = data['new_username']
    db.session.commit()
    return '', 200


@app.route('/api/admin/search', methods=['POST'])
@login_required
def admin_search():
    if not current_user.has_role('Admin'):
        return '', 400
    data = request.get_json()
    if not data:
        return '', 201
    query_params = {}
    if data.get('username'):
        query_params['username'] = data['username']
    elif data.get('id'):
        query_params['id'] = data['id']
    elif data.get('email'):
        query_params['email'] = data['email']
    user = User.query.filter_by(**query_params).limit(10).all()
    if not user:
        return '', 201
    else:
        re = []
        book = []
        for i in user:
            if i.has_role('User'):
                borrow = Borrow.query.filter_by(user_id=i.id).all()
                for j in borrow:
                    book.append({'book_id': j.book_id, 'start_time': j.start_time, 'end_time': j.end_time})
                re.append({'id': i.id, 'username': i.username, 'email': i.email, 'borrow': book})
        return jsonify(re), 200


@app.route('/api/book/search', methods=['POST'])
@login_required
def book_search():
    data = request.get_json()
    if not data:
        return '', 400
    book = Book.query.filter(or_(Book.id == data['id'], Book.author.like('%' + data['author'] + '%'),
                                 Book.name.like('%' + data['name'] + '%'))).limit(10).all()
    if not book:
        return '', 202
    else:
        if current_user.has_role('User'):
            re = []
            for i in book:
                if i.number > 0:
                    available = True
                else:
                    available = False
                re.append({'id': i.id, 'name': i.name, 'available': available,
                           'max_time': i.max_time, 'author': i.author})
            return jsonify(re), 200
        elif current_user.has_role('Admin'):
            re = []
            for i in book:
                if i.number > 0:
                    available = True
                else:
                    available = False
                re.append({'id': i.id, 'name': i.name, 'available': available,
                           'max_time': i.max_time, 'author': i.author, 'number': i.number,
                           'summary': i.summary})
            return jsonify(re), 201
        else:
            return '', 400


@app.route('/api/book/borrow', methods=['POST'])
@login_required
def book_borrow():
    if not current_user.has_role('User'):
        return '', 400
    data = request.get_json()
    if not data:
        return '', 400
    if data.get('id'):
        book = Book.query.filter_by(id=data['id']).first()
        if not book or book.number <= 0:
            return '', 201
        time = datetime.datetime.now()
        borrow = Borrow(user_id=current_user.id, book_id=book.id,
                        start_time=time, end_time=time+datetime.timedelta(days=book.max_time))
        db.session.add(borrow)
        book.number = book.number-1
        db.session.commit()
        return '', 200
    else:
        return '', 400


@app.route('/api/book/return', methods=['POST'])
@login_required
def book_return():
    if not current_user.has_role('User'):
        return '', 400
    data = request.get_json()
    if data.get('id'):
        book = Book.query.filter_by(id=data['id']).first()
        if not book:
            return '', 201
        borrow = Borrow.query.filter_by(user_id=current_user.id, book_id=book.id).first()
        if not borrow:
            return '', 201
        db.session.delete(borrow)
        book.number = book.number+1
        db.session.commit()
        return '', 200
    else:
        return '', 400


@app.route('/api/book/add', methods=['POST'])
@login_required
def book_add():
    if not current_user.has_role('Admin'):
        return '', 400
    data = request.get_json()
    if data.get('number'):
        summary = int(data['number'])
    else:
        summary = 1
    if data.get('max_time'):
        max_time = int(data['max_time'])
    else:
        max_time = 30
    if data.get('id') and data.get('number'):
        book = Book.query.filter_by(id=data['id']).first()
        book.summary = book.summary + summary
        book.number = book.number + summary
        db.session.commit()
        return '', 200
    elif data.get('name') and data.get('author'):
        book = Book.query.filter(and_(Book.name == data['name'], Book.author == data['author'])).first()
        if book is not None:
            book.summary = book.summary + summary
            book.number = book.number + summary
        else:
            new = Book(name=data['name'], author=data['author'], number=summary,
                       summary=summary, max_time=max_time)
            db.session.add(new)
        db.session.commit()
        return '', 200
    else:
        return '', 201


@app.route('/api/book/remove', methods=['POST'])
@login_required
def book_remove():
    if not current_user.has_role('Admin'):
        return '', 400
    data = request.get_json()
    if data.get('number'):
        number = int(data['number'])
    else:
        number = 1
    if data.get('id'):
        book = Book.query.filter_by(id=data['id']).first()
        if book is not None:
            if book.summary - number > 0:
                book.summary = book.summary-number
            else:
                db.session.remove(book)
            db.session.commit()
            return '', 200
        else:
            return '', 201
    else:
        return '', 201


@app.route('/api/book/modify', methods=['POST'])
@login_required
def book_modify():
    if not current_user.has_role('Admin'):
        return '', 400
    data = request.get_json()
    if data.get('id'):
        book = Book.query.filter_by(id=data['id']).first()
        if not book:
            return '', 201
        else:
            if data.get('summary'):
                book.summary = data['summary']
            if data.get('max_time'):
                book.max_time = data['max_time']
            if data.get('author'):
                book.author = data['author']
            db.session.commit()
            return '', 200
    else:
        return '', 201


app.run(debug=True)
