from mycroft import MycroftSkill, intent_file_handler


class Farting(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('farting.intent')
    def handle_farting(self, message):
        self.speak_dialog('farting')


def create_skill():
    return Farting()

