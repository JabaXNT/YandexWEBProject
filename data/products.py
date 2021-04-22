import sqlalchemy

from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def __repr__(self):
        return f"Product {self.title} {self.content}"
