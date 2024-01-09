from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .database_connection import Base
from sqlalchemy.orm import relationship
import uuid


class Users(Base):
    __tablename__ = "users"

    username = Column(String(100), primary_key=True, index=True)
    password = Column(String(100))
    disabled = Column(Boolean)
    scopes = Column(String)
    conversations = relationship("Conversations", back_populates="user")

    class Config:
        orm_mode = True


class Conversations(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    language = Column(String(100))
    user_username = Column(String(100), ForeignKey("users.username"))

    user = relationship("Users", back_populates="conversations")
    language_processing_logs = relationship(
        "LanguageProcessingLog", back_populates="conversation"
    )
    transcription = Column(String)  # Transcription of the languageProcessing input text


class LanguageProcessingLog(Base):
    __tablename__ = "language_processing_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    input_text = Column(String)
    output_text = Column(String)
    conversation_id = Column(String(36), ForeignKey("conversations.id"))

    conversation = relationship(
        "Conversations", back_populates="language_processing_logs"
    )
    audio_logs = relationship("AudioLog", back_populates="language_processing")


class AudioLog(Base):
    __tablename__ = "audio_logs"

    audio_key = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    language_processing_id = Column(
        String(36), ForeignKey("language_processing_logs.id")
    )

    language_processing = relationship(
        "LanguageProcessingLog", back_populates="audio_logs"
    )
