from PyQt5.QtCore import QTimer
from sqlalchemy import create_engine, Column, String, Integer, Enum, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Определение модели пользователя
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(Enum('user', 'auctioneer', name='user_role'))

# Определение модели лота
class Lot(Base):
    __tablename__ = 'lots'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    min_price = Column(Float)
    current_price = Column(Float, default=0.0)
    timer_seconds = Column(Integer, default=60)

    def __init__(self, name, description, min_price, timer_seconds=60):
        super().__init__(name=name, description=description, min_price=min_price, timer_seconds=timer_seconds)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def update_timer(self):
        self.timer_seconds -= 1
        if self.timer_seconds <= 0:
            self.timer.stop()

    def is_active(self):
        return self.timer_seconds > 0

# Определение модели ставки
class Bid(Base):
    __tablename__ = 'bids'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    lot_id = Column(Integer, nullable=False)
    amount = Column(Float)

# Подключение к базе данных
engine = create_engine('postgresql://postgres:59723833@localhost/auction', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()