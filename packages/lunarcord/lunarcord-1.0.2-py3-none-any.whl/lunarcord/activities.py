PLAYING = 0
STREAMING = 1
LISTENING = 2
WATCHING = 3

ONLINE = 'online'
IDLE = 'idle'
DND = 'dnd'
DO_NOT_DISTURB = DND
DONOTDISTURB = DND
IDLING = IDLE
ACTIVE = ONLINE
INVISIBLE = 'invisible'
INVIS = INVISIBLE
OFFLINE = INVIS
INACTIVE = INVIS

from .errors import StatusError

class Activity:
    def __init__(self, type: int, name: str):
        self.type = type
        self.name = name
        
    def toJson(self):
        return {'type': self.type, 'name': self.name}
		
	
class Playing(Activity):
    def __init__(self, game: str):
        super().__init__(PLAYING, game)
		
class Watching(Activity):
    def __init__(self, video: str):
        super().__init__(WATCHING, video)
		
class Streaming(Activity):
    def __init__(self, game: str):
        super().__init__(STREAMING, game)

class Listening(Activity):
    def __init__(self, song: str):
        super().__init__(LISTENING, song)

Game = Playing
Video = Watching
Stream = Streaming
Music = Listening		
ListeningTo = Listening