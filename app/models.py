from sqlalchemy import Column, Integer, String, Text, Date, TIMESTAMP, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Organizer(Base):
    __tablename__ = "organizers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    position = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    events = relationship("Event", back_populates="organizer")

class EventVersion(Base):
    __tablename__ = "event_versions"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", deferrable=True, initially="DEFERRED"), nullable=False)
    version_number = Column(Integer, nullable=False)
    description_text = Column(Text, nullable=False)
    changed_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    changed_by = Column(String(100), default="system")

    __table_args__ = (UniqueConstraint("event_id", "version_number"),)

    event = relationship("Event", foreign_keys=[event_id], back_populates="versions")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    event_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    organizer_id = Column(Integer, ForeignKey("organizers.id", ondelete="SET NULL"))
    status = Column(String(30), nullable=False)
    budget = Column(Integer, default=0)
    parent_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))
    current_version_id = Column(Integer, ForeignKey("event_versions.id", deferrable=True, initially="DEFERRED"))
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    organizer = relationship("Organizer", back_populates="events")
    parent = relationship("Event", remote_side=[id], backref="children")
    versions = relationship("EventVersion", foreign_keys=[EventVersion.event_id], back_populates="event")
    current_version = relationship("EventVersion", foreign_keys=[current_version_id])

class Seminar(Base):
    __tablename__ = "seminars"
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True)
    speaker = Column(String(255), nullable=False)
    educational_points = Column(Integer, nullable=False)

    event = relationship("Event")

class Conference(Base):
    __tablename__ = "conferences"
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True)
    scientific_committee = Column(Text)
    deadline = Column(Date)

    event = relationship("Event")

class CorporateEvent(Base):
    __tablename__ = "corporate_events"
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True)
    entertainment_program = Column(String(500))
    expected_guests = Column(Integer)

    event = relationship("Event")

class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

class EventParticipant(Base):
    __tablename__ = "event_participants"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    participant_id = Column(Integer, ForeignKey("participants.id", ondelete="CASCADE"), nullable=False)
    attendance_status = Column(String(30), default="registered")

    __table_args__ = (UniqueConstraint("event_id", "participant_id"),)

class Venue(Base):
    __tablename__ = "venues"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(500), nullable=False)
    description = Column(String(500))
    capacity = Column(Integer, nullable=False)

class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.id"))
    event_date = Column(Date, nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    description = Column(String(500))

class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    last_check_date = Column(Date, nullable=False)

class EventEquipment(Base):
    __tablename__ = "event_equipment"
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    issue_status = Column(String(50), nullable=False)
    issued_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")