from flask import Flask, render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from constants import *
import os
from flask import request
import constants


# Configure Flask app
app = Flask(__name__, static_url_path='/static')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Database
db = SQLAlchemy(app)

# Import + Register Blueprints
# Workflow is as follows:
#from app.blue import blue as blue
#app.register_blueprint(blue)

# Default functionality of rendering index.html
def render_page():
  return render_template('index.html')



# React Catch All Paths
@app.route('/', methods=['GET'])
def index():
  return render_page()

@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
  return render_page()

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404

@app.route('/kanban/boards', methods=['POST'])
def createBoard():
  data = base.Boards(request.args['title'])
  db.session.add(data)
  db.session.commit()
  
  
  board = data.to_dict()
  board["board_elements"] = data.board_elements
  dic = dict()
  boards = dict()
  boards["board"] = board
  dic["success"] = True  
  dic["data"] = boards
  
  return jsonify(dic)

@app.route('/kanban/boards', methods=['DELETE'])
def deleteBoard():
  target = base.Boards.query.get(request.args['id'])
  db.session.delete(target)
  db.session.commit()
  return jsonify({"success":True})




@app.route('/kanban/board_elements', methods=['POST'])
def createElement():
    
    board_id = request.args['board_id']
    description = request.args['description']
    category = request.args['category']
    newData = base.Elements(board_id, category, description)
    board = base.Boards.query.get(board_id)
    board.update_at = db.func.current_timestamp()
    if category == T:
      board.todo_count += 1
    if category == I:
      board.inprogress_count += 1
    if category == D:  
      board.done_count += 1
    db.session.add(newData)
    db.session.commit()
    
    dic = dict()
    elements = dict()
    elements["board_element"] = newData.to_dict()
    dic["success"] = True  
    dic["data"] = elements
    
    
    return jsonify(dic)

@app.route('/kanban/board_elements', methods=['DELETE'])
def deleteBoardElements():
  
  
    target=base.Elements.query.get(request.args['board_element_id'])
    board = base.Boards.query.get(target.board_id)
    category = target.category
    
    if category == T:
      board.todo_count -= 1
    if category == I:
      board.inprogress_count -= 1
    if category == D:  
      board.done_count -= 1
    board.update_at = db.func.current_timestamp()
    db.session.delete(target)
    db.session.commit()
    return jsonify({"success":True})

@app.route('/kanban/boards', methods=['GET'])
def getBoards():
  data = base.Boards.query.all()
  dataDict = [item.to_dict() for item in data]
  dic = dict()
  boards = dict()
  boards["boards"] = dataDict
  dic["success"] = True  
  dic["data"] = boards
  return jsonify(dic)

@app.route('/kanban/boards/<board_id>', methods=['GET'])
def getBoard(board_id):
  board = base.Boards.query.get(board_id)

  dataDict = board.to_dict()
  listT = base.Elements.query.filter_by(board_id = board.id, category = T).all()
  dataDict[T] = [item.to_dict() for item in listT]
  listI = base.Elements.query.filter_by(board_id = board.id, category = I).all()
  dataDict[I] = [item.to_dict() for item in listI]
  listD = base.Elements.query.filter_by(board_id = board.id, category = D).all()
  dataDict[D] = [item.to_dict() for item in listD]
  dic = dict()
  boards = dict()
  boards["board"] = dataDict
  dic["success"] = True  
  dic["data"] = boards
  return jsonify(dic)

@app.route('/kanban/board_elements/advance', methods=['POST'])
def advanceElement():
  changed = False
  target = base.Elements.query.get(request.args['id'])
  board = base.Boards.query.get(target.board_id)
  category = target.category
  
  if category == T:
    target.category = I
    board.todo_count -= 1
    board.inprogress_count += 1
    changed = True
  elif category == I:
    target.category = D
    board.inprogress_count -= 1
    board.done_count += 1
    changed = True
  
  if changed :
    board.update_at = db.func.current_timestamp()    
    db.session.commit()
  return jsonify({"success": changed})
