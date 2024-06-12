from .errors import ParameterError
from .basetypes import Message
import asyncio

class FutureMessage:
    def __init__(self, bot, content: str, channel: int | str):
        '''
        A planned message that can be later sent to the specified channel at any moment and as many times as desired, using its :meth:`send` method.
        
        Parameters
        ----------
        bot: `Lunarcord.Bot`
            The bot client to send the message from.
        
        content: `str`
            The content of the message to send. Must be a string or convertible to string.
            
        channel: `int`, `Lunarcord.Channel`
            The channel to send the message to. Can be a discord snowflake, or a Channel object.
        '''
        
        self.content = content
        self.channel = channel
        self.bot = bot
        
    @property
    def content(self):
        '''
        The future message's content. Must be a string or convertible to string.
        '''
        
        return self.__content__
        
    @content.setter
    def content(self, value):
        if type(value) is not str:
            try: value = str(value)
            except: raise ParameterError(type(value).__name__)
            
        self.__content__ = value
        
    @content.deleter
    def content(self):
        self.__content__ = None

    @property
    def channel(self):
        '''
        The channel in which the planned message will be sent. Must be an integer or convertible to integer, representing a discord snowflake. It could also be a Channel object.
        '''
        
        return self.__channel__
    
    @channel.setter
    def channel(self, value):
        if type(value) not in (int, str):
            try: value = int(value)
            except: raise ParameterError(type(value).__name__)
            
        self.__channel__ = value
        
    async def send(self, delay: int | float = None):
        '''
        Sends the planned/future message and returns the result.
        
        Parameters
        ----------
        delay: `float`, `int`
            How much time to wait before sending the message. Defaults to None, which sends the message instantly.
            
        Returns
        -------
        message: `Lunarcord.Message`
            A Message object representing the newly sent message.
        '''
        
        if delay:
            await asyncio.sleep(delay)
            
        new = await self.bot.__gateway__.manager.sendMessage(self.channel, self.content)
        msg = Message(
            bot=self.bot,
            data=new
        )
        await msg.__proc__()
        
        return msg