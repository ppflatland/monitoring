import sqlite3
import datetime
import re
import config
from config import database

class SQLighter:
    # Status_code
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def status_code(self, number):
            """ проверка кода ответа """
            with self.connection:
                result = self.cursor.execute('SELECT code, time FROM Status_Code WHERE id_server ="%s"' %(number)).fetchall()
                #print(result[0][0],result[0][1])
                return result
    def update_status_code(self, code, ts, number):
        """ обновление кода ответа кода ответа """
        with self.connection:
                self.cursor.execute('UPDATE Status_Code SET code="%s",time="%s" WHERE id_server = "%s"'%(code,ts,number))

    def status_error(self, number):
        """ проверка на ошибки """
        with self.connection:
            result = self.cursor.execute('SELECT error, time FROM Status_Code WHERE id_server ="%s"' %(number)).fetchall()
            #print(result[0][0],result[0][1])
            return result
    def all_status_code(self):
        """ получения статуса от всех серверов """
        with self.connection:
            result = self.cursor.execute('SELECT id_server, code FROM Status_Code').fetchall()
            return result
    def update_status_error(self, error, ts, number):
        """ обновление состояние ошибок """
        with self.connection:
                self.cursor.execute('UPDATE Status_Code SET error="%s",time="%s" WHERE id_server = "%s"'%(error,ts,number))
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
