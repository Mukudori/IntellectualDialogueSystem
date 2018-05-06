
class User(object):
    def __init__(self):
        super().__init__()
        self.setUser(id=0, first_name='None', last_name='None',
                 username='None')

    def setUser(self, id=0, first_name='None', last_name='None',
                 username='None'):
        self.id = id
        self.first_name = first_name
        self.last_name=last_name
        self.username=username

class Chat(object):
    def __init__(self):
        super().__init__()
        self.setID(0)

    def setID(self, id):
        self.id=id


class UserMessage(object):
    def __init__(self, text=0):
        super().__init__()
        self.from_user = User()
        self.chat = Chat()
        self.text = text

    def setText(self, text):
        self.text=text
    

