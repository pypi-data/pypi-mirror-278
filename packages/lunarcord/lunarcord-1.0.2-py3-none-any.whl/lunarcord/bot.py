from .__core__.gateway import Gateway, _, Utils, Manager, User, Channel, Message, Guild, Snowflake, Signal, Role, Member, inspect, os
from . import Activity, Playing, Watching, Listening, Streaming, StatusError
from .errors import UnauthorizedError, RegisterError, UnregisterError, ReregisterError
from .commands import __createSlashCommand__, __createEvent__, __createTextCommand__, SlashCommand, TextCommand, Registrable, Event
from .tasks import __createTask__, __createLoop__, NameLike, TimeLike, Iterable, Task, Loop

import asyncio, time, sys, json

from importlib.util import spec_from_file_location, module_from_spec
from os.path import isfile, split, join
from os import listdir

from threading import Thread

class NoTimeout: ...

class Anyone: ...
class Anything: ...
class Any: ...


class Observer(Thread):
    
    '''
    Looks and notifies for changes in given files.
    '''
    
    def __init__(self, files: list[str] = []):
        
        super().__init__()
        
        self.running: bool = True
        
        self.files: list[str] = files
        self.times: dict[str, float] = {}
        
        self.updatedPaths: list[str] = files
        self.deletedPaths: list[str] = files
        self.areDeleted: list[str] = []
        
        self.updated: Signal = Signal(str, bool)
        self.deleted: Signal = Signal(str, bool)
        
    def addFile(self, *file: str, updated: bool = True, deleted: bool = True):
        
        files = list(file)
        self.files.extend(files)
        
        if updated:
            self.updatedPaths.extend(files)
            
        if deleted:
            self.deletedPaths.extend(files)
        
        for file in files:
            
            if file in self.areDeleted: # To avoid confusion
                self.areDeleted.remove(file)
            
            if updated:
                self.setLastUpdate(file)
        
    def removeFile(self, *file: str):
        
        files = list(file)
        
        for file in files:
            
            if file in self.files:
                self.files.remove(file)
                
            if file in self.areDeleted:
                self.areDeleted.remove(file)
                
            if file in self.updatedPaths:
                self.updatedPaths.remove(file)
                
            if file in self.deletedPaths:
                self.deletedPaths.remove(file)
                
    def notify(self, *args):
        
        self.updated.callSync(*args)
        
    def getLastUpdate(self, path: str):
        
        try:
            
            timestamp = os.path.getmtime(path)
        
        except:
            
            timestamp = time.time()
            
        return timestamp
    
    def setLastUpdate(self, path: str):
            
        self.times[path] = self.getLastUpdate(path)
        
        
    def isUpdated(self, path: str):
        
        if self.times.get(path) < self.getLastUpdate(path):
            
            self.setLastUpdate(path)
            return True
        
        return False
    
    def isDeleted(self, path: str):
        
        if not os.path.exists(path):
            
            self.removeFile(path)
            return True
        
        return False
    
    def search(self, paths: list[str]):
        
        for path in paths:
            
            if path in self.updatedPaths and path not in self.areDeleted:
                
                if self.isUpdated(path):
                    self.notify(path, os.path.isfile(path))
                
    def lookForDeleted(self, paths: list[str]):
        
        for path in paths:
            
            if path in self.deletedPaths and path not in self.areDeleted:
            
                if self.isDeleted(path):
                    self.deleted.callSync(path)
                
    def run(self):
        
        while self.running:
            
            if self.files:
                self.lookForDeleted(paths=self.files)
                self.search(paths=self.files)
                
            time.sleep(1.0)
            
    def stop(self):
        
        self.running = False

class Bot:
    
    def __init__(self, prefix: str = None, prefixes: tuple | list | set = [], token: str = None):
        '''
        A Bot object representing a Discord Bot User.
        
        Parameters
        ----------
        prefix: `str`
            A prefix for all text commands. It is appended to the `prefixes` list, if provided.
            
        prefixes: `tuple`, `list`, `set`
            A tuple, list or set of multiple unique prefixes. If `prefix` is given, it will be added to the list.
        
        token: `str`
            A Discord user or bot token to connect to the gateway with. If provided, it won't be needed in `Bot.run()`.
        '''
        
        try:
            fback = inspect.currentframe().f_back
            module = inspect.getmodule(fback)
            mpath = inspect.getsourcefile(module)
            origin = os.path.dirname(mpath)
            
        except:
            origin = None
            mpath = None
        
        self.origin: str = origin # Original path
        self.mainfile: str = mpath # Main file path
        
        __this__ = sys.modules[__name__]
        path = inspect.getsourcefile(__this__)
        
        self.installation: str = os.path.dirname(path)
        
        # self.installation is the path of the current
        # lunarcord installation being used.
        
        #print(self.mainfile)
        #self.__loadMainFile()
        
        if self.origin != self.installation:
        
            #registrables = self.__loadMainFile()
            #print(registrables)
            
            ...
        
        self.startTimes = 0
        
        prefixes: list = list(prefixes)
        prefixes = [str(prefix) for prefix in prefixes]
        
        if prefix is not None:
            
            if type(prefix) is not str:
                prefix = str(prefix)
            
            prefixes.append(prefix)
            
        prefixes = Utils.removeDuplicates(prefixes)
        
        self.asyncio = asyncio
        self.__gateway__: Gateway = Gateway(self)
        self.prefixes: list = prefixes
        self.presence: dict = {}
        self.token: str = token
        
        self.pendingSlashCommands: list[SlashCommand] = []
        self.textCommands: list[TextCommand] = []
        
        #self.loadedFiles: list[str] = []
        self.registered: dict[list[Registrable]] = {}
        
        self.observer = Observer()
        self.observer.start()
        self.observer.updated.connect(self.__fileUpdated__)
        self.observer.deleted.connect(self.__fileDeleted__)
        
    
    @property
    def isBot(self):
        '''
        Whether this is a bot or normal user account.
        '''
        
        return self.__gateway__.isBot
    
    @property
    def uptime(self):
        
        '''
        The bot's uptime. (Seconds elapsed since start)
        '''
        
        return self.__gateway__.uptime
        
    @property
    def mention(self):
        
        '''
        Returns a string that can be used to mention this `Bot`, for example `<@12345678>` where `12345678` is the bot's ID.
        '''
        
        return '<@' + str(self.id) + '>'
    
    @property
    def started(self):
        
        '''
        A boolean value representing whether the `Bot` is ready. This is `False` before the `onReady` event is executed, and `True` right after.
        '''
        
        return self.__gateway__.isReady
        
    async def start(self, token: str = None, login: str = None, password: str = None, delay: float = None, terminate: float = None, loop = None):
        '''
        Initializes the bot, connects to the gateway, and starts the running process.
        
        Parameters
        ----------
        token: `str`
            The bot's token, used to connect. If provided when the `lunarcord.Bot` object was created, this parameter is not needed.
        
        login: `str`
            If `token` was never given, this will be used along with `password`. This method can only be used for normal user accounts, and this parameter should be a `str` representing an account's `email` or `phone number`.
            
        password: `str`
            Cooperates with `login` in order to get the user's token for you. This is a `str` representing a discord account's `password`. Read `login` for more details on how those two work together.
            
        delay: `float`
            Wait `delay` seconds before starting the bot. By default, do not wait any additional time.
            
        terminate: `float`
            Run for `terminate` seconds, then exit the running process automatically.
            
        loop: `asyncio.AbstractEventLoop`
            The event loop to use. If not given, `asyncio.get_event_loop()` is used instead.
        '''
        
        self.startTimes += 1
        
        if delay is not None:
            await asyncio.sleep(delay)
        
        if self.startTimes > 1: # Don't create new Gateway if it's the first time starting the bot
            self.__gateway__ = Gateway(self, self.__gateway__)
            
        if token is None and login is not None and password is not None:
            
            token = await self.login(login, password)
        
        if self.token is not None:
            
            token = self.token
            
        else:
            
            if token is None:
                raise UnauthorizedError()
            
            self.token = token
        
        self.__gateway__.setToken(token)
        
        existing = await self.manager.slashCommands()
        await self.__updateSlashCommands__(existing=existing)
                
        def terminateAfter(duration: int | float, gateway: Gateway):
            
            if duration is None:
                return None
            
            time.sleep(duration)
            gateway.stop()
            
        terminateThread = Thread(target=terminateAfter, args=(terminate, self.__gateway__))
        await self.__gateway__.start(runAfterThread=terminateThread)
        
    def run(self, token: str = None, login: str = None, password: str = None, delay: float = None, terminate: float = None):
        '''
        Initializes the bot, connects to the gateway, and starts the running process.
        
        Parameters
        ----------
        token: `str`
            The bot's token, used to connect. If provided when the `lunarcord.Bot` object was created, this parameter is not needed.
        
        login: `str`
            If `token` was never given, this will be used along with `password`. This method can only be used for normal user accounts, and this parameter should be a `str` representing an account's `email` or `phone number`.
            
        password: `str`
            Cooperates with `login` in order to get the user's token for you. This is a `str` representing a discord account's `password`. Read `login` for more details on how those two work together.
            
        delay: `float`
            Wait `delay` seconds before starting the bot. By default, do not wait any additional time.
            
        terminate: `float`
            Run for `terminate` seconds, then exit the process automatically.
        '''
        
        loop = None
        
        try:
            loop = asyncio.get_event_loop()
            
        except:
            loop = None
            
        if not loop:
            
            loop = asyncio.new_event_loop()
        
        loop.create_task(
            
            self.start(
                token = token,
                login = login,
                password = password,
                delay = delay,
                terminate = terminate
            )
            
        )
        
        loop.run_forever()
        
    def stop(self):
        '''
        Forcefully stops and terminates the bot's process, shutting down its connection with Discord.
        '''
        
        self.__gateway__.stop()
        self.observer.stop()

    @property 
    def eventloop(self):
        if not hasattr(self, '__eventloop__') or self.__eventloop__ is None:
            loop = asyncio.new_event_loop()
            loop.run_forever()
            self.__eventloop__ = loop
            return loop
        else:
            return self.__eventloop__
        
    async def __authenticate__(self):
        
        try:
            bot = await self.__gateway__.manager.clientInfo()
        except:
            bot = {}
            
        user = await self.__gateway__.manager.me()
        self.user = User(self, user)
        
        try:
            self.id, self.name, self.description = user.get('id'), bot.get('name'), bot.get('description')
            self.icon, self.type = bot.get('icon'), bot.get('type')
            self.summary, self.isPublic, self.requiresCodeGrant = bot.get('summary'), bot.get('bot_public', False), bot.get('bot_require_code_grant')
            self.verifyKey, self.flags, self.hook, self.isMonetized = bot.get('verify_key'), bot.get('flags'), bot.get('hook'), bot.get('is_monetized')
            self.redirectUris, self.interactionsEndpointUrl, self.roleConnectionsVerificationUrl = bot.get('redirect_uris'), bot.get('interactions_endpoint_url'), bot.get('role_connections_verification_url')
            self.owner, self.guilds, self.interactionsEventTypes = bot.get('owner'), bot.get('approximate_guild_count'), bot.get('interactions_event_types')
            self.interactionsVersion, self.explicitContentFilter, self.rpcApplicationState = bot.get('interactions_version'), bot.get('explicit_content_filter'), bot.get('rpc_application_state')
            self.storeApplicationState, self.monetizationState, self.verificationState = bot.get('store_application_state'), bot.get('creator_monetization_state'), bot.get('verification_state')
            self.public, self.discoverabilityState, self.discoveryEligibilityFlags = bot.get('integration_public'), bot.get('integration_require_code_grant'), bot.get('discoverability_state')
            self.team, self.verified, self.bio, self.locale = bot.get('team'), bot.get('verified'), user.get('bio'), user.get('locale')
            self.internalGuildRestriction, self.avatar, self.publicFlags = bot.get('internal_guild_restriction'), user.get('avatar'), user.get('public_flags')
            self.accentColor, self.banner, self.bannerColor = user.get('accent_color'), user.get('banner'), user.get('banner_color')
            self.mfa, self.mfaEnabled, self.email = user.get('mfa_enabled'), user.get('mfa_enabled'), user.get('email')
            self.displayName, self.avatarDecorationData = user.get('global_name'), user.get('avatar_decoration_data')
            self.monetizationEligibilityFlags = bot.get('monetization_eligibility_flags')
            self.username, self.discriminator = user.get('username'), user.get('discriminator')
            
            if self.displayName is not None:
                self.displayName: str = self.displayName
                self.name = self.displayName
                
            if self.id:
                self.id = int(self.id)

            self.owner: User = await self.fetchUser(
                id = self.owner.get("id")
            )
            
        except:
            import traceback; traceback.print_exc()
        
    @property
    def manager(self):
        manager: Manager = Utils.manager(self)
        return manager
    
    @property
    def tokenPrefix(self):
        '''
        The token's prefix ("Bot" or "Bearer")
        '''
        
        return 'Bot' if self.isBot else 'Bearer'
    
    @property
    def fullToken(self):
        '''
        The full token including its prefix, eg "Bearer {Token}" or "Bot {Token}"
        '''
        
        return self.tokenPrefix + ' ' + self.token
        
    def event(self, type: int = None, **filters):
        '''
        Create an event listener. The type represents the type of event to listen for. It's not required, and if not provided, the event type will be based on your listener function's name - for example, if your function's name is "on_message", it will listen for new messages.
        
        Parameters
        ----------
        type: `int`
            The event type for the listener. Examples: `Lunarcord.ON_START`, `Lunarcord.ON_MESSAGE`...

        filters: `any`
            Additional parameters used to filter the listener's usage.
        '''
        
        def inner(func):
            name = func.__name__.lower()
            
            event = __createEvent__(
                bot = self,
                callback = func,
                name = name,
                type = type
            )
            
            return event
                
        return inner
    
    def register(self, registrable: Registrable, name: str = ...):
        '''
        Registers a new, registrable object.
        
        Parameters
        ----------
        registrable: `lunarcord.Registrable`
            The item to register. This must have __register__ method.
        '''
        
        item = type(registrable)
        
        if not issubclass(item, Registrable):
            raise RegisterError('notRegistrable')
        
        if not hasattr(item, '__register__'):
            raise RegisterError('noAttribute')
            
        if registrable.registered:
            raise RegisterError('registered')
        
        registrable.__register__(self, name)
        
    def unregister(self, registrable: Registrable):
        '''
        Un-registers an already registered registrable object.
        
        Parameters
        ----------
        registrable: `lunarcord.Registrable`
            The item to register. This must have __unregister__ method.
        '''
        
        item = type(registrable)
        
        if not issubclass(item, Registrable):
            raise UnregisterError('notRegistrable')
        
        if not hasattr(item, '__unregister__'):
            raise UnregisterError('noAttribute')
            
        if registrable not in self.registered:
            raise UnregisterError('notRegistered')
        
        registrable.__unregister__(self)
        
    def reregister(self, registrable: Registrable):
        '''
        Unregisters and registers again a registered object.
        
        Parameters
        ----------
        registrable: `lunarcord.Registrable`
            The item to re-register. This must have __reregister__ method.
        '''
        
        item = type(registrable)
        
        if not issubclass(item, Registrable):
            raise ReregisterError('notRegistrable')
        
        if not hasattr(item, '__reregister__'):
            raise ReregisterError('noAttribute')
        
        '''if registrable not in self.registered:
            raise ReregisterError('notRegistered')'''
        
        registrable.__reregister__()
        
    
    def reset(self, textCommands: bool = True, slashCommands: bool = True, events: bool = True):
        
        if textCommands:
            self.textCommands = []
            
        if slashCommands:
            self.pendingSlashCommands = []
            
        if events:
            
            for container in ['onStartFunctions', 'onMessageFunctions', 'channelUpdateFunctions', 'typingStartedFunctions', 'presenceUpdateFunctions']:
                setattr(self.__gateway__, container, [])
                
                
    def addPrefix(self, *prefix: str):
        '''
        Adds one or more new `prefixes` to the bot's text command prefixes.
        If one of the prefixes already exists, the bot completely ignores it (and goes on with the next, if it exists).
        
        Parameters
        ----------
        prefix: `str`
            The prefix (or prefixes) to add to the list of all bot prefixes.
        '''
        
        prefixes = list(prefix)
        
        for prefix in prefixes:
        
            if type(prefix) is not str:
                
                try:
                    prefix = str(prefix)
                    
                except:
                    continue
                
            prefix: str = prefix.strip()
            
            if prefix in self.prefixes:
                continue
            
            self.prefixes.append(prefix)
        
        
    def removePrefix(self, *prefix: str):
        '''
        Removes one or more already existing `prefixes` from the bot's text command prefixes.
        If the prefix doesn't already exist, a `ValueError` will be raised.
        
        Parameters
        ----------
        *prefix: `str`
            The prefix(es) to remove from the list of bot prefixes.
        '''
        
        prefixes = list(prefix)
        
        for prefix in prefixes:
        
            if type(prefix) is not str:
                
                try:
                    prefix = str(prefix)
                    
                except:
                    continue
                
            prefix: str = prefix.strip()
                
            if prefix not in self.prefixes:
                raise ValueError(f'"{prefix}" not in prefixes')
                
            self.prefixes.remove(prefix)
            
    def addMentionedPrefix(self):
        
        '''
        Creates an `onMention` prefix for the bot.
        Using this will allow users to ping the bot as a prefix for text commands.
        '''
        
        self.addPrefix(self.mention)
        
    def removeMentionedPrefix(self):
        
        '''
        Deletes an already existing `onMention` prefix from this bot.
        Mention prefixes allow users to ping the bot in order to execute text commands.
        '''
        
        try:
            
            self.removePrefix(self.mention)
            
        except:
            
            raise ValueError(f'No mention prefix to remove')
            
            
    def hasPrefix(self, *prefix: str):
        '''
        Checks if the bot has any of the given prefix(es) set to it.
        
        Parameters
        ----------
        *prefix: `str`
            The prefix or prefixes to check against.
            
        Returns
        -------
        exists: `bool`
            `True` if one of the prefixes exists. `False` if none of them do.
        '''
        
        if len(prefix) == 1:
            prefixes = [prefix[0]]
            
        else:
            prefixes = list(prefix)
            
        del prefix
        
        for prefix in prefixes:
            
            if prefix in self.__gateway__.prefixes:
                return True
            
        return False
        
        
    
    def slashCommand(self, name: str = None, description: str = None, guilds: list[int] = None, cooldown: int | float = None):
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
                bot = self,
                callback = func,
                name = name,
                description = description,
                guilds = guilds,
                cooldown = cooldown
            )
            
            return slashCommand
        
        def inner(func):
            
            slashCommand = __createSlashCommand__(
                bot = self,
                callback = func,
                name = name,
                description = description,
            )
                    
            return slashCommand
                
        return inner
    
    def textCommand(self, name: str = None, description: str = None, aliases: list[str] = [], cooldown: int | float = None):
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
                bot = self,
                name = name,
                description = description,
                aliases = aliases,
                cooldown = cooldown
            )
            
            return textCommand
        
        def inner(func):
            
            textCommand = __createTextCommand__(
                callback = func,
                bot = self,
                name = name,
                description = description,
                aliases = aliases,
                cooldown = cooldown
            )
                    
            return textCommand
                
        return inner
    
    def task(self, name: str = None, autorun: bool = True):
        
        '''
        Create a new task and start its execution in another thread. If `bot` is not provided and this is never registered from a cog or with `Bot.register()`, the task will never be ran. As long as the task is registered to some bot, the given bot will take care of it immediately.
        
        Parameters
        ----------
        activity: `callable`
            Any type of callable to be ran as this Task's main activity. This is required.
            
        name: `str`
            A name for this task. If not given, it'll be generated using the activity's name.
            
        autorun: `bool`
            If this is set to `False`, the task will not be executed by the bot automatically, but by you (eg. if the activity name is `myActivity`, then `myActivity()`)
            
        bot: `Bot`
            The bot that should take care of this task and its activity. If not given, the task can't start.
        '''
        
        def create(activity):
            
            nonlocal self, name, autorun
        
            return __createTask__(
                bot = self,
                activity = activity,
                name = name,
                autorun = autorun
            )
            
        return create
    
    def loop(self, name: NameLike[str] = None, every: TimeLike[int | float] = 1, iterable: Iterable = None):
        
        '''
        Create a new loop and start it in another thread. If `bot` is not provided and this is never registered from a cog or with `Bot.register()`, the loop will never start. As long as this loop is registered to some bot, the bot will take care of it immediately.
        
        Parameters
        ----------
        name: `NameLike`
            A name for this task. If not given, it'll be generated using the activity's name.
            
        iterable: `Iterable`
            An iterable (for example a `list`) to pass items from in every iteration. This can be useful for automatically updating the bot's activity, and not only.
            
        every: `TimeLike`
            Seconds to wait before every execution of the loop's activity.
        '''
        
        def create(activity):
            
            nonlocal name, every
        
            return __createLoop__(
                bot = self,
                activity = activity,
                name = name,
                every = every,
                iterable = iterable
            )
            
        return create
        
    def __getCommandsOf(self, path: str) -> list[Registrable]:
        
        '''
        Get all attributes of type `SlashCommand`, `TextCommand` or `Event` in the module represented by the given `path`.
        
        Parameters
        ----------
        path: `str`
            The path of the target module.
            
        Returns
        -------
        commands: `list`
            A list of all `lunarcord.SlashCommand`/`lunarcord.TextCommand`/`lunarcord.Event` objects in the module.
        '''
        
        if not isfile(path):
            path += '.py'
            
            if not isfile(path):
                return []
            
        head, tail = split(path)
        initFile = join(head, '__init__.py')
        locations = []
        
        if isfile(initFile):
            hasInit = True
            locations.append(initFile)
            
        
        moduleName = split(path)[0].replace('.py', '')
        module = Utils.module(moduleName, path, locations)

        for x in ("bot", "client"):
            
            if hasattr(module, x) and getattr(module, x) is ...:
                
                setattr(module, x, self)
        
        commands = []
        
        for name in dir(module):
            item = getattr(module, name)
            
            if issubclass(type(item), Registrable):
                item.varname = name
                commands.append(item)
            
        return commands
    
    def __loadModuleFrom(self, __path: str, name = 'LunarcordModule', execute: bool = True):
        
        spec = spec_from_file_location(name, __path)
        module = module_from_spec(spec)
        
        if execute:
            spec.loader.exec_module(module)
        
        return module
    
    def __loadMainFile(self):
        
        return None
        
        time.sleep(1)
        
        module = self.__loadModuleFrom(
            self.mainfile,
            name = 'LunarcordMain'
        )
        
        regs = []
            
        return regs
            
    
    def loadFile(self, path: str, exceptions: list[str] = [], ignoreExisting: bool = False):
        
        '''
        Load all slash and text commands as well as events in the module representing the given path.
        
        You can consider this some sort of "cog".
        
        Parameters
        ----------
        path: `str`
            The path of the module containing `lunarcord.SlashCommand`, `lunarcord.TextCommand` and/or `lunarcord.Event` objects.
            
        exceptions: `list[str]`
            A list of command or event names. All registrations in this file with a name contained in this list will be ignored.
            
        Returns
        -------
        commands: `list`
            A list of all commands and events succesfully added to the bot.
        '''
        
        if path not in self.registered:
            self.registered[path] = []
        
        succesful = []
        commands = self.__getCommandsOf(path)
        namedCommands: dict[str, Registrable] = {x.__name__: x for x in self.registered[path] if hasattr(x, "__name__")}
        
        for command in commands:
                
            if ignoreExisting:

                if hasattr(command, "name") and command.name in namedCommands:

                    existing = namedCommands.get(command.__name__)
                    existingSource = Utils.functionToString(existing, imports=False)
                    source = Utils.functionToString(command, imports=False)

                    if source == existingSource:

                        continue # Continue because it already exists
            
            try:
                if ((hasattr(command, 'name'))  and(command.name in exceptions)):
                    continue # Ignore command because it is in exceptions.
                
                if True: # Treat Registrables
                    self.register(command, command.varname)
                
                self.registered[path].append(command) # Append to the list of all registrables.
                succesful.append(command) # Append to the list of succesfully added items.
                
            except:
                
                import traceback
                traceback.print_exc()
                continue # ignore errors and proceed to the next command.
        
        self.observer.addFile(path)
        return succesful # Return all succesfully added commands.
    
    def unloadFile(self, path: str) -> list[Registrable]:
        
        '''
        Un-load all previously loaded slash and text commands as well as events in the module representing the given path.
        
        Parameters
        ----------
        path: `str`
            The path of the module containing `lunarcord.SlashCommand`, `lunarcord.TextCommand` and/or `lunarcord.Event` objects.
        
        Returns
        -------
        removed: `list[Registrable]`
            All registrables (Text or Slash Commands and Events) that were previously registered from this file before the removal.
        '''
        
        if path not in self.registered:
            self.registered[path] = []
            
        before = []
        
        for regist in self.registered[path]:
            
            try:
                
                gw = self.__gateway__

                if False: # Disabled stuff
                
                    try: self.unregister(regist)
                    except: pass # This doesnt even work I think
                
                for l in self.textCommands, gw.slashCommands, gw.onStartFunctions, gw.onMessageFunctions, gw.reactionAddFunctions, gw.channelUpdateFunctions, gw.messagePinnedFunctions, gw.typingStartedFunctions, gw.typingStoppedFunctions, gw.messageDeletedFunctions, gw.messageUpdatedFunctions, gw.presenceUpdateFunctions, gw.reactionRemoveFunctions, gw.views, gw.tasks, gw.loops:
                    
                    found = False
                    
                    if regist in l:

                        found = True
                        l.remove(regist)
                        
                    if found:

                        before.append(regist)
                        
                        try: gw.views.remove(regist)
                        except: pass

                        if hasattr(regist, "__unregister__"):
                            try: regist.__unregister__()
                            except: pass
                
            except:
                ... # Ignore error and continue
        
        self.observer.removeFile(path)
        self.registered[path] = []
        return before
                
        
    
    def reloadFile(self, path: str):
        
        '''
        Re-load all previously loaded slash and text commands as well as events in the module representing the given path.
        
        Parameters
        ----------
        path: `str`
            The path of the module containing `lunarcord.SlashCommand`, `lunarcord.TextCommand` and/or `lunarcord.Event` objects.

        Returns
        -------
        commands: `list`
            A list of all commands and events that have been succesfully updated.
        '''

        from .ui import View
        
        before = self.unloadFile(path)
        after = self.loadFile(path, ignoreExisting=False)
        
        return [x for x in after if type(x) is TextCommand], [x for x in after if type(x) is SlashCommand], [x for x in after if type(x) is Event], [x for x in after if type(x) is View], [x for x in after if type(x) is Task], [x for x in after if type(x) is Loop]
    
    def unload(self) -> list[Registrable]:
        '''
        Un-load all previously loaded files and folders, removing all commands or `lunarcord.Registrable` objects of any subclassed type.
        '''
        
        unloaded = []
        
        for file in self.registered:
            
            commands = self.unloadFile(file)
            unloaded.extend(commands)
            
        return unloaded
    
    def reload(self) -> list[Registrable]:
        '''
        Re-load all previously loaded files and folders, updating and adding any new commands or `lunarcord.Registrable` objects of any subclassed type.
        '''
        
        reloaded = []
        
        for file in self.registered:
            
            files = self.reloadFile(file)
            reloaded.extend(files)
            
        return reloaded
                
    def loadFolder(self, directory: str, ignoreInit: bool = True, fileExceptions: list[str] = [], commandExceptions: list[str] = [], *, recursive: bool = True):
        
        '''
        Go through all the files in the given folder, and add their slash/text commands and events to the bot.
        
        This is almost the same as doing:
        
        ```
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            bot.loadFile(path)
        ```
        
        ... but with some extra additions to make your life easier.
        
        Parameters
        ----------
        directory: `str`
            The path of the folder to load commands, views and events from.
            
        ignoreInit: `bool`
            Whether to ignore the folder's `__init__.py` file, if it exists. By default, this is `True`.
            
        fileExceptions: `list[str]`
            A list of file paths. All files in this folder that have a name contained in this list will be ignored.
            
        commandExceptions: `list[str]`
            A list of command or event names. All commands/events which have a name contained in this list will be ignored.
            
        recursive: `bool`
            Whether to also load files of sub-folders of this folder. This is True, by default.
            
        Returns
        -------
        registrations: `list`
            A list of all commands, views and events that have been succesfully added to the bot.
        '''
        
        def checklist(item):
            if not isinstance(item, list):
                if hasattr(item, '__iter__'): # is iterable
                    item = list(item)
                else:
                    if item is None:
                        item = []
                    else:
                        item = [item]
            return item
        
        fileExceptions = checklist(fileExceptions)
        commandExceptions = checklist(commandExceptions)
                
        if ignoreInit:
            fileExceptions.append('__init__.py')
            
        fileExceptions.append('__pycache__')
        
        commands = [] # Create empty list of successes.
        files = listdir(directory) # Get all files of the directory.
        
        for file in files:
            
            path = join(directory, file) # Retrieve the full path of module.
            
            if (path in fileExceptions) or (file in fileExceptions):
                continue # Ignore the command, as expected.
            
            if os.path.isdir(path):
                
                if recursive:
                    
                    recursed = self.loadFolder(path, ignoreInit, fileExceptions, commandExceptions)
                    commands.extend(recursed) # Add all recursively loaded commands to the list
                
                continue
            
            try:
                successes = self.loadFile(path, commandExceptions) # Add and get all command in the file.
                commands.extend(successes) # Append all commands added to list of succesfully added commands.
                
            except:

                import traceback
                traceback.print_exc()
                continue # Ignore errors and continue with next file.
            
        return commands # Return all succesfully added commands.
    
    def unloadFolder(self, directory: str, ignoreInit: bool = True, fileExceptions: list[str] = [], commandExceptions: list[str] = [], *, recursive: bool = True):
        
        '''
        Go through all the files in the given folder, and remove their slash/text commands and events from the bot, if they are in.
        
        This is almost the same as doing:
        
        ```
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            bot.unloadFile(path)
        ```
        
        ... but with some extra additions to make your life easier.
        
        Parameters
        ----------
        directory: `str`
            The path of the folder to unload commands, views and events from.
            
        ignoreInit: `bool`
            Whether to ignore the folder's `__init__.py` file, if it exists. By default, this is `True`.
            
        fileExceptions: `list[str]`
            A list of file paths. All files in this folder that have a name contained in this list will be ignored.
            
        commandExceptions: `list[str]`
            A list of command or event names. All commands/events which have a name contained in this list will be ignored.
            
        recursive: `bool`
            Whether to also unload files of sub-folders of this folder. This is True, by default.
            
        Returns
        -------
        registrations: `list`
            A list of all commands, views and events that have been succesfully removed from the bot.
        '''
        
        # Time for some copypasting from loadFile
        
        def checklist(item):
            if not isinstance(item, list):
                if hasattr(item, '__iter__'): # is iterable
                    item = list(item)
                else:
                    if item is None:
                        item = []
                    else:
                        item = [item]
            return item
        
        fileExceptions = checklist(fileExceptions)
        commandExceptions = checklist(commandExceptions)
                
        if ignoreInit:
            fileExceptions.append('__init__.py')
        
        commands = [] # Create empty list of successes.
        files = listdir(directory) # Get all files of the directory.
        
        for file in files:
            
            path = join(directory, file) # Retrieve the full path of module.
            
            if (path in fileExceptions) or (file in fileExceptions):
                continue # Ignore the command, as expected.
            
            if os.path.isdir(path):
                
                if recursive:
                    
                    recursed = self.unloadFolder(path, ignoreInit, fileExceptions, commandExceptions)
                    commands.extend(recursed) # Add all recursively loaded commands to the list
                
                continue
            
            try:
                successes = self.unloadFile(path, commandExceptions) # Add and get all command in the file.
                commands.extend(successes) # Append all commands added to list of succesfully added commands.
                
            except:
                continue # Ignore errors and continue with next file.
            
        self.observer.addFile(directory)
            
        return commands # Return all succesfully removed commands.
    
    def reloadFolder(self, directory: str, ignoreInit: bool = True, fileExceptions: list[str] = [], commandExceptions: list[str] = [], *, recursive: bool = True):
        
        '''
        Go through all the files in the given folder, reloading and updating all their slash/text commands and events.
        
        This is almost the same as doing:
        
        ```
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            bot.reloadFile(path)
        ```
        
        ... but with some extra additions to make your life easier.
        
        Parameters
        ----------
        directory: `str`
            The path of the folder to load commands and events from.
            
        ignoreInit: `bool`
            Whether to ignore the folder's `__init__.py` file, if it exists. By default, this is `True`.
            
        fileExceptions: `list[str]`
            A list of file paths. All files in this folder that have a name contained in this list will be ignored.
            
        commandExceptions: `list[str]`
            A list of command or event names. All commands/events which have a name contained in this list will be ignored.
            
        recursive: `bool`
            Whether to also load files of sub-folders of this folder. This is True, by default.
            
        Returns
        -------
        registrations: `list`
            A list of all commands, views and events that have been succesfully added to the bot.
        '''
        
        def checklist(item):
            if not isinstance(item, list):
                if hasattr(item, '__iter__'): # is iterable
                    item = list(item)
                else:
                    if item is None:
                        item = []
                    else:
                        item = [item]
            return item
        
        fileExceptions = checklist(fileExceptions)
        commandExceptions = checklist(commandExceptions)
                
        if ignoreInit:
            fileExceptions.append('__init__.py')
        
        commands = [] # Create empty list of successes.
        files = listdir(directory) # Get all files of the directory.
        
        for file in files:
            path = join(directory, file) # Retrieve the full path of module.
            
            if (path in fileExceptions) or (file in fileExceptions):
                continue # Ignore the command, as expected.
            
            if os.path.isdir(path):
                
                if recursive:
                    
                    recursed = self.reloadFolder(path, ignoreInit, fileExceptions, commandExceptions)
                    commands.extend(recursed) # Add all recursively loaded commands to the list
                
                continue
            
            try:
                successes = self.reloadFile(path, commandExceptions) # Add and get all command in the file.
                commands.extend(successes) # Append all commands added to list of succesfully reloaded commands.
                
            except:
                continue # Ignore errors and continue with next file.
            
        return commands # Return all succesfully added commands.
    
    def loadFolders(self, *folders: str):

        """
        Loads all provided folders using a for loop and `Bot.loadFolder`.
        If you want more control over the way your folders are loaded (additional parameters), you should manually use `Bot.loadFolder` for each of your folders.
        Additionally, this will ignore any errors and exceptions normally raised by `loadFolder`.

        Returns
        -------
        registrations: `list`
            A list of all commands, views and events that have been succesfully added to the bot.
        """

        regist = []

        for folder in folders:

            try:
                regist.extend(
                    self.loadFolder(folder)
                )

            except:
                continue

        return regist
    
    def __fileUpdated__(self, path: str):
        
        '''
        Called when an observed file or folder is updated, from the `Observer`'s `updated` signal.
        '''
        
        try:
            text, slash, events, views, tasks, loops = self.reloadFile(path)
            text, slash, events, views, tasks, loops = len(text), len(slash), len(events), len(views), len(tasks), len(loops)

            self.__updateSlashCommandsSync__()

            items = ""
            data = []

            for x in ( ("text command", text), ("slash command", slash), ("event", events), ("view", views), ("task", tasks), ("loop", loops) ):

                name, value = x

                if value > 0:
                    s = Utils.ending(value)
                    string = f"{value} {name}{s}"
                    data.append(string)

            if data:

                useand = False
                
                if len(data) > 1:
                    remains = data.pop()
                    useand = True

                items = ", ".join(data)

                if useand:
                    items += f" and {remains}"

            if items != "":
                print(f'[-] Updated {items} in "{path}".')
            
        except:
            # print(f'[!] Failed to update commands of "{path}".')
            pass
        
    def __fileDeleted__(self, path: str):
        
        '''
        Called when an observed file or folder is deleted, from the `Observer`'s `deleted` signal.
        '''
        
        try:
            cmds = self.unloadFile(path)
            self.__updateSlashCommandsSync__()
            amt = len(cmds)
            print(f'[-] Deleted {amt} commands from missing file "{path}".')
            
        except:
            ...
    
    def setStatus(self, type: str = None, activity: Activity = None):

        from .basetypes import Status
        
        invalidType = None

        if isinstance(type, Status):

            status: Status = type
            
            if status.activity is not None:
                
                activity = status.activity

            mobile = status.mobile if isinstance(status.mobile, bool) else False
            type = status.type
        
        if not isinstance(activity, Activity) and activity is not None:
            
            if isinstance(activity, str):
                
                found = False
                
                isact = activity.lower().startswith
                stringtypes = (('playing', Playing), ('watching', Watching), ('streaming', Streaming), ('listening to', Listening), ('listeningto', Listening), ('listening', Listening))
                
                for stringtype in stringtypes:
                    stringtype, classtype = stringtype
                    
                    if isact(stringtype):
                        
                        game: str = Utils.removeFirst(stringtype, activity)
                        activity = classtype(game.strip())
                        found = True
                        break
                    
                if not found:
                    activity = Playing(activity)
                    
        if type not in ('online', 'idle', 'dnd', 'invisible', None):
            
            if not isinstance(type, Status):
                invalidType = 1
            
        if invalidType is not None:
            raise StatusError(invalidType)
        
        if activity is not None:
            activities = [activity.toJson()]
            
        else:
            if not hasattr(self, '__activity__') or self.__activity__ is None:
                activities = []
            else:
                if isinstance(self.__activity__, list) and len(self.__activity__) < 1:
                    activities = [self.__activity__]
                else:
                    activities = [self.__activity__]
                
        if type is None:
            if not hasattr(self, '__statustype__'):
                type = 'online'
                
            else:
                type = self.__statustype__ if self.__statustype__ is not None else 'online'
            
        presence = {
            'status': type,
            'afk': False,
            'activities': activities
        }
        
        coro = self.__gateway__.changeStatus(
            activities=activities,
            status=type
        )
        
        self.__gateway__.doTask(coro)
            
        try:
            self.__activity__ = activities[0]
        except:
            ... # Leave activity as is
        self.__statustype__ = type
        self.presence = presence
        
    @property
    def activity(self):
        '''
        The bot's activity. Must be a `lunarcord.Activity` (for example `lunarcord.Activity(lunarcord.PLAYING, 'with Lunarcord')` OR a `str` such as `"Playing with Lunarcord"`).
        
        When this property is changed (`bot.activity = ...`), the bot's status will instantly be updated - if it's valid.
        '''
        
        return self.__activity__
    
    @activity.setter
    def activity(self, value):
        self.setStatus(activity=value)
        
    @activity.deleter
    def activity(self):
        self.__activity__ = None
        self.setStatus(None, None)
        
    @property
    def status(self):
        '''
        The bot's status type. It can be `lunarcord.ONLINE`, `lunarcord.DND`, `LUNARCORD.IDLE`, `lunarcord.OFFLINE` or an alias of these. It can also be a `string` (such as `"online"`, `"offline"`, `"idle"`, `"dnd"`).
        
        When this property is changed (`bot.status = ...`), the bot's status will instantly be updated - if it's valid.
        '''
        
        return self.__statustype__
    
    @status.setter
    def status(self, value):
        self.setStatus(value, None)
        
    @status.deleter
    def status(self):
        self.__statustype__ = 'online'
        self.setStatus(None, None)
        
    def getUser(self, id: int) -> User:
        
        '''
        Get and return the `User` of the corresponding `id` from the cache, if found.
        
        Parameters
        ----------
        id: `int`
            The target user's ID. Must be an integer or convertible to integer.
            
        Returns
        -------
        user: `User`
            A `lunarcord.User` object representing the target user, or `None` if not found.
        '''
        
        if type(id) is not int:
            try:
                id = int(id)
                
            except:
                return None
            
        for user in self.__gateway__.users:
            if user.id == id:
                return user
            
    async def fetchUser(self, id: int) -> User:
        
        '''
        Get and return the `User` of the corresponding `id` from the cache, or create it on request if not found.
        
        Parameters
        ----------
        id: `int`
            The target user's ID. Must be an integer or convertible to integer.
            
        Returns
        -------
        user: `User`
            A `lunarcord.User` object representing the target user.
        '''
        
        if type(id) is not int:
            
            try:
                id = int(id)
                
            except:
                return None
            
        found = self.getUser(id)
        
        if found is not None:
            return found
        
        try:
        
            user = await User.fromID(
                bot = self,
                user = id
            )
            
        except:
            
            user = None
            
        return user
        
    def getChannel(self, id: int) -> Channel:
        
        '''
        Get and return the `Channel` of the corresponding `id` from the cache, if found.
        
        Parameters
        ----------
        id: `int`
            The target channel's ID. Must be an integer or convertible to integer.
            
        Returns
        -------
        channel: `Channel`
            A `lunarcord.Channel` object representing the target messageable, or `None` if not found.
        '''
        
        if type(id) is not int:
            try:
                id = int(id)
                
            except:
                return None
            
        for channel in self.__gateway__.channels:
            if channel.id == id:
                return channel
            
    async def fetchChannel(self, id: int) -> Channel:
        
        '''
        Get and return the `Channel` of the corresponding `id` from the cache, or create it on request if not found.
        
        Parameters
        ----------
        id: `int`
            The target channel's ID. Must be an integer or convertible to integer.
            
        Returns
        -------
        channel: `Channel`
            A `lunarcord.Channel` object representing the target messageable.
        '''
        
        if type(id) is not int:
            try:
                id = int(id)
                
            except:
                return None
            
        found = self.getChannel(id)
        
        if found is not None:
            return found
        
        try:
            
            channel = await Channel.fromID(
                bot = self,
                channel = id
            )
            
        except:
            
            channel = None
        
        return channel
        
    def getMessage(self, id: int) -> Message:
        
        '''
        Get and return the `Message` of the corresponding `id` from the cache, if found.
        
        Parameters
        ----------
        id: `int`
            The target message's ID. Must be an integer or convertible to integer.
            
        Returns
        -------
        message: `Message`
            A `lunarcord.Message` object representing the target message, or `None` if not found.
        '''
        
        if type(id) is not int:
            try:
                id = int(id)
                
            except:
                return None
            
        for message in self.__gateway__.messages:
            if message.id == id:
                return message
            
    async def fetchMessage(self, channel: int, id: int) -> Message:
        
        '''
        Get and return the `Message` of the corresponding `id` from the cache, or create it on request if not found.
        
        Parameters
        ----------
        channel: `int`
            The channel ID in which the message is located. Must be an integer or convertible to integer.
            
        id: `int`
            The target message's ID. Must be an integer or convertible to integer.
            
        Returns
        -------
        message: `Message`
            A `lunarcord.Message` object representing the target message.
        '''
        
        if type(id) is not int:
            try:
                id = int(id)
                
            except:
                return None
            
        found = self.getMessage(id)
        
        if found is not None:
            return found
        
        try:
        
            message = await Message.fromID(
                bot = self,
                channel = channel,
                message = id
            )
            
        except:
            
            message = None
            
        return message
    
    def getGuild(self, id: int) -> Guild:
        
        '''
        Get and return the `Guild` of the corresponding `id` from the cache, if found.
        
        Parameters
        ----------
        id: `int`
            The target guild's ID. Must be an integer or convertible to integer.
            
        Returns
        -------
        guild: `Guild`
            A `lunarcord.Guild` object representing the target guild, or `None` if not found.
        '''
        
        if type(id) is not int:
            try:
                id = int(id)
                
            except:
                return None
            
        for guild in self.__gateway__.guilds:
            if guild.id == id:
                return guild
            
    async def fetchGuild(self, id: int) -> Guild:
        
        '''
        Get and return the `Guild` of the corresponding `id` from the cache, or create it on request if not found.
        
        Parameters
        ----------
        id: `int`
            The target Guild's ID. Must be an integer or convertible to integer.
            
        Returns
        -------
        guild: `Guild`
            A `lunarcord.Guild` object representing the target guild/server.
        '''
        
        if type(id) is not int:
            
            try:
                id = int(id)
                
            except:
                return None
            
        found = self.getGuild(id)
        
        if found is not None:
            return found
        
        try:
        
            guild = await Guild.fromID(
                bot = self,
                guild = id
            )
            
        except:
            
            guild = None
            
        return guild
    
    def getRole(self, id: int) -> Role | None:
        
        '''
        Get and return the `Role` of the corresponding `id` from the cache, if found.
        
        Parameters
        ----------
        id: `int`
            The target role's ID. Must be an integer or convertible to integer.
            
        Returns
        -------
        role: `Role`
            A `lunarcord.Role` object representing the target role, or `None` if not found.
        '''
        
        if type(id) is not int:
            try:
                id = int(id)
                
            except:
                return None
            
        for role in self.__gateway__.roles:
            if role.id == id:
                return role
            
    def getMember(self, guild: Guild | int, id: int) -> Member | None:

        """
        Get and return the `Member` of the corresponding `id` in the given `guild` from the cache, if found.
        
        Parameters
        ----------
        guild: `Guild`, `int`
            The guild this member belongs to. Must be a guild, an integer, or a convertible to integer.
        id: `int`
            The target user's ID. Must be an integer or convertible to integer.
            
        Returns
        -------
        member: `Member`
            A `lunarcord.Member` object representing the target member, or `None` if not found.
        """

        if type(guild) is not Guild:
            guild = self.getGuild(guild)

        if guild is None:
            return
        
        try:
            id = int(id)
        except:
            return
        
        for member in guild.members:
            if member.id == id:
                return member
            
    async def fetchMember(self, guild: Guild | int, id: int) -> Member:

        """
        Get and return the `Member` of the corresponding `id` from the cache, or create it on request if not found.
        
        Parameters
        ----------
        guild: `Guild`, `int`
            The guild this member is part of. Must be a `Guild` object, an integer, or convertible to integer.

        id: `int`
            The user ID of the target member. Must be an integer or convertible to integer.
            
        Returns
        -------
        member: `Member`
            A `lunarcord.Member` object representing the requested member.
        """

        found = self.getMember(guild, id)

        if found:
            return found
        
        if type(guild) is not Guild:
            guild = await self.fetchGuild(guild)

        data: dict = await self.__gateway__.manager.loadMember(guild.id, id)
        user: dict = data.pop("user")

        return await Member.__create__(
            bot = self,
            user = user,
            data = data,
            guild = guild
        )

    
    def getChannelNamed(self, name: str) -> Channel:
        
        '''
        Get and return the `Channel` with the given `name` from the cache, if found.
        
        Parameters
        ----------
        name: `str`
            The target channel's name. Must be a string, or convertible to string.
            
        Returns
        -------
        channel: `Channel`
            A `lunarcord.Channel` object representing the target messageable, or `None` if not found.
        '''
        
        if type(id) is not str:
            try:
                id = str(id)
                
            except:
                return None
            
        for channel in self.__gateway__.channels:
            if channel.name == name:
                return channel
            
    def getUserNamed(self, name: str) -> User:
        
        '''
        Get and return the `User` with the given `name` from the cache, if found.
        This works with both display name (if existing) and real username.
        
        Parameters
        ----------
        name: `str`
            The target user's name. Must be a string, or convertible to string.
            
        Returns
        -------
        channel: `User`
            A `lunarcord.User` object representing the target user, or `None` if not found.
        '''
        
        if type(id) is not str:
            try:
                id = str(id)
                
            except:
                return None
            
        for user in self.__gateway__.users:
            if user.displayName == name or user.username == name:
                return user
            
    def getGuildNamed(self, name: str) -> Guild:
        
        '''
        Get and return the `Guild` with the given `name` from the cache, if found.
        
        Parameters
        ----------
        name: `str`
            The target guild's name. Must be a string, or convertible to string.
            
        Returns
        -------
        guild: `Guild`
            A `lunarcord.Guild` object representing the target guild, or `None` if not found.
        '''
        
        if type(id) is not str:
            try:
                id = str(id)
                
            except:
                return None
            
        for guild in self.__gateway__.guilds:
            if guild.name == name:
                return guild
            
    def getRoleNamed(self, name: str) -> Role:
        
        '''
        Get and return the `Role` with the given `name` from the cache, if found.
        
        Parameters
        ----------
        name: `str`
            The target role's name. Must be a string, or convertible to string.
            
        Returns
        -------
        role: `Role`
            A `lunarcord.Role` object representing the target role, or `None` if not found.
        '''
        
        if type(id) is not str:
            try:
                id = str(id)
                
            except:
                return None
            
        for role in self.__gateway__.roles:
            if role.name == name:
                return role
            
    def getView(self, name: str):

        """
        Gets a view with the given name. If you hadn't given your `View` a name when creating it, the variable name you used works too.

        Parameters
        ----------
        name: `str`
            The target view's custom name.

        Returns
        -------
        view: `View`, `None`
            The view that was found. Can be `None` if no view was found.
        """

        for view in self.__gateway__.views:
            if view.name == name:
                return view
    
    async def waitForMessage(
        
        self,
        author: User | Snowflake = Anyone,
        timeout: int | float = NoTimeout,
        catch: bool = False
        
    ) -> Message | None:
        
        '''
        Wait until a new message is sent by anyone if `author` is not given or is None, otherwise for a message from the specified `author`. If `timeout` passes without any messages being sent, raise an `asyncio.TimeoutError`.
        
        Parameters
        ----------
        author: `User`, `Snowflake`
            A `User` object - or an integer (or a convertible to integer) representing a Discord `Snowflake`. If this is None (or not given at all), messages by any user will be sent back.
        
        timeout: `int`, `float`
            A float or convertible to float in which time the target message should have been sent. If `None`, no error will be raised in any cases.
            
        catch: `bool`
            Whether to return `None` instead of raising an exception in case of a timeout. By default this is `False`.
        '''
        
        if author == Anyone:
            author = None
            
        if timeout == NoTimeout:
            timeout = None
            
        if author is not None:
            
            if type(author) is not User:
                
                try:
                    author = await self.fetchUser()
                    
                except:
                    author = None
            
        if type(timeout) is not float:
            
            try:
                timeout = float(timeout)
            except:
                timeout = None
                
        if type(catch) is not bool:
            
            try:
                catch = bool(catch)
                
            except:
                catch - False
                
        checked = False
        success = True
        result = None
        
        async def check(message: Message):
            
            nonlocal author, self, checked, result, success
            
            gateway = self.__gateway__
            
            if author is not None and message.author != author:
                checked = True
                success = False
            
            try:
                
                gateway.onMessageFunctions.remove(check)
                
            except:
                
                ... # Just ignore the error.
            
            result = message
            checked = True
            
            
        self.__gateway__.onMessageFunctions.append(check)
                
        while not checked:
            continue
        
        if success:
            return result
        
            
    async def __updateSlashCommands__(self, existing: list[dict] = None):
        
        '''
        Update slash commands, adding pending ones and deleting any that are missing. This is a helper method and should be used only be lunarcord itself.
        '''
        
        if existing is None:
            
            existing = await self.__gateway__.manager.slashCommands()

        existingIDs = [int(x.get("id")) for x in existing if "id" in x]
    
        createdIDs = []
        
        for pending in self.pendingSlashCommands:
            new = await pending.toJson()
            createdIDs.append(int(new.get("id")))
        
        missingIDs = [x for x in existingIDs if x not in createdIDs]
        
        if missingIDs:
            
            await self.__gateway__.manager.deleteSlashCommands(*missingIDs)
        
        self.pendingSlashCommands = []
        
    def __updateSlashCommandsSync__(self, existing: list[dict] = None):
        
        '''
        Same as using __updateSlashCommands__, but this is no longer a coroutine function, and it also happens in a separate thread - improving speed.
        '''
        
        self.__gateway__.runInThread(
            
            function = self.__updateSlashCommands__,
            existing = existing
            
        )

    async def login(self, login: str, password: str):
        
        '''
        Login using a `login` (an `email` or a `phone number`) and the corresponding account's `password`.
        This returns the account's token (a `str`) which can later be used to run this bot.
        If the credentials are invalid or something else is wrong (eg. "New login location detected..." and such errors), the returned `token` will be `None`.
        '''
        
        try:
            
            return await self.__gateway__.manager.login(login, password)
        
        except:
            
            #import traceback
            #traceback.print_exc()
            return None
        
    async def request(self, url: str, data = None):

        """
        This method exists to make your life as a coder easier.
        No more need to use additional modules for requests!
        You can use this to perform a `GET` request on any `url` with the given `data` payload.

        Parameters
        ----------
        url: `str`
            The URL to perform the request on.

        data: `Any`
            Any data to pass as the request payload.

        Returns
        -------
        returned: `bytes`, `str`, `json` or `None`
            The data returned from the other side. Can have multiple types, and could be `None` if nothing is returned.
        """

        returns: bytes = await self.manager.get(url, data, customUrl=True, returns=bytes)

        try:
            string = returns.decode()
        except:
            return returns
        
        try:
            return json.loads(string)
        except:
            return string
        
    async def cat(self) -> str | None:

        """
        If you found this method randomly, consider yourself lucky.
        This is meant to be an easter egg, but could still be useful!

        Returns
        -------
        url: `str`
            A URL leading to a random cat picture. All images provided by `thecatapi` API!
        """

        data: list[dict] = await self.request("https://api.thecatapi.com/v1/images/search")
        return data[0].get("url", None)
    
    async def europapa(self):

        """????"""

        print("[-] Joost mode activated.")
        
        gifs = [

            "https://tenor.com/view/joost-klein-joost-joost-europapa-joost-klein-europapa-joost-klein-hey-gif-8063808885285976612",
            "https://tenor.com/view/europapa-joost-klein-gif-2406371744907006571",
            "https://tenor.com/view/europapa-joost-klein-gif-15870040348330019344",
            "https://tenor.com/view/joost-joost-klein-europapa-eurovision-contest-eurovision-2024-gif-10493321365734631409",
            "https://tenor.com/view/joost-joost-klein-erik-sussy-gif-18398024777456892539",
            "https://tenor.com/view/europapa-joost-klein-gif-2444755365992642313",
            "https://tenor.com/view/joost-joost-klein-europapa-joost-wave-joost-klein-wave-gif-317417478880584456",
            "https://tenor.com/view/joost-klein-jumping-rope-eurovision-esc-gif-14556300775786763513"

        ]

        try:

            self.activity = "Listening to Europapa"

            for gif in gifs:

                try:
                    await self.owner.dm(gif)
                except:
                    await asyncio.sleep(3)

            await self.owner.dm("https://www.youtube.com/watch?v=IiHFnmI8pxg")

        except:
            ...
        
    def __repr__(self):
        
        if hasattr(self, 'name'):
            
            return f'<Bot name={self.name}>'
        
        return f'<Bot object at {hex(id(self))}>'
    
    def __str__(self):
        
        if hasattr(self, 'name'):
            
            return self.name
        
        return f'<Bot object at {hex(id(self))}>'
    
    addPrefixes = addPrefix
    removePrefixes = removePrefix
    hasPrefixes = hasPrefix