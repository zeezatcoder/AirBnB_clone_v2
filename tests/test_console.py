#!/usr/bin/python3
"""unittest module for the console"""
from models.user import User
from models.base_model import BaseModel
from models import storage
from console import HBNBCommand
from unittest import TestCase
from unittest.mock import patch
from io import StringIO
import unittest
import sqlalchemy
from os import getenv
import json
import MySQLdb
import sys
sys.path.insert(0, '/root/AirBnB_clone_v2')


class TestHBNBCommand(TestCase):
    """Tst class for the HBNBCommand class.
    """
    @unittest.skipIf(
        getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_create(self):
        """Tests create command on file storage"""
        with patch('sys.stdout', new=StringIO()) as std:
            cons_cmd = HBNBCommand()
            cons_cmd.onecmd('create City name="Lagos"')
            tst_id = std.getvalue().strip()
            self.assertIn('City.{}'.format(tst_id), storage.all().keys())
            cons_cmd.onecmd('show City {}'.format(tst_id))
            self.assertIn("'name': 'Lagos'", std.getvalue().strip())
            cons_cmd.onecmd('create User name="wrash" age=27 height=8.1')
            tst_id = std.getvalue().strip()
            self.assertIn('User.{}'.format(tst_id), storage.all().keys())
            cons_cmd.onecmd('show User {}'.format(tst_id))
            self.assertIn("'name': 'wrash'", std.getvalue().strip())
            self.assertIn("'age': 27", std.getvalue().strip())
            self.assertIn("'height': 8.1", std.getvalue().strip())

    @unittest.skipIf(
        getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """Tests cases for the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as std:
            cons_cmd = HBNBCommand()
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                cons_cmd.onecmd('create User')
            cons_cmd.onecmd(
                'create User email="wrash@gmail.com" password="12345"')
            tst_id = std.getvalue().strip()
            db_con = MySQLdb.connect(
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                db=getenv('HBNB_MYSQL_DB')
            )
            cursor = db_con.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(tst_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('wrash@gmail.com', result)
            self.assertIn('12345', result)
            cursor.close()
            db_con.close()

    @unittest.skipIf(
        getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """Tests the show command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as std:
            cons_cmd = HBNBCommand()
            obj = User(email="wrash@gmail.com", password="12345")
            db_con = MySQLdb.connect(
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                db=getenv('HBNB_MYSQL_DB')
            )
            cursor = db_con.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is None)
            cons_cmd.onecmd('show User {}'.format(obj.id))
            self.assertEqual(
                std.getvalue().strip(),
                '** no instance found **'
            )
            obj.save()
            db_con = MySQLdb.connect(
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                db=getenv('HBNB_MYSQL_DB')
            )
            cursor = db_con.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            cons_cmd.onecmd('show User {}'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('wrash@gmail.com', result)
            self.assertIn('12345', result)
            self.assertIn('wrash@gmail.com', std.getvalue())
            self.assertIn('12345', std.getvalue())
            cursor.close()
            db_con.close()

    @unittest.skipIf(
        getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Tests the count command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as std:
            cons_cmd = HBNBCommand()
            db_con = MySQLdb.connect(
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                db=getenv('HBNB_MYSQL_DB')
            )
            cursor = db_con.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            result = cursor.fetchone()
            prev_count = int(result[0])
            cons_cmd.onecmd('create State name="Lagos"')
            cons_cmd.onecmd('count State')
            cnt = std.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            cons_cmd.onecmd('count State')
            cursor.close()
            db_con.close()
