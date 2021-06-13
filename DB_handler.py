from pymongo import MongoClient
import json
import uuid

class DBModule:
  def __init__(self):
    client = MongoClient('localhost', 27017)
    self.db = client.user_db

  def login(self, id, pwd):
    users = self.db.userInfo.find()
    for user in users:
      if id == user["uid"]:
        if pwd == user["info"]["pwd"]:
          return True
    return False

  def signin_verification(self, uid):
    users = self.db.userInfo.find()
    for user in users:
      if uid == user["uid"]:
        return False
    return True

  def signin(self, _id_, pwd, name, email):
    information = {
      "uid" : _id_,
      "info" : {
        "pwd" : pwd,
        "uname" : name,
        "email" : email
      }
    }
    if not self.signin_verification(_id_):
      return False
    else:
      self.db.userInfo.save(information)
      return True

  def write_post(self, title, contents, uid):
    pid = str(uuid.uuid4())[:10]
    information = {
      "title" : title,
      "contents" : contents,
      "uid" : uid,
      "pid" : pid
    }
    self.db.post.save(information)

  def post_list(self, uid):
    post_lists = self.db.post.find({"uid" : uid})
    return post_lists
  def post_detail(self, uid, pid):
    post = self.db.post.find({"uid" : uid, "pid" : pid})
    return post

  def post_delete(self, pid):
    self.db.post.remove({"pid" : pid})