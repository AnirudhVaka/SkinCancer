import os
import image
import numpy as np
import pandas as pd
import tensorflow as tf
from flask import request, Flask, send_from_directory, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import mysql
import mysql.connector

mydb = mysql.connector.connect(host='localhost', user='root', password='root', port='3306', database='skin')
app = Flask(__name__)
app.secret_key = 'random string'

classes = ['Benign:', 'Malignant:']


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM skin WHERE Email=%s and Password=%s"
        val = (email, password)
        cur = mydb.cursor()
        cur.execute(sql, val)
        results = cur.fetchall()
        mydb.commit()
        if len(results) >= 1:
            return render_template('loginhomepage.html', msg='success')
        else:
            return render_template('login.html', msg='fail')
    return render_template('login.html')


@app.route("/Register", methods=['GET', 'POST'])
def Register():
    if request.method == "POST":
        print('entered')
        name = request.form['name']
        email = request.form['email']
        psw = request.form['psw']
        cpsw = request.form['cpsw']

        if psw == cpsw:
            sql = 'SELECT * FROM skin'
            cur = mydb.cursor()
            cur.execute(sql)
            all_emails = cur.fetchall()
            mydb.commit()
            all_emails = [i[2] for i in all_emails]
            if email in all_emails:
                return render_template('Register.html', msg='exists')
            else:
                sql = 'INSERT INTO skin(Email,Password) values(%s,%s)'
                cur = mydb.cursor()
                values = (email, psw)
                cur.execute(sql, values)
                mydb.commit()
                cur.close()
                return render_template('Register.html', msg='Success')
        else:
            return render_template('Register.html', msg='Mismatch')
    return render_template('Register.html')


@app.route("/loginhomepage")
def loginhomepage():
    return render_template('loginhomepage.html')


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':

        m = int(request.form["alg"])
        myfile = request.files['file']
        acc = pd.read_csv("skin1.csv")
        fn = myfile.filename
        mypath = os.path.join("images/", fn)
        myfile.save(mypath)

        print("{} is the file name", fn)
        print("Accept incoming file:", fn)
        print("Save it to:", mypath)

        if m == 1:
            print("bv1")
            new_model = load_model(r'models\DenseNet201.h5')
            test_image = image.load_img(mypath, target_size=(128, 128))
            # test_image = image.img_to_array(test_image)
            a = acc.iloc[m - 1, 1]

        elif m == 2:
            print("bv2")
            new_model = load_model(r'models\ResNet101.h5')
            test_image = image.load_img(mypath, target_size=(128, 128))
            test_image = image.img_to_array(test_image)
            a = acc.iloc[m - 1, 1]

        elif m == 3:
            print("bv3")
            new_model = load_model(r'models\vgg16.h5')
            test_image = image.load_img(mypath, target_size=(128, 128))
            test_image = image.img_to_array(test_image)
            a = acc.iloc[m - 1, 1]

        elif m == 4:
            print("bv3")
            new_model = load_model(r'models\MobileNetv2.h5')
            test_image = image.load_img(mypath, target_size=(128, 128))
            test_image = image.img_to_array(test_image)
            a = acc.iloc[m - 1, 1]

        elif m == 5:
            print("bv3")
            new_model = load_model(r'models\DCNN.h5')
            test_image = image.load_img(mypath, target_size=(256, 256))
            test_image = image.img_to_array(test_image)
            a = acc.iloc[m - 1, 1]

        else:
            print("bv3")
            new_model = load_model(r'models\AlexNet.h5')
            test_image = image.load_img(mypath, target_size=(256, 256))
            test_image = image.img_to_array(test_image)
            a = acc.iloc[m - 1, 1]

        test_image = np.expand_dims(test_image, axis=0)
        result = new_model.predict(test_image)
        preds = classes[np.argmax(result)]

        return render_template("templates.html", text=preds, image_name=fn, a=a)
    return render_template("upload.html")


if __name__ == '__main__':
    app.run(debug=True)
