from sqlalchemy.orm import sessionmaker,joinedload,subqueryload,selectinload,immediateload
from sqlalchemy import and_, func,or_,not_
from models import Course, Student, User,engine,Address
import random

Session = sessionmaker(bind=engine)

session=Session()

#users=session.query(User).filter_by(id=1).one_or_none()

#session.delete(users)
#session.commit()

#print("id:",users.id)
#print("name:",users.name)
#print("age:",users.age)

#for user in users:
#    print(f"user_id:{user.id},name:{user.name},age:{user.age}")

#names =["ayushi parekj","siddh parekh","dev parekh","sejal parekh","shreya parekh"]
#ages = [20,21,22,25,26,28,29,30]

#for x in range(20):
 #   user = User(name=random.choice(names),age=random.choice(ages))
  #  session.add(user)

#session.commit()

#query all users by age(ascending)
#users=session.query(User).order_by(User.age.desc()).all()
#for user in users:
#   print(f"user_age:{user.age},name:{user.name}")

#query all users
#users_all=session.query(User).all()

#query all users with age greater then  or equal to 25
#users_filtered=session.query(User).filter(User.age >=25, User.name == "dev parekh").all()

#print("All users:",len(users_all))
#print("filtered users",len(users_filtered))

#query all users with age=25
#users=session.query(User).filter_by(age=25).all()

#for user in users:
   # print(f"user age:{user.age}")


#userss=session.query(User).where(and_(User.age >=15,User.name=="dev parekh")).all()

#userss=(
#   session.query(User).where(
 #       or_(
  #          not_(User.name == "siddh parekh"),
   #         and_(
    #            User.age > 25,
     #           User.age <30
      #      )
       # )
   # )
#)

#for user in userss:
 #   print(f"{user.age}-{user.name}")

#group users by age
#users = session.query(User.age).group_by(User.age).all()
#print(users)


#by using all the functions,groupby,filtering,orderby in one
#users_tuple=(
#  session.query(User.age,func.count(User.id))
#   .filter(User.age>24)
 #   .order_by(User.age)
#  .filter(User.age < 50)
 #   .group_by(User.age)
  #  .all()
#)

#for age,count in users_tuple:
#   print(f"Age:{age}-{count} users")

'''from sqlalchemy import func

users = (
    session.query(User.age, func.count(User.id))
    .filter(User.name == "sejal parekh")
    .group_by(User.age)
    .all()
)

for age, count in users:
    print(f"age: {age}, count of users: {count}")'''

#
'''u1 = User(name="Ayushi", age=22)

# Create addresses
a1 = Address(city="Jamnagar", state="Gujarat", zip_code=361008)
a2 = Address(city="Ahmedabad", state="Gujarat", zip_code=380001)

# Add addresses to user
u1.addresses = [a1, a2]

session.add(u1)
session.commit()

print("Data inserted successfully!")

user = session.query(User).filter_by(name="Ayushi").first()

print("Name:", user.name)
for addr in user.addresses:
    print(addr.city, addr.state, addr.zip_code)


address = session.query(Address).first()
print(address.city, "belongs to:", address.user.name)'''



'''math = Course(title="mathematics")
physics = Course(title="physics")
bill = Student(name="Bill",courses=[math,physics])
rob = Student(name="rob",courses=[math])

session.add_all ([math,physics,bill,rob])
session.commit()'''

'''rob = session.query(Student).filter(Student.name == "Bill").first()

if rob is None:
    print("Student not found")
else:
    courses = [course.title for course in rob.courses]
    print(courses)'''

'''result = session.query(User,Address).join(Address,full=True).filter(User.addresses == None,Address.user_id == None).all()
print(result)'''

#left outer join
'''result = session.query(User).outerjoin(Address).all()
print(result)'''

#right outer join
'''result=session.query(Address).outerjoin(User).all()
print(result)'''

#full outer join
'''left_join = session.query(User,Address).outerjoin(Address) # get all users
right_join = session.query(User,Address).outerjoin(User) # get all addresses
full_outer_join = left_join.union(right_join)
print(full_outer_join)'''

#joinedload
'''query = session.query(User).options(joinedload(User.addresses))
print(query)'''

#subquery
'''query=session.query(User).options(subqueryload(User.addresses))
print(query.all())'''

#selectinload
'''query=session.query(User).options(selectinload(User.addresses))
print(query.all())'''

#immediateload
query=session.query(User).options(immediateload(User.addresses))
print(query.all())