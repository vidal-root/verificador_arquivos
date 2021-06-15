import sqlite3
from sqlite3 import Error
import os


class appDAO:

    def __init__(self):
        self.conn = None
        self.create_tables()

    def insert_historico(self, nm_caminho):
        try:
            self.conn = self.conectar()
            cursor = self.conn.cursor()

            sql = f"""INSERT INTO HISTORICO(NM_CAMINHO) VALUES('{nm_caminho}');"""

            cursor.execute(sql)
            self.conn.commit()

        except self.conn.Error as e:
            self.conn.rollback()
            print(e)
            print('Erro ao inserir tema!')

    def deletar_historico(self):
        try:
            self.conn = self.conectar()
            cursor = self.conn.cursor()

            sql = f"""DELETE FROM HISTORICO;"""

            cursor.execute(sql)
            self.conn.commit()

        except self.conn.Error as e:
            self.conn.rollback()
            print(e)
            print('Erro ao deletar histórico!')

    def insert_tema(self, nm_tema):
        try:
            self.conn = self.conectar()
            cursor = self.conn.cursor()

            sql = f"""DELETE FROM USUARIO_TEMA;
                    
                    INSERT INTO USUARIO_TEMA VALUES('{nm_tema}');
                   """

            cursor.executescript(sql)
            self.conn.commit()

        except self.conn.Error as e:
            self.conn.rollback()
            print(e)
            print('Erro ao inserir tema!')

    def select_historico(self):
        try:
            self.conn = self.conectar()
            cursor = self.conn.cursor()

            sql = f"""SELECT * FROM HISTORICO GROUP BY NM_CAMINHO ORDER BY 1 DESC;"""
            cursor.execute(sql)

            return cursor.fetchall()

        except self.conn.Error as e:
            print(e)

    def select_tema(self):
        try:
            self.conn = self.conectar()
            cursor = self.conn.cursor()

            sql = f"""SELECT * FROM USUARIO_TEMA;"""
            cursor.execute(sql)

            return cursor.fetchall()

        except self.conn.Error as e:
            print(e)

    def create_tables(self):
        try:
            self.conn = self.conectar()
            cursor = self.conn.cursor()

            sql = """CREATE TABLE IF NOT EXISTS HISTORICO (
                ID_HISTORICO INTEGER PRIMARY KEY AUTOINCREMENT,
                NM_CAMINHO TEXT NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS USUARIO_TEMA (
                NM_TEMA TEXT NOT NULL
            );
            """
            cursor.executescript(sql)
            self.conn.commit()

        except self.conn.Error as e:
            self.conn.rollback()
            print(e)
            print('Erro ao criar tabelas!')

    def conectar(self):
        db_file = os.getcwd() + '\db_verificador_arquivo.db3'
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn
