from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List, Optional

from models import Contact
from schemas import ContactCreate, ContactUpdate


def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()


def get_contact_by_id(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def search_contacts(db: Session, query: Optional[str] = None):
    if query:
        search_pattern = f"%{query}%"
        return db.query(Contact).filter(
            (Contact.first_name.ilike(search_pattern)) |
            (Contact.last_name.ilike(search_pattern)) |
            (Contact.email.ilike(search_pattern))
        ).all()
    return []


def get_upcoming_birthdays(db: Session):
    today = date.today()
    future = today + timedelta(days=7)

    # Використовуємо функцію для отримання місяця та дня
    contacts = db.query(Contact).filter(
        (
                (
                    (Contact.birthday.cast(String).like(f"%-%-{today.strftime('%d')}"))
                ) | (
                    (
                            (Contact.birthday.cast(String).like(f"%-%-___"))
                            & (
                                (
                                    (
                                        (Contact.birthday.cast(String).like(f"%-%-%%"))
                                    )
                                )
                            )
                    )
                )
        )
    ).all()

    # Перевірка, чи потрапляє день народження в найближчі 7 днів
    upcoming = []
    for contact in contacts:
        bday_this_year = date(today.year, contact.birthday.month, contact.birthday.day)
        if today <= bday_this_year <= future:
            upcoming.append(contact)
        else:
            # Обробка випадку, коли день народження вже пройшов цього року, але наближається наступного
            bday_next_year = date(today.year + 1, contact.birthday.month, contact.birthday.day)
            if today <= bday_next_year <= future:
                upcoming.append(contact)
    return upcoming