from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    __scopes = relationship(
        "Scope",
        primaryjoin="User.id == UserScope.user_id",
        secondary="join(Scope, UserScope, Scope.name == UserScope.scope_name)"
    )

    @property
    def scopes(self):
        return [s.name for s in self.__scopes]


class Scope(Base):
    __tablename__ = "scopes"

    name = Column(String, primary_key=True)


class UserScope(Base):
    __tablename__ = "users_scopes"

    user_id = Column(ForeignKey("users.id"), primary_key=True)
    scope_name = Column(ForeignKey("scopes.name"), primary_key=True)

