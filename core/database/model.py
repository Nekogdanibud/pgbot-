from datetime import datetime
from sqlalchemy import (
    Column, Integer, BigInteger, String, DateTime, 
    Text, Index, func, ForeignKey, CheckConstraint,
    UniqueConstraint
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index('idx_user_telegram_id', 'telegram_id'),
        Index('idx_user_username', 'username'),
        CheckConstraint(
            "role IN ('ADMIN', 'SUPPORT', 'USER', 'BANNED')", 
            name="check_user_role"
        ),
    )

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True, index=True)
    role = Column(String(20), nullable=False, server_default="USER")
    balance = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    mailings = relationship("Mailing", back_populates="creator")
    tickets = relationship("Ticket", back_populates="user", foreign_keys="Ticket.user_id")
    subscriptions = relationship(
        "Subscription", 
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        Index('idx_subscription_user_id', 'user_id'),
        Index('idx_marzban_username', 'marzban_username'),
        UniqueConstraint('marzban_username', name='uq_marzban_username'),
    )

    subscription_id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    marzban_username = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="subscriptions")

class Mailing(Base):
    __tablename__ = "mailings"
    __table_args__ = (
        Index('idx_mailing_status', 'status'),
        Index('idx_mailing_scheduled', 'scheduled_at', 'status'),
        CheckConstraint(
            "status IN ('PENDING', 'SENT', 'FAILED')", 
            name="check_mailing_status"
        ),
    )

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, server_default="PENDING")
    created_at = Column(DateTime, server_default=func.now())
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Relationship
    creator = relationship("User", back_populates="mailings")

class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = (
        Index('idx_ticket_status', 'status'),
        Index('idx_ticket_user', 'user_id'),
        CheckConstraint(
            "status IN ('OPEN', 'IN_PROGRESS', 'CLOSED')", 
            name="check_ticket_status"
        ),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, server_default="OPEN")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    assigned_to = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    # Relationships
    user = relationship("User", back_populates="tickets", foreign_keys=[user_id])
    assigned_support = relationship("User", foreign_keys=[assigned_to])
