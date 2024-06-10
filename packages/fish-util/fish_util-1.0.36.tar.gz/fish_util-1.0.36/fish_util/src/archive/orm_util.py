from sqlalchemy import create_engine, Column, Integer, String,UniqueConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

# 连接到MySQL数据库
engine = create_engine('mysql+mysqlconnector://root:fishyer2850@127.0.0.1:3306/testdb')

# 创建数据模型
Base = declarative_base()

class HistoryEntity(Base):
    __tablename__ = 'histoty_table'
    id = Column(Integer, primary_key=True)
    url = Column(String(255),unique=True)
    title = Column(String(255))
    tabId = Column(Integer)
    openerTabId = Column(Integer)

    __table_args__ = (
        UniqueConstraint('url', name='url_unique'),
    )

# 创建表格
Base.metadata.create_all(engine)

def add_history_entity(url, title, tabId, openerTabId):
    if openerTabId=="undefined":
        openerTabId=-1
    # 创建一个Session类，用于管理数据库会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 创建数据对象并插入到数据表中
    data={'url': url, 'title': title, 'tabId': tabId, 'openerTabId': openerTabId}
    entity = HistoryEntity(**data)
    session.add(entity)
    try:
        session.commit()
    except IntegrityError:
        # 忽略 IntegrityError 异常
        session.rollback()
    
    # 关闭会话
    session.close()
    print("添加历史记录表成功: ", url, title, tabId, openerTabId)