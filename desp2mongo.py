from pymongo import *
import datetime

class journalDB():

    def __init__(self,titol):
        #Crear documento de desplazamiento
        client = MongoClient("mongodb+srv://Willydbuser:Abracadabra1@willymongo-vkgl5.mongodb.net/test?retryWrites=true&w=majority")
        time_inici=datetime.datetime.now().timestamp()

        post = {
            "time_inici": time_inici,
            "titol": titol,
            "punts": [{
                "pos": {
                    "x": 0,             
                    "y": 0
                },
                "time_punt": time_inici
            }]
        }

        db = client.WillyDB
        self.__posts = db.Journals
        self.__post_id = self.__posts.insert_one(post).inserted_id

    def updateJournal(self,x,y):
        #anadir entrada en el array de puntos dentro del doc
        time_punt=datetime.datetime.now().timestamp()
        myquery = { "_id": self.__post_id }
        newvalues = { "$push": { "punts": { "pos":{ "x": x, "y": y }, "time_punt": time_punt } }}

        self.__posts.update_one(myquery, newvalues)