from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from configuration import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    brand = Column(String)
    vendor_id = Column(Integer, ForeignKey('vendors.id'))
    vendor = relationship("Vendor")

