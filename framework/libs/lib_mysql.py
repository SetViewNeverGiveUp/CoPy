# encoding: utf-8

"""
author: ringzero@0x557.org
home:   http://github.com/ring04h/fpymysql
desc:   A Friendly pymysql CURD Class

https://dev.mysql.com/doc/connector-python/en/connector-python-reference.html

SQL Injection Warning: pymysql.escape_string(value)

"""

import pymysql
from pymysql.converters import escape_string

class MYSQL:
    """A Friendly pymysql Class, Provide CRUD functionality"""

    def __init__(self, dbhost, dbuser, dbpwd, dbname, dbcharset, dbport='3306'):
        self.dbhost = dbhost
        self.dbuser = dbuser
        self.dbpwd = dbpwd
        self.dbname = dbname
        self.dbcharset = dbcharset
        self.dbport = int(dbport)
        self.connection = self.connect()

    def connect(self):
        """Connect to the database"""
        connection = pymysql.connect(
                host = self.dbhost,
                port = self.dbport,
                user = self.dbuser,
                password = self.dbpwd,
                db = self.dbname,
                charset = self.dbcharset,
                cursorclass=pymysql.cursors.DictCursor)
        return connection

    def insert(self, table, data):
        """mysql insert() function"""
        with self.connection.cursor() as cursor:
            params = self.join_field_value(data);
            sql = "INSERT INTO {table} SET {params}".format(table=table, params=params)
            result = cursor.execute(sql)
            self.connection.commit() # not autocommit
            self.lastrowid = cursor.lastrowid
            return result

    def delete(self, table, condition=None, limit=None):
        """mysql delete() function"""
        with self.connection.cursor() as cursor:
            if not condition:
                where = '1';
            elif isinstance(condition, dict):
                where = self.join_field_value( condition, ' AND ' )
            else:
                where = condition

            limits = "LIMIT {limit}".format(limit=limit) if limit else ""
            sql = "DELETE FROM {table} WHERE {where} {limits}".format(
                table=table, where=where, limits=limits)

            result = cursor.execute(sql)
            self.connection.commit() # not autocommit

            return result

    def update(self, table, data, condition=None):
        """mysql update() function"""
        with self.connection.cursor() as cursor:
            params = self.join_field_value(data)
            if not condition:
                where = '1';
            elif isinstance(condition, dict):
                where = self.join_field_value( condition, ' AND ' )
            else:
                where = condition

            sql = "UPDATE {table} SET {params} WHERE {where}".format(
                table=table, params=params, where=where)
            result = cursor.execute(sql)
            self.connection.commit() # not autocommit

            return result

    def count(self, table, condition=None):
        """count database record"""
        with self.connection.cursor() as cursor:
            # WHERE CONDITION
            if not condition:
                where = '1';
            elif isinstance(condition, dict):
                where = self.join_field_value( condition, ' AND ' )
            else:
                where = condition
            
            # SELECT COUNT(*) as cnt
            sql = "SELECT COUNT(*) as cnt FROM {table} WHERE {where}".format(
                table=table, where=where)

            # EXECUTE SELECT COUNT sql
            cursor.execute(sql)

            # RETURN cnt RESULT
            return cursor.fetchone().get('cnt')


    def fetch_rows(self, table, fields=None, condition=None, order=None, limit=None, fetchone=False):
        """mysql select() function"""
        with self.connection.cursor() as cursor:
            # SELECT FIELDS
            if not fields:
                fields = '*'
            elif isinstance(fields, tuple) or isinstance(fields, list):
                fields = '`, `'.join(fields)
                fields = '`{fields}`'.format(fields=fields)
            else:
                fields = fields

            # WHERE CONDITION
            if not condition:
                where = '1';
            elif isinstance(condition, dict):
                where = self.join_field_value( condition, ' AND ' )
            else:
                where = condition

            # ORDER BY OPTIONS
            if not order:
                orderby = ''
            else:
                orderby = 'ORDER BY {order}'.format(order=order)

            # LIMIT NUMS
            limits = "LIMIT {limit}".format(limit=limit) if limit else ""
            sql = "SELECT {fields} FROM {table} WHERE {where} {orderby} {limits}".format(
                fields=fields, 
                table=table, 
                where=where, 
                orderby=orderby,
                limits=limits)
            cursor.execute(sql)

            if fetchone:
                return cursor.fetchone()
            else:
                return cursor.fetchall()

    def query(self, sql, fetchone=False):
        """execute custom sql query"""
        with self.connection.cursor() as cursor:
            if not sql:
                return
            cursor.execute(sql)
            self.connection.commit() # not auto commit
            if fetchone:
                return cursor.fetchone()
            else:
                return cursor.fetchall()

    def close(self):
        try:
            if(callable(self.connection)):
                return self.connection.close()
        except:
            print('Not create connection')


    def join_field_value(self, data, glue = ', '):
        sql = comma = ''
        "Compatible with 3 otherwise iteritems()"
        for key, value in data.items():
            if isinstance(value, str):
                value = escape_string(value)
            sql +=  "{}`{}` = '{}'".format(comma, key, value)
            comma = glue
        return sql

    def __del__(self):
        """close mysql database connection"""

        self.close()

