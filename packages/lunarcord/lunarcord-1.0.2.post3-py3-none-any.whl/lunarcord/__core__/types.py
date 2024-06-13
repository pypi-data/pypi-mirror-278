from .addons import Utils, SlashOption, time
from ..basetypes import User, Interaction, Context
from ..errors import UnregisterError
 
class convertibleToStr: pass
class function: pass
class method: pass

ON_START = 0
ON_READY = 0
ON_MESSAGE = 1
ON_CHANNEL_UPDATE = 2
ON_TYPING_START = 3
ON_PRESENCE_UPDATE = 4
ON_MESSAGE_DELETE = 5
ON_MESSAGE_EDIT = 6
ON_MESSAGE_UPDATE = 6
ON_REACTION_ADD = 7
ON_REACTION_REMOVE = 8
ON_TYPING_STOP = 9
ON_CHANNEL_CREATE = 10
ON_CHANNEL_DELETE = 11
ON_MEMBER_JOIN = 12
ON_MEMBER_UPDATE = 13
ON_MEMBER_LEAVE = 14


class Bot: ... # Can't import lunarcord.Bot so why not..

class Registrable:
    def __init__(self):
        
        self.bot: Bot = None
        self.__registered__: bool = False
        
    def __register__(self, bot: Bot):
        '''
        Implement `bot.register(self)`.
        
        This should generally be something like:
        ```
        def __register__(self, bot: lunarcord.Bot):
            
            self.bot = bot
            name = "whateverName"
            
            if not hasattr(self.bot, name) or type(getattr(self.bot, name)) is not list:
                setattr(self.bot, name, [])
                
            items = getattr(self.bot, name)
            items.append(self)
            setattr(self.bot, name, items)
            self.__registered__ = True
            
        ```
        The above simply gets a list named `name` (in this case "whateverName") for the bot (or creates it if it doesn't exist) and adds `self` `(lunarcord.Registrable)` to the list.
        '''
        
        self.bot = bot
        name = "registrations"
        if not hasattr(self.bot, name) or type(getattr(self.bot, name)) is not list:
            setattr(self.bot, name, [])
        items: list = getattr(self.bot, name)
        items.append(self)
        setattr(self.bot, name, items)
        
    def __unregister__(self):
        '''
        Implement `bot.unregister(self)`.
        
        This should generally be something like:
        ```
        def __unregister__(self):
            
            name = "whateverName"
            
            if not hasattr(self.bot, name) or type(getattr(self.bot, name)) is not list:
                setattr(self.bot, name, [])
            items = getattr(self.bot, name)
            
            if self not in items:
                print("Failed to unregister item - it hasn't been registered before!")
            else:
                items.remove(self)
                setattr(self.bot, name, items)
                self.__registered__ = False
                
            self.bot = None
            
        ```
        The above simply gets a list named `name` (in this case "whateverName") for the bot (or creates it if it doesn't exist) and removes `self` `(lunarcord.Registrable)` to the list - or prints an error if it hasn't been registered before..
        '''
        
        name = "registrations"
        
        if not hasattr(self.bot, name) or type(getattr(self.bot, name)) is not list:
            setattr(self.bot, name, [])
            
        items: list = getattr(self.bot, name)
        if self not in items:
            raise UnregisterError()
        
        items.remove(self)
        setattr(self.bot, name, items)
        
        self.bot = None
        
    def __reregister__(self):
        '''
        Implement `bot.reregister(self)`.
        
        This should generally be something like:
        ```
        def __reregister__(self):
            if self.__registered__:
                bot = self.bot
                self.__unregister__()
            self.__register__(bot)
        ```
        '''
        
        bot = self.bot
        self.__unregister__()
        self.__register__(bot)
        
    @property
    def registered(self):
        '''
        Whether the registrable is currently registered to a bot.
        '''
        
        return self.bot is not None
    
class TextCommand(Registrable):
    
    def __init__(self, bot: Bot, name: str | convertibleToStr, description: str | convertibleToStr, callback: function | method, aliases: list[str], cooldown: int | float):
        
        self.bot = bot
        self.name = str(name).strip()
        self.names = [self.name] + aliases
        self.namesLower = [n.lower() for n in self.names]
        self.description = str(description).strip().replace('\n', ' ')
        self.callback = callback

        if cooldown not in (None, ...):
            self.cooldown = float(cooldown)
            self.hasCooldown = True

        else:
            self.cooldown = None
            self.hasCooldown = False
        
        self.__addedToBot__ = False
        
        if self.bot is not None:
            self.bot.textCommands.append(self)
            self.__addedToBot__ = True
            
    def __eq__(self, other):
        
        if not isinstance(other, TextCommand):
            return False
        
        if self.name != other.name:
            return False
        
        if self.description != other.description:
            return False
        
        return True
            
    def __register__(self, bot: Bot, name: str = ...):
        
        self.bot = bot
        self.bot.textCommands.append(self)
        self.__addedToBot__ = True
        
    def __unregister__(self):
        
        self.bot.textCommands.remove(self)
        self.bot = None
        self.__addedToBot__ = False
        
    def __reregister__(self):
        
        bot = self.bot
        
        if bot is not None:
            self.__unregister__()
            self.__register__(bot)
            
    def __repr__(self):
        
        return f'<TextCommand name="{self.name}" description="{self.description}"'
    
    def __str__(self):
        
        return self.name
    
    async def __call__(self, ctx: Context, *args, **kwargs):
        '''
        Call the text command's callback function, applying the context in which it was triggered as well as the args and kwargs given.
        '''
        
        if len(args) == 1:
            args = [args[0]]
            
        else:
            args = list(args)

        await Utils.execute(
            self.callback,
            ctx,
            *args,
            **kwargs,
            bot = self.bot
        )

        if self.hasCooldown:

            ends = self.cooldown + time.time()

            ctx.author.setCooldown(
                name=self.name,
                ends=ends,
                type="textcommand"
            )

class SlashCommand(Registrable):
    
    def __init__(self, bot, name: str | convertibleToStr, description: str | convertibleToStr, guilds: list[int], callback: function | method, cooldown: int | float):
        
        self.bot = bot
        self.name = str(name).strip()
        self.description = str(description).strip().replace('\n', ' ')
        self.callback = callback
        self.options = list(self.getOptions())
        self.id: int = None
        self.cooldown: int | float = cooldown
        
        if guilds is None:
            self.guilds = guilds
            
        else:
            self.guilds: list[int] = [int(guild) for guild in guilds]
        
        self.__addedToPending__ = False
        self.__addedToGateway__ = False
        
        if self.bot is not None:
            self.bot.pendingSlashCommands.append(self)
            self.__addedToPending__ = True
            
    def __register__(self, bot: Bot, name: str = ...):
        
        self.bot = bot
        self.bot.pendingSlashCommands.append(self)
        self.__addedToPending__ = True
        
    def __unregister__(self):
        
        try:
            self.bot.pendingSlashCommands.remove(self)
        except:
            pass
        self.bot = None
        self.__addedToPending__ = False
        
    def __reregister__(self):
        
        bot = self.bot
        
        if bot is not None:
            self.__unregister__()
            self.__register__(bot)
        
    def getOptions(self):
        
        if True:
            from ..basetypes import User, Channel, Role, Member
            from ..builders import Attachment
            Types = (User, Channel, Role, Member, "Mentionable", Attachment)
                
        options, self.params = Utils.slashOptions(
            function = self.callback,
            Types = Types
        )
        
        return options
    
    async def toJson(self, override: bool = True):
        
        data: dict = await self.bot.manager.createSlash(
            
            name = self.name,
            description = self.description,
            options = self.options,
            override = override,
            guilds = self.guilds
            
        )
        
        if override:
        
            if self.id is None:
                
                self.id = data.get('id')
            
            if self.bot is not None:
                
                self.bot.__gateway__.slashCommands.append(self)
                self.__addedToGateway__ = True
        
        return data
        
    def fromJson(bot, data, cooldown: int | float = None):
        
        new = SlashCommand(
            bot = bot,
            name = data['name'],
            description = data['description'],
            options = data['options'],
            guilds = [data.get('guild_id')],
            cooldown = cooldown
        )
        
        return new
        
    async def __call__(self, interaction: Interaction, *args, **kwargs):
        '''
        Call the slash command's on-interaction callback function, applying the interaction that triggered it as well as the arguments given.
        '''
        
        return await Utils.execute(
            self.callback,
            interaction,
            *args,
            **kwargs,
            bot = self.bot,
            params = self.params,
        )
    
    def __repr__(self):
        return f'<SlashCommand name="{self.name}" description="{self.description}">'
    
    def __str__(self):
        return self.name
    
class Event(Registrable):
    def __init__(self, bot, name: str | convertibleToStr, type: int, callback: function | method, container: str, params: dict):
        
        self.bot = bot
        self.name = name
        self.type = type
        self.callback = callback
        self.container = container
        self.extraparams = params
        self.__connected__ = False
        
        if self.bot is not None and not self.__connected__:
            self.connect()
            
    def __register__(self, bot: Bot, name: str = ...):
        
        self.bot = bot
        self.connect()
        self.__connected__ = True
        
    def __unregister__(self):
        
        self.deconnect()
        self.bot = None
        self.__connected__ = False
        
    def __reregister__(self):
        
        bot = self.bot
        
        if bot is not None:
            self.__unregister__()
            self.__register__(bot)
        
    def connect(self):
        new_container = getattr(self.bot.__gateway__, self.container)
        new_container.append(self)
        setattr(self.bot.__gateway__, self.container, new_container)
        self.connected = True
        
    def deconnect(self):
        new_container = getattr(self.bot.__gateway__, self.container)
        try:
            new_container.remove(self)
        except:
            ...
        setattr(self.bot.__gateway__, self.container, new_container)
        self.connected = False
        
    async def __call__(self, *args, **kwargs):
        '''
        Emit the event and execute its callback, applying the given arguments.
        '''
        
        await Utils.execute(
            self.callback,
            *args,
            **kwargs
        )
        
    def __repr__(self):
        return f'<Event name="{self.name}" type="{self.type}" callback="{self.callback}">'
    
    def __str__(self):
        return self.name