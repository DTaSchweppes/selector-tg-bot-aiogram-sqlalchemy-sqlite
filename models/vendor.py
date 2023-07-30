from sqlalchemy import Column, Integer, String

from configuration import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)
    category = Column(String)
    rating = Column(String)