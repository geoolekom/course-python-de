from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = "mysql+pymysql://root:secret@localhost:3306/python-de"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
)


class Base(DeclarativeBase):
    pass


Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
