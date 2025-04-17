from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import DB


engine = create_engine(url=DB, echo=False)
'''Создание базы(требуется ссылка в формате postgresql+psycopg2://user_name:password@host:port/db_name
    если база находиться на вашем пк то ставьте host : localhost, port : 5432'''

Session = sessionmaker(engine)
'''создание сессии (подключение к базе)'''

session = Session()
'''обращение к сессии'''


class Base(DeclarativeBase):
    """Наследуется от DeclarativeBase для формирования Таблиц"""
    ...


class Document(Base):
    """Модель таблицы documents и столбцов id: primary key, filename: имя документа, content: текст из документе"""
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    filename = Column(Text, nullable=False)
    content = Column(Text, nullable=False)


def start():
    """Инициализация Таблиц и столбцов"""
    Base.metadata.create_all(engine)