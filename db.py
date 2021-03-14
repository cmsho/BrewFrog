# Colton Shoenberger, cs3585@drexel.edu
# CS530: DUI, Final Project

import os
import re
import sqlite3


SQLITE_PATH = os.path.join(os.path.dirname(__file__), 'beer.db')


class Database:

    ## GENERAL
    def __init__(self):
        self.conn = sqlite3.connect(SQLITE_PATH)

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()

    def close(self):
        self.conn.close()


    ## BEER
    def get_beer(self, n, offset, abvMin, abvMax, ibuMin, ibuMax, calMin, calMax):
        data = self.select(
            'SELECT * FROM beer WHERE abv>=? AND abv<=? AND ibu>=? AND ibu<=? AND calories>=? and calories<=? ORDER BY uid ASC LIMIT ? OFFSET ?', 
            [abvMin, abvMax, ibuMin, ibuMax, calMin, calMax, n, offset])
        return [{
            'uid': d[0],
            'name': d[1],
            'brewery': d[2],
            'style': d[3],
            'abv': d[4],
            'ibu': d[5],
            'calories': d[6],
            'image': d[7]
        } for d in data]

    def get_total_beer_count(self, abvMin, abvMax, ibuMin, ibuMax, calMin, calMax):
        data = self.select(
            'SELECT COUNT(*) FROM beer WHERE abv>=? AND abv<=? AND ibu>=? AND ibu<=? AND calories>=? AND calories<=?', 
            [abvMin, abvMax, ibuMin, ibuMax, calMin, calMax])
        return data[0][0]



    ## USERS
    def create_user(self, name, username, encrypted_password):
        self.execute('INSERT INTO users (name, username, encrypted_password) VALUES (?, ?, ?)',
                     [name, username, encrypted_password])

    def get_user(self, username):
        data = self.select('SELECT * FROM users WHERE username=?', [username])
        if data:
            d = data[0]
            return {
                'uid': d[0],
                'name': d[1],
                'username': d[2],
                'encrypted_password': d[3]
            }
        else:
            return None
    
    def get_users(self, n, offset):
        data = self.select(
            'SELECT * FROM users ORDER BY uid ASC LIMIT ? OFFSET ?', [n, offset])
        return [{
            'uid': d[0],
            'name': d[1],
            'username': d[2],
            'encrypted_password': d[3]
        } for d in data]

    def get_total_user_count(self):
        data = self.select('SELECT COUNT(*) FROM users')
        return data[0][0]


    ## FAVORITES
    def add_favorite(self, user_id, beer_id):
        self.execute('INSERT INTO favorites (user_id, beer_id) VALUES (?, ?)', [user_id, beer_id])

    def unfavorite(self, user_id, beer_id):
        self.execute('DELETE FROM favorites WHERE user_id=? AND beer_id=?', [user_id, beer_id])

    def my_favorites(self, user_id, n, offset):
        data = self.select('SELECT * FROM favorites AS f, beer AS b WHERE f.user_id = ? AND f.beer_id = b.uid LIMIT ? OFFSET ?', [user_id, n, offset])
        return [{
            'uid': d[2],
            'name': d[3],
            'brewery': d[4],
            'style': d[5],
            'abv': d[6],
            'ibu': d[7],
            'calories': d[8],
            'image': d[9]
        } for d in data]

    def get_favorites(self, n, offset):
        data = self.select(
            'SELECT * FROM favorites ORDER BY user_id ASC LIMIT ? OFFSET ?', [n, offset])
        return [{
            'user_id': d[0],
            'beer_id': d[1]
        } for d in data]

    def get_my_favorites_count(self, user_id):
        data = self.select('SELECT COUNT(*) FROM favorites WHERE user_id = ?', [user_id])
        return data[0][0]

    def get_total_favorites_count(self):
        data = self.select('SELECT COUNT(*) FROM favorites')
        return data[0][0]