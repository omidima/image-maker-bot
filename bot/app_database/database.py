from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

DatabaseSession = sessionmaker(autoflush=True, autocommit=False, bind=engine)
Base = declarative_base()


db = None
def get_db():
    global db

    if( db == None):
        db = DatabaseSession()

    return db