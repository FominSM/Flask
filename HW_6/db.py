from settings import settings
import databases
import sqlalchemy
from sqlalchemy import create_engine

DATABASE_URL = settings.DATABASE_URL

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("surname", sqlalchemy.String(128)),
    sqlalchemy.Column("birthday", sqlalchemy.String(128)),
    sqlalchemy.Column("adress", sqlalchemy.String(128)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(128)),
)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(100)),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("price", sqlalchemy.Float(128)),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("id_product",sqlalchemy.ForeignKey('products.id')),
    sqlalchemy.Column("id_user", sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column("date_order", sqlalchemy.String(15)),
    sqlalchemy.Column("status_order", sqlalchemy.String(100))
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)