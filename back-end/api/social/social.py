
from flask import Flask,jsonify,request
from flask_cors import CORS 
from flask_sqlalchemy import SQLAlchemy, model

import datetime
from flask_marshmallow import Marshmallow

from marshmallow import fields

app = Flask(__name__)
CORS(app, support_credentials=True)



#todo set login user
SessionUserId = 1
PWD='1'
USR='root';


app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://{}:{}@localhost:3306/social_media'.format(USR, PWD)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Users(db.Model):
    Id = db.Column(db.Integer,primary_key = True)
    UserName = db.Column(db.String(45))
    Password = db.Column(db.String(45))
    Name = db.Column(db.String(45))
    Surname = db.Column(db.String(45))
    PhoneNumber = db.Column(db.String(13))
    EmailAddress = db.Column(db.String(45))
    Country = db.Column(db.String(45))
    City = db.Column(db.String(45))
    BirthDate = db.Column(db.DateTime,default = datetime.datetime.now)
    CreatedOn = db.Column(db.DateTime,default = datetime.datetime.now)

    def __init__(self,userName,password,name,surname,phoneNumber,emailAdress,country,city,birthDate,createdOn):
        self.UserName = userName
        self.Password = password
        self.Name = name
        self.Surname = surname
        self.PhoneNumber = phoneNumber
        self.EmailAddress = emailAdress
        self.Country = country
        self.City = city
        self.BirthDate = birthDate
        self.CreatedOn = createdOn

    
class ChatGroup(db.Model):
    Id = db.Column(db.Integer,primary_key = True)
    Name = db.Column(db.String(40))
    Description = db.Column(db.String(1000))
    CreatedOn = db.Column(db.DateTime,default = datetime.datetime.now)

class Comments(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    postId = db.Column(db.Integer, db.ForeignKey('Posts.id'))
    userId = db.Column(db.Integer,db.ForeignKey('Users.id'))
    repliedCommentId = db.Column(db.Integer,db.ForeignKey('Comments.id'))
    text = db.Column(db.String(1000))
    createdOn = db.Column(db.DateTime,default = datetime.datetime.now)
    def __init__(self,userId,postId,repliedCommentId,text,createdOn):
        self.userId = userId
        self.postId = postId
        self.repliedCommentId = repliedCommentId
        self.text = text
        self.createdOn = createdOn


class Followers(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    userId = db.Column(db.Integer,db.ForeignKey('Users.id'))
    followedUserId = db.Column(db.Integer,db.ForeignKey('Users.id'))
    def __init__(self,userId,followedUserId):
        self.userId = userId
        self.followedUserId = followedUserId
    
class Likes(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    userId = db.Column(db.Integer,db.ForeignKey('Users.id'))
    postId = db.Column(db.Integer,db.ForeignKey('Posts.id'))
    type = db.Column(db.Integer)
    def __init__(self,userId,postId,type):
        self.userId = userId
        self.postId = postId
        self.type = type

class Message(db.Model):
    Id = db.Column(db.Integer,primary_key = True)
    ChatGroupId = db.Column(db.Integer,db.ForeignKey('ChatGroup.id'))
    UserId = db.Column(db.Integer,db.ForeignKey('Users.id'))
    RepliedMessageId = db.Column(db.Integer,db.ForeignKey('Message.id'))
    Text = db.Column(db.String(1000))
    CreatedOn = db.Column(db.DateTime,default = datetime.datetime.now)

class Posts(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    userId = db.Column(db.Integer,db.ForeignKey('Users.id'))
    content = db.Column(db.String(1000))
    createdOn = db.Column(db.DateTime,default = datetime.datetime.now)
    
    def __init__(self,userId,content):
        self.userId = userId
        self.content = content

class UserChatGroup(db.Model):
    Id = db.Column(db.Integer,primary_key = True)
    UserId = db.Column(db.Integer,db.ForeignKey('Users.id'))
    ChatGroupIdId = db.Column(db.Integer,db.ForeignKey('ChatGroup.id'))
    Role = db.Column(db.Integer)
    CreatedOn = db.Column(db.DateTime,default = datetime.datetime.now)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('Id','UserName','Password','Name','Surname','PhoneNumber','EmailAddress','Country','City','BirthDate','CreatedOn')

class PostSchema (ma.Schema):
    class Meta:
        fields = ('id','userId','content','createdOn')


class PostDaoSchema (ma.Schema):
    class Meta:
        fields = ('id','userId','UserName','likeCount','unlikeCount','content','createdOn')

class FollowSchema (ma.Schema):
    class Meta:
        fields = ('id','userId','followedUserId')

class LikeSchema (ma.Schema):
    class Meta:
        fields = ('id','userId','postId','type')

class CommentSchema (ma.Schema):
    class Meta:
        fields = ('id','postId','userId','repliedCommentId','text','createdOn')






user_schema = UserSchema(many = True)
post_schema = PostSchema(many = True)
postdao_schema = PostDaoSchema(many = True)
follower_schema = FollowSchema(many = True)
likes_schema = LikeSchema(many = True)
comments_schema = CommentSchema(many = True)



@app.route('/get_posts',methods = ['GET'])
def get_posts():
    all_posts = Posts.query.all()

    results = post_schema.dump(all_posts)
    return jsonify(results)

# followed users posts
@app.route('/get_followed_posts',methods = ['GET'])
def get_followed_posts():
    #ids = [id[0] for id in Followers.query.filter_by(userId = 2).with_entities(Followers.followedUserId).all()]

    FollowedUsers = [id[0] for id in Followers.query.filter_by(userId = SessionUserId).with_entities(Followers.followedUserId).all()]
    all_posts = Posts.query.filter(Posts.userId.in_(FollowedUsers)).all()
    results = post_schema.dump(all_posts)
    return jsonify(results)
 


@app.route('/add_post',methods = ['POST'])
def add_post():
    userId = request.json['userId']
    content = request.json['content']
    
    ppost = Posts(userId,content)
    
    db.session.add(ppost)
    db.session.commit()
    
    return ppost.content

@app.route('/like_post',methods = ['POST'])
def like_post():
    userId = request.json['userId']
    postId = request.json['postId']
    type = request.json['type']
    
    like = Likes(userId,postId,type)
    
    db.session.add(like)
    db.session.commit()
    
    return str(like.type)

@app.route('/add_comment',methods = ['POST'])
def add_comment():
    userId = request.json['userId']
    postId = request.json['postId']
    repliedCommentId = request.json['repliedCommentId']
    text = request.json['text']
    createdOn = request.json['createdOn']
    
    comment = Comments(userId,postId,repliedCommentId,text,createdOn)
    
    db.session.add(comment)
    db.session.commit()
    
    return str(comment.text)

@app.route('/get_post_comments/<postId>',methods = ['GET'])
def get_post_comments(postId):
    #unfollowedUser = Followers.query.filter((Followers.userId == SessionUserId)&(Followers.followedUserId == f_user)).first()
    all_comments = Comments.query.filter((Comments.postId == postId)& (Comments.repliedCommentId == None)).all()
    results = comments_schema.dump(all_comments)
    return jsonify(results)


@app.route('/get_comment_comments/<postId>',methods = ['GET'])
def get_comment_comments(repliedId):

    all_comments = Comments.query.filter( (Comments.repliedCommentId == repliedId)).all()
    results = comments_schema.dump(all_comments)
    return jsonify(results)



@app.route('/get_post_like/<postId>/<type>',methods = ['GET'])
def get_post_like(postId,type):
    likeCount = Likes.query.filter((Likes.postId == postId)& (Likes.type == type)).count()
    
    return str(likeCount)



@app.route('/get_users',methods = ['GET'])
def get_users():
    all_users = Users.query.all()
    results = user_schema.dump(all_users)
    return jsonify(results)

@app.route('/get_users/<id>/', methods = ['GET'])
def post_details(id):
    u = Users.query.get(id)
    return user_schema.jsonify(u)


@app.route('/add_user',methods = ['POST'])
def add_user():
    userName = request.json['UserName']
    password = request.json['Password']
    name = request.json['Name']
    surname = request.json['Surname']
    phoneNumber = request.json['PhoneNumber']
    emailAddress = request.json['EmailAddress']
    country = request.json['Country']
    city = request.json['City']
    birthDate = request.json['BirthDate']
    createdOn =request.json['CreatedOn']

    users =Users(userName,password,name,surname,phoneNumber,emailAddress,country,city,birthDate,createdOn)
    db.session.add(users)
    db.session.commit()
    return str(users.UserName)

@app.route('/get_followers',methods = ['GET'])
def get_followers():
    all_followers = Followers.query.all()
    results = follower_schema.dump(all_followers)
    return jsonify(results)
    #return jsonify({'results':'resd'})
 
@app.route('/add_follow',methods = ['POST'])
def add_follow():
    userId = request.json['userId']
    followedUserId = request.json['followedUserId']
    
    follow = Followers(userId,followedUserId)
    
    db.session.add(follow)
    db.session.commit()
    
    return str(follow.followedUserId)
@app.route('/unfollow/<f_user>/', methods = ['DELETE'])
def unfollow(f_user):

    unfollowedUser = Followers.query.filter((Followers.userId == SessionUserId)&(Followers.followedUserId == f_user)).first()
    print(unfollowedUser)
    db.session.delete(unfollowedUser)
    db.session.commit()


if __name__ == "__main__":
    app.run(debug = True) 