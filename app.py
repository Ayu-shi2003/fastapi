from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_,or_,not_
from models import User,engine
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

users = session.query(User.age).group_by(User.age).all()
print(users)