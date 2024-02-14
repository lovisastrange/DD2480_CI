from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

engine = create_engine('sqlite:///CI.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class BuildHistory(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    #今の時刻
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


# from datetime import datetime
# from flask import current_app

# test_builds = [
#         {
#         "id": 10, 
#         "date": datetime(2024, 2, 1).strftime("%d/%m/%Y, %H:%M:%S"),
#         "branch": "new-branch",
#         "event": "pull request",
#         "status": "fail", 
#         },
#         {
#         "id": 11, 
#         "date": datetime(2024, 2, 3).strftime("%d/%m/%Y, %H:%M:%S"),
#         "branch": "new-branch",
#         "event": "push",
#         "status": "success", 
#         },
#         {
#         "id": 12, 
#         "date": datetime(2024, 2, 5).strftime("%d/%m/%Y, %H:%M:%S"),
#         "branch": "another-new-branch",
#         "event": "push",
#         "status": "success", 
#         },
#         {
#         "id": 13, 
#         "date": datetime(2024, 2, 7).strftime("%d/%m/%Y, %H:%M:%S"),
#         "branch": "fix-wrong-type",
#         "event": "pull request",
#         "status": "fail", 
#         },
#     ]
# builds = test_builds #temporary

# def query_build(build_id):
#     """
#     Function returning a specific build from the database.
#     """
#     data_source = test_builds if current_app.config.get("TESTING") else builds
#     return next((build for build in data_source if build["id"] == build_id), None)

# def query_builds():
#     """
#     Function returning the list of all builds from the database.
#     """
#     return test_builds if current_app.config.get("TESTING") else builds