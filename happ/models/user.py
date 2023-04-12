from sqlalchemy import Column, Integer, String

from happ.db.base_class import Base


class User(Base):
    __tablename__ = 't_user'
    __table_args__ = ({'schema': 'alemb', 'comment': 'Users'})

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
