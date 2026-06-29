from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

def get_event_tree_native(db: Session):
    """
    Возвращает иерархическое дерево мероприятий.
    Ограничение глубины – 100 уровней (защита от циклов).
    """
    query = text("""
        WITH RECURSIVE event_tree AS (
            SELECT id, name, parent_id, 1 AS level
            FROM events WHERE parent_id IS NULL
            UNION ALL
            SELECT e.id, e.name, e.parent_id, et.level + 1
            FROM events e
            JOIN event_tree et ON e.parent_id = et.id
            WHERE et.level < 100
        )
        SELECT * FROM event_tree ORDER BY level, id;
    """)
    try:
        result = db.execute(query)
        # ✅ Правильное преобразование строк в словари
        rows = []
        for row in result:
            # row._mapping даёт доступ к полям по имени, а dict() превращает в словарь
            rows.append(dict(row._mapping))
        return rows
    except Exception as e:
        logger.error(f"Ошибка выполнения запроса дерева: {e}", exc_info=True)
        raise

def get_seminars_native(db: Session):
    query = text("""
        SELECT e.id, e.name, e.status, e.budget,
               s.speaker, s.educational_points
        FROM events e
        JOIN seminars s ON e.id = s.event_id;
    """)
    result = db.execute(query)
    return [dict(row._mapping) for row in result]

def get_event_versions_native(db: Session, event_id: int):
    query = text("""
        SELECT version_number, description_text, changed_at, changed_by
        FROM event_versions
        WHERE event_id = :event_id
        ORDER BY version_number;
    """)
    result = db.execute(query, {"event_id": event_id})
    return [dict(row._mapping) for row in result]