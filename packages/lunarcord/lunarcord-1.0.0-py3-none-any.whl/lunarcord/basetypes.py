from .errors import PermissionsError, InteractionNotRespondedError, InteractionRespondedError, IllegalError
from .activities import Activity
from .__core__.addons import Utils, Cooldown, lunarlist
import asyncio, discord_emoji, re

# Some placeholders below

class Snowflake(int): ...
class Message: ...
class View: ...
class Embed: ...
class EmbedArray: ...
class Button: ...
class Modal: ...
class Color: ...

# End of placeholders...

class Message:
        
    def __init__(self, bot, data: dict):
        
        from .bot import Bot
        from .builders import Attachment
            
        _ = data.get
        self.type, self.tts, self.timestamp, self.__content__, self.reference, self.pinned, self.mentions, self.nonce, self.mentionedRoles, self.mentionsEveryone, self.__memberData__, self.id, self.flags, self.embeds, self.__editedTime__, self.components, self.channel, self.author, self.attachments, self.guild  = (
            _('type', 0),
            _('tts', False),
            _('timestamp', None),
            _('content', ''),
            _('referenced_message', None),
            _('pinned', False),
            _('mentions', []),
            _('nonce', 0),
            _('mention_roles', []),
            _('mention_everyone', False),
            _('member', None),
            _('id', 0),
            _('flags', 0),
            _('embeds', []),
            _('edited_timestamp', None),
            _('components', []),
            _('channel_id', 0),
            _('author', None),
            _('attachments', []),
            _('guild_id', None)
        )
            
        self.bot: Bot = bot
        
        for x in ('id', 'referenced_message', 'channel_id', 'guild_id'):
            try: setattr(self, x, int(getattr(self, x)))
            except: continue
            
        try:
            self.timestamp: float = Utils.isoToUnix(self.timestamp)
        except:
            self.timestamp = None
        
        if self.reference is not None:
            self.reference: Message = Message(self.bot, self.reference)
            
        self.reactions: list[Reaction] = []
        self.attachments: list[Attachment] = self.attachments
        
        self.raw: dict = data

        self.__isGuild__ = False

        if self.__memberData__ is not None:

            self.__isGuild__ = True
            
        self.type: int; self.tts: bool; self.content: str; self.pinned: bool; self.mentions: list; self.mentionedRoles: list; self.mentionsEveryone: bool; self.nonce: int; self.flags: int; self.embeds: list; self.edited: float; self.components: list; self.channel: int; self.author: User | Member; self.attachments: list; self.guild: int; self.channel: Channel

    @property
    def isEdited(self):
        
        '''
        Whether this message has been edited before.
        '''
        
        return self.__editedTime__ is not None
    
    @property
    def edited(self):
        
        '''
        The time (in UNIX format) of when the message was last edited, or `None` if it has not been edited yet.
        '''
        
        return Utils.isoToUnix(self.__editedTime__) if self.isEdited else None
    
    @property
    def isReply(self):
        
        '''
        Whether this message is replying to another message.
        If it is, you can get the target message using `Message.reference` where `Message` is this message.
        '''
        
        return self.reference is not None
        
    async def __proc__(self, /):
        
        '''
        Further process the `Message` object to complete asynchronous initialization.
        '''

        from .builders import Attachment
        
        if type(self.author) is dict:
            authorID = self.author.get('id')
            
        elif type(self.author) is int:
            authorID = self.author
            
        elif type(self.author) is User:
            authorID = self.author.id
            
        else:
            try: authorID = int(authorID)
            except: authorID = None
            
        if type(self.channel) is dict:
            channelID = self.channel.get('id')
            
        elif type(self.channel) is int:
            channelID = self.channel
            
        elif type(self.channel) is Channel:
            channelID = self.channel.id
            
        else:
            try: channelID = int(self.channel)
            except: channelID = None
        
        coros = []

        if not self.__isGuild__:

            coros.append(self.bot.fetchUser(authorID))

        coros.append(self.bot.fetchChannel(channelID))
        
        if self.reference is not None:
            
            coros.append(
                self.reference.__proc__()
            )

        async def loadAttachments():

            self.attachments = [

                await Attachment.fromPayload(
                    bot = self.bot,
                    payload = x
                )

                for x in self.attachments

            ]
            
        results: list = list(await asyncio.gather(*coros, loadAttachments()))
        
        if not self.__isGuild__:
            
            self.author: User | Member = results.pop(0)
        
        channel = results.pop(0)

        if type(channel) is Channel:
            
            self.channel: Channel = channel
        
            channel.messages.append(
                self
            )

            self.guild: Guild = self.channel.guild

            if self.__isGuild__:

                self.author: User | Member = await self.bot.fetchMember(self.guild, authorID)
            
    async def __create__(bot, data: dict):
        
        '''
        Create and fully initialize a new `Message` from the given data. 
        '''
        
        if data is None:
            return None
        
        new = Message(bot, data)
        await new.__proc__()
        return new
            
       
    async def fromID(*, bot, channel: int | str, message: int | str):
        '''
        Creates and returns a new Message using the message's ID.
        
        Parameters
        ----------
        bot: `Bot`
            A Lunarcord bot object representing your bot client.
            
        channel: `int`, `str`
            The ID of the channel where the message was sent.
        
        message: `int`, `str`
            The ID of the message.
            
        Returns
        -------
        message: `Message`, `None`
            The requested message as a Message object, or None if not found.
        '''
            
        data = await bot.__gateway__.manager.loadMessage(channel, message)
        return await Message.__create__(bot, data)
    
    @property
    def content(self):
        '''
        The message's content. You can edit the message by reassigning this property `(msg.content = 'New Content')` or delete it by deleting the property `(del msg.content)` where `msg` is a `Lunarcord.Message`.
        '''
        
        return self.__content__
    
    @content.setter
    def content(self, new: str):
        
        self.bot.__gateway__.runInThread(self.edit, content=new)
    
    @content.deleter
    def content(self):
        
        self.bot.__gateway__.runInThread(self.delete)
    
    def __str__(self):
        return self.content if type(self.content) is str else ''
    
    def __repr__(self):
        return f'<Message id={self.id} content="{self.__content__}">'
    
    def __eq__(self, other):
        
        if type(other) is Message:
            return self.id == other.id
        
        else:
            
            try:
                other = int(other)
                return self.id == other
            
            except:
                return False
    
    async def send(self, content: str = None, reference: Message = None, embed: Embed = None, embeds: list = None, attachments: list = [], view: View | str = None, button: Button = None, buttons: list[Button] = []):
        '''
        Creates a new Message in the same channel as this message.
        The newly sent and created Message is returned.
        
        Parameters
        ----------
        content: `str`
            The content of the new message.
            
        reference: `Message`
            The message to reply to. If None (the default value), the new message will not reply to any previously sent messages.
        
        embed: `Embed`
            An embed to send. If both this and the `embeds` parameter are given, they will be mixed together.
            
        embeds: `list`
            A list of `Lunarcord.Embed` objects representing Discord embeds. Can also be one, singular embed to attach - or None (the default value) in order to send no embeds.
        
        attachments: `list`
            A list of `Lunarcord.Attachment` objects representing Discord attachments/files. Can also be one, singular file to attach - or None (the default value) in order to send no attachments.
        
        view: `View`
            A `Lunarcord.View` view made up of buttons or select menus, or the name of an existing View.
            
        button: `Button`
            A `Lunarcord.Button` button to be added to a `View` and sent.
            
        buttons: `list`
            A `list` of `Lunarcord.Button` buttons to be added to the message's view.
            
        Returns
        -------
        message: `Message`
            A `Lunarcord.Message` object representing the Discord message that was sent.
        '''
        
        if embeds is None:
            embeds = []
            
        return await self.channel.send(content, reference, embed, embeds, attachments, view, button, buttons)
    
    async def sendEmbed(self, title: str = None, description: str = None, footer: str = None, footerIcon: str = None, thumbnail: str = None, color: Color = None, image: str = None, timestamp: int | float | str = None, reply: bool = False):
        """
        Creates a new `Embed` and sends it in this channel.
        This is a shorthand for creating a new `Embed` and sending it using `await Channel.send(embed=embed)` where `embed` is your new `Embed`.

        The parameters are the same as the ones for an `Embed`'s constructor.
        """

        return await self.channel.sendEmbed(
            title = title,
            description = description,
            footer = footer,
            footerIcon = footerIcon,
            thumbnail = thumbnail,
            color = color,
            image = image,
            timestamp = timestamp,
            reference = self
        )
        
    async def reply(self, content: str = None, embeds: list = [], attachments: list = []):
        '''
        Shorthand for `message.send(content, message.id)` where message is a `Lunarcord.Message` object.
        
        Parameters
        ----------
        content: `str`
            The content of the new message.
            
        reference: `int`
            The message to reply to. If None (the default value), the new message will not reply to any previously sent messages.
            
        embeds: `list`
            A list of `(WIP)` `Lunarcord.Embed` objects representing Discord embeds. Can also be one, singular embed to attach - or None (the default value) in order to send no embeds.
        
        attachments: `list`
            A list of `(WIP)` `Lunarcord.Attachment` objects representing Discord attachments/files. Can also be one, singular file to attach - or None (the default value) in order to send no attachments.
        
        Returns
        -------
        message: `Message`
            A `Lunarcord.Message` object representing the Discord message that was sent.
        '''
        
        return await self.send(content, self.id, embeds, attachments)
        
    async def copy(self, reply: bool = False, multiplier: int = 1):
        '''
        Shorthand for `message.send(message)` where message is a `Lunarcord.Message`.
        
        Parameters
        ----------
        reply: `bool`
            Whether the message(s) should reply to the original one. Defaults to `False`, meaning they wpn't reply anywhere.
            
        multiplier: `int`
            How many times to send (spam) the message. Minimum is 1, maximum is 5. If not provided, the target message will be 'copied' only once.
        '''
        
        params = (
            self.content,
            self.id if reply else None
        )
        
        if multiplier > 5 or multiplier < 1:
            multiplier = 1
        
        for x in range(multiplier):
            await self.send(*params)
            
    async def delete(self, *, catch: bool = False):
        '''
        Deletes the target message, if the bot has enough permissions to do so.
        If not, a `PermissionsError` will be raised, unless you have set `catch` to `True`.
        '''
        
        try:
            await self.bot.__gateway__.manager.deleteMessage(self.channel.id, self.id)
        except:
            if catch:
                return
            raise PermissionsError()
        
    async def edit(self, content: str):
        '''
        Updates the target message, if it was originally sent by the bot.
        If not, a `PermissionsError` will be raised.
        
        Parameters
        ----------
        content: `str`
            The message's new content.
        '''
        
        try:
            
            try:
                content = str(content)
                
            except:
                raise TypeError(f'Content must be string or convertible to string, not {type(content).__name__}')
            
            await self.bot.__gateway__.manager.editMessage(self.channel.id, self.id, content)
            
        except:
            raise PermissionsError()
        
        
    async def react(self, emoji: str):
        '''
        Adds an emoji reaction to the message.
        
        Parameters
        ----------
        emoji: `str`
            The emoji to react with.
        '''
        
        await self.bot.__gateway__.manager.addReaction(self.channel.id, self.id, emoji)
        
    async def unreact(self, emoji: str):
        '''
        Removes an emoji reaction from the message.
        
        Parameters
        ----------
        emoji: `str`
            The reaction emoji to remove.
        '''
        
        await self.bot.__gateway__.manager.removeReaction(self.channel.id, self.id, emoji)
        
    async def pin(self):
        '''
        Adds this message to the channel's pins, if the bot has enough permissions for this.
        If not, a `PermissionsError` will be raised.
        '''
        
        try:
            await self.bot.__gateway__.manager.pinMessage(self.channel.id, self.id)
            
        except:
            raise PermissionsError()
        
    async def unpin(self):
        '''
        Removes this message from the channel's pins, if the bot has enough permissions for this.
        If not, a `PermissionsError` will be raised.
        '''
        
        try:
            await self.bot.__gateway__.manager.unpinMessage(self.channel.id, self.id)
            
        except Exception as exception:
            raise PermissionsError()
        
    def startsWith(self, prefix: str, caseSensitive: bool = False):
        
        '''
        Return whether `message.content` starts with given `prefix`.
        
        Parameters
        ----------
        prefix: `str`
            The prefix to check for.
            
        caseSensitive: `bool`
            Whether the check should be case-sensitive. Defaults to `False`.
        '''
        
        content = self.content.strip()
        content = content.lower() if not caseSensitive else content
        prefix = prefix.lower() if not caseSensitive else prefix
        return content.startswith(prefix)
    
    def endsWith(self, suffix: str, caseSensitive: bool = False):
        
        '''
        Return whether `message.content` ends with given `suffix`.
        
        Parameters
        ----------
        suffix: `str`
            The suffix to check for.
            
        caseSensitive: `bool`
            Whether the check should be case-sensitive. Defaults to `False`.
        '''
        
        content = self.content.strip()
        content = content.lower() if not caseSensitive else content
        suffix = suffix.lower() if not caseSensitive else suffix
        return content.endswith(suffix)
    
    def split(self, seperator: str = ' '):
        
        '''
        Split the message's content by the given `seperator`.
        
        Parameters
        ----------
        seperator: `str`
            The string to separate values by. Defaults to `' '`.
        '''
        
        return self.content.strip().split(seperator)
        
class User:
        
    def __init__(self, bot, data: dict):
        
        from .bot import Bot
        
        _ = data.pop
        
        self.bot: Bot = bot
        
        self.id: int = _("id", None)
        """The user's ID."""

        self.username: str = _("username", None)
        """The user's username (not display name)."""

        self.displayName: str = _("global_name", None)
        """The display name set by the user. Can be None."""

        self.discriminator: int = _("discriminator", 0)
        """The user discriminator (#) for people still using the old system."""

        self.publicFlags: int = _("public_flags", 0)
        """The user's public flags. This is an integer."""

        self.flags: int = _("flags", 0)
        """The user's flags. This is an integer."""

        self.nitroType: int = _("premium_type", 0)
        """The integer representing the purchased nitro subscription type."""

        self.hasNitro: bool = self.nitroType != 0
        """Whether this user has a currently active Nitro subscription."""

        self.profileColor: str = _("accent_color", None)
        """The user's profile color, for nitro users."""

        self.isBot: bool = _("bot", False)
        """Whether this is a bot user."""

        self.avatarHash: str = _("avatar", None)
        """The user's avatar hash found in the avatar url."""

        self.bannerHash: str = _("banner", None)
        """The user's custom banner hash, if they have one."""

        self.bannerColor: str = _("banner_color", None)
        """The color of the user's free banner."""

        self.avatarDecorationData = _("avatar_decoration_data", None)
        self.avatarDecoration = _("avatar_decoration", None)

        for x in ('id', 'discriminator', 'nitroType', 'flags', 'publicFlags'):
            try: setattr(self, x, int(getattr(self, x)))
            except: continue
        
        self.avatar = Avatar(user=self)
        """The user's icon/avatar image."""

        self.bot.__gateway__.users.append(self)

    async def __proc__(self):

        self.channel: Channel = await self.__getChannel__()
        """The user's dm channel with the bot."""
    
    @classmethod
    async def fromID(cls, *, bot, user: int | str):
        '''
        Creates and returns a new User using the user's ID.
        
        Parameters
        ----------
        bot: `Bot`
            A Lunarcord bot object representing your bot client.
            
        message: `int`, `str`
            The ID of the target user.
            
        Returns
        -------
        message: `User`, `None`
            The requested user as a User object, or None if not found.
        '''
        
        data = await bot.__gateway__.manager.loadUser(user)
        new = cls(bot, data)
        await new.__proc__()
        return new
    
    async def __getChannel__(self):
        '''
        Fetches and gets the channel object representing the user\'s direct message channel with your client/bot user. If it doesn\'t exist, it gets created by the bot.
        It's generally better and more advisable for a user to start DM 'conversations' with the bot instead of the bot messaging the user.
        '''

        try:
        
            data = await self.bot.__gateway__.manager.channelFor(self.id)
            
            channel: Channel = Channel(
                bot=self.bot,
                data=data
            )

            await channel.__proc__()
            return channel
        
        except:

            return None
    
    def dm(self, *args, **kwargs) -> Message | None:

        """
        Sends a direct message to the target user. This is a shorthand for `await User.channel.send()`.
        """

        if self.channel:

            return self.channel.send(*args, **kwargs)
    
    @property
    def name(self):
        '''The user\'s global/display name if they have one, otherwise username.'''
        return self.displayName if self.displayName is not None else self.username
    
    @property
    def mention(self):
        '''
        The string used to "mention" the user.
        '''
        
        return f'<@{self.id}>'
    
    def __str__(self):
        return self.name if type(self.name) is str else 'Unknown'
    
    def __repr__(self):
        return f'<User id={self.id} name="{self.name}">'
    
    def __eq__(self, other):
        
        from .bot import Bot
        
        if type(other) is User:
            return self.id == other.id
        
        if type(other) is Bot:
            return self.id == other.id
        
        if type(other) is int:
            return self.id == other
    
    @classmethod
    async def __convert__(cls, object: str, default = None, bot = None):
        
        if type(object) is not str:
            
            if type(object) is not int:
                return object
                
            object = str(object)
        
        base = object # Keep for later usage
        
        object = base.replace('<@', '').replace('>', '').strip()
        
        try:
            snowflake = int(object)
        
        except:
            return default
        
        try:
            user = await cls.fromID(bot=bot, user=snowflake)
            found = user is not None
            
        except:
            found = False
            
        if found:
            return user
        
        return default
    
    def get(self, item: str, default = 0, update: bool = True):
        
        '''
        Get an item from the Database for this `User`.
        
        Parameters
        ----------
        item: `str`
            The name of the item.
            
        default: `Any`
            The default value to return if the item is not found. If not given, this will be `None`.
            
        update: `bool`
            Whether to update the value to `default`, if it is not found, instead of just returning it.
        
        Returns
        -------
        value: `Any`
            The value found, or `default` if not in the database.
        '''
        
        values = self.all()
        
        if type(values) is not dict:
            return default
        
        try:
            
            value = values[item]
            
        except:
            
            value = default
            
            if update:
                self.bot.__gateway__.db.updateUser(
                    id = self.id,
                    item = item,
                    value = default
                )
            
        return value
        
    def set(self, item: str, value):
        
        '''
        Update or create a new key-value pair for this `User` in the Bot's `Database`.
        
        Parameters
        ----------
        item: `str`
            The name of the item.
            
        value: `Any`
            The new value of this item.
        '''
        
        self.all() # Fetch just in case to avoid any errors in the Database
        
        self.bot.__gateway__.db.updateUser(
            id = self.id,
            item = item,
            value = value
        )
        
    def increase(self, item: str, value: int = 1, default: int = 0):
        
        '''
        Increase value of given `item` (must be `int`) by `value` (must also be `int`).
        
        Parameters
        ----------
        item: `str`
            The key-name for the target `int` value. If not found, or if the value is not an integer, `default` will be used.
            
        value: `int`
            How much the target value should be increased. Must be an integer (or convertible to integer).
            
        default: `int`
            Not required. The fallback value if the `item` is not found. Must also be an integer.
            
        Returns
        -------
        new: `int`
            The new value after the increase has been made.
        '''
        
        if type(value) is not int:
            
            try:
                value = int(value)
                
            except:
                raise TypeError('Value must be integer or convertible to integer')
            
        if type(default) is not int:
            
            try:
                default = int(default)
                
            except:
                raise TypeError('Default must be integer or convertible to integer')
        
        current = self.get(item, default)
        
        if type(current) is not int:
            
            try:
                current = int(current)
                
            except:
                raise TypeError('The item\'s value must be integer or convertible to integer')
            
        new = current + value
        self.set(item, new)
        return new
        
    def decrease(self, item: str, value: int = 1, default: int = 0):
        
        '''
        Decrease value of given `item` (must be `int`) by `value` (must also be `int`).
        
        Parameters
        ----------
        item: `str`
            The key-name for the current `int` value. If not found, or if the value is not an integer, `default` will be used.
            
        value: `int`
            How much the target value should be decreased. Must be an integer (or convertible to integer).
            
        default: `int`
            Not required. The fallback value if the `item` is not found. Must also be an integer.
            
        Returns
        -------
        new: `int`
            The new value after the decrease has been made.
        '''
        
        return self.increase(item, -value, default)
        
    def all(self) -> dict:
        
        '''
        Get all values in the Database for this `User`.
        
        Returns
        -------
        values: `dict`
            A dictionary of key-value pairs.
        '''
        
        data = self.bot.__gateway__.db.loadUser(self.id)
        
        if data is None:
            self.bot.__gateway__.db.createUser(self.id)
            return {}
        
        return data
    
    def getCooldowns(self, type: str = "*") -> dict[str, float]:

        """Gets all of the user's saved cooldowns. This is for internal use only."""

        cooldowns: dict[str, dict] = self.get("cooldowns", {})
        type = str(type).lower()

        if type == "*":

            all = {}

            for x in cooldowns:

                value = cooldowns.get(x)

                if type(value) is dict:
                    all.update(value)

            return all
        
        if type == ".":
            return cooldowns
        
        return cooldowns.get(type, {})
    
    def getCooldown(self, name: str, type: str = "*"):
        """Gets a user cooldown with the given `name` of the provided `type`. This is meant to be used internally."""
        return self.getCooldowns(type).get(name, 0.0)
    
    def setCooldown(self, name: str, ends: float, type: str):

        """Creates or updates an already existing user cooldown of given `type`."""

        all = self.getCooldowns(".")
        existing = all.get(type, {})
        existing[name] = float(ends)
        all[type] = existing
        self.set("cooldowns", all)
    
class Channel:
        
    def __init__(self, bot, data):
        
        from .bot import Bot
        
        _ = data.get
        self.bot: Bot = bot
        
        self.raw = data
        
        self.id, self.type, self.flags, self.guild, self.__name__, self.category, self.rateLimit, self.topic, self.position, self.permissionOverwrites, self.nsfw, self.emoji, self.themeColor, self.recipients, self.rtcRegion, self.bitrate = (
            _('id', 0),
            _('type', 0),
            _('flags', 0),
            _('guild_id', None),
            _('name', None),
            _('parent_id', None),
            _('rate_limit_per_user', None),
            _('topic', None),
            _('position', 0),
            _('permission_overwrites', []),
            _('nsfw', False),
            _('icon_emoji', None),
            _('theme_color', None),
            _('recipients', None),
            _('rtc_region', None),
            _('bitrate', 64000)
        )
        
        self.messages: lunarlist[Message] = lunarlist()
        
        self.id: int = int(self.id)
        self.type: int = int(self.type)
        self.lastMessage: Message
        self.flags: int = int(self.flags)
        self.name: str; self.topic: str
        self.permissionOverwrites: list
        self.nsfw: bool
        self.recipients: list
        self.rtcRegion: str
        self.bitrate: int

        if self.position is not None:
            self.position: int = int(self.position)
        
        if self.guild is not None:
            self.guild: int = int(self.guild)
        
        if self.category is not None:
            self.category: int = int(self.category)
        
        if self.rateLimit is not None:
            self.rateLimit: int = int(self.rateLimit)
        
        if self.emoji is not None:
            self.emoji: Emoji = Emoji(self.bot, self.emoji)
        
        if self not in self.bot.__gateway__.channels:
            self.bot.__gateway__.channels.append(self)
            
    @property
    def isDmChannel(self):
        return self.type == 1
    
    @property
    def isTextChannel(self):
        return self.type == 0
    
    @property
    def isVoiceChannel(self):
        return self.type == 2
    
    @property
    def isCategory(self):
        return self.type == 4
    
    @property
    def isGroupChat(self):
        return self.type == 3
    
    @property
    def isAnnouncementChannel(self):
        return self.type == 5
    
    @property
    def isPrivateThread(self):
        return self.type == 12
    
    @property
    def isPublicThread(self):
        return self.type == 11
    
    @property
    def isAnnouncementThread(self):
        return self.type == 10
    
    @property
    def isThread(self):
        return self.isPrivateThread or self.isPublicThread or self.isAnnouncementThread
    
    @property
    def isStageChannel(self):
        return self.type == 13
    
    @property
    def isDirectory(self):
        return self.type == 14
    
    @property
    def isForum(self):
        return self.type == 15
    
    @property
    def isMedia(self):
        return self.type == 16
    
    @property
    def isRenamable(self):
        return not self.isDmChannel and not self.isDirectory
    
    @property
    def isNotRenamable(self):
        return self.isDmChannel or self.isDirectory
    
    @property
    def typeString(self):
        return 'TextChannel' if self.isTextChannel else 'VoiceChannel' if self.isVoiceChannel else 'GroupChat' if self.isGroupChat else 'DirectMessage' if self.isDmChannel else 'Category' if self.isCategory else 'AnnouncementChannel' if self.isAnnouncementChannel else 'AnnouncementThread' if self.isAnnouncementThread else 'PrivateThread' if self.isPrivateThread else 'PublicThread' if self.isPublicThread else 'DirectoryChannel' if self.isDirectory else 'Forum' if self.isForum else 'Media' if self.isMedia else 'StageChannel' if self.isStageChannel else 'UnknownChannel'
    
    @property
    def mention(self):
        '''
        The string used to "mention" the channel.
        '''
        
        return f'<#{self.id}>'
    
    @property
    def children(self):
        '''
        If this `Channel` is a `Category`, return a list of sub-channels in it. If not, return `None`.
        '''
        
        if not self.isCategory:
            return None
        
        return [channel for channel in self.guild.channels if channel.category == self]
    
    async def __proc__(self):
        '''
        Further process the `Channel` to finish its initialization.
        '''
        
        coros = [
            self.bot.fetchChannel(self.category),
            self.bot.fetchGuild(self.guild)
        ]
        
        category, guild = tuple(await asyncio.gather(*coros))
        
        if self.category is not None and category is not None:
            self.category: Channel = category
            
        if self.guild is not None and guild is not None:
            self.guild: Guild = guild
    
    @classmethod
    async def fromID(cls, *, bot, channel: int | str):
        '''
        Creates and returns a new Channel using the channel's ID.
        
        Parameters
        ----------
        bot: `Bot`
            A Lunarcord bot object representing your bot client.
            
        channel: `int`, `str`
            The ID of the desired channel.
            
        Returns
        -------
        channel: `Channel`, `None`
            The requested discord channel as a `Channel` object - or None if not found.
        '''
        
        # if True:
        
        try:
            data = await bot.__gateway__.manager.loadChannel(channel)
        except:
            data = None

        if data:
            newChannel = cls(bot, data)
            await newChannel.__proc__()
        else:
            newChannel = None
            
        return newChannel
    
    def getMessage(self, id: int) -> Message:
        
        try:
            id = int(id)
            
        except:
            return None
        
        for message in self.messages:
            if message.id == id:
                return message
            
    async def fetchMessage(self, id: int) -> Message:
        
        found = self.getMessage(id)
        
        if found is not None:
            return found
        
        return await Message.fromID(bot=self.bot, channel=self.id, message=id)
    
    async def send(self, content: str = None, reference: int = None, embed: Embed = None, embeds: list = [], attachments: list = [], view: View | str = None, button: Button = None, buttons: list[Button] = []) -> Message:
        '''
        Creates a new Message in this Discord channel.
        The newly sent and created Message is returned.
        
        Parameters
        ----------
        content: `str`
            The content of the new message.
            
        reference: `Message`
            The message to reply to. If None (the default value), the new message will not reply to any previously sent messages.
        
        embed: `Embed`
            An embed to send. If both this and the `embeds` parameter are given, they will be mixed together.
            
        embeds: `list`
            A list of `Lunarcord.Embed` objects representing Discord embeds. Can also be one, singular embed to attach - or None (the default value) in order to send no embeds.
        
        attachments: `list`
            A list of `Lunarcord.Attachment` objects representing Discord attachments/files. Can also be one, singular file to attach - or None (the default value) in order to send no attachments.
        
        view: `View`
            A `Lunarcord.View` view made up of buttons or select menus, or the name of an existing View.
            
        button: `Button`
            A `Lunarcord.Button` button to be added to a `View` and sent.
            
        buttons: `list`
            A `list` of `Lunarcord.Button` buttons to be added to the message's view.
            
        Returns
        -------
        message: `Message`
            A `Lunarcord.Message` object representing the Discord message that was sent.
        '''
        
        from .builders import Embed, EmbedArray
        from .ui import View, Button

        if embeds in (None, []):
            embeds = EmbedArray()
        
        if type(reference) is int:
            ... # Keep as is
            
        elif type(reference) is str:
            try: reference = int(reference)
            except: reference = None
        
        elif type(reference) is Message:
            reference = reference.id
            
        else:
            
            reference = None
            
        if embed is not None and type(embed) is Embed:
            
            if True:
            
                if type(embeds) is list:
                    
                    embeds.append(embed)
                    
                elif type(embeds) is EmbedArray:
                    
                    embeds = embeds + embed
                    
        if view is not None and type(view) is not View:
            view = self.bot.getView(str(view))
            
        if button is not None and type(button) is not Button:
            button = None
        
        buttons = [button for button in buttons if type(button) is Button]
        
        if button:
            buttons.append(button)
            
        if buttons:
            
            if not view:
                
                from random import choice
                from string import ascii_letters
                view: View = View(name="".join([choice(ascii_letters) for x in range(10)]))
                view.__register__(self.bot, view.name)
                
            view.addComponents(*buttons)
            
        components = []
            
        if view:
            components = view.toJson()
            
        self.bot.__gateway__.views.append(view)
        
        self.typing = False
        
        new = await self.bot.__gateway__.manager.sendMessage(self.id, content, reference, embeds, attachments, components)
        created = await Message.__create__(self.bot, new)

        if created:

            if view:
                
                view.updateMessages(created)

        return created
    
    async def sendEmbed(self, title: str = None, description: str = None, footer: str = None, footerIcon: str = None, thumbnail: str = None, color: Color = None, image: str = None, timestamp: int | float | str = None, reference: Message | Snowflake = None):

        """
        Creates a new `Embed` and sends it in this channel.
        This is a shorthand for creating a new `Embed` and sending it using `await Channel.send(embed=embed)` where `embed` is your new `Embed`.

        The parameters are the same as the ones for an `Embed`'s constructor.
        """

        from .builders import Embed

        embed = Embed(
            title = title,
            description = description,
            footer = footer,
            footerIcon = footerIcon,
            thumbnail = thumbnail,
            color = color,
            image = image,
            timestamp = timestamp
        )

        await self.send(embed=embed, embeds=[], reference=reference)
    
    async def showTyping(self):
        '''
        Shows that the bot/user is typing in this `Channel`. The typing indicator stops after `10 seconds`, or once the bot sends a new message in the `Channel`.
        '''
        
        await self.bot.__gateway__.manager.showTyping(self.id)
        #self.typing = True
        
    async def rename(self, name: str):
        '''
        Updates the channel's name to the given string.
        If the bot does not have enough permissions to do this, a `PermissionsError` will be raised.
        If the channel is not rename-able, a `TypeError` exception will be raised.
        
        Parameters
        ----------
        name: `str`
            The new channel name.
        '''
        
        if self.isNotRenamable:
            raise TypeError(f'Channel type must be Rename-able, not "{self.typeString}"')
        
        try:
            await self.bot.__gateway__.manager.setChannelName(self.id, name)
            
        except Exception as exception:
            
            exception = exception.args[0]
            
            if exception == 'Missing Permissions':
                raise PermissionsError()
            
            else:
                raise ValueError()
            
    async def addRecipient(self, user: User | Snowflake):
        '''
        Adds a new member / recipient to the group chat.
        If the channel is not a `GroupChat`, raises a `TypeError`.
        The same error can be raised if `user` is not a valid user.
        
        Parameters
        ----------
        user: `User`, `Snowflake`
        The user to add. Can be a `lunarcord.User`, or just their ID (as an integer or convertible to integer).
        '''
        
        if type(user) is int:
            userID = user
            
        elif type(user) is User:
            userID = user.id
            
        else:
            try:
                userID = int(user)
            except:
                raise TypeError(f'Expected User or Snowflake (int), got "{type(user).__name__}"')
        
        if not self.isGroupChat:
            raise TypeError(f'Channel type must be GroupChat, not "{self.typeString}"')
            
        await self.bot.__gateway__.manager.groupDmAddRecipient(self.id, userID)
        
    async def removeRecipient(self, user: User | Snowflake):
        '''
        Removes a member / recipient from the group chat.
        If the channel is not a `GroupChat`, raises a `TypeError`.
        The same error can be raised if `user` is not a valid user.
        `PermissionsError` might also be raised if the user does not have enough permissions.
        Lastly, `IllegalError` will be raised in case of the user not being in the group.
        
        Parameters
        ----------
        user: `User`, `Snowflake`
        The user to remove. Can be a `lunarcord.User`, or just their ID (as an integer or convertible to integer).
        '''
        
        if type(user) is int:
            userID = user
            
        elif type(user) is User:
            userID = user.id
            
        else:
            try:
                userID = int(user)
            except:
                raise TypeError(f'Expected User or Snowflake (int), got "{type(user).__name__}"')
        
        if not self.isGroupChat:
            raise TypeError(f'Channel type must be GroupChat, not "{self.typeString}"')
        
        try:
            
            await self.bot.__gateway__.manager.groupDmRemoveRecipient(self.id, userID)
            
        except Exception as error:
            
            error = error.args[0]
            
            if error == 'Missing Permissions':
            
                raise PermissionsError()
            
            else:
                
                raise IllegalError(error)
        
    
    @property
    def name(self):
        return self.__name__ if self.__name__ is not None else ', '.join([recipient.get('global_name') if recipient.get('global_name') is not None else recipient.get('username') for recipient in self.recipients])
    
    def __str__(self):
        return self.name if type(self.name) is str else 'Unknown'
    
    def __repr__(self):
        return f'<Channel id={self.id} name="{self.name}" type={self.typeString}>'
    
    def __int__(self):
        return self.id
    
    def __eq__(self, other):
        
        if type(other) is Channel:
            
            return self.id == other.id
        
        if type(other) is int:
            
            return self.id == other
        
        if type(other) is str:
            
            try:
                return int(other) == self.id
            
            except:
                return self.name == other
            
        return False
            
        
    
    def __ne__(self, other):
        
        return not self.__eq__(other)
    
    @classmethod
    async def __convert__(cls, object: str, default = None, bot = None):
        
        if type(object) is not str:
            return object
        
        object = object.replace('<#', '').replace('>', '').strip()
        
        try:
            snowflake = int(object)
        
        except:
            return default
        
        try:
            channel: Channel = await bot.fetchChannel(snowflake)
            found = channel is not None
            
        except:
            found = False
            
        if found:
            return channel
        
        return default
    
class Guild:
        
    def __init__(self, bot, data: dict):
        
        from .bot import Bot
        
        _ = data.get
        self.bot: Bot = bot
        
        self.id: int = int(_('id', 0))
        self.name: str = _('name', 'Unknown')
        self.iconHash: str = _('icon')
        self.description: str = _('description')
        self.homeHeader = _('home_header')
        self.splash = _('splash')
        self.discoverySplash = _('discovery_splash')
        self.features: list = _('features', [])
        self.bannerHash: str = _('banner')
        self.owner: int = int(_('owner_id'))
        self.permissions: str = _('permissions')
        self.applicationID: str = _('application_id')
        self.region: str = _('region')
        self.afkChannel: str = _('afk_channel_id')
        self.afkTimeout: int = _('afk_timeout')
        self.systemChannel: str = _('system_channel_id')
        self.systemChannelFlags: int = _('system_channel_flags', 0)
        self.widgetEnabled: bool = _('widget_enabled', False)
        self.widgetChannel: int = _('widget_channel_id', None)
        self.verificationLevel: int = _('verification_level', 0)
        self.roles: list[dict] = _('roles', [])
        self.defaultMessageNotifications: int = _('default_message_notifications', 0)
        self.mfaLevel: int = _('mfa_level', 0)
        self.explicitContentFilter: int = _('explicit_content_filter')
        self.maxPresences = _('max_presences', None)
        self.maxMembers: int = _('max_members', 500000)
        self.maxStageVideoChannelUsers: int = _('max_stage_video_channel_users', 50)
        self.maxVideoChannelUsers: int = _('max_video_channel_users', 25)
        self.vanityUrlCode: str = _('vanity_url_code')
        self.premiumTier: int = _('premium_tier', 0)
        self.premiumSubscriptionCount: int = _('premium_subscription_count', 0)
        self.preferredLocale: str = _('en-US')
        self.rulesChannel: str = _('rules_channel_id')
        self.safetyAlertsChannel: str = _('safety_alerts_channel_id')
        self.publicUpdatesChannel: str = _('public_updates_channel_id')
        self.hubType: int = _('hub_type')
        self.premiumProgressBar: bool = _('premium_progress_bar_enabled', False)
        self.latestOnboardingQuestion: int = _('latest_onboarding_question_id')
        self.nsfw: bool = _('nsfw', False)
        self.nsfwLevel: int = _('nsfw_level', 0)
        self.emojis: list[dict] = _('emojis', [])
        self.emojis: list[Emoji] = [Emoji(self.bot, emoji) for emoji in self.emojis]
        self.stickers: list[dict] = _('stickers', [])
        self.incidentsData = _('incidents_data', None)
        self.inventorySettings = _('inventory_settings')
        self.embedEnabled: bool = _('embed_enabled', False)
        self.embedChannel: str = _('embed_channel_id')
        self.boostLevel: int = self.premiumTier

        self.channels: lunarlist[Channel] = lunarlist()
        self.roles: lunarlist[Role] = lunarlist()
        self.members: lunarlist[Member] = lunarlist()
        
        if self not in self.bot.__gateway__.guilds:
            self.bot.__gateway__.guilds.append(self)
        
    async def __proc__(self):
        '''
        Further process the `Guild`'s initialization.
        '''
        
        coros = [
            self.loadChannels(),
            self.loadRoles(),
            self.loadMembers(),
            self.bot.fetchMember(self, self.owner),
            self.bot.fetchChannel(self.afkChannel),
            self.bot.fetchChannel(self.embedChannel),
            self.bot.fetchChannel(self.rulesChannel),
            self.bot.fetchChannel(self.systemChannel),
            self.bot.fetchChannel(self.widgetChannel)
        ]
        
        results = await asyncio.gather(*coros)
        
        channels, roles, members, owner, afkChannel, embedChannel, rulesChannel, systemChannel, widgetChannel = tuple(results)
        
        self.owner: Member = owner
        self.afkChannel: Channel = afkChannel
        self.embedChannel: Channel = embedChannel
        self.rulesChannel: Channel = rulesChannel
        self.systemChannel: Channel = systemChannel
        self.widgetChannel: Channel = widgetChannel
        
        for channel in channels:
            if channel not in self.channels:
                self.channels.append(channel)

        for role in roles:
            self.roles.append(role)

        for member in members:
            self.members.append(member)
        
        
    async def fromID(*, bot, guild: int | str):
        '''
        Creates and returns a new Guild using the guild's ID.
        
        Parameters
        ----------
        bot: `Bot`
            A Lunarcord bot object representing your bot client.
            
        guild: `int`, `str`
            The ID of the desired guild.
            
        Returns
        -------
        guild: `Guild`, `None`
            The requested discord guild as a Guild object - or `None` if not found.
        '''
        
        try:
            data = await bot.__gateway__.manager.loadGuild(guild)
        
        except:
            data = None
            
        if data is None:
            return None
        
        return await Guild.__create__(bot, data)
    
    async def __create__(bot, data: dict):
        
        '''
        Create and fully initialize a new `Guild` from the given data. 
        '''
        
        if data is None:

            return None
        
        new = Guild(bot, data)
        await new.__proc__()
        return new
    
    @property
    def hasIcon(self):
        return self.icon is not None
    
    @property
    def hasBanner(self):
        return self.banner is not None
    
    @property
    def hasAfkChannel(self):
        return self.afkChannel is not None
    
    @property
    def explicitContentAllowed(self):
        return self.explicitContentFilter == 0
    
    @property
    def hasVanity(self):
        return self.vanityUrlCode is not None
    
    @property
    def vanityUrl(self):
        return 'https://discord.com/invite/' + self.vanityUrlCode if self.hasVanity else None
    
    @property
    def hasHub(self):
        return self.hubType is not None
    
    @property
    def emojiMentions(self):
        '''
        Returns a list of the mentions (eg <:emoji:12345678>) for all of the guild emojis.
        '''
        
        return [emoji.mention for emoji in self.emojis]
    
    @property
    def emojiIDs(self):
        '''
        Returns a list of all the IDs for all the guild emojis.
        '''
        
        return [emoji.id for emoji in self.emojis]
    
    @property
    def emojiNames(self):
        '''
        Returns a list of all the names for all the custom guild emojis.
        '''
        
        return [emoji.name for emoji in self.emojis]
    
    @property
    def iconUrl(self):
        '''
        The `URL` to the guild's icon image.
        '''
        
        return 'https://cdn.discordapp.com/icons/' + self.id + '/' + self.iconHash
    
    @property
    def bannerUrl(self):
        '''
        The `URL` to the guild's banner image.
        '''
        
        return 'https://cdn.discordapp.com/banners/' + self.id + '/' + self.bannerHash
    
    @property
    def hasEmbedChannel(self):
        '''
        Whether this `Guild` has an `EmbedChannel`.
        '''
        
        return self.embedChannel is not None
    
    @property
    def hasRulesChannel(self):
        '''
        Whether this `Guild` has a `RulesChannel`.
        '''
        
        return self.rulesChannel is not None
    
    @property
    def hasSystemChannel(self):
        '''
        Whether this `Guild` has a `SystemChannel`.
        '''
        
        return self.systemChannel is not None
    
    @property
    def hasWidgetChannel(self):
        '''
        Whether this `Guild` has a `WidgetChannel`.
        '''
        
        return self.widgetChannel is not None
    
    @property
    def textChannels(self):
        '''
        A list of all `TextChannel` channels in this `Guild`.
        '''
        
        return [channel for channel in self.channels if channel.isTextChannel]
    
    @property
    def voiceChannels(self):
        '''
        A list of all `VoiceChannel` channels in this `Guild`.
        '''
        
        return [channel for channel in self.channels if channel.isVoiceChannel]
    
    @property
    def categories(self):
        '''
        A list of all `Category` channels (categories) in this `Guild`.
        '''
        
        return [channel for channel in self.channels if channel.isCategory]
    
    @property
    def membersCount(self):
        '''
        Returns the amount of members inside this `Guild`.
        '''

        return len(self.members)
    
    @property
    def me(self):
        '''
        The `Member` of this guild representing your bot.
        '''

        return self.getMember(self.bot.id)
        
    async def loadChannels(self):
        
        '''
        Returns a `list` with all the accessible `Channel` objects in this `Guild`.
        '''
        
        raw = await self.bot.__gateway__.manager.guildChannels(self.id)
        coros = []
        channels: lunarlist[Channel] = []
        
        async def loadChannel(rawChannel):
            
            nonlocal self, channels
            
            if type(rawChannel) is not dict:
                
                return None
            
            channelID = rawChannel.get('id')
            channel = self.bot.getChannel(channelID)
            
            if channel is None:
                
                try:
                    
                    channel = Channel(
                        bot = self.bot,
                        data = rawChannel
                    )
                    
                    await channel.__proc__()
                    
                except:
                    
                    return
            
            if channel:
                
                channels.append(channel)
        
        for rawChannel in raw:
            
            coros.append(loadChannel(rawChannel))
            
        await asyncio.gather(*coros)
            
        return channels
    
    async def loadRoles(self):

        """
        Returns a list of `Role` objects representing all roles in this `Guild`. This is for internal usage only. For external usage, you should make use of `Guild.roles`.
        """

        raw = await self.bot.__gateway__.manager.loadRoles(self.id)
        roles: lunarlist[Role] = []

        coros = []

        async def load(data: dict):

            if type(data) is not dict:
                return

            try:
                role = Role(self.bot, data)
                #await role.__proc__()

            except:
                return
                
            roles.append(role)

        await asyncio.gather(*[load(x) for x in raw])
        return roles
    
    async def loadMembers(self):

        """
        Returns a lunar-list of `Member` objects representing all members in this `Guild`. This is for internal usage.
        """

        raw = await self.bot.__gateway__.manager.loadMembers(self.id)
        members: lunarlist[Member] = []

        async def load(data: dict):

            if type(data) is not dict:
                return

            try:

                user: dict = data.get("user")

                model = await Member.__create__(
                    bot = self.bot,
                    user = user,
                    data = data,
                    guild = self
                )

            except:
                return
                
            members.append(model)

        await asyncio.gather(*[load(x) for x in raw])
        return members
            
    def getRole(self, id: int):
        """
        Gets the role of the given ID and returns it.

        Parameters
        ----------
        id: `int`
            The role's ID. Must be an integer or convertible to integer.

        Returns
        -------
        role: `Role`
            The role that was found, if any, else `None`.
        """

        if type(id) is not int:
            
            try:
                id = int(id)
            except:
                return None

        for role in self.roles:
            if role.id == id:
                return role
            
    def getRoleNamed(self, name: str):
        """
        Gets the role with the given name and returns it.

        Parameters
        ----------
        name: `str`
            The role name. Must be an string or convertible to string.

        Returns
        -------
        role: `Role`
            The role that was found, if any, else `None`.
        """

        if type(name) is not str:
            
            try:
                name = str(name)
            except:
                return None

        for role in self.roles:
            if role.name == name:
                return role
            
        return None
    
    def getEmojiNamed(self, name: str):
        
        '''
        Searches for an emoji with the given `name` and returns it (or `None` if not found).
        
        Parameters
        ----------
        name: `str`
            The target emoji's name. This is not case-sensitive.
            
        Returns
        -------
        emoji: `Emoji`, `None`
            The emoji, or `None` if not found.
        '''
        
        if type(name) is not str:
            
            try:
                name = str(name)
                
            except:
                return None
            
        name = name.lower()
        
        for emoji in self.emojis:
            if name == emoji.name.lower():
                return emoji
            
        return None # Not found
    
    def getMember(self, id: int):
        """Returns the `Member` of this `Guild` with the given `id`, or `None` if not found."""
        return self.bot.getMember(guild=self, id=id)
    
    def fetchMember(self, id: int):
        """Creates a new `Member` object or gets it from the cache. If you want to use this in non-async context, go with `Guild.getMember` to get them directly from the cache."""
        return self.bot.fetchMember(guild=self, id=id)
    
    def __eq__(self, other):
        
        if type(other) is Guild:
            
            return self.id == other.id
        
        if type(other) is int:
            
            return self.id == other
        
        if type(other) is str:
            
            try:
                
                return int(other) == self.id
            
            except:
                
                return self.name == other
            
        return False
    
    def __ne__(self, other):
        
        return not self.__eq__(other)
    
    def __repr__(self):
        
        return f'<Guild id={self.id} name="{self.name}">'
    
    def __str__(self):
        
        return self.name if self.name is not None else 'Unknown'

class Role:

    def __init__(self, bot, data: dict):

        from .bot import Bot
        self.bot: Bot = bot

        _ = data.pop

        self.id = int(_("id"))
        """The role's unique ID."""

        self.name: str = _("name")
        """The `Role`'s name, visible on Discord."""

        self.description: str = _("description")
        """A description describing the role."""

        self.permissions: int = _("permissions")
        """An integer representing the role's permissions."""

        self.position: int = _("position")
        """The role's position in the role hierarchy."""

        self.color: int = _("color")
        """The role's custom color."""

        self.hoist: bool = _("hoist")
        """Whether this role should show up in the guild's members (online & offline) screen."""

        self.managed: bool = _("managed")
        """Whether this role is managed by an integration (is a bot's role)."""

        self.mentionable: bool = _("mentionable")
        """Whether this role can be mentioned (is mentionable)."""

        self.icon: str | None = _("icon")
        """The role's icon hash, if any."""

        self.emoji: str | None = _("unicode_emoji")
        """The unicode emoji representing the role."""

        self.flags: int = _("flags")
        """The role's flags."""

    @property
    def mention(self):
        """
        The string used to mention the role.
        """
        return f"<@&{self.id}>"

    @classmethod
    async def __convert__(cls, object: str, default = None, bot = None):
        
        if type(object) is not str:
            return object
        
        object = object.replace('<@&', '').replace('>', '').strip()
        
        try:
            snowflake = int(object)
        
        except:
            return default
        
        try:
            role: Role = bot.getRole(snowflake)
            found = role is not None
            
        except:
            found = False
            
        if found:
            return role
        
        return default

    def __str__(self):

        return self.name
    
    def __repr__(self):

        return f"<Role id={self.id} name=\"{self.name}\""
    
    def __eq__(self, other):

        return self.id == other.id if type(other) is Role else other == self.id if type(other) is int else self.name == other if type(other) is str else False
        
class Member(User):

    def __init__(self, bot, id: str, data: dict):

        from .bot import Bot

        self.bot: Bot = bot
        self.id: str = id

        _ = data.pop

        self.roles: lunarlist[Role] = _("roles", [])
        """A list of roles that have been assigned to this `Member`."""

        self.boosterSince: int | None = _("premium_since", None)
        """The time (in unix timestamp) since the `Member` started boosting the server, or `None` if they are not a booster."""

        if self.boosterSince is not None:
            self.boosterSince = Utils.isoToUnix(self.boosterSince)

        self.booster: bool = self.boosterSince is not None
        """Whether this member is currently boosting the server."""

        self.muted: bool = _("mute", False)
        """Whether this user has their microphone muted."""

        self.deafened: bool = _("deaf", False)
        """Whether this user is deafened."""

        self.guildAvatarHash: str | None = _("avatar", "")
        """The member's custom server avatar's hash."""

        self.timedOutUntil: int | None = _("communication_disabled_until", None)
        """If the member is currently timed out, this is the time until which they'll be muted. Otherwise, this is `None`."""

        if self.timedOutUntil is not None:
            self.timedOutUntil = Utils.isoToUnix(self.timedOutUntil)

        self.timeout: bool = self.timedOutUntil is not None
        """Whether this member is currently timed out."""

        self.joinedAt: str = _("joined_at", "")
        """The unix timestamp representing the time this user joined the server."""

        self.joinedAt: int = Utils.isoToUnix(self.joinedAt)

        self.nickname: str | None = _("nick", None)
        """The user's guild nickname, if any, else `None`."""

        self.guild: Guild = None
        """The `Guild` guild this member belongs to."""

    async def __proc__(self, data: dict = None):

        if data is None:
            
            data: dict = await self.bot.__gateway__.manager.loadUser(self.id)

        if data:

            super().__init__(self.bot, data)

    def __updateRoles__(self):

        roles: lunarlist[Role] = lunarlist()

        for role in self.roles:

            found = self.guild.getRole(role)

            if found:
                roles.append(found)

        self.roles = roles

    def __setGuild__(self, guild: Guild):

        self.guild = guild

        if self in self.guild.members:
            self.guild.members.remove(self)

        self.guild.members.append(self)
        self.__updateRoles__()

    @classmethod
    async def __create__(cls, bot, user: int | dict, data: dict, guild: Guild = None):

        if type(user) is int:
            userData = None
            userID = user

        elif type(user) is dict:
            userData = user
            userID = 0

        new = cls(bot, userID, data)
        await new.__proc__(userData)

        if guild:
            new.__setGuild__(guild)

        return new
    
    async def addRoles(self, *roles: Role | Snowflake, reason: str = ...):

        """
        Adds the provided roles to the member. If you're unsure whether the user should have one or more roles **removed** instead (based on whether or not they already have it), use `Member.grantRoles` instead.

        Parameters
        ----------
        roles: `Role`, `Snowflake`
            An unlimited amount of roles. Those can be either `lunarcord.Role` objects or just integers (or convertible to integers) representing a discord `Snowflake`.

        reason: `str`
            If given and not `None`, this will show up as the reason in the audit logs.
        """

        coros: list = []

        for role in roles:

            if type(role) is not int:

                if type(role) is Role:

                    role = role.id

                else:

                    try:
                        role = int(role)
                    except:
                        continue

            coros.append(
                self.bot.__gateway__.manager.addRole(self.guild.id, self.id, role, reason)
            )

        await asyncio.gather(*coros)

    async def removeRoles(self, *roles: Role, reason: str = ...):

        """
        Removes the provided roles from the member. If you're unsure whether the user should have one or more roles **added** instead (based on whether or not they already have it), use `Member.grantRoles` instead.

        Parameters
        ----------
        roles: `Role`, `Snowflake`
            An unlimited amount of roles. Those can be either `lunarcord.Role` objects or just integers (or convertible to integers) representing a discord `Snowflake`.

        reason: `str`
            If given and not `None`, this will show up as the reason in the audit logs.
        """

        coros: list = []

        for role in roles:

            if type(role) is not int:

                if type(role) is Role:

                    role = role.id

                else:

                    try:
                        role = int(role)
                    except:
                        continue

            coros.append(
                self.bot.__gateway__.manager.removeRole(self.guild.id, self.id, role, reason)
            )

        await asyncio.gather(*coros)

    async def grantRoles(self, *roles: Role, reason: str = ...):

        """
        For every role given, checks if the user already has it. If they do, removes the `Role`. If they don't, adds it accordingly.

        Parameters
        ----------
        roles: `Role`, `Snowflake`
            An unlimited amount of roles. Those can be either `lunarcord.Role` objects or just integers (or convertible to integers) representing a discord `Snowflake`.

        reason: `str`
            If given and not `None`, this will show up as the reason in the audit logs.
        """

        coros: list = []

        for role in roles:

            if type(role) is not int:

                if type(role) is Role:

                    role = role.id

                else:

                    try:
                        role = int(role)
                    except:
                        continue

            if self.hasRole(role):

                coros.append(
                    self.bot.__gateway__.manager.removeRole(self.guild.id, self.id, role, reason)
                )

            else:

                coros.append(
                    self.bot.__gateway__.manager.addRole(self.guild.id, self.id, role, reason)
                )

        await asyncio.gather(*coros)

    def hasRole(self, role: Role | Snowflake):

        """
        Checks whether the user has the given role.

        Parameters
        ----------
        role: `Role`, `Snowflake`
            Can be a `Role` object, or just an integer or convertible to integer representing the role's ID.
        """

        if type(role) is not Role and type(role) is not int:

            try:
                role = int(role)
            except:
                return False

        for owned in self.roles:
            if role == owned.id or role == owned:
                return True
            
        return False
    
    @classmethod
    async def __convert__(cls, object: str, default = None, bot = None, source = None):

        if type(object) is not str:
            return object
        
        object = object.replace('<@', '').replace('>', '').strip()
        
        try:
            snowflake = int(object)
        
        except:
            return default
        
        try:
            return await bot.fetchMember(source.guild, snowflake)
        except:
            return default

    def __eq__(self, other):

        return other.id == self.id if type(other) in (User, Member) else other == self.id if type(other) is int else int(other) == self.id if type(other) is str and other.isnumeric() else False
    
    def __str__(self):

        return self.nickname if self.nickname is not None else self.name
    
    def __repr__(self):

        nick = f'"{self.nickname}"' if self.nickname is not None else "None"
        return f"<Member id={self.id} name=\"{self.name}\" {nick} roles={len(self.roles)}"
    
class Interaction:

    def __init__(self, /, bot, data: dict):
        
        from .bot import Bot, SlashCommand
        from .ui import SelectMenuOption
        
        _ = data.get
        
        self.version, self.type, self.interactionToken, member, user, self.locale, self.interactionID, self.data, self.applicationID, self.channel, self.guild, self.message = (
            _('version', 1),
            _('type', 2),
            _('token', None),
            _('member', None),
            _('user', None),
            _('locale', 'en-US'),
            _('id', 0),
            _('data', {}),
            _('application_id'),
            _('channel_id'),
            _('guild_id'),
            _('message')
        )
        
        _ = self.data.get
        
        self.options, self.name, self.commandID, self.customID, self.componentType, self.values, self.filled = (
            _('options', []),
            _('name'),
            _('id'),
            _('custom_id'),
            _('component_type'),
            _('values', []),
            _('components', [])
        )
        
        if member is not None and user is None:
            self.__memberData__ = member
            self.author = member.get('user')
            
        else:
            self.author = user
            self.__memberData__ = None
            
        self.values: list[SelectMenuOption]
        self.filled: list[dict]
        self.bot: Bot = bot
        self.command: SlashCommand = None
        self.cooldown: Cooldown = None
        self.acknowledged: bool = False
        self.user: User | Member = ...
        
    @property
    def args(self):
        
        return tuple([option.get('value') for option in self.options])
    
    @property
    def isComponent(self):
        
        return self.componentType is not None
    
    @property
    def resolved(self) -> dict[str]:
        """The resolved data of the `Interaction`."""
        return self.data.get("resolved", {})
    
    @property
    def attachments(self) -> dict[str, dict[str]]:
        """The resolved attachments data, if any."""
        return self.resolved.get("attachments", {})

    async def __proc__(self):
        
        awaitingUser = False
        awaitingMessage = False
        awaitingChannel = False
        awaitingGuild = False
        awaitingMember = False
        
        coros = []

        if self.__memberData__ is None:
        
            if type(self.author) is dict:
                
                authorID: int = self.author.get('id')
                awaitingUser = True
                
                coros.append(
                    self.bot.fetchUser(authorID)
                )
            
        if self.message is not None and type(self.message) is dict:
            
            messageID: int = self.message.get('id')
            
            if self.bot.getMessage(messageID) is None:
                
                awaitingMessage = True
                
                coros.append(
                    Message.__create__(self.bot, self.message)
                )
                
            else:
                
                self.message: Message = self.bot.getMessage(messageID)
            
        if type(self.channel) is str:
            
            channelID: int = int(self.channel)
            awaitingChannel = True
            
            coros.append(
                self.bot.fetchChannel(channelID)
            )
            
        if self.guild is not None and type(self.guild) is str:
            
            guildID: int = int(self.guild)
            awaitingGuild = True
            
            coros.append(
                self.bot.fetchGuild(guildID)
            )

            awaitingMember = True
        
        results: list = await asyncio.gather(*coros)
        
        if awaitingUser:
            self.author: User | Member = results.pop(0)
            self.user = self.author
            
        if awaitingMessage:
            self.message: Message = results.pop(0)
            
        if awaitingChannel:
            self.channel: Channel = results.pop(0)
            
        if awaitingGuild:
            self.guild: Guild | None = results.pop(0)

        if awaitingMember and not awaitingUser:
            authorID = int(self.author.get("id"))
            self.author: User | Member = await self.bot.fetchMember(self.guild, authorID)
            self.user = self.author

        self.interactionID: int = int(self.interactionID)
        self.version: int
        self.type: int
        self.interactionToken: str
        self.locale: str
        self.data: dict
        
    async def send(self, content: str = None, ephemeral: bool = False, catch: bool = True, components: list = [], embed: Embed = True, embeds: list | EmbedArray = [], attachments: list = []):
        '''
        Sends a response message to the interaction - if an already sent one does not exist. If it does, an `InteractionRespondedError` will be raised.
        
        Parameters
        ----------
        content: `str`
            The new response message's content.
            
        ephemeral: `bool`
            Whether the followup should be ephemeral (visible to the user only).
            
        catch: `bool`
            Whether to use `Interaction.followup` instead of raising an `InteractionRespondedError` in case the interaction has already been responded before. For ease of use, this is `True` by default.
        '''
        
        if self.isComponent and self.acknowledged:
            
            await self.followup(content, ephemeral)
            return None
        
        from .builders import Embed, EmbedArray
        from .ui import View
        
        if ephemeral:
            flags = 64
            
        else:
            flags = None
            
        if embed is not None and type(embed) is Embed:
            
            if type(embeds) is list:
                
                embeds.append(embed)
                
            elif type(embeds) is EmbedArray:
                
                embeds = embeds + embed
        
        try:
            embeds = await embeds.__json__()
            if not isinstance(embeds, list) and isinstance(embeds, dict):
                embeds = [embeds]
        except:
            for idx, embed in enumerate(embeds):
                embeds[idx] = await embed.__json__()
                
        #attachments = attachments.__json__()
        attachments = None
      
        payload = {
            'type': 4,
            'data': {
                'content': content,
                'flags': flags,
                'embeds': embeds
            }
        }
        
        try:
            
            await self.bot.manager.respondToInteraction(
                self, payload, attachments
            )
            
            self.acknowledged = True
            
        except Exception as error:
            
            if hasattr(error, 'code'):
                
                if error.code == 400: # Already Responded
                    
                    if catch:
                        await self.followup(content, ephemeral)
                        
                    else:
                        raise InteractionRespondedError()
        
    async def defer(self, ephemeral: bool = False):
        '''
        Shows that the bot is thinking, if an already sent response does not exist. If it does, an `InteractionRespondedError` will be raised.
        
        Parameters
        ----------
        ephemeral: `bool`
            Whether the followup should be ephemeral (visible to the user only).
        '''
        
        flags = 1 << 3
        
        if ephemeral:
            flags += 64
      
        payload = {
            'type': 5,
            'data': {
                'flags': flags
            }
        }
        
        await self.bot.manager.respondToInteraction(
            self, payload
        )
        
        self.acknowledged = True
        
    async def ack(self):
        
        '''
        Acknowledge a `Component` based `Interaction`. This cannot be used with other types of `Interaction` objects (eg with `SlashCommand` ones).
        '''
        
        payload = {
            'type': 6
        }
        
        try:
            
            await self.bot.manager.respondToInteraction(
                self, payload
            )
            
            self.acknowledged = True
            
        except:
            
            ...
    
    async def followup(self, content: str, ephemeral: bool = False):
        '''
        Sends a followup to the original interaction response, if it exists. If not, an `InteractionNotRespondedError` will be raised.
        
        Parameters
        ----------
        content: `str`
            The followup message's content.
            
        ephemeral: `bool`
            Whether the followup should be ephemeral (visible to the user only).
        '''
        
        if ephemeral:
            flags = 64
            
        else:
            flags = None
            
        payload = {
            'content': content,
            'flags': flags
        }
    
        
        await self.bot.manager.post(
            url = f'webhooks/{self.applicationID}/{self.interactionToken}', json = payload
        )
    
    async def edit(self, content: str):
        '''
        Edits the interaction response message, if it exists. If not, an `InteractionNotRespondedError` will be raised.
        
        Parameters
        ----------
        content: `str`
            The new message content for the interaction response.
        '''
        
        payload = {
            'content': content
        }
        
        try:
            await self.__response__('patch', payload)
        except:
            raise InteractionNotRespondedError()
    
    async def delete(self):
        '''
        Deletes the interaction response message, if it exists. If not, an `InteractionNotRespondedError` will be raised.
        
        This method takes no arguments and returns no values.
        '''
        
        try:
            await self.__response__('delete')
            
        except:
            raise InteractionNotRespondedError()
        
    async def sendModal(self, modal: Modal):
        
        from .ui import Modal
        modal: Modal = modal
        
        if type(modal) is not Modal:
            
            return None
            
        payload = {
            'type': 9,
            'data': modal.toJson()
        }
        
        modal.setBot(bot=self.bot)
        
        try:
            
            await self.bot.manager.respondToInteraction(
                interaction = self,
                payload = payload
            )
            
            self.bot.__gateway__.modals.append(modal)
            
        except:
            
            await self.send(":x: Failed to send modal. Please try again later...", ephemeral=True)
        
        
    async def __response__(self, type: str = 'get', payload: dict = None):
        
        url = f'webhooks/{self.applicationID}/{self.interactionToken}/messages/@original'
        return await self.bot.manager.request(url=url, type=type, json=payload)
    
    
class Context:
    
    def __init__(self, /, bot, message: Message, triggerer: str, prefix: str, command):
        
        from .bot import Bot, TextCommand
        
        self.bot: Bot = bot
        self.message: Message = message
        self.msg: Message = self.message
        self.channel: Channel = self.msg.channel
        self.guild: Guild | None = self.channel.guild
        self.author: User | Member = self.msg.author
        self.user: User | Member = self.author
        self.content: str = self.msg.content
        
        self.send = self.msg.send
        self.reply = self.msg.reply
        self.copy = self.msg.copy
        self.delete = self.msg.delete
        self.sendEmbed = self.msg.sendEmbed
        
        self.prefixUsed: str = prefix
        self.triggerer: str = triggerer
        self.command: TextCommand = command

        cdtimer = self.author.getCooldown(self.command.name, "textcommand")
        self.cooldown = Cooldown.construct(cdtimer)
        
    async def wait(self, seconds: float = 0, ms: float = 0):
        
        '''
        Stops the execution of the command callback for given time.
        If both seconds and milliseconds (`ms`) are given, the total time
        will be `seconds + milliseconds / 1000`.
        '''
        
        time = seconds + (ms / 1000)
        await asyncio.sleep(time)

class Emoji:
    
    def __init__(self, bot, data: dict):
        
        from .bot import Bot
        
        self.bot: Bot = bot
        
        self.name: str = data.get('name')
        self.id: int = data.get('id')
        
        if self.id is not None:
            self.id = int(self.id)
        
        self.roles: list = data.get('roles', [])
        self.requireColons: bool = data.get('require_colons', True)
        self.managed: bool = data.get('managed', False)
        self.animated: bool = data.get('animated', False)
        self.available: bool = data.get('available', True)
        
    @property
    def referer(self):
        return self.id if self.id is not None else self.name
    
    @property
    def mention(self):
        
        '''
        The string used to "mention" the custom emoji, eg `<:emoji:12345678>` - or the `:emoji_name:` for default emojis.
        '''
        
        try:
            return f'<:{self.name}:{self.id}>' if self.custom else discord_emoji.to_discord(self.name)[0]
        except:
            return None
    
    @property
    def custom(self):
        
        '''
        Whether this is a custom, guild emoji - otherwise it is just a normal, default discord emoji.
        '''
        
        return self.id is not None
    
    @property
    def default(self):
        
        '''
        Whether this is a default discord emoji - otherwise, it is a custom guild emoji.
        '''
        
        return self.id is None
    
    @property
    def url(self):
        
        '''
        The URL to the emoji image from Discord's Content Delivery Network (CDN).
        '''

        if self.default:
            return
        
        return f'https://cdn.discordapp.com/emojis/{self.id}.png'
    
    @classmethod
    def fromUnicode(cls, unicode: str):

        data = {"name": unicode}
        return cls(None, data)
    
    @classmethod
    def fromName(cls, name: str):

        unicode = discord_emoji.to_unicode(name)

        if not unicode:
            return
        
        return cls.fromUnicode(unicode)
    
    @classmethod
    def fromID(cls, id: str):

        id = str(id)
        pattern = r"<:.*:(\d+)>"

        match = re.search(pattern, id)

        if match:
            id = match.group(1)

        try:
            id = int(id)
        except:
            return None
        
        data = {"id": id}
        return cls(None, data)
    
    @classmethod
    def create(cls, source: str):

        emoji = cls.fromName(source)

        if not emoji:
            emoji = cls.fromID(source)

        if not emoji:
            return cls.fromUnicode(source)
        
        return emoji

    async def load(self, quality: int = 'lossless', size: int = 48) -> bytes:
        
        '''
        The emoji image data in bytes.
        
        Parameters
        ----------
        quality: `int`
            The image quality. Can be 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 or 2048. An additional option, which is also the default, is "lossless".
            
        size: `int`
            The image's width and height (in pixels). Defaults to 48.
            
        Returns
        -------
        data: `bytes`
            The image content of the emoji in raw bytes.
        '''
        
        if self.default:
            return b''
        
        url = f'{self.url}?quality={quality}&size={size}'
        return await self.bot.__gateway__.manager.get(url, customUrl=True, returns=bytes)
    
    async def save(self, path: str = None, quality: int = 'lossless', size: int = 48):
        
        '''
        Saves the emoji image with given `quality` and `size` to the given `path`
        
        Parameters
        ----------
        path: `str`
            The path to save the emoji to. Defaults to the emoji's name.
            
        quality: `int`
            The image quality. Can be 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 or 2048. An additional option, which is also the default, is "lossless".
            
        size: `int`
            The image's size (in pixels). Defaults to 48.
        '''
        
        if path is None:
            path = f'{self.name}.png'
            
        data = await self.load(quality, size)
            
        with open(path, 'wb') as output:
            output.write(data)
        
    def __repr__(self):
        
        return f'<Emoji id={self.id}, name="{self.name}">'
    
    def __str__(self):
        
        return self.name
    
    def __int__(self):
        
        return self.id
        
        
class Reaction:
    
    def __init__(self, bot, user: int, message: int, channel: int, emoji: dict):
        
        from .bot import Bot
        
        self.bot: Bot = bot
        """The `Bot` bot in which this `Reaction` object belongs to."""

        self.user = user
        """The user who reacted with this `Reaction`."""

        self.emoji = emoji
        """The `Emoji` emoji represented by this `Reaction`."""

        self.message = message
        """The `Message` message that this `Reaction` belongs to."""

        self.channel = channel
        """The `Channel` this `Reaction`'s `Message` belongs to."""
        
    @property
    def exists(self):
        
        return self in self.message.reactions
    
    @property
    def userID(self):

        """The ID of the user who reacted with this `Reaction`."""
        return self.user.id
    
    @property
    def emojiName(self):

        """The name of this reaction's emoji."""
        return self.emoji.name
    
    @property
    def emojiID(self):

        """The ID of this reaction's emoji."""
        return self.emoji.id
        
    async def remove(self):
        
        '''
        Remove the reaction from its message if it is yours (or if you have enough permissions to remove others' reactions), otherwise raise a `PermissionsError`. The same exception can be raised if the reaction has already been removed.
        '''
        
        if not self.user.id == self.bot.id:
            raise PermissionsError()
        
        if not self.exists:
            raise PermissionsError()
        
        await self.message.unreact(self.emoji)
        
    async def __proc__(self):
        
        self.channel: Channel = await self.bot.fetchChannel(self.channel)
        self.message: Message = await self.bot.fetchMessage(self.channel.id, self.message)
        self.user: User = await self.bot.fetchUser(self.user)
        self.emoji: Emoji = Emoji(self.bot, self.emoji)
        
        if self.message:
            
            self.message.reactions.append(self)
        
    def __repr__(self):
        
        return f'<Reaction message="{self.message}", user="{self.user}", emoji="{self.emoji}">'
    
    def __str__(self):
        
        return self.emoji.name
    
    def __eq__(self, other):

        return self.emoji == other if type(other) is Emoji else self.emoji.name == other if type(other) is str else self.emoji.id == other if type(other) is int else False
        
class Avatar:

    """A class representing a user's avatar as an image."""

    def __init__(self, user: User):

        self.user = user
        self.bot = self.user.bot

    @property
    def hash(self):

        """The avatar hash."""

        return self.user.avatarHash
    
    @property
    def url(self):


        """The URL leading to the user avatar in Discord's CDN."""

        return self.generate()

    def generate(self, quality: int | str = ..., size: int = ...) -> str:

        """
        Generates a URL with customized proportions for this avatar image.
        """

        if quality is ... and size is ...:

            return f'https://cdn.discordapp.com/avatars/{self.user.id}/{self.hash}.png'

        if quality is ...:

            quality = "lossless"

        if size is ...:
            
            size = 48

        return f"{self.url}?quality={quality}&size={size}"

    async def load(self, quality: int | str = ..., size: int = ...) -> bytes:
        
        '''
        Reads and returns the raw data (in `bytes`) of this user icon.
        
        Parameters
        ----------
        quality: `int`
            The image quality. Can be 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 or 2048. An additional option, which is also the default, is "lossless".
            
        size: `int`
            The image's width and height (in pixels). Defaults to 48.
            
        Returns
        -------
        data: `bytes`
            The image content of the avatar in raw bytes.
        '''
        
        url = self.generate(quality=quality, size=size)
        return await self.bot.__gateway__.manager.get(url, customUrl=True, returns=bytes)
    
    async def save(self, path: str = None, quality: int = 'lossless', size: int = 48):
        
        '''
        Saves the emoji image with given `quality` and `size` to the given `path`
        
        Parameters
        ----------
        path: `str`
            The path to save the emoji to. Defaults to the emoji's name.
            
        quality: `int`
            The image quality. Can be 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 or 2048. An additional option, which is also the default, is "lossless".
            
        size: `int`
            The image's size (in pixels). Defaults to 48.
        '''
        
        if path is None:
            path = f'{self.user.username}.png'
            
        data = await self.load(quality, size)
            
        with open(path, 'wb') as output:
            output.write(data)

    def __str__(self):

        return str(self.url)
    
    def __repr__(self):

        return str(self)
        
class Status:
    def __init__(self, activity: str | Activity, mobile: bool = False, type: str = 'online'):
        '''
        A discord status which you can later use for your bot by doing so:
        
        `bot.status = Status(activity, mobile, type)`
        
        Parameters
        ----------
        activity: `str`, `Lunarcord.Activity`
            A custom activity. Example usages:
            
            `activity = Lunarcord.Watching('Lunarcord')` or
            `activity = 'Watching Lunarcord'`
            
        mobile: `bool`
            Whether the bot should show up as if it was logged in from a mobile device (True) or a desktop device (False).
            
        type: `str`
            A status - can be one of the following: 
            
            `online`, `idle`, `dnd`, `offline`
        '''

        self.activity = activity
        self.mobile = mobile
        self.type = type