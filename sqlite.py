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
                return result

    def update_status_code(self, code, ts, number):
        """ обновление кода ответа кода ответа """
        with self.connection:
                self.cursor.execute('UPDATE Status_Code SET code="%s",time="%s" WHERE id_server = "%s"'%(code,ts,number))

    def status_error(self, number):
        """ проверка на ошибки """
        with self.connection:
            result = self.cursor.execute('SELECT error, time FROM Status_Code WHERE id_server ="%s"' %(number)).fetchall()
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


    def update_iformation_reputation(self, time, EMAIL_REPUTATION, WEB_REPUTATION, WEIGHTED_REPUTATION, VOLUME_CHANGE, BL, name):
       """ обновление информации о репутации серверов """
       with self.connection:
           self.cursor.execute('UPDATE server_reputation SET time="%s", email_rep ="%s", web_rep="%s", weighted_rep="%s", volume_change="%s", bl="%s" WHERE server="%s"' %(time, EMAIL_REPUTATION, WEB_REPUTATION, WEIGHTED_REPUTATION, VOLUME_CHANGE, BL, name))

    def iformation_reputation_server(self, name):
       """ получение информации о репутации сервера """
       with self.connection:
           result = self.cursor.execute('SELECT time, email_rep, web_rep, weighted_rep, volume_change, bl FROM server_reputation WHERE server="%s"' %(name)).fetchall()
           return result

    def all_iformation_reputation_servers(self):
        """ получение всей информации о серверах """
        with self.connection:
           result = self.cursor.execute('SELECT * FROM server_reputation').fetchall()
           return result
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()


