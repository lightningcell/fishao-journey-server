from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
# Diğer alt modüller için de aynı şekilde ekleme yapabilirsiniz.