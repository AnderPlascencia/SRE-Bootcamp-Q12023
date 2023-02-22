# These functions need to be implemented
from flask import jsonify
import mysql.connector
import jwt
import hashlib

# DB Credentials
DB_HOST = "sre-bootcamp-selection-challenge.cabf3yhjqvmq.us-east-1.rds.amazonaws.com"
DB_PORT = 3306
DB_USER = "secret"
DB_PASSWORD = "jOdznoyH6swQB9sTGdLUeeSrtejWkcw"
DB_NAME = "bootcamp_tht"

jwt_secret = "my2w7wjd7yXF64FIADfJxNs1oupTGAuW"

class Token:

    def generate_token(self, username, password):
        conn = mysql.connector.connect(
        user=DB_USER, 
        password=DB_PASSWORD, 
        host=DB_HOST, 
        port=DB_PORT, 
        database=DB_NAME)
        cursor = conn.cursor()
        query = ("SELECT * FROM users WHERE username=%s")
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if not result:
            return False
        username_db, password_db, salt, role = result
        password_hash = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
        if username == username_db and password_hash == password_db:
            payload = {'sub': username, 'role': role}
            token = jwt.encode(payload, jwt_secret, algorithm='HS256')
            return token
        else:
            return ('Invalid username or password')
        


class Restricted:

    def access_data(self, authorization):
        if not authorization:
            return jsonify({"error": "Missing authorization header"}), 401

        token = authorization.split("Bearer ")[1]

        try:
            # decode the JWT token
            payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])

            # check if the user has the required role
            if payload["role"] != "admin":
                return jsonify({"error": "Access denied"}), 403

            # return the protected data
            return ("You are under protected data")
        except: 
            return ("Invalid token")