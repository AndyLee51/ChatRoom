from modle.tables import User,ChatRoom,Members,History
import random
# for i in range(1,6):
#     user = User.get_one({"name":"user"+str(i*2)})
#     print(user)    
#     # room = ChatRoom(room_name="我的聊天室"+str(i),owner=user["_id"])
#     # room.save()

# for i in range(7,10):
#     room = ChatRoom(room_name="我的聊天室"+str(i),owner=User.get_one({"name":"user2"})["_id"])
#     insert = room.save()
#     room_id=insert.inserted_id
print(ChatRoom.get_one({"room_name":"asdsad"}))
# for i in ChatRoom.get_all():
    # print(i)
    # for j in range(7):
    #     user_num = random.randint(1,10)
    #     while (user_num in a) or (user_num==i):
    #         user_num = random.randint(1,10)
    #     a.append(user_num)
    #     user_id = User.get_one({"name":"user"+str(user_num)})["_id"]
    #     members = Members(room=room_id,member=user_id)
    #     members.save()

# room = ChatRoom(room_name="我的聊天室",owner=User.get_one({"name":"lixin"})["_id"])
# room.save()

# member = Members(room_foregin=ChatRoom.get_one({"room_name":"我的聊天室"})["_id"],member_foreign=User.get_one({"name":"lixin"})["_id"])
# member.save()