from pymongo import *
from PrintMap import *

client = MongoClient("mongodb+srv://Willydbuser:Abracadabra1@willymongo-vkgl5.mongodb.net/test?retryWrites=true&w=majority")

db = client.WillyDB
posts = db.Journals
journal = posts.find_one({"titol": "prueba_print_01"})
a = PrintMap(journal["_id"])
a.printSVG()
