from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# DB
engine = create_engine("sqlite:///teste.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()


class HashCode(Base):
    __tablename__ = 'hashtable'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hashed = Column(String(128))
    ch_id = Column(Integer)

    def __repr__(self):
        return f'{self.hashed}'


Base.metadata.create_all(engine)
