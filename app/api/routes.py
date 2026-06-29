from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, services, native_sql
from typing import List
import logging
import traceback

logger = logging.getLogger(__name__)

router = APIRouter()

# ----- Organizers -----
@router.post("/organizers/", response_model=schemas.Organizer)
def create_organizer(organizer: schemas.OrganizerCreate, db: Session = Depends(get_db)):
    return crud.create_organizer(db, organizer)

@router.get("/organizers/", response_model=List[schemas.Organizer])
def list_organizers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_organizers(db, skip, limit)

@router.get("/organizers/{organizer_id}", response_model=schemas.Organizer)
def get_organizer(organizer_id: int, db: Session = Depends(get_db)):
    org = crud.get_organizer(db, organizer_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organizer not found")
    return org

@router.put("/organizers/{organizer_id}", response_model=schemas.Organizer)
def update_organizer(organizer_id: int, organizer: schemas.OrganizerCreate, db: Session = Depends(get_db)):
    org = crud.update_organizer(db, organizer_id, organizer)
    if not org:
        raise HTTPException(status_code=404, detail="Organizer not found")
    return org

@router.delete("/organizers/{organizer_id}")
def delete_organizer(organizer_id: int, db: Session = Depends(get_db)):
    crud.delete_organizer(db, organizer_id)
    return {"message": "Organizer deleted"}

# ----- Events -----
@router.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_event(db, event)
    except Exception as e:
        error_text = traceback.format_exc()
        logger.error(f"Ошибка создания мероприятия:\n{error_text}")
        raise HTTPException(status_code=500, detail=f"Ошибка создания: {str(e)}")

@router.get("/events/", response_model=List[schemas.EventBrief])   # <-- ИСПРАВЛЕНО
def list_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        events = crud.get_events(db, skip, limit)
        return events
    except Exception as e:
        error_text = traceback.format_exc()
        logger.error(f"Ошибка загрузки мероприятий:\n{error_text}")
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки: {str(e)}")

@router.get("/events/{event_id}", response_model=schemas.Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/events/{event_id}", response_model=schemas.Event)
def update_event(event_id: int, event_update: schemas.EventUpdate, db: Session = Depends(get_db)):
    try:
        event = crud.update_event(db, event_id, event_update)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event
    except Exception as e:
        error_text = traceback.format_exc()
        logger.error(f"Ошибка обновления мероприятия:\n{error_text}")
        raise HTTPException(status_code=500, detail=f"Ошибка обновления: {str(e)}")

@router.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    crud.delete_event(db, event_id)
    return {"message": "Event deleted"}

# ----- Seminars -----
@router.post("/seminars/", response_model=schemas.Seminar)
def create_seminar(seminar: schemas.SeminarCreate, db: Session = Depends(get_db)):
    return crud.create_seminar(db, seminar)

@router.get("/seminars/", response_model=List[schemas.Seminar])
def list_seminars(db: Session = Depends(get_db)):
    return crud.get_seminars(db)

@router.get("/seminars/{event_id}", response_model=schemas.Seminar)
def get_seminar(event_id: int, db: Session = Depends(get_db)):
    sem = crud.get_seminar(db, event_id)
    if not sem:
        raise HTTPException(status_code=404, detail="Seminar not found")
    return sem

@router.put("/seminars/{event_id}", response_model=schemas.Seminar)
def update_seminar(event_id: int, seminar_update: schemas.SeminarUpdate, db: Session = Depends(get_db)):
    sem = crud.update_seminar(db, event_id, seminar_update)
    if not sem:
        raise HTTPException(status_code=404, detail="Seminar not found")
    return sem

@router.delete("/seminars/{event_id}")
def delete_seminar(event_id: int, db: Session = Depends(get_db)):
    crud.delete_seminar(db, event_id)
    return {"message": "Seminar deleted"}

# ----- Conferences -----
@router.post("/conferences/", response_model=schemas.Conference)
def create_conference(conf: schemas.ConferenceCreate, db: Session = Depends(get_db)):
    return crud.create_conference(db, conf)

@router.get("/conferences/", response_model=List[schemas.Conference])
def list_conferences(db: Session = Depends(get_db)):
    return crud.get_conferences(db)

@router.get("/conferences/{event_id}", response_model=schemas.Conference)
def get_conference(event_id: int, db: Session = Depends(get_db)):
    conf = crud.get_conference(db, event_id)
    if not conf:
        raise HTTPException(status_code=404, detail="Conference not found")
    return conf

@router.put("/conferences/{event_id}", response_model=schemas.Conference)
def update_conference(event_id: int, conf_update: schemas.ConferenceUpdate, db: Session = Depends(get_db)):
    conf = crud.update_conference(db, event_id, conf_update)
    if not conf:
        raise HTTPException(status_code=404, detail="Conference not found")
    return conf

@router.delete("/conferences/{event_id}")
def delete_conference(event_id: int, db: Session = Depends(get_db)):
    crud.delete_conference(db, event_id)
    return {"message": "Conference deleted"}

# ----- Corporate Events -----
@router.post("/corporate_events/", response_model=schemas.CorporateEvent)
def create_corporate_event(corp: schemas.CorporateEventCreate, db: Session = Depends(get_db)):
    return crud.create_corporate_event(db, corp)

@router.get("/corporate_events/", response_model=List[schemas.CorporateEvent])
def list_corporate_events(db: Session = Depends(get_db)):
    return crud.get_corporate_events(db)

@router.get("/corporate_events/{event_id}", response_model=schemas.CorporateEvent)
def get_corporate_event(event_id: int, db: Session = Depends(get_db)):
    corp = crud.get_corporate_event(db, event_id)
    if not corp:
        raise HTTPException(status_code=404, detail="Corporate event not found")
    return corp

@router.put("/corporate_events/{event_id}", response_model=schemas.CorporateEvent)
def update_corporate_event(event_id: int, corp_update: schemas.CorporateEventUpdate, db: Session = Depends(get_db)):
    corp = crud.update_corporate_event(db, event_id, corp_update)
    if not corp:
        raise HTTPException(status_code=404, detail="Corporate event not found")
    return corp

@router.delete("/corporate_events/{event_id}")
def delete_corporate_event(event_id: int, db: Session = Depends(get_db)):
    crud.delete_corporate_event(db, event_id)
    return {"message": "Corporate event deleted"}

# ----- Versions -----
@router.get("/events/{event_id}/versions/")
def get_event_versions(event_id: int, db: Session = Depends(get_db)):
    return crud.get_event_versions(db, event_id)

@router.get("/events/{event_id}/versions-native/")
def get_event_versions_native(event_id: int, db: Session = Depends(get_db)):
    return native_sql.get_event_versions_native(db, event_id)

# ----- Tree -----
@router.get("/events/tree/")
def get_event_tree(db: Session = Depends(get_db)):
    try:
        return services.EventService.get_event_tree(db)
    except Exception as e:
        error_text = traceback.format_exc()
        logger.error(f"Ошибка в /events/tree/:\n{error_text}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения дерева: {str(e)}")

# ----- Participants -----
@router.post("/participants/", response_model=schemas.Participant)
def create_participant(participant: schemas.ParticipantCreate, db: Session = Depends(get_db)):
    return crud.create_participant(db, participant)

@router.get("/participants/", response_model=List[schemas.Participant])
def list_participants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_participants(db, skip, limit)

@router.get("/participants/{participant_id}", response_model=schemas.Participant)
def get_participant(participant_id: int, db: Session = Depends(get_db)):
    p = crud.get_participant(db, participant_id)
    if not p:
        raise HTTPException(status_code=404, detail="Participant not found")
    return p

@router.put("/participants/{participant_id}", response_model=schemas.Participant)
def update_participant(participant_id: int, participant: schemas.ParticipantCreate, db: Session = Depends(get_db)):
    p = crud.update_participant(db, participant_id, participant)
    if not p:
        raise HTTPException(status_code=404, detail="Participant not found")
    return p

@router.delete("/participants/{participant_id}")
def delete_participant(participant_id: int, db: Session = Depends(get_db)):
    crud.delete_participant(db, participant_id)
    return {"message": "Participant deleted"}
