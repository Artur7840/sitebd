from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

def init_db():
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже организаторы
        if db.query(models.Organizer).count() > 0:
            print("База данных уже содержит данные, пропускаем инициализацию")
            return

        print("Добавление тестовых данных...")

        # --- Организаторы ---
        org1 = models.Organizer(
            full_name="Иванов Иван Иванович",
            phone="+7(999)123-45-67",
            email="ivanov@org.ru",
            position="Зав. отделом мероприятий"
        )
        org2 = models.Organizer(
            full_name="Петрова Анна Сергеевна",
            phone="+7(999)234-56-78",
            email="petrova@org.ru",
            position="Организатор"
        )
        org3 = models.Organizer(
            full_name="Сидоров Алексей Петрович",
            phone="+7(999)345-67-89",
            email="sidorov@org.ru",
            position="Координатор"
        )
        db.add_all([org1, org2, org3])
        db.flush()

        # --- Участники ---
        part1 = models.Participant(
            full_name="Смирнов Алексей Владимирович",
            phone="+7(900)111-22-33",
            role="Слушатель"
        )
        part2 = models.Participant(
            full_name="Козлова Мария Дмитриевна",
            phone="+7(900)222-33-44",
            role="Спикер"
        )
        part3 = models.Participant(
            full_name="Васильев Дмитрий Олегович",
            phone="+7(900)333-44-55",
            role="Слушатель"
        )
        part4 = models.Participant(
            full_name="Морозова Екатерина Андреевна",
            phone="+7(900)444-55-66",
            role="Слушатель"
        )
        db.add_all([part1, part2, part3, part4])
        db.flush()

        # --- Мероприятия ---
        event1 = models.Event(
            name="Корпоративный семинар по SQL",
            event_type="Seminar",
            description="Обучение сотрудников основам SQL",
            status="completed",
            budget=15000,
            organizer_id=org1.id
        )
        event2 = models.Event(
            name="Ежегодный корпоратив",
            event_type="Corporate",
            description="Тимбилдинг коллектива",
            status="planning",
            budget=50000,
            organizer_id=org2.id
        )
        event3 = models.Event(
            name="Конференция по базам данных",
            event_type="Conference",
            description="Обмен опытом специалистов БД",
            status="completed",
            budget=30000,
            organizer_id=org3.id
        )
        db.add_all([event1, event2, event3])
        db.flush()

        # --- Создаём первую версию для каждого мероприятия ---
        def create_first_version(event):
            version = models.EventVersion(
                event_id=event.id,
                version_number=1,
                description_text=event.description,
                changed_by="system"
            )
            db.add(version)
            db.flush()
            event.current_version_id = version.id

        create_first_version(event1)
        create_first_version(event2)
        create_first_version(event3)

        # --- Наследники ---
        seminar = models.Seminar(
            event_id=event1.id,
            speaker="Доцент Смирнов А.И.",
            educational_points=16
        )
        db.add(seminar)

        conference = models.Conference(
            event_id=event3.id,
            scientific_committee="Члены IEEE",
            deadline="2026-05-01"
        )
        db.add(conference)

        corporate = models.CorporateEvent(
            event_id=event2.id,
            entertainment_program="Квест, фуршет, дискотека",
            expected_guests=120
        )
        db.add(corporate)

        # Фиксируем всё
        db.commit()
        print("Тестовые данные успешно добавлены!")

    except Exception as e:
        print(f"Ошибка при инициализации БД: {e}")
        db.rollback()
    finally:
        db.close()
