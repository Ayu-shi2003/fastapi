from datetime import date, datetime
from sqlalchemy import (
    String, Integer, ForeignKey, create_engine, Date, DateTime
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

# Database URL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create Session factory
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


class Appointment(Base):
    __tablename__ = 'appointments'

    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey('doctors.id'))
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'))
    appointment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    notes: Mapped[str] = mapped_column(String)

    doctor: Mapped["Doctor"] = relationship(back_populates="appointments")
    patient: Mapped["Patient"] = relationship(back_populates="appointments")


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    speciality: Mapped[str] = mapped_column(String)

    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="doctor",
        cascade="all, delete-orphan"
    )


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    dob: Mapped[date] = mapped_column(Date)

    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="patient",
        cascade="all, delete-orphan"
    )


# Create tables
Base.metadata.create_all(engine)

# ---- INSERT DATA ----
session = SessionLocal()

'''dr_smith = Doctor(name='Dr Smith', speciality="Cardiology")
john_doe = Patient(name="John Doe", dob=date(2003, 11, 7))
appointment = Appointment(
    doctor=dr_smith,
    patient=john_doe,
    notes="Routine checkup"
)

session.add_all([dr_smith, john_doe, appointment])
session.commit()
session.close()'''

#find all appointments for dr.smith
appointments_for_drsmith=session.query(Appointment).filter(Appointment.doctor.has(name='Dr Smith')).all()
print(appointments_for_drsmith)

#find all appointments for patient
appointment_for_patient = session.query(Appointment).filter(Appointment.patient.has(name='John Doe')).all()
print(appointment_for_patient)

