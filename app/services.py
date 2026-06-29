from app import crud, native_sql
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class EventService:
    @staticmethod
    def get_event_with_history(db: Session, event_id: int):
        event = crud.get_event(db, event_id)
        versions = crud.get_event_versions(db, event_id)
        return {"event": event, "versions": versions}

    @staticmethod
    def get_event_tree(db: Session):
        try:
            return native_sql.get_event_tree_native(db)
        except Exception as e:
            logger.error(f"EventService.get_event_tree ошибка: {e}")
            raise

    @staticmethod
    def get_seminars(db: Session):
        return native_sql.get_seminars_native(db)