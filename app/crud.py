from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
from app import models, schemas
from typing import Optional

# ----- Organizers -----
def get_organizer(db: Session, organizer_id: int):
    return db.query(models.Organizer).filter(models.Organizer.id == organizer_id).first()

def get_organizers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Organizer).offset(skip).limit(limit).all()

def create_organizer(db: Session, organizer: schemas.OrganizerCreate):
    db_organizer = models.Organizer(**organizer.model_dump())
    db.add(db_organizer)
    db.commit()
    db.refresh(db_organizer)
    return db_organizer

def update_organizer(db: Session, organizer_id: int, organizer_update: schemas.OrganizerCreate):
    db_organizer = get_organizer(db, organizer_id)
    if not db_organizer:
        return None
    for key, value in organizer_update.model_dump().items():
        setattr(db_organizer, key, value)
    db.commit()
    db.refresh(db_organizer)
    return db_organizer

def delete_organizer(db: Session, organizer_id: int):
    db.query(models.Organizer).filter(models.Organizer.id == organizer_id).delete()
    db.commit()

# ----- Events -----
def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).options(
        selectinload(models.Event.organizer),
        selectinload(models.Event.children),
        selectinload(models.Event.versions)
    ).first()

def get_events(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.Event).offset(skip).limit(limit).options(
            selectinload(models.Event.organizer),
            selectinload(models.Event.children)
        ).all()
    except Exception as e:
        print(f"Ошибка в get_events: {e}")
        # Возвращаем без подгрузки связанных данных, если ошибка
        return db.query(models.Event).offset(skip).limit(limit).all()

def create_event(db: Session, event: schemas.EventCreate):
    # 1. Создаём мероприятие
    db_event = models.Event(**event.model_dump())
    db_event.current_version_id = None
    db.add(db_event)
    db.flush()

    # 2. Создаём первую версию описания
    first_version = models.EventVersion(
        event_id=db_event.id,
        version_number=1,
        description_text=db_event.description,
        changed_by="system"
    )
    db.add(first_version)
    db.flush()

    # 3. Обновляем ссылку на текущую версию
    db_event.current_version_id = first_version.id
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event_update: schemas.EventUpdate):
    db_event = get_event(db, event_id)
    if not db_event:
        return None

    old_description = db_event.description
    update_data = event_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_event, key, value)

    if 'description' in update_data and update_data['description'] != old_description:
        max_version = db.query(models.EventVersion).filter(
            models.EventVersion.event_id == db_event.id
        ).order_by(models.EventVersion.version_number.desc()).first()
        next_version = (max_version.version_number + 1) if max_version else 1

        new_version = models.EventVersion(
            event_id=db_event.id,
            version_number=next_version,
            description_text=db_event.description,
            changed_by="system"
        )
        db.add(new_version)
        db.flush()

        db_event.current_version_id = new_version.id

    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db.query(models.Event).filter(models.Event.id == event_id).delete()
    db.commit()

# ----- Seminars -----
def get_seminar(db: Session, event_id: int):
    return db.query(models.Seminar).filter(models.Seminar.event_id == event_id).options(selectinload(models.Seminar.event)).first()

def get_seminars(db: Session):
    return db.query(models.Seminar).options(selectinload(models.Seminar.event)).all()

def create_seminar(db: Session, seminar: schemas.SeminarCreate):
    db_seminar = models.Seminar(**seminar.model_dump())
    db.add(db_seminar)
    db.commit()
    db.refresh(db_seminar)
    return db_seminar

def update_seminar(db: Session, event_id: int, seminar_update: schemas.SeminarUpdate):
    db_seminar = get_seminar(db, event_id)
    if not db_seminar:
        return None
    update_data = seminar_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_seminar, key, value)
    db.commit()
    db.refresh(db_seminar)
    return db_seminar

def delete_seminar(db: Session, event_id: int):
    db.query(models.Seminar).filter(models.Seminar.event_id == event_id).delete()
    db.commit()

# ----- Conferences -----
def get_conference(db: Session, event_id: int):
    return db.query(models.Conference).filter(models.Conference.event_id == event_id).options(selectinload(models.Conference.event)).first()

def get_conferences(db: Session):
    return db.query(models.Conference).options(selectinload(models.Conference.event)).all()

def create_conference(db: Session, conference: schemas.ConferenceCreate):
    db_conf = models.Conference(**conference.model_dump())
    db.add(db_conf)
    db.commit()
    db.refresh(db_conf)
    return db_conf

def update_conference(db: Session, event_id: int, conf_update: schemas.ConferenceUpdate):
    db_conf = get_conference(db, event_id)
    if not db_conf:
        return None
    update_data = conf_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_conf, key, value)
    db.commit()
    db.refresh(db_conf)
    return db_conf

def delete_conference(db: Session, event_id: int):
    db.query(models.Conference).filter(models.Conference.event_id == event_id).delete()
    db.commit()

# ----- Corporate Events -----
def get_corporate_event(db: Session, event_id: int):
    return db.query(models.CorporateEvent).filter(models.CorporateEvent.event_id == event_id).options(selectinload(models.CorporateEvent.event)).first()

def get_corporate_events(db: Session):
    return db.query(models.CorporateEvent).options(selectinload(models.CorporateEvent.event)).all()

def create_corporate_event(db: Session, corp: schemas.CorporateEventCreate):
    db_corp = models.CorporateEvent(**corp.model_dump())
    db.add(db_corp)
    db.commit()
    db.refresh(db_corp)
    return db_corp

def update_corporate_event(db: Session, event_id: int, corp_update: schemas.CorporateEventUpdate):
    db_corp = get_corporate_event(db, event_id)
    if not db_corp:
        return None
    update_data = corp_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_corp, key, value)
    db.commit()
    db.refresh(db_corp)
    return db_corp

def delete_corporate_event(db: Session, event_id: int):
    db.query(models.CorporateEvent).filter(models.CorporateEvent.event_id == event_id).delete()
    db.commit()

# ----- Versions -----
def get_event_versions(db: Session, event_id: int):
    return db.query(models.EventVersion).filter(models.EventVersion.event_id == event_id).order_by(models.EventVersion.version_number).all()

# ----- Participants -----
def create_participant(db: Session, participant: schemas.ParticipantCreate):
    db_participant = models.Participant(**participant.model_dump())
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

def get_participants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Participant).offset(skip).limit(limit).all()

def get_participant(db: Session, participant_id: int):
    return db.query(models.Participant).filter(models.Participant.id == participant_id).first()

def update_participant(db: Session, participant_id: int, participant_update: schemas.ParticipantCreate):
    db_participant = get_participant(db, participant_id)
    if not db_participant:
        return None
    for key, value in participant_update.model_dump().items():
        setattr(db_participant, key, value)
    db.commit()
    db.refresh(db_participant)
    return db_participant

def delete_participant(db: Session, participant_id: int):
    db.query(models.Participant).filter(models.Participant.id == participant_id).delete()
    db.commit()
