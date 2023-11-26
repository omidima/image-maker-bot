from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://devops:omid51172123@141.98.210.50/review"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

DatabaseSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


db = None
def get_db():
    global db

    if( db == None):
        db = DatabaseSession()

    return db