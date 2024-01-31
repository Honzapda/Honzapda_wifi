import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mysql.connector
from honzapda_admin import admin_main
import bcrypt
from decouple import config

def authenticate():
    # MySQL 데이터베이스 연결 설정
    cnx = mysql.connector.connect(
        host=config('MYSQL_HOST'),  # your MySQL server host
        user=config('MYSQL_DB_USER'),  # your MySQL username
        password=config('MYSQL_DB_PASSWORD'),  # your MySQL password
        database=config('MYSQL_DB_NAME')  # your MySQL database
    )

    cursor = cnx.cursor(buffered=True, dictionary=True)

    query = "SELECT * FROM shop WHERE login_id = %s"
    cursor.execute(query, (user_var.text(),))

    if cursor.rowcount:
        result = cursor.fetchone()  
        password = pass_var.text().encode('utf-8')  
        hashed_password = result['password'].replace('{bcrypt}', '').encode('utf-8')
        if bcrypt.checkpw(password, hashed_password):  
            QMessageBox.information(None, "Login info", "Login Successful")
            root.close()
            admin_main(result['id'])
        else:
            QMessageBox.information(None, "Login info", "Login Failed")
    else:
        QMessageBox.information(None, "Login info", "Login Failed")

    cursor.close()
    cnx.close()
    
app = QApplication(sys.argv)


root = QMainWindow()
root.setWindowTitle("honzapda_admin")

user_label = QLabel(root)
user_label.setText("User Name")
user_label.move(50, 50)

user_var = QLineEdit(root)
user_var.move(150, 50)

pass_label = QLabel(root)
pass_label.setText("Password")
pass_label.move(50, 100)

pass_var = QLineEdit(root)
pass_var.setEchoMode(QLineEdit.Password)
pass_var.move(150, 100)

login_button = QPushButton(root)
login_button.setText("Login")
login_button.move(150, 150)
login_button.clicked.connect(authenticate)

root.setGeometry(200, 200, 400, 250)
root.show()

sys.exit(app.exec_())
