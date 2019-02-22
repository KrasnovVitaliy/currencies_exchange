import datetime
from sqlalchemy import create_engine, Column, DateTime, Integer, String, func, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DB_URI = 'sqlite:///data.db'

Base = declarative_base()

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(DB_URI))
session = scoped_session(Session)


class CurrenciesRecord(Base):
    __tablename__ = 'currencies'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=func.now())
    code = Column(String(5))
    name = Column(String(10))
    cb_currency = Column(Float)
    raif_buy = Column(Float)
    raif_sale = Column(Float)
    best_buy = Column(Float)
    best_sale = Column(Float)
    best_buyer = Column(String(50))
    best_sailer = Column(String(50))

    def __init__(self, code, name, cb_currency, raif_buy, raif_sale, best_buy, best_sale, best_buyer, best_sailer):
        self.code = code
        self.name = name
        self.cb_currency = cb_currency
        self.raif_buy = raif_buy
        self.raif_sale = raif_sale
        self.best_buy = best_buy
        self.best_sale = best_sale
        self.best_buyer = best_buyer
        self.best_sailer = best_sailer

    def serialize(self, to_serialize):
        d = {}
        for attr_name in to_serialize:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, datetime.datetime):
                attr_value = str(attr_value)
            d[attr_name] = attr_value
        return d

    def to_json(self):
        to_serialize = ['id', 'create_date', 'code', 'name', 'cb_currency', 'raif_buy', 'raif_sale', 'best_buy',
                        'best_sale', 'best_buyer', 'best_sailer']
        return self.serialize(to_serialize)


def prepare_db():
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


# creates database
if __name__ == "__main__":
    prepare_db()
