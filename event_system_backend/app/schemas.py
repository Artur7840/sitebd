from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List

class OrganizerBase(BaseModel):
    full_name: str
    phone: str
    email: str
    position: str

class OrganizerCreate(OrganizerBase):
    pass

class Organizer(OrganizerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class EventVersionBase(BaseModel):
    version_number: int
    description_text: str
    changed_at: datetime
    changed_by: str

class EventVersion(EventVersionBase):
    id: int
    event_id: int

class EventBase(BaseModel):
    name: str
    event_type: str
    description: str
    status: str
    budget: Optional[int] = 0
    organizer_id: Optional[int] = None
    parent_id: Optional[int] = None

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    budget: Optional[int] = None
    organizer_id: Optional[int] = None
    parent_id: Optional[int] = None

class Event(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime
    current_version_id: Optional[int] = None
    organizer: Optional[Organizer] = None
    children: List["Event"] = []
    versions: List[EventVersion] = []

    model_config = ConfigDict(from_attributes=True)

# ---- Наследники ----
class SeminarBase(BaseModel):
    event_id: int
    speaker: str
    educational_points: int

class SeminarCreate(SeminarBase):
    pass

class SeminarUpdate(BaseModel):
    speaker: Optional[str] = None
    educational_points: Optional[int] = None

class Seminar(SeminarBase):
    event: Optional[Event] = None

class ConferenceBase(BaseModel):
    event_id: int
    scientific_committee: Optional[str] = None
    deadline: Optional[date] = None

class ConferenceCreate(ConferenceBase):
    pass

class ConferenceUpdate(BaseModel):
    scientific_committee: Optional[str] = None
    deadline: Optional[date] = None

class Conference(ConferenceBase):
    event: Optional[Event] = None

class CorporateEventBase(BaseModel):
    event_id: int
    entertainment_program: Optional[str] = None
    expected_guests: Optional[int] = None

class CorporateEventCreate(CorporateEventBase):
    pass

class CorporateEventUpdate(BaseModel):
    entertainment_program: Optional[str] = None
    expected_guests: Optional[int] = None

class CorporateEvent(CorporateEventBase):
    event: Optional[Event] = None

# ---- Остальные ----
class ParticipantBase(BaseModel):
    full_name: str
    phone: str
    role: str

class ParticipantCreate(ParticipantBase):
    pass

class Participant(ParticipantBase):
    id: int
    created_at: datetime

class EventParticipantCreate(BaseModel):
    event_id: int
    participant_id: int
    attendance_status: Optional[str] = "registered"

class EventParticipant(EventParticipantCreate):
    id: int

class VenueBase(BaseModel):
    address: str
    description: Optional[str] = None
    capacity: int

class VenueCreate(VenueBase):
    pass

class Venue(VenueBase):
    id: int

class ScheduleCreate(BaseModel):
    event_id: int
    venue_id: Optional[int] = None
    event_date: date
    start_time: datetime
    end_time: datetime
    description: Optional[str] = None

class Schedule(ScheduleCreate):
    id: int

class EquipmentBase(BaseModel):
    name: str
    status: str
    last_check_date: date

class EquipmentCreate(EquipmentBase):
    pass

class Equipment(EquipmentBase):
    id: int

class EventEquipmentCreate(BaseModel):
    equipment_id: int
    event_id: int
    issue_status: str

class EventEquipment(EventEquipmentCreate):
    id: int
    issued_at: datetime