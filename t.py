from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:make5211314@127.0.0.1:3306/store_manage"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

class Roles(db.Model):
    __tablename__ = 'roles'
    role = db.Column(db.String(30))
    account = db.Column(db.String(30), primary_key=True, nullable=False)
    password = db.Column(db.String(30), nullable=False, default='123')
    phone = db.Column(db.String(11))
    state = db.Column(db.Integer, default=0)



@app.route('/login', methods=['POST'])
def login():
    account = request.json['account']
    password = request.json['password']
    role = Roles.query.filter(Roles.account == account).first()
    state = 0 if role is None or role.password != password else 1
    return jsonify({'state': state})


@app.route('/users', methods=['GET', 'POST'])
def users():
    search_content = request.args['search_content']
    print(search_content)
    if search_content == '':
        roles = Roles.query.all()
    else:
        roles = Roles.query.filter(or_(Roles.role == search_content, Roles.account == search_content)).all()
    lst = []
    for i, role in enumerate(roles):
        lst.append({'role': role.role, 'account': role.account, 'password': role.password, 'phone': role.phone, 'state': bool(role.state)})
    return jsonify({'users': lst})

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    account = data['account']
    roles = Roles.query.filter(Roles.account == account).all()
    ret = True if len(roles) != 0 else False
    if ret:
        info = '用户名存在!'
    else:
        role = Roles(role=data['role'], account=data['account'], password=data['password'], phone=data['phone'], state=1)
        db.session.add(role)
        db.session.commit()
        info = '注册成功!'
    return jsonify({'ret': info})


@app.route('/change_state', methods=['POST'])
def change_state():
    data = request.json
    account = data['account']
    state = int(data['state'])
    Roles.query.filter(Roles.account == account).update({'state': state})
    db.session.commit()
    return jsonify({'ret': '修改成功'})



@app.route('/change_info', methods=['POST'])
def change_info():
    data = request.json
    account = data['account']
    target_info = {}
    for key, values in data.items():
        target_info[key] = values
    Roles.query.filter(Roles.account == account).update(target_info)
    db.session.commit()
    return jsonify({'ret': '修改成功!'})


@app.route('/delete_user', methods=['POST'])
def delete_user():
    account = request.json['account']
    Roles.query.filter(Roles.account == account).delete()
    db.session.commit()
    return jsonify({'ret': '删除成功!'})



@app.route('/', methods=['GET'])
def page():
    return "<h1>hello service</h1>"
@app.route('/hello', methods=['GET'])
def hello():
    s = r"https://github.com/cockmake?tab=repositories"
    return "<h1>hello i am make</h1>" + "<br>" + f"<h2><a href={s}>Welcome come to my Github</a></h2>"
@app.route('/home', methods=['GET'])
def home():
    return '<button style="width: 200px; height: 200px; margin: 0 auto;">我是按钮</button>'

if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
    app.run(host='0.0.0.0', port=7230)

