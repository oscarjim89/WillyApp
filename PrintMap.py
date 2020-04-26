from pymongo import *

class PrintMap():

    def __init__(self,id,res=10):

        client = MongoClient("mongodb+srv://Willydbuser:Abracadabra1@willymongo-vkgl5.mongodb.net/test?retryWrites=true&w=majority")
        db = client.WillyDB
        self.__posts = db.Journals
        self.__journal = self.__posts.find_one({"_id": id})
        self.__count = print(len(self.__journal["punts"]))
        self.__res = res

    def printSVG(self):

        x1 = 50
        y1 = 50
        image = "<div style=\"height: 500px;width: 500px;\"><svg height=\"100%\" width=\"100%\">"

        for i in range(self.__res):
            x1 = x1 + (self.__journal["punts"][i]["pos"]["x"]*self.__res)
            y1 = y1 - (self.__journal["punts"][i]["pos"]["y"]*self.__res)

            x2 = x1 + (self.__journal["punts"][i+1]["pos"]["x"]*self.__res)
            y2 = y1 - (self.__journal["punts"][i+1]["pos"]["y"]*self.__res)

            image = image + "<line x1=\""+x1+"%\" y1=\""+y1+"%\" x2=\""+x2+"%\" y2=\""+y2+"%\" style=\"stroke:rgb(255,0,0);stroke-width:2\" />"

        image = image + "</svg></div>"

        dirFichero = './templates/prova.html'
        fichero = open(dirFichero, 'w')
        fichero.write(image)
        fichero.close()

        return image

    #def updateSVG(self):
