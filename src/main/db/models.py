# from sqlalchemy import Column, Integer, String, DateTime
# import datetime
# from .database import Base

# class BuildHistory(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     #今の時刻
#     date = Column(DateTime, default=datetime.now())
#     branch = Column(String(50))
#     event = Column(String(50))
#     status = Column(String(50))
    

#     def __init__(self, branch, event, status):
        
#         self.branch = branch
#         self.event = event
#         self.status = status

#     def __repr__(self):
#         return f'<User {self.name!r}>'