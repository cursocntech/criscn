import os

class Config:
    SECRET_KEY = 'troque_para_uma_chave_secreta'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_database_uri():
        # Usa DATABASE_URL do ambiente, se existir (Postgres no Railway)
        # Caso contrário, usa SQLite local
        return os.environ.get('DATABASE_URL', 'sqlite:///database.db')

    SQLALCHEMY_DATABASE_URI = get_database_uri()
