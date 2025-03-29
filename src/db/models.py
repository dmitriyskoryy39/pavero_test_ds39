
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, String

from core import Base


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)


class TokenOrm(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, index=True, nullable=False)
    access_token: Mapped[str] = mapped_column(unique=True, nullable=False)
    refresh_token: Mapped[str] = mapped_column(unique=True, nullable=False)
    expires_in: Mapped[str] = mapped_column(unique=True, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))


class AudioFileOrm(Base):
    __tablename__ = "audiofiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    path: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))