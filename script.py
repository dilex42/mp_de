import requests
import datetime
import re
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import models

URL = "https://data-engineering-interns.macpaw.io"
DB_PATH = "postgresql://mp_de:mp_de@db/postgres"


def func_title(s):
    s = s.lower()
    s = re.sub(r"\W+", " ", s)
    s = re.sub(r"\s", "_", s)
    return s


def func_rate(o):
    return o["rating"] >= 4.2


def parse():
    print("\nJob started\n")

    data = {
        "song": [],
        "movie": [],
        "app": [],
    }
    files_name = []

    data_file = requests.get(f"{URL}/files_list.data")
    files_list = set(data_file.text.split("\n"))

    engine = sa.create_engine(DB_PATH)
    # print('!!! Dropping all tables !!!')
    # models.Base.metadata.drop_all(engine, models.Base.metadata.tables.values())
    # print('!!! All tables dropped !!!')
    models.Base.metadata.create_all(
        engine, models.Base.metadata.tables.values()
    )

    Session = sessionmaker(bind=engine)
    with Session.begin() as session:
        processed_df = {df.name for df in session.query(models.DataFile).all()}

    for f in files_list - processed_df:
        print("-" * 42)
        print(f"New file ::: {f}")
        content = requests.get(f"{URL}/{f}").json()
        print(f"{len(content)} elements")
        for obj in content:
            t = obj["type"]
            if t == "song":
                data["song"].append(
                    obj["data"] | {"ingestion_time": datetime.datetime.now()}
                )
            if t == "movie":
                data["movie"].append(
                    obj["data"]
                    | {
                        "original_title_normalized": func_title(
                            obj["data"]["original_title"]
                        )
                    }
                )
            if t == "app":
                data["app"].append(
                    obj["data"] | {"is_awesome": func_rate(obj["data"])}
                )
        files_name.append(f)
        print("*" * 42)

    print(f"Data files parsed: {len(files_name)}")
    print(f"New song objects: {len(data['song'])}")
    print(f"New movie objects: {len(data['movie'])}")
    print(f"New app objects: {len(data['app'])}")
    if len(files_name):
        print("Inserting into db......")

    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.add_all([models.Song(**song) for song in data["song"]])
        session.add_all([models.Movie(**movie) for movie in data["movie"]])
        session.add_all([models.App(**app) for app in data["app"]])
        session.add_all(
            [models.DataFile(name=file_name) for file_name in files_name]
        )
        session.commit()

        print("^" * 42)
        print(
            f"Total song objects in db: {session.query(models.Song).count()}"
        )
        print(
            f"Total movie objects in db: {session.query(models.Movie).count()}"
        )
        print(f"Total app objects in db: {session.query(models.App).count()}")
        print(
            f"Total data files parsed: {session.query(models.DataFile).count()}"
        )
        print("-" * 42)
