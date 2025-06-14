from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


from .base_entity import BaseEntity
from .player import *
from .item import *
from .home import *
from .fishing import *
from .club import *
from .area import *
from .outfit import *
from .payment_integration import *
from .player_budget import *
from .report import *
from .task import *
from .trade import *
from .event_and_npc_integration import *
from .fish_shop import *
from .chat import *
from .collection import *
