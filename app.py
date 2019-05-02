import time
from flask import Flask,render_template,flash,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)

###################################数据库连接配置#########################################
app.secret_key="xiaosiqi"
#1、配置数据库的地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dome_xiaosiqi_me:19961218@127.0.0.1/dome_xiaosiqi_me'
# 跟踪数据库的修改
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
########################################书籍管理系统#######################################
# 2、创建数据库对象
book_db=SQLAlchemy(app)
# 3、创建数据库模型
class Author(book_db.Model):# 作者表
    #表名
    __tablename__="authors"
    # 字段
    id=book_db.Column(book_db.Integer,primary_key=True)
    name=book_db.Column(book_db.String(16),unique=True)

    # 关系引用
    #books 是给自己用的，author是给book模型用的
    books=book_db.relationship("Book",backref="author")
class Book(book_db.Model):# 书籍表
    __tablename__ = "books"
    # 字段
    id = book_db.Column(book_db.Integer, primary_key=True)
    name = book_db.Column(book_db.String(16), unique=True)
    author_id=book_db.Column(book_db.Integer,book_db.ForeignKey("authors.id"))

    # wpf表单类
class AuthorForm(FlaskForm):
    author = StringField("作者", validators=[DataRequired()])
    book = StringField("书籍", validators=[DataRequired()])
    submit = SubmitField("提交")
@app.route('/book',methods=["POST","GET"])
def book():
    book_db.create_all()  # 创建表
    author_form = AuthorForm()  # 实例化表单类
    if request.method=="POST":
        if author_form.validate_on_submit():
            author_name=author_form.author.data #获取表单作者名字
            book_name=author_form.book.data#获取表单书籍名字
            author=Author.query.filter_by(name=author_name).first() #查找作者表，查询作者是否存在
            if author:
                pass #作者存在
            else:#作者不存在
                try:
                    author=Author(name=author_name)
                    book_db.session.add(author)
                    book_db.session.commit()
                except Exception as e:
                    print(e)
                    flash("添加作者失败")
                    book_db.session.rollback()  # 数据库回滚
            book = Book.query.filter_by(name=book_name).first()  # 查找书籍表，查询书籍是否存在
            if book:#书籍存在
                flash("已存在同名书籍")
            else:   #书籍不存在
                try:
                    new_book=Book(name=book_name,author_id=author.id)
                    book_db.session.add(new_book)
                    book_db.session.commit()
                except Exception as e:
                    print(e)
                    flash("添加书籍失败")
                    book_db.session.rollback()# 数据库回滚
        else:
            flash("参数不全")

    authors=Author.query.all()
    return render_template("books.html" ,authors=authors,form=author_form)
# 删除书籍
@app.route("/book/del_book/<int:book_id>")
def del_book(book_id):
    # 查询数据库，是否有该ID
    book=Book.query.get(book_id)
    if book:#有该ID,就删除
        book_db.session.delete(book)
        book_db.session.commit()
    else:
        flash("书籍找不到，也许已经被删除")
    # redirect:重定向，需要传入一个网址或路由地址
    # url_for:传入视图函数，返回该视图函数对应的路由地址
    return redirect(url_for("book"))

# 删除作者，删除作者时应该删除它名下的所有书籍
@app.route("/book/del_author/<int:author_id>")
def del_author(author_id):
    # 查询数据库，是否有该ID
    author = Author.query.get(author_id)
    if author:  # 有该ID,就删除
        Book.query.filter_by(author_id=author_id).delete()# 删除该作者名下的书籍
        book_db.session.delete(author)#删除该作者
        book_db.session.commit() #提交修改
    else:
        flash("找不到这个作者，也许已经被删除")
    # redirect:重定向，需要传入一个网址或路由地址
    #url_for:传入视图函数，返回该视图函数对应的路由地址
    return redirect(url_for("book"))


##################################BBS 留言板系统###########################################
# 创建数据库对象
bbs_db=SQLAlchemy(app)
# 创建数据模型
class BBSitem(bbs_db.Model):
    __tablename__ = "bbs_item"
    id = bbs_db.Column(bbs_db.Integer, primary_key=True)
    theme=bbs_db.Column(bbs_db.String(16))
    message = bbs_db.Column(bbs_db.Text)
    upvote=bbs_db.Column(bbs_db.Integer,default=0)
    downvote=bbs_db.Column(bbs_db.Integer,default=0)
    nowtime=bbs_db.Column(bbs_db.DATETIME)
# bbs 主界面逻辑
@app.route("/bbs" ,methods=["POST","GET"])
def bbs():
    bbs_db.create_all()
    bbs_items = BBSitem.query.all()

    if request.method == "POST":
        theme = request.form.get("theme")
        message = request.form.get("message")
        if not all([theme,message]):
            flash("没有填写完整")
        else:
            nowtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            bbs_item=BBSitem(theme=theme,message=message,nowtime=nowtime)
            bbs_db.session.add(bbs_item)
            bbs_db.session.commit()
            return redirect(url_for("bbs"))
    return render_template("bbs.html",bbs_items=bbs_items)

# 点赞
@app.route("/bbs/upvote/<int:bbsitem_id>")
def bbs_upvote(bbsitem_id):
    # 查询数据库，是否有该ID
    bbsitem = BBSitem.query.get(bbsitem_id)
    if bbsitem:  # 有该ID
        bbsitem.upvote+=1
        bbs_db.session.commit()
    else:
        pass
    # redirect:重定向，需要传入一个网址或路由地址
    # url_for:传入视图函数，返回该视图函数对应的路由地址
    return redirect(url_for("bbs"))
# 点踩
@app.route("/bbs/downvote",methods=["POST"])
def bbs_downvote():
    if request.method == "POST":
        bbsitem_id = request.form.get("id")
        bbsitem = BBSitem.query.get(bbsitem_id)
        if bbsitem:  # 有该ID
            bbsitem.downvote += 1
            bbs_db.session.commit()
        else:
            pass
    # 查询数据库，是否有该ID
    # redirect:重定向，需要传入一个网址或路由地址
    # url_for:传入视图函数，返回该视图函数对应的路由地址
    return redirect(url_for("bbs"))
# 删除留言
@app.route("/bbs/delitem/<int:bbsitem_id>")
def bbs_delitem(bbsitem_id):
    print(bbsitem_id)
    # 查询数据库，是否有该ID
    bbsitem = BBSitem.query.get(bbsitem_id)
    print(bbsitem.message)
    if bbsitem:  # 有该ID,就删除
        bbs_db.session.delete(bbsitem)
        bbs_db.session.commit()
    else:
        pass
    # redirect:重定向，需要传入一个网址或路由地址
    # url_for:传入视图函数，返回该视图函数对应的路由地址
    return redirect(url_for("bbs"))

#目录界面
@app.route("/")
def index():
    links={"book":"书籍管理系统","bbs":"留言板系统"}
    return render_template("index.html",links=links)

if __name__ == '__main__':
    app.run()
