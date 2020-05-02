from pymongo import *

class PrintMap():

    def __init__(self,id,res=2):

        client = MongoClient("mongodb+srv://Willydbuser:Abracadabra1@willymongo-vkgl5.mongodb.net/test?retryWrites=true&w=majority")
        db = client.WillyDB
        self.__posts = db.Journals
        self.__journal = self.__posts.find_one({"_id": id})
        self.__count = len(self.__journal["punts"])
        self.__res = res

    def printSVG(self):

        xi = 50
        yi = 50

        image = "<!DOCTYPE html><html><div style=\"height: 500px;width: 500px;\"><svg height=\"100%\" width=\"100%\">"

        for i in range(self.__count):
            x1 = xi + (self.__journal["punts"][i]["pos"]["x"]*self.__res)
            y1 = yi - (self.__journal["punts"][i]["pos"]["y"]*self.__res)

            try:
                x2 = xi + (self.__journal["punts"][i+1]["pos"]["x"]*self.__res)
                y2 = yi - (self.__journal["punts"][i+1]["pos"]["y"]*self.__res)
            except IndexError:
                #x2 = xi + (self.__journal["punts"][0]["pos"]["x"]*self.__res)
                #y2 = yi - (self.__journal["punts"][0]["pos"]["y"]*self.__res)
                
            image = image + "<line x1=\""+str(x1)+"%\" y1=\""+str(y1)+"%\" x2=\""+str(x2)+"%\" y2=\""+str(y2)+"%\" style=\"stroke:rgb(255,0,0);stroke-width:2\" />"            


        image = image + "</svg></div></html>"

        dirFichero = './templates/prova.html'
        fichero = open(dirFichero, 'w')
        fichero.write(image)
        fichero.close()

        return image

    #def updateSVG(self):
