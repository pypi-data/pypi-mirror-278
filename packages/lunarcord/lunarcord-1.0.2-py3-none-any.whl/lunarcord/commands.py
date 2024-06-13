'''
A lunarcord extension for writing text commands or slash commands and creating event listeners for your lunarcord `Bot`.
Below is a simple example snippet:

```
from lunarcord import commands, Bot

bot = Bot(prefix='!')

@commands.textCommand()
async def say(ctx, *args: str):

    msg = ' '.join(args)
    await ctx.send(msg)
    
bot.run("BOT123TOKEN456")
```

This creates a `!say` command that can be used to make the bot repeat whatever message the user wants.
For more examples, refer to `Commands` in lunarcord's official documentation (`SOON!`).

'''

from .__core__.types import (
    Registrable,
    TextCommand,
    SlashCommand,
    Event,
    ON_START,
    ON_MESSAGE,
    ON_CHANNEL_UPDATE,
    ON_TYPING_START,
    ON_PRESENCE_UPDATE,
    ON_MESSAGE_UPDATE,
    ON_MESSAGE_DELETE,
    ON_REACTION_ADD,
    ON_REACTION_REMOVE,
    ON_TYPING_STOP,
    ON_CHANNEL_CREATE,
    ON_CHANNEL_DELETE,
    ON_MEMBER_JOIN,
    ON_MEMBER_LEAVE,
    ON_MEMBER_UPDATE
)

def __createSlashCommand__(callback, bot = None, name: str = None, description: str = None, guilds: list = None, cooldown: int | float = None):

    slashCommand = SlashCommand(
        bot = bot,
        name = name if name is not None else callback.__name__,
        description = description if description is not None else callback.__doc__,
        guilds = guilds,
        callback = callback,
        cooldown = cooldown
    )
            
    return slashCommand

def slashCommand(name: str = None, description: str = None, guilds: list[int] = [], cooldown: int | float = None):
    '''
    Create a bot slash command. If not given, the name will be taken from the function name.
    
    Parameters
    ----------
    name: `str`
        The slash command name which will be displayed on Discord. If None, it will be the decorated function's name.
        
    description: `str`
        The informative description for the slash command. If not given, it will be the callback function's docstring.
            
    guilds: `list`
        A list of guild (server) IDs that this command should be available in. If not given, it will be available everywhere.

    cooldown: `int`, `float`
        A command cooldown. This will be useful if you want to use `Interaction.cooldown`.
    '''
    
    if callable(name):
        func = name
        name = func.__name__
        description = func.__doc__
        
        slashCommand = __createSlashCommand__(
            callback = func,
            name = name,
            description = description,
            guilds = guilds,
            cooldown = cooldown
        )
        
        return slashCommand
    
    def inner(func):
        
        slashCommand = __createSlashCommand__(
            callback = func,
            name = name,
            description = description,
        )
                
        return slashCommand
            
    return inner

def __createEvent__(callback, bot = None, name: str = None, type: int = None, params: dict = {}) -> Event:
    
    if name in ('on_start', 'start', 'onstart', 'on_ready', 'onready', 'ready') or type == ON_START:
        cont = 'onStartFunctions'
        type = ON_START

    elif name in ('on_message', 'message', 'onmessage') or type == ON_MESSAGE:
        cont = 'onMessageFunctions'
        type = ON_MESSAGE

    elif name in ('on_channel_update', 'onchannelupdate', 'channel_update', 'channelupdate', 'channel_updated', 'channelupdated', 'on_channel_updated', 'onchannelupdated') or type == ON_CHANNEL_UPDATE:
        cont = 'channelUpdateFunctions'
        type = ON_CHANNEL_UPDATE

    elif name in ('on_channel_create', 'onchannelcreate', 'channel_create', 'channelcreate', 'channelcreated', 'channel_created', 'on_channel_created', 'onchannelcreated') or type == ON_CHANNEL_CREATE:
        cont = 'channelCreateFunctions'
        type = ON_CHANNEL_CREATE

    elif name in ('on_channel_delete', 'onchanneldelete', 'channel_delete', 'channeldelete', 'channeldeleted', 'channel_deleted', 'on_channel_deleted', 'onchanneldeleted') or type == ON_CHANNEL_DELETE:
        cont = 'channelDeleteFunctions'
        type = ON_CHANNEL_DELETE
    
    elif name in ('on_typing', 'ontyping', 'on_type', 'ontype', 'typing', 'typing_start', 'typingstart' 'on_typing_start', 'ontypingstart', 'on_type_start', 'ontypestart') or type == ON_TYPING_START:
        cont = 'typingStartedFunctions'
        type = ON_TYPING_START

    elif name in ('on_status_change', 'on_status_changed', 'status_change', 'status_changed', 'status_update', 'status_updated', 'on_status_update', 'on_presence_update', 'presence_update') or type == ON_PRESENCE_UPDATE:
        cont = 'presenceUpdateFunctions'
        type = ON_PRESENCE_UPDATE

    elif name in ('on_message_edit', 'onmessageedit', 'message_edit', 'messageedit', 'messageedited', 'message_edited') or type == ON_MESSAGE_UPDATE:
        cont = 'messageUpdatedFunctions'
        type = ON_MESSAGE_UPDATE

    elif name in ('on_message_delete', 'onmessagedelete', 'message_delete', 'messagedelete', 'message_deleted', 'messagedeleted') or type == ON_MESSAGE_DELETE:
        cont = 'messageDeletedFunctions'
        type = ON_MESSAGE_DELETE

    elif name in ('on_reaction_add', 'onreactionadd', 'reaction_add', 'reactionadd', 'reaction_added', 'reactionadded', 'on_react', 'onreact' 'reaction', 'react') or type == ON_REACTION_ADD:
        cont = 'reactionAddFunctions'
        type = ON_REACTION_ADD

    elif name in ('on_reaction_remove', 'onreactionremove', 'reaction_remove', 'reactionremove', 'reaction_removed', 'reactionremoved') or type == ON_REACTION_REMOVE:
        cont = 'reactionRemoveFunctions'
        type = ON_REACTION_REMOVE

    elif name in ('on_typing_stop', 'ontypingstop', 'on_type_stop', 'ontypestop', 'typingstop', 'typing_stop', 'typingstop') or type == ON_TYPING_STOP:
        cont = 'typingStoppedFunctions'
        type = ON_TYPING_STOP

    elif name in ('on_member_join', 'onmemberjoin', 'on_join', 'onjoin', 'onjoined', 'on_joined', 'on_member_joined', 'onmemberjoined', 'memberjoin', 'member_join', 'member_joined', 'memberjoined') or type == ON_MEMBER_JOIN:
        cont = 'memberJoinFunctions'
        type = ON_MEMBER_JOIN

    elif name in ('on_member_leave', 'onmemberleave', 'on_leave', 'onleave', 'onleft', 'on_left', 'on_member_left', 'onmemberleft', 'memberleave', 'member_leave', 'member_left', 'memberleft') or type == ON_MEMBER_LEAVE:
        cont = 'memberLeaveFunctions'
        type = ON_MEMBER_JOIN

    elif name in ('on_member_update', 'onmemberupdate', 'on_member_updated', 'onmemberupdated', 'memberupdated', 'member_updated', 'member_updated', 'memberupdated') or type == ON_MEMBER_UPDATE:
        cont = 'memberUpdateFunctions'
        type = ON_MEMBER_UPDATE

    else:
        return None
        
    event = Event(
        bot = bot,
        name = name,
        type = type,
        callback = callback,
        container = cont,
        params = params
    )
    
    return event

        
def event(type: int = None, **filters) -> Event:
    '''
    Create an event listener. The type represents the type of event to listen for. It's not required, and if not provided, the event type will be based on your listener function's name - for example, if your function's name is "on_message", it will listen for new messages.
    
    Parameters
    ----------
    type: `int`
        The event type for the listener. Examples: `Lunarcord.ON_START`, `Lunarcord.ON_MESSAGE`...
        
    filters: `any`
        Additional parameters used to filter the listener's usage.
    '''
    
    if callable(type):
        
        callback = type
        del type
        
        name = callback.__name__.lower()
        
        event = __createEvent__(
            callback = callback,
            name = name
        )
        
        return event
    
    def inner(func):

        name = func.__name__.lower()
        
        event = __createEvent__(
            callback = func,
            name = name,
            type = type
        )
        
        return event
            
    return inner

def __createTextCommand__(callback, bot = None, name: str = None, description: str = None, aliases: list = [], cooldown: int | float = None):

    textCommand = TextCommand(
        bot = bot,
        name = name if name is not None else callback.__name__,
        description = description if description is not None else callback.__doc__,
        callback = callback,
        aliases = aliases,
        cooldown = cooldown
    )
            
    return textCommand

def textCommand(name: str = None, description: str = None, aliases: list[str] = [], cooldown: int | float = None):
    '''
    Create a bot text command. If not given, the name will be taken from the callback's name.
    
    Parameters
    ----------
    name: `str`
        The text command's name, which will cause it to be triggered. If None, it will be based on the callback function's name.
        
    description: `str`
        The informative description for the text command, shown in the auto-help (if it exists). If not given, it will be the callback function's docstring.
        
    aliases: `list[str]`
        Additional names that can also trigger the command's execution.

    cooldown: `int`, `float`
        A command cooldown. This will be useful if you want to use `Context.cooldown`.
    '''
        
    aliases = list(aliases)
    
    if callable(name):
        
        # When someone uses @textCommand instead of @textCommand()
        
        func = name
        name = func.__name__
        description = func.__doc__
        
        textCommand = __createTextCommand__(
            callback = func,
            name = name,
            description = description,
            aliases = aliases,
            cooldown = cooldown
        )
        
        return textCommand
    
    def inner(func):
        
        textCommand = __createTextCommand__(
            callback = func,
            name = name,
            description = description,
            aliases = aliases,
            cooldown = cooldown
        )
                
        return textCommand
            
    return inner