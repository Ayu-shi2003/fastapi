from sqlalchemy import String, Integer, ForeignKey, create_engine, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship,sessionmaker




# Database URL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(bind=engine)

session=Session()



class Base(DeclarativeBase):
    pass

#One-to-one relationship:-
class Person(Base): #table model name Person
    __tablename__ = "persons"  #tablename persons

    id:Mapped[int] = mapped_column(primary_key=True)  #created id column for person 
    name:Mapped[str] = mapped_column(String)    #created name column for person
    passport: Mapped["Passport"] = relationship(back_populates="person",uselist=False)


class Passport(Base):
    __tablename__ = "passports"

    id:Mapped[int] = mapped_column(primary_key=True)
    passport_number : Mapped[str] = mapped_column(String)
    person_id : Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person:Mapped["Person"] = relationship(back_populates="passport")

Base.metadata.create_all(engine)

p=Person(name="Ayushi")
pp = Passport(passport_number="IND12345",person=p)
session.add_all([p,pp])
session.commit()