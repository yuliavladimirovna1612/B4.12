import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


class User(Base):

    # Описывает структуру таблицы user для хранения регистрационных данных пользователей

    # задаем название таблицы
    __tablename__ = 'user'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол пользователя
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения пользователя
    birthdate = sa.Column(sa.Text)
    # рост пользователя
    height = sa.Column(sa.Float)

class Athelete(Base):

    # Описывает структуру таблицы athelete, содержащую данные об атлетах

    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def connect_db():

    # Устанавливает соединение к базе данных и возвращает объект сессии

    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def request_data():

    # Запрашивает у пользователя данные
    print("Найдем атлета, имеющего пожие данные с пользователем.")
    user_id = input("Введите идентификатор пользователя: ")
    return int(user_id)

def convert_str_to_date(date_str):

    # Конвертирует дату в формат  datetime.date

    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date


def search_bd(user, session):

    # Поиск атлета ближайшего по дате рождения

    athletes_list = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athletes_list:
        bd = convert_str_to_date(athlete.birthdate)
        athlete_id_bd[athlete.id] = bd

    user_bd = convert_str_to_date(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_bd = None

    for id_, bd in athlete_id_bd.items():
        dist = abs(user_bd - bd)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_bd = bd

    return athlete_id, athlete_bd


def search_height(user, session):

    # Поиск ближайшего по росту атлета

    athletes_list = session.query(Athelete).filter(Athelete.height != None).all()
    athlete_id_height = {athlete.id: athlete.height for athlete in athletes_list}

    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for id_, height in athlete_id_height.items():
        if height is None:
            continue

        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height

    return athlete_id, athlete_height

def main():

    session = connect_db()
    user_id = request_data()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print("Такого пользователя в базе данных не существует.")
    else:
        bd_athlete, bd = search_bd(user, session)
        height_athlete, height = search_height(user, session)
        print(
            "Ближайший по дате рождения атлет: {}, его дата рождения: {}".format(bd_athlete, bd)
        )
        print(
            "Ближайший по росту атлет: {}, его рост: {}".format(height_athlete, height)
        )

if __name__ == "__main__":
    main()
