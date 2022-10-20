"""
skill farting-skill
Copyright (C) 2020  Andreas Lorensen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import random
import time
from datetime import datetime, timedelta
from os import listdir, path
from os.path import abspath, dirname, isfile, join, splitext
from tinytag import TinyTag

from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.audioservice import AudioService
from mycroft.messagebus.message import Message

class CalamityWouldYouRather(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        # retained to avoid errors 
        valid_codecs = ['.mp3']
        self.path_to_sound_files = path.join(abspath(dirname(__file__)), 'sounds')
        self.sound_files = [f for f in listdir(self.path_to_sound_files) if splitext(f)[1] in valid_codecs]
        self.audio_service = AudioService(self.bus)
        self.random_farting = False  # flag to indicate whether random farting mode is active
        self.counter = 0  # variable to increment to make the scheduled event unique

    def handle_fart_event(self, message):
        # repurposed to randomly schedule next random comment
        self.log.info("Handling fart event")
        if not self.random_farting:
            return
        self.cancel_scheduled_event('random_fart'+str(self.counter))
        self.counter += 1
        self.schedule_event(self.handle_fart_event, datetime.now() 
                            + timedelta(seconds=random.randrange(30, 60)),
                            name='random_fart'+str(self.counter))
        self.fart_and_comment()

    @intent_file_handler('random.intent')
    def handle_random_intent(self, message):
        # repurposed to start random comments
        self.log.info("Triggering random farting")
        #self.speak_dialog('random_farting')
        self.random_farting = True
        self.schedule_event(self.handle_fart_event, datetime.now()
                            + timedelta(seconds=random.randrange(30, 60)),
                            name='random_fart'+str(self.counter))

    @intent_file_handler('farting.intent')
    def fart_and_comment(self):
        # repurposed to generate all random comments
        self.log.info("Comment")
        #sound_file = path.join(self.path_to_sound_files,
        #                       random.choice(self.sound_files))
        #sound_url = 'file://' + path.join(self.path_to_sound_files,
        #                                  random.choice(self.sound_files))
        #tag = TinyTag.get(sound_file)
        #self.audio_service.play(tracks=sound_url)
        #self.log.info("Fart duration " + str(int(tag.duration)))
        #time.sleep(int(tag.duration))
        self.speak_dialog('noise')
    
    @intent_file_handler('halt_farting.intent')
    def halt_farting(self, message):
        self.log.info("Stopping")
        # repurposed to stop random comments
        if self.random_farting:
            self.log.info("Stopping random farting event")
            #self.speak_dialog('cancel')
            self.random_farting = False
            self.cancel_scheduled_event('random_fart'+str(self.counter))


def create_skill():
    return CalamityWouldYouRather()

