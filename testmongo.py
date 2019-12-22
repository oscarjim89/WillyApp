from pymongo import *

client = MongoClient("mongodb+srv://Willydbuser:Abracadabra1@willymongo-vkgl5.mongodb.net/test?retryWrites=true&w=majority")

db = client.WillyDB

post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"]}

posts = db.Journals
post_id = posts.insert_one(post).inserted_id
print(post_id)