from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
import os

if not os.path.exists('CI.db'):
    # make file
    open('CI.db', 'w').close()

engine = create_engine('sqlite:///CI.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class BuildHistory(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now)
    branch = Column(String(50))
    event = Column(String(50))
    status = Column(String(50))
    

    def __init__(self, branch, event, status):
        
        self.branch = branch
        self.event = event
        self.status = status

    def __repr__(self):
        return f'<User {self.name!r}>'

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    
    Base.metadata.create_all(bind=engine)
    # Insert a row of data
    build1 = BuildHistory('new-branch', 'pull request', 'fail')
    db_session.add(build1)
    db_session.commit()
