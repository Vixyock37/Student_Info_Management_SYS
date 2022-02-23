# -*- coding: utf-8 -*-
import base64
import os
import shutil
from io import BytesIO

import numpy as np
from flask import Flask, render_template, request, url_for, redirect, session,flash
from verificationCode import *
from dbSqlite3 import *
import re


app = Flask(__name__)

app.secret_key = 'abcdefgh!@#$%'


def CheckLogin():
    if 'username' not in session:
        return False
    else:
        return True

code = ''
@app.route('/login', methods=['POST', 'GET'])
def login():
    global code
    if request.method=="GET":
        image, code = image_code()
        print(code)
        new_img = image.convert("RGB")
        img_byte = BytesIO()
        new_img.save(img_byte, format='PNG')  # format: PNG or JPEG
        binary_content = img_byte.getvalue()
        img_stream = base64.b64encode(binary_content).decode()
        return render_template('login.html', img_stream=img_stream)
    result, _ = GetSql2("select * from users where username='%s'" % request.form['username'])
    username = request.form['username']
    pwd = request.form['pwd']
    #print (result)
    #若登陆成功，重定向至第1页
    if len(result) > 0 and result[0][1] == request.form['pwd'] and request.form['code'] == code:
        session["username"] = request.form['username']
        print(request.form['code'])
        return redirect(url_for('page_to',pageid=1))
    #否则，继续登录
    if len(result) > 0 and result[0][1] == request.form['pwd'] and request.form['code'] != code:
        image, code = image_code()
        print(code)
        new_img = image.convert("RGB")
        img_byte = BytesIO()
        new_img.save(img_byte, format='PNG')  # format: PNG or JPEG
        binary_content = img_byte.getvalue()
        img_stream = base64.b64encode(binary_content).decode()
        flash("验证码错误！")
        return render_template('login.html', img_stream=img_stream,pwd='',username=username)
    else:
        image, code = image_code()
        print(code)
        new_img = image.convert("RGB")
        img_byte = BytesIO()
        new_img.save(img_byte, format='PNG')  # format: PNG or JPEG
        binary_content = img_byte.getvalue()
        img_stream = base64.b64encode(binary_content).decode()
        flash("用户名或密码错误！")
        return render_template('login.html', img_stream=img_stream, pwd='', username=username)
        #return redirect(url_for('login'))
        #return render_template('login.html',image=src)


@app.route('/', methods=['GET'])
def index():
    if not CheckLogin():
        return redirect(url_for('login'))
    else:
        return redirect(url_for('page_to', pageid=1))


@app.route('/page/<int:pageid>', methods=['GET'])
def page_to(pageid):
    if not CheckLogin():
        return redirect(url_for('login'))
    strWhere = []
    schfilter = "?name="  # 过滤器，用来在切换页面的时候保持GET请求参数
    if "name" in request.args:
        name = request.args["name"]
        if name != "":
            strWhere.append("stu_name like '%%%s%%'" % name)
            schfilter += name
    schfilter + "&stuno="
    if "stuno" in request.args:
        stuno = request.args["stuno"]
        if stuno != "":
            strWhere.append("stu_id = '%s'" % stuno)
            schfilter += stuno

    tablename = "student_info"
    sql = "SELECT stu_id 学号,stu_name 姓名,stu_sex 性别,stu_age 年龄,stu_origin 户籍,p.stu_profession 专业 FROM student_info s INNER JOIN stu_profession p " \
          "on s.stu_profession_id=p.stu_profession_id"

    if len(strWhere) > 0:
        sql = sql + " where " + " and ".join(strWhere)
        print(sql)

    result, fields = GetSql2(sql)

    n_per_page = 20  # 每页显示的条数
    total_page = int(len(result) / n_per_page + 0.99)
    print(total_page)

    return render_template('show.html', datas=result[(pageid-1)*n_per_page:(pageid)*n_per_page],
                           fields=fields, pageid=pageid, total_page=total_page, schfilter=schfilter)


@app.route('/search', methods=['GET', 'post'])
def search():
    return render_template('search.html')


@app.route('/add', methods=['GET', 'post'])
def add():
    if not CheckLogin():
        return redirect(url_for('login'))

    if request.method == "GET":
        datas, _ = GetSql2("select * from stu_profession")
        stu_ids, _ = GetSql2("select stu_id from student_info")
        stu_ids = np.array(stu_ids).reshape((len(stu_ids)))
        return render_template('add.html', datas=datas,stu_ids=stu_ids)
        # return render_template('add.html')

    else:
        data = dict(
            stu_id=request.form['stu_id'],
            stu_name=request.form['stu_name'],
            stu_sex=request.form['stu_sex'],
            stu_age=request.form['stu_age'],
            stu_origin=request.form['stu_origin'],
            stu_profession_id=request.form['stu_profession']
        )

        res, check_info = dataAddCheck(data)
        if res:
            InsertData(data, "student_info")
            flash("添加成功！")
            return redirect(url_for("index"))
        else:
            flash("请通过合法途径访问网站！")
            return redirect(url_for("index"))


@app.route('/del/<id>', methods=['GET'])
def delete(id):
    if not CheckLogin():
        return redirect(url_for('login'))
    DelDataById("stu_id", id, "student_info")
    flash("删除成功！")
    return redirect(url_for("index"))


@app.route('/page/update', methods=['GET', 'post'])
def update():
    if not CheckLogin():
        return redirect(url_for('login'))
    if request.method == "GET":
        id = request.args['id']
        result, _ = GetSql2("select * from student_info where stu_id='%s'" % id)
        print(result[0])
        print(type(result[0]))
        # for p in pro:
        #     print(p)+
        pro, _ = GetSql2("select * from  stu_profession")
        return render_template('update.html', data=result[0], pro=pro)
    else:

        data = dict(
            stu_id=request.form['stu_id'],
            stu_name=request.form['stu_name'],
            stu_sex=request.form['stu_sex'],
            stu_age=request.form['stu_age'],
            stu_origin=request.form['stu_origin'],
            stu_profession_id=request.form['stu_profession']
        )
        res, check_info = dataUpdateCheck(data)
        if res:
            UpdateData(data, "student_info")
            flash("修改成功！")
            # time.sleep(3)
            return redirect(url_for("index"))
        else:
            flash("请通过合法途径访问页面！")
            return redirect(url_for("index"))


@app.route('/delete_students', methods=['GET', 'post'])
def delete_students():
    if not CheckLogin():
        return redirect(url_for('login'))
    ids = request.values.getlist('array')
    # print(ids)
    if len(ids)==0:
        flash("未选中任何学生信息！")
    for id in ids:
        DelDataById('stu_id', id, 'student_info')
    flash("批量删除成功！")
    return redirect(url_for('page_to', pageid=1))

def idAddCheck(stu_id):
    if not re.match("^[0-9]{9}$", stu_id):
        return False
    stu_ids, _ = GetSql2("select stu_id from student_info")
    stu_ids = np.array(stu_ids).reshape((len(stu_ids)))
    return stu_id not in stu_ids


def idUpdateCheck(stu_id):
    stu_ids, _ = GetSql2("select stu_id from student_info")
    stu_ids = np.array(stu_ids).reshape((len(stu_ids)))
    return stu_id in stu_ids


def nameCheck(stu_name):
    return not stu_name == ""


def sexCheck(stu_sex):
    return stu_sex == "男" or stu_sex == "女"


def ageCheck(stu_age):
    return 1 <= stu_age <= 100


def originCheck(stu_origin):
    return not stu_origin == ""


def professionCheck(stu_profession_id):
    profession_id, titles = GetSql2("select stu_profession_id from stu_profession")
    profession_id = np.array(profession_id).reshape((len(profession_id)))
    # print(profession_id)
    return stu_profession_id in profession_id


def dataAddCheck(data):
    stu_id = data['stu_id']
    stu_name = data['stu_name'].strip()
    stu_sex = data['stu_sex']
    stu_age = int(data['stu_age'])
    stu_origin = data['stu_origin'].strip()
    stu_profession_id = int(data['stu_profession_id'])

    if not idAddCheck(stu_id):
        return False, "学号必须为9位纯数字且不能已存在！"
    if not nameCheck(stu_name):
        return False, "学生姓名不能为空！"
    if not sexCheck(stu_sex):
        return False, "性别只能为男或女！"
    if not ageCheck(stu_age):
        return False, "年龄范围为1-100！"
    if not originCheck(stu_origin):
        return False, "籍贯不能为空！"
    if not professionCheck(stu_profession_id):
        return False, "不存在该专业！"

    return True, "数据合法！"


def dataUpdateCheck(data):
    stu_id = data['stu_id']
    stu_name = data['stu_name'].strip()
    stu_sex = data['stu_sex']
    stu_age = int(data['stu_age'])
    stu_origin = data['stu_origin'].strip()
    stu_profession_id = int(data['stu_profession_id'])

    if not idUpdateCheck(stu_id):
        return False, "不存在该学生！"
    if not nameCheck(stu_name):
        return False, "学生姓名不能为空！"
    if not sexCheck(stu_sex):
        return False, "性别只能为男或女！"
    if not ageCheck(stu_age):
        return False, "年龄范围为1-100！"
    if not originCheck(stu_origin):
        return False, "籍贯不能为空！"
    if not professionCheck(stu_profession_id):
        return False, "不存在该专业！"

    return True, "数据合法！"

if __name__ == '__main__':
    # app.run("0.0.0.0",debug=True)
    app.run(debug=True,port=5005)
    # app.run()
