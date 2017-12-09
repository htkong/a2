from marshmallow_sqlalchemy import ModelSchema
from . import db
import constants


class Base(db.Model):
  """
  Base database model
  """
  __abstract__ = True
  created_at = db.Column(db.DateTime, default = db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, default = db.func.current_timestamp())

    
class Boards(Base):
  __tablename__ = 'boards'
  
  
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(280), nullable=False)
  board_elements = db.relationship("Elements",uselist = True)
  todo_count = db.Column(db.Integer,default = 0)
  inprogress_count = db.Column(db.Integer,default = 0)
  done_count = db.Column(db.Integer,default = 0)

  def to_dict(self):
       return {t.name: getattr(self, t.name) for t in self.__table__.columns}

  def __init__(self, title):
    self.title = title
    board_elements = list()
  
  def __repr__(self):
        return "<boards(id='%i', title='%s')>" % (                              self.id, self.title)
  


class Elements(Base):
  __tablename__ = 'elements'
  
  id = db.Column(db.Integer, primary_key=True)
  board_id = db.Column(db.Integer, db.ForeignKey('boards.id'), nullable=False)
  category = db.Column(db.String(280), nullable=False)    
  description = db.Column(db.Text, nullable=False)
  

  def __init__(self, board_id, category, description):
    self.board_id = int(board_id)
    self.description = description
    self.category = category
   
  def to_dict(self):
       return {t.name: getattr(self, t.name) for t in self.__table__.columns}
    
    
db.create_all()
db.session.commit()