class EntryPoint():

    @LinkRelateion("Info")
    Info: Link[Info]

    @LinkRelateion("ProcessingSteps")
    @Mandatory
    ProcessingSteps: MandatoryLink[Info]

    user: User = Info.navigate().User.navigate()
    seld["CreateUser"].Excecute()


    entrypoint.navigate("Info")
    def CreateUser(dojgpsj):

class Info():

    CurrentUser: Link[User]

class User():

class Job():

    name = ""
    title = ""
    status = ""

