# coding = utf-8
from footcom_route.db.basic_db import Base

from footcom_route.db.tables import route_info, login_info



class FootRoute(Base):
    __table__ = route_info


class LoginInfo(Base):
    __table__ = login_info

