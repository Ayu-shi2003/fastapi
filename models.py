from sqlalchemy import String, Integer, ForeignKey, create_engine, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Database URL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase"
engine = create_engine(SQLALCHEMY_DATABASE_URL)


class Base(DeclarativeBase):
    pass


# -------------------------
# ONE-TO-MANY (User → Address)
# -------------------------
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)

    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String)
    state: Mapped[str] = mapped_column(String)
    zip_code: Mapped[int] = mapped_column(Integer)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")


# -------------------------
# MANY-TO-MANY (Student ↔ Course)
# -------------------------

# Association Table
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", ForeignKey("students.id"), primary_key=True),
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
)

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    courses: Mapped[list["Course"]] = relationship(
        secondary=student_course,
        back_populates="students"
    )


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)

    students: Mapped[list["Student"]] = relationship(
        secondary=student_course,
        back_populates="courses"
    )


# Create all tables
Base.metadata.create_all(engine)
