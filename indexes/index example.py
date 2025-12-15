from sqlalchemy import Index, create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass

#we can add in 2 ways index like just add index=true in particular column field or else we can do _tableargs_=(Index("idx_user_name","name")),idx_user_name=indename wherease name=where index is apply on that particular column    

class User(Base): 
    __tablename__ = "users2"   

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    __table_args__=(  #gives extra information for table 
        Index("idxf_user_name","name","id"), #idxf_user_name=indexname,name=index given to this particular column
    )

    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user"
    )
    #defines 1-many relationship with address ,backpopulates=user links back from address


class Address(Base):
    __tablename__ = "address2"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users2.id"),   
        index=True
    )
    #foreign key linking Address.user_id → User.id
    user: Mapped["User"] = relationship(
        back_populates="addresses"
    )
    #relationship back to User table


Base.metadata.create_all(engine) #create tables in database

# insert data
u1 = User(name="Ayushi")
u2 = User(name="Krisha")

a1 = Address(city="Ahmedabad", user=u1)
a2 = Address(city="Rajkot", user=u1)

session.add_all([u1, u2, a1, a2]) #adds data
session.commit() #saves data in database 

'''user = session.query(User).filter(User.name=="Ayushi").first()
print(user.name) 

# fetch
user = session.get(User, 1)
print(user.addresses)'''

'''user_name_index=Index("idxf_user_name",User.name)
user_name_index.create(bind=engine)'''

user=session.query(User).filter(
    User.name=="Ayushi",
    User.id ==1
).first()
print(user.name,user.id) #print the result
#session.query=starts a query for users table,.filter=adds where condition with both columns and this should match the index that we made in tableargs,.first=return first matching row