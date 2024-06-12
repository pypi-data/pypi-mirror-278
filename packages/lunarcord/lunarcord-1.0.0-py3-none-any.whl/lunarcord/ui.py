'''
A lunarcord extension that aims to make the usage of `Components`, `Buttons` and `SelectMenus` easier with the use of `View` objects.
Below is a small snippet showcasing how this extension can possibly be used to create a single `Button` and send it:

```
from lunarcord import ui, Bot

bot = Bot()

@bot.event()
async def onReady():

    view = ui.View()
    
    @view.button("Click Me!", style=ui.ButtonStyle.Green)
    async def button1(interaction):
    
        await interaction.send("Click!", ephemeral=True)
        
    channel = await bot.fetchChannel(12345678)
    await channel.send(f"Logged in as **{bot}**!", view=view)
    
bot.run("EXAMPLE123TOKEN45")
```

The above example would create a `Bot` that, upon logging in, sends a new `Message` in the `Channel` of ID `12345678` which contains a button with the label "Click Me!". Upon clicking the button, an ephemeral `Message` will appear, reading "Click!".
For more examples, read more about `Views` in lunarcord's official docs (`SOON`).
'''

from typing import TypeVar, Generic, Callable
from .__core__.requests import asyncio
from .basetypes import Channel, Context, Interaction, Channel, Message, Emoji
from .__core__.addons import Utils
from .__core__.types import Registrable
from .errors import NotRegisteredError

import time

T = TypeVar('T')

class Component:
    
    def __init__(self, type: int, customID: str = None, row: int = None, callbacks: list = []):
        
        '''
        A base class for all `Component` types (`ActionRow`, `Button`, `SelectMenu`, `Modal`).
        '''
        
        if not isinstance(type, int):
            
            try:
                type = int(type)
                
            except:
                type = 1
        
        self.type: int = type
        
        if customID:
            self.customID: str = customID
        
        if row:
            self.row: int = row
            
        self.callbacks = callbacks
        self.bot = None
        self.message: Message = None
        self.underlying: View = None
        
    @property
    def size(self):
        
        '''
        How much size of an `ActionRow` this `Component` takes. This is usually either `1` or `5`.
        '''
        
        if self.type == View.TEXT_INPUT:
            
            return 5
        
        if self.type == View.BUTTON:
            
            return 1
        
        return 0
    
    @property
    def attached(self):
        
        '''
        Whether this `Component` is part of a `View`.
        '''
        
        return self.underlying is not None
    
    @property
    def view(self):
        
        '''
        The `View` this `Component` is attached to. If it isn't attached to any views, creates a new one containing it and returns it.
        '''
        
        if not self.attached:
            
            return self.toView()
        
        return self.underlying
    
    def toView(self):
        
        '''
        Creates a new `View` which consists of this `Component` only.
        '''
        
        return View(self)
    
    def addTo(self, view):
        
        '''
        Adds this `Component` to the given `View`. Returns the `ActionRow` if any.
        '''
        
        if view and type(view) is View:
            
            return view.addComponent(self)
        
        return None
    
    def remove(self):
        
        '''
        Removes this `Component` from its underlying `View`, if any, and returns the `Row` it was in.
        '''
        
        if self.attached:
            
            return self.underlying.removeComponent(self)
        
        return None
    
    def setView(self, view):
        
        '''
        Removes this `Component` from its current `View`, if any, and adds it to the new one.
        '''
        
        self.remove()
        return self.addTo(view)
        
    def toJson(self) -> dict:
        
        '''
        Converts this `Component` to a JSON-like `dict`.
        '''
        
        jsonified = {
            'type': self.type
        }
        
        if self.type != View.ACTION_ROW and self.customID is not None:
            
            jsonified['custom_id'] = self.customID
            
        return jsonified
        
class ActionRow(Generic[T], Component):
    
    def __init__(self, idx: int):
        
        '''
        Represents an action row component with other sub-components in it.
        '''
        
        super().__init__(View.ACTION_ROW)
        
        self.components: list[Component] = []
        self.totalSpace: int = 5
        self.idx: int = idx
        
    @property
    def size(self):
        
        '''
        Returns the total occupied `ActionRow` size for this action row based on all components inside it.
        '''
        
        total = 0
        
        for component in self.components:
            
            total += component.size
            
        return total
            
    @property
    def length(self):
        
        '''
        The amount of `Component` objects inside this `ActionRow` action row.
        '''
        
        return len(self.components)
            
    @property
    def space(self):
        
        '''
        Returns how much component size / space is left in this `ActionRow` action row.
        '''
        
        return self.totalSpace - self.size
    
    @property
    def hasSpaceForButtons(self) -> bool:
        
        '''
        Whether you can add more buttons to this `ActionRow`, or not if it's already full.
        '''
        
        return self.space >= 1
    
    @property
    def hasSpaceForSelect(self) -> bool:
        
        '''
        Whether you can add a `SelectMenu` to this `ActionRow`, or not if there are other components already.
        '''
        
        return self.space >= 5
        
    def hasSpaceFor(self, component: Component):
        
        '''
        Returns a `bool` representing whether you can and should add this `Component` inside this `ActionRow` or not.
        '''
        
        if type(component) is Button:
            
            return self.hasSpaceForButtons
        
        elif type(component) is SelectMenu:
            
            return self.hasSpaceForSelect
        
        return False
    
    def extend(self, *rows):
        
        '''
        Extends this `ActionRow` action row by adding as many components as possible from the other `rows` to it.
        '''
        
        for row in rows:
            
            if type(row) is not ActionRow:
                
                continue
            
            for component in row:
                
                if self.hasSpaceFor(component):
                    
                    self.addComponent(component)
        
    def toJson(self):
        
        components = []
        type = self.type
        
        for component in self.components:
            
            components.append(
                component.toJson()
            )
            
        jsonified = {
            'type': self.type,
            'components': components
        }
        
        return jsonified
    
    def addComponent(self, component: Component):
        
        '''
        Adds a sub-component to this `ActionRow` component.
        '''
        
        if not self.hasSpaceFor(component):
            raise IndexError('Not enough action row space')
        
        component.row = self.idx
        self.components.append(component)
        
    def removeComponent(self, component: Component):
        
        '''
        Removes an already added component from this `ActionRow` action row. Raises `ValueError` if this `Component` is not present.
        '''
        
        try:
            
            self.components.remove(component)
            
        except ValueError:
            
            raise ValueError('Component not in action row')
        
    def __iter__(self):
        
        return self.components.__iter__()
        
class ButtonStyle:
    
    class Primary: id = 1
    class Secondary: id = 2
    class Success: id = 3
    class Danger: id = 4
    class Link: id = 5
    
    class Blurple: id = 1
    class Gray: id = 2
    class Grey: id = 2
    class Green: id = 3
    class Red: id = 4
        
class Button(Component):
    

    
    def __init__(self, name: str = None, customID: str = None, style: ButtonStyle = ButtonStyle.Primary, emoji: str | int = None, row: int = None, callback: Callable = None):
        
        '''
        A clickable message `Component` that can have one or more callbacks.
        
        Parameters
        ----------
        name: `str`
            The button's name/title/label. This will show up on Discord.
            
        customID: `str`
            A custom ID to be used for identifying this button. Must be unique among all other components in its `View`. If not given, it is automatically derived from the button's label for you.
            
        style: `ButtonStyle`
            A ButtonStyle, or a string representing a style, or an int representing a style's ID.
            
        row: `int`
            The row this should be placed in in your `View`. If not given, Lunarcord automatically handles it for you.
            
        callback: `Callable`
            A callback function that should be ran when someone on Discord presses this button.
        '''
        
        if name is None:
            name = 'Button'
            
        if customID is None:
            customID = name.lower().replace(' ', '_')
            
        try:
            style = style.id
            
        except:
            
            try:
                style = int(style)
                
            except:
                
                if type(style) is str:

                    style = style.lower()
                    
                    match style:
                        case 'primary', 'blurple':
                            style = 1
                        case 'secondary', 'gray', 'grey':
                            style = 2
                        case 'success', 'green':
                            style = 3
                        case 'danger', 'red':
                            style = 4
                        case 'link', 'url':
                            style = 5
                    
                else:
                    style = 1
            
        super().__init__(View.BUTTON, customID)
            
        self.name: str = name
        self.row: int = row
        self.style: int = style
        self.callbacks: list = []

        self.emoji: Emoji | None = None

        if type(emoji) in (str, int):
            emoji = Emoji.create(emoji)

        if type(emoji) is Emoji:
            self.emoji = emoji
        
        if callback is not None:
            self.bind(callback)
            
    def connect(self, callback):
        
        '''
        Add an on clicked callback for this `Button`. When someone on Discord clicks this `Button`, the connected `callback` will be called.
        '''
        
        if callable(callback):
            
            self.callbacks.append(callback)
            
    def bind(self, *callbacks):
        
        '''
        Similarly to `Button.connect()`, this allows you to add another callback. The only difference is that you can pass multiple callbacks at once here.
        '''
        
        for callback in callbacks:
            
            self.connect(callback)
            
    def callback(self, func = None):
        
        '''
        You can use this as a decorator for your callback instead of using `Button.connect`.
        '''
        
        if func is not None and callable(func):
            
            return self.connect(func)
        
        return self.connect
        
    def toJson(self):
        
        jsonified = {
            'type': self.type,
            'label': self.name,
            'custom_id': self.customID,
            'style': self.style
        }

        if self.emoji is not None:
            
            emoji = {
                'name': self.emoji.name,
                'id': self.emoji.id,
                'animated': self.emoji.animated
            }

            jsonified['emoji'] = emoji
        
        return jsonified
    
    def __str__(self):
        
        return f'<Button name="{self.name}" customID="{self.customID}" row={self.row}>'
    
    async def __call__(self, interaction, *args, **kwargs):
        
        '''
        Execute all bound/connected callback functions as if the button has been clicked.
        '''
        
        from .__core__.addons import Utils
        
        coros = []
        
        for callback in self.callbacks:
            
            coros.append(
                
                Utils.execute(callback, interaction, *args, self.bot, **kwargs)
                
            )
            
        await asyncio.gather(*coros)
    
class SelectMenuOption:
    
    def __init__(
        self,
        name: str,
        value: str = None,
        description: str = None,
        emoji: str | int = None,
        callback: Callable = None
    ):
        
        if value is None:
            
            value = name.lower().replace(' ', '_')
        
        self.name: str = name
        self.value: str = value
        self.description: str = description
        self.callbacks: list[Callable] = []

        self.emoji: Emoji | None = None

        if type(emoji) in (str, int):
            emoji = Emoji.create(emoji)

        if type(emoji) is Emoji:
            self.emoji = emoji
        
        if callback is not None:
            self.connect(callback)

        self.bot = None
        self.message: Message = None
            
    def connect(self, callback: Callable):
        
        '''
        Connect a `Callback` function to be executed when this `SelectMenuOption` is called.
        '''
        
        if callable(callback):
            
            self.callbacks.append(callback)
            
    def bind(self, *callbacks: Callable):
        
        '''
        Similar to `SelectMenuOption.connect()`, but allows you to connect multiple `callback` functions by passing all of them at once.
        '''
        
        for callback in callbacks:
            
            self.connect(callback)
            
    def callback(self, func = None):
        
        '''
        You can use this as a decorator for your callback instead of using `SelectMenuOption.connect` or `SelectMenuOption.bind`.
        '''
        
        if func is not None and callable(func):
            
            self.connect(func)
        
    def copy(self):
        
        '''
        Returns a shallow copy of this `SelectMenuOption` option.
        '''
        
        return SelectMenuOption(self.name, self.value, self.description, self.emoji)
        
    def toJson(self):
        
        data = {
            'label': self.name,
            'value': self.value
        }
        
        if self.description is not None:
            
            data['description'] = self.description
            
        if self.emoji is not None:
            
            emoji = {
                'name': self.emoji.name,
                'id': self.emoji.id,
                'animated': self.emoji.animated
            }
            
            data['emoji'] = emoji
            
        return data
    
    def __str__(self):
        
        string = f'<SelectMenuOption name="{self.name}"'
            
        if self.emoji is not None:
            
            string += f' emoji={self.emoji}'
            
        return string + '>'
    
    def __repr__(self):
        
        return self.name
    
    async def __call__(self, interaction, *args, **kwargs):
        
        '''
        Execute all bound/connected callback functions as if the option has been clicked.
        '''
        
        from .__core__.addons import Utils
        
        coros = []
        
        for callback in self.callbacks:
            
            coros.append(
                
                Utils.execute(callback, interaction, *args, self.bot, **kwargs)
                
            )
            
        await asyncio.gather(*coros)
    
    
class SelectMenu(Component):
    
    def __init__(self, name: str = None, options: list[SelectMenuOption] = None, customID: str = None, row: int = None, minvalues: int = 1, maxvalues: int = 1, callback: Callable = None):
        
            
        if type(options) not in (list, tuple, set):
            
            options = []
            
        options = [option for option in options if type(option) is SelectMenuOption]
        
        if customID is None:
            
            value = name if name is not None else '_'.join([option.value.replace(' ', '_') for option in options]) if len(options) >= 1 else 'Select Menu'
            customID = value.lower().replace(' ', '_')
            
        super().__init__(View.STRING_SELECT, customID)
        
        self.name: str = name
        self.callbacks: list[Callable] = []
        self.row: int = row
        self.options: list[SelectMenuOption] = options
        self.min: int = minvalues
        self.max: int = maxvalues
        
        if callback:
            
            self.bind(callback)
            
    def connect(self, callback):
        
        '''
        Add an on clicked callback for this `SelectMenu`. When someone on Discord clicks this `Selectmenu`, the connected `callback` will be called.
        '''
        
        if callable(callback):
            
            self.callbacks.append(callback)
            
    def bind(self, *callbacks):
        
        '''
        Similarly to `SelectMenu.connect()`, this allows you to add another callback. The only difference is that you can pass multiple callbacks at once here.
        '''
        
        for callback in callbacks:
            
            self.connect(callback)
            
    def callback(self, func = None):
        
        '''
        You can use this as a decorator for your callback instead of using `SelectMenu.connect` or `SelectMenu.bind`.
        '''
        
        if func is not None and callable(func):
            
            self.connect(func)
    
    def addSelectOption(self, option: SelectMenuOption):
        
        '''
        Adds a `SelectMenuOption` to the select menu's options.
        '''
        
        if type(option) is SelectMenuOption:
            self.options.append(option)
    
    def addOption(
        self,
        name: str,
        value: str = None,
        description: str = None,
        emoji: str | int = None
    ):
        
        '''
        Creates a new `SelectMenuOption` and adds it to the `SelectMenu`. If you want to add a `SelectMenuOption` object that you have, use `SelectMenu.addSelectOption()`.
        '''
        
        newOption = SelectMenuOption(name, value, description, emoji)
        self.addSelectOption(newOption)
        return newOption
    
    def option(self, name: str = None, value: str = None, description: str = None, emoji: str | int = None):
        
        '''
        A decorator that creates a new `SelectMenuOption` with the decorated function as its `Callback`, adds it to the `SelectMenu`, and returns it.
        '''
        
        def decorator(decorated: Callable) -> Button:
            
            nonlocal self, name, value, description, emoji
        
            option = self.addOption(
                
                name = name,
                value = value,
                description = description,
                emoji = emoji
                
            )
            
            option.bind(decorated)
            return option
            
        return decorator
    
    
    def toJson(self):

        if self.min < 1:
            self.min = 1

        if self.max > len(self.options):
            self.max = -1

        if self.max == -1:
            self.max = len(self.options)
        
        data = {
            'type': self.type,
            'custom_id': self.customID,
            'min_values': self.min,
            'max_values': self.max,
            'options': [option.toJson() for option in self.options]
        }
        
        if self.name:
            
            data['placeholder'] = self.name
            
        return data
    
    async def __call__(self, interaction, *args, **kwargs):
        
        '''
        Execute all bound/connected callback functions as if an option of the select menu has been clicked.
        '''
        
        from .__core__.addons import Utils
        
        coros = []
        
        for callback in self.callbacks:
            
            coros.append(
                
                Utils.execute(callback, interaction, *args, self.bot, **kwargs)
                
            )
            
        await asyncio.gather(*coros)
    
    def __str__(self):
        
        return f'<SelectMenu name="{self.name}" customID="{self.customID}" row={self.row}>'
    
class TextInputStyle:
    
    class Short: '''Single-line text input.'''; type = 1
    class Paragraph: '''Multi-line text input.'''; type = 2

    class Small: '''Multi-line text input.'''; type = 1
    class Big: '''Multi-line text input.'''; type = 2
    
    class SingleLine: '''Multi-line text input.'''; type = 1
    class MultiLine: '''Multi-line text input.'''; type = 2
    
    STYLES: list[type] = [Short, Paragraph, Small, Big, SingleLine, MultiLine]
    
class TextInput:
    
    def __init__(
        self,
        name: str = None,
        style: TextInputStyle = TextInputStyle.Short,
        minLength: int = None,
        maxLength: int = None,
        placeholder: str = None,
        required: bool = True,
        customID: str = None,
        callback: Callable = None
    ):
        
        '''
        A text-input object for `Modal` Components.
        '''
        
        if minLength is None or type(minLength) is not int:
            
            try: minLength = int(minLength)
            except: minLength = 1
            
        if maxLength is None or type(maxLength) is not int:
            
            try: maxLength = int(maxLength)
            except: maxLength = 4000
            
        if customID is None:
            
            customID = name.lower().replace(' ', '_')
            
        if type(style) is not int and style not in TextInputStyle.STYLES:
            
            style = TextInputStyle.Short
            
        else:
            
            if type(style) is not int:
                
                style = style.type
        
        self.bot = None
        self.name: str = name
        self.style: TextInputStyle = style
        self.customID: str = customID
        self.minLength: int = minLength
        self.maxLength: int = maxLength
        self.placeholder: str = placeholder
        self.required: bool = required
        self.value: str = None
        self.callbacks: list[Callable] = []
        
        if callback and callable(callback):
            
            ...
            
    def connect(self, callback: Callable):
        
        '''
        Connect a `Callback` function to be executed when this `TextInput` is filled.
        '''
        
        if callable(callback):
            
            self.callbacks.append(callback)
            
    def bind(self, *callbacks: Callable):
        
        '''
        Similar to `TextInput.connect()`, but allows you to connect multiple `callback` functions by passing all of them at once.
        '''
        
        for callback in callbacks:
            
            self.connect(callback)
            
    def callback(self, func):
        
        '''
        You can use this as a decorator for your callback instead of using `TextInput.connect` or `TextInput.bind`.
        '''
        
        if func is not None and callable(func):
            
            self.connect(func)
            
    def toJson(self) -> dict[str, int | list[dict[str]]]:
        
        row = {
            'type': View.ACTION_ROW,
            'components': []
        }
        
        data = {
            'type': View.TEXT_INPUT,
            'custom_id': self.customID,
            'label': self.name,
            'style': self.style,
            'min_length': self.minLength,
            'max_length': self.maxLength,
            'required': self.required
        }
        
        if self.placeholder is not None:
            data['placeholder'] = self.placeholder
        
        row['components'].append(data)
        
        return row
    
    def __str__(self):
        
        return f'<TextInput name="{self.name}" customID="{self.customID}" value="{self.value}">'
    
    def __repr__(self):
        
        return self.name.__repr__()
    
    async def __call__(self, interaction, *args, **kwargs):
        
        '''
        Execute all bound/connected callback functions as if this input has been filled.
        '''
        
        from .__core__.addons import Utils
        
        coros = []
        
        for callback in self.callbacks:
            
            coros.append(
                
                Utils.execute(callback, interaction, *args, self.bot, **kwargs)
                
            )
            
        await asyncio.gather(*coros)
    
    
        
        
    
class Modal():
    
    def __init__(self, name: str = None, inputs: list[TextInput] = None, customID: str = None, callback: Callable = None):
        
        '''
        A message `Component` made up of multiple `TextInput` text inputs.
        This component allows you to take inputs from users.
        
        Parameters
        ----------
        name: `str`
            The title that shows up on the modal.
            
        inputs: `list`
            A list of `TextInput` objects to be added upon creation.
            
        customID: `str`
            A developer-defined `customID` for this `Component`. If not given, this is automatically derived from the `name`.
            
        callback: `Callable`
            A callable (function, method or class) to be executed once a response has been given.
        '''
        
        if type(inputs) not in (list, tuple, set):
            
            inputs = []
        
        if name is None:
            
            name = 'Modal'
            
        if customID is None:
            
            customID = name.lower().replace(' ', '_')
            
        self.bot = None
        self.name: str = name
        self.customID: str = customID
        self.callbacks: list[Callable] = []
        self.inputs: list[TextInput] = []
        
        if callback and callable(callback):
            
            self.bind(callback)
            
        for input in inputs:
            
            if type(input) is TextInput:
                
                self.inputs.append(input)
            
    def connect(self, callback):
        
        '''
        Add an on clicked callback for this `Modal`. When someone on Discord sends something through this `Modal`, the connected `callback` will be called.
        '''
        
        if callable(callback):
            
            self.callbacks.append(callback)
            
    def bind(self, *callbacks):
        
        '''
        Similarly to `Modal.connect()`, this allows you to add another callback. The only difference is that you can pass multiple callbacks at once here.
        '''
        
        for callback in callbacks:
            
            self.connect(callback)
            
    def callback(self, func = None):
        
        '''
        You can use this as a decorator for your callback instead of using `Modal.connect` or `Modal.bind`.
        '''
        
        if func is not None and callable(func):
            
            self.bind(func)
            
    def addInput(self, input: TextInput):
        
        '''
        Add another `TextInput` input to this `Modal`.
        '''
        
        if type(input) is not TextInput:
            
            return None
        
        self.inputs.append(input)
        
    def createInput(
        self,
        name: str = None,
        style: TextInputStyle = TextInputStyle.Short,
        minLength: int = None,
        maxLength: int = None,
        placeholder: str = None,
        required: bool = True,
        customID: str = None,
        callback: Callable = None
    ):
        
        '''
        Create a new `TextInput`, add it to the `Modal`, and return it.
        '''
        
        input = TextInput(name, style, minLength, maxLength, placeholder, required, customID)
        input.connect(callback=callback)
        self.addInput(input=input)
        return input
        
        
    def input(
        self,
        name: str = None,
        style: TextInputStyle = TextInputStyle.Short,
        minLength: int = None,
        maxLength: int = None,
        placeholder: str = None,
        required: bool = True,
        customID: str = None
    ):
        
        '''
        A decorator that creates a new `TextInput` with the given arguments and the decorated function as its callback, and adds it to the `Modal`.
        '''
        
        def decorator(function: Callable) -> TextInput:
            
            nonlocal name, style, minLength, maxLength, placeholder, required, customID
            
            if not callable(function):
                
                return None
            
            return self.createInput(name, style, minLength, maxLength, placeholder, required, customID, function)
        
        return decorator
            
            
    def setBot(self, bot):
        
        '''
        For internal use only. Updates the `bot` value for this `Modal` and all of its `TextInput` input components.
        '''
        
        self.bot = bot
        
        for input in self.inputs:
            
            input.bot = bot
            
    def toJson(self):
        
        data = {
            'title': self.name,
            'custom_id': self.customID,
            'components': [inp.toJson() for inp in self.inputs]
        }
        
        return data
            
    async def __call__(self, interaction: Interaction, *args, **kwargs):
        
        '''
        Execute all bound/connected callback functions as if an option of the select menu has been clicked.
        '''
        
        from .__core__.addons import Utils
        
        coros = []
        
        for callback in self.callbacks:
            
            coros.append(
                
                Utils.execute(callback, interaction, *args, self.bot, **kwargs)
                
            )
            
        await asyncio.gather(*coros)
    
    def __str__(self):
        
        return f'<Modal name="{self.name}" customID="{self.customID}" inputs={self.inputs}>'
    
    def __repr__(self):
        
        return self.name
            

    
class View(Registrable):
    
    ACTION_ROW = 1
    BUTTON = 2
    STRING_SELECT = 3
    TEXT_INPUT = 4
    USER_SELECT = 5
    ROLE_SELECT = 6
    MENTIONABLE_SELECT = 7
    CHANNEL_SELECT = 8
    
    VALID_COMPONENT_TYPES = [1, 2, 3, 4, 5, 6, 7, 8]
    SELECT_MENU = [3, 5, 6, 7, 8]
    
    def __init__(self, name: str = ..., permanent: bool = False):
        
        '''
        Creates a new `View` with the given components in it. Views can be made up of `Button` and `SelectMenu` objects.

        Parameters
        ----------
        name: `str`
            A name that you will use to recognize your `View`. You can use this later to get it using `Bot.loadView()`.

        permanent: `bool`
            Whether the `View` should live forever. If this is set to `False`, the view will be no longer functional after not being used for 24 hours.
        '''
        
        self.rows: list[ActionRow[Component]] = [ActionRow(x + 1) for x in range(5)]
        
        for row in self.rows:
            
            row.underlying = self
        
        self.bot = None
        self.messages: list[Message] = []
        self.last: float = time.time()

        self.permanent: bool = permanent
        self.name = name

    @property
    def name(self) -> str:
        return self.__viewname__
    
    @name.setter
    def name(self, new: str):

        if type(new) is not str:
            if new not in (..., None):
                new = str(new)

        if self.__checkName__(new):
            self.__viewname__ = new

    def __checkName__(self, name: str) -> bool:

        if self.bot is None:
            return True
        
        for view in self.bot.__gateway__.views:

            if view.name == name:

                raise NameError("Can't have two or more views of the same name")
            
        return True

    def __register__(self, bot, name: str):

        from .bot import Bot
        bot: Bot = bot
        gw = bot.__gateway__
        gw.views.append(self)
        self.bot: Bot = bot
        
        if self.name in (..., None):
            self.name = name

        for child in self.children:
            if hasattr(child, "setBot"):
                child.setBot(bot)
            elif hasattr(child, "bot"):
                child.bot = bot

        self.bot.__gateway__.__updateSavedViews__()

    def __unregister__(self):

        if self.bot is None:
            return
        
        try:
            self.bot.__gateway__.views.remove(self)
        except:
            ...

        self.bot = None

            
    @property
    def components(self):
        
        '''
        All the components in this `View`, from all `ActionRow` rows, in one list.
        '''
        
        all: list[Component] = []
        
        for row in self.rows:
            
            all.extend(
                row.components
            )
            
        return all
    
    @property
    def buttons(self) -> list[Button]:
        
        '''
        All the buttons in this `View`, from all `ActionRow` rows. This is the same as `View.components`, but this contains buttons only.
        '''
        
        return [component for component in self.components if component.type == View.BUTTON]
    
    @property
    def selectMenus(self) -> list[SelectMenu]:
        
        '''
        All the select menus in this `View`, from all `ActionRow` rows.
        '''
        
        return [component for component in self.components if component.type in View.SELECT_MENU]
    
    @property
    def length(self):
        
        '''
        Returns an integer representing the amount of all components inside this `View`.
        '''
        
        return len(self.components)
    
    @property
    def children(self):

        '''
        Returns all of the View's children, whether those are `ActionRow` rows or any type of `Component`.
        '''

        return self.components + self.rows
    
    @property
    def expired(self):

        '''
        Whether more than a day has passed since the last interaction.
        '''

        return self.last > time.time() + 86400
    
    @property
    def alive(self):

        '''
        Whether this `View` is still alive. To prevent it from dying, set `View.permanent` to `True`.
        '''

        return self.expired if not self.permanent else True
        
    def addComponent(self, component: Component):
        
        '''
        Adds a new `Component` to the best available `ActionRow` and returns it. If no action row is available or the given row is full, raises an `IndexError`. Another exception that may be raised is `KeyError`, when a component with the same custom ID already exists.
        '''
        
        if not self.isUnique(component.customID):
            
            raise KeyError('Component customID must be unique to its view')
        
        if component.row is None or type(component.row) is not int:
        
            for row in self.rows:
                
                try:
                    
                    row.addComponent(component)
                    component.underlying = self
                    #component.row = row.row
                    return row
                    
                except:
                    
                    continue
                
            raise IndexError('No action row available')
        
        else:
            
            if component.row > 5 or component.row > 1:
                
                raise IndexError('Invalid action row')
            
            try:
                
                index = component.row - 1
                row = self.rows[index]
                row.addComponent(component)
                component.underlying = self
                return row
            
            except:
                
                raise IndexError('Action row does not have enough space')
    
    def removeComponent(self, component: Component):
        
        '''
        Removes an already added `Component` from its corresponding `ActionRow` and returns the action row. Raises `ValueError` if the given `Component` is not present.
        '''
        
        for row in self.rows:
            
            try:
                
                row.removeComponent(component)
                component.underlying = None
                return row
            
            except:
                
                continue
            
        raise ValueError('Component not in any action rows')
    
    def addComponents(self, *components: Component):
        
        '''
        Add all given `Component` objects to this `View`, ignoring any errors that would normally be raised by using just `addComponent`.
        '''
        
        for component in components:
            
            try:
                self.addComponent(component)
                
            except:
                continue
            
    def removeComponents(self, *components: Component):
        
        '''
        Remove all given `Component` objects from this `View`, ignoring any errors that would normally be raised by using just `removeComponent`.
        '''
        
        for component in components:
            
            try:
                self.removeComponent(component)
                
            except:
                continue
            
    def getComponent(self, customID: str, default = None):
        
        '''
        Gets a `Component` by its `customID` which should have been passed when it was created. If not found, `default` will be returned.
        '''
        
        for component in self.components:
            
            if customID == component.customID:
                
                return component
            
        return default
    
    def getButton(self, customID: str, default = None):
        
        '''
        Gets a `Button` by its `customID`. This is the same as using `getButton`, but is limited to `Button` objects and no other component types.
        '''
        
        for button in self.buttons:
            
            if customID == button.customID:
                
                return button
            
        return default
    
    def getSelectMenu(self, customID: str, default = None):
        
        '''
        Gets a `SelectMenu` by its `customID`. This is the same as using `getButton`, but is limited to `SelectMenu` objects and no other component types.
        '''
        
        for select in self.selectMenus:
            
            if customID == select.customID:
                
                return select
            
        return default
    
    def isButtonUnique(self, customID: str):
        
        '''
        Get whether the `customID` given is unique and not used for any other buttons.
        '''
        
        return self.getButton(customID) is None
    
    def isSelectMenuUnique(self, customID: str):
        
        '''
        Get whether the `customID` given is unique and not used for any other select menus.
        '''
        
        return self.getSelectMenu(customID) is None
    
    def exists(self, customID: str):
        
        '''
        Returns whether a `Component` which goes by this `customID` already exists.
        '''
        
        return self.getComponent(customID) is not None
    
    def isUnique(self, customID: str):
        
        '''
        Returns whether a component `customID` is unique and not used by any other components.
        '''
        
        return not self.exists(customID)
            
    def createComponent(self, component: type[Button | SelectMenu], *args, **kwargs):
        
        '''
        Create a new `Component` of given `component` type with the applied `*args` arguments and `**kwargs` keyword arguments, adding it to the view and returning it.
        '''
        
        if component not in (Button, SelectMenu):
            
            return None
        
        new = component(*args, **kwargs)
        self.addComponent(new)
        return new
    
    def addButton(self, name: str = None, customID: str = None, style: int = 1, emoji: str | int = None, row: int = None) -> Button:
        
        '''
        Create a new `Button`, add it to the `View`, and return it just in case it's needed for later use.
        '''
        
        return self.createComponent(
            
            component = Button,
            name = name,
            customID = customID,
            style = style,
            emoji = emoji,
            row = row
            
        )
        
    def addSelect(self, name: str = None, options: list[SelectMenuOption] = None, customID: str = None, minvalues: int = 1, maxvalues: int = 1, row: int = None) -> SelectMenu:
        
        '''
        Create a new `SelectMenu`, add it to the `View`, and return it.
        '''
        
        return self.createComponent(
            
            component = SelectMenu,
            options = options,
            name = name,
            customID = customID,
            minvalues = minvalues,
            maxvalues = maxvalues,
            row = row
        )
        
    def button(self, name: str = None, customID: str = None, style: int = 1, emoji: str | int = None, row: int = None):
        
        '''
        A decorator that creates a new `Button` with the decorated function as its `Callback`, adds it to the `View`, and returns it.
        '''
        
        def decorator(decorated: Callable) -> Button:
            
            nonlocal self, name, customID, style, row
        
            button = self.addButton(
                
                name = name,
                customID = customID,
                style = style,
                emoji = emoji,
                row = row
                
            )
            
            button.bind(decorated)
            return button
            
        return decorator
    
    def select(self, name: str = None, options: list[SelectMenuOption] = None, customID: str = None, minvalues: int = 1, maxvalues: int = 1, row: int = None):
        
        '''
        A decorator that creates a new `SelectMenu` with the decorated function as its `Callback`, adds it to the `View`, and returns it.
        '''
        
        def decorator(decorated: Callable) -> SelectMenu:
            
            nonlocal self, name, customID, row
        
            select = self.addSelect(
                
                options = options,
                name = name,
                customID = customID,
                minvalues = minvalues,
                maxvalues = maxvalues,
                row = row
                
            )
            
            select.bind(decorated)
            return select
            
        return decorator
    
    def extend(self, *views):
        
        '''
        Extends this `View` by adding as many `Component` components from the other `views` to it as possible.
        '''
        
        views = [view for view in views if type(view) is View]
        
        for view in views:
            
            for row in self:
                
                row.extend(view.rows)
            
    async def send(
        self,
        ctx: Context | Interaction = ...,
        channel: Channel = ...,
        *args, **kwargs
    ) -> Message | None:
        
        '''
        Sends the `View` as a `Message` with the given `ctx` as a `Context` or an `Interaction`. Instead of passing some context, you can pass a `channel` to send this to. If none of these parameters is passed or the types are invalid, nothing will happen.
        You can use arguments and keyword arguments to be used when sending the message, eg `content = "This is a view"`
        '''
        
        if ( ctx in (..., None) and channel in (..., None) ) or ( not ctx and not channel ):
            
            return None
        
        if channel and type(channel).__name__ != 'Channel':
            
            args += (channel,)
            channel = None
        
        if ctx and ctx not in (..., None):
            
            try:
                
                return await ctx.send(*args, **kwargs, view=self)
                
            except:
                
                return None
            
        if channel and channel not in (..., None):
            
            try:
                
                return await channel.send(*args, **kwargs, view=self)
            
            except:
                
                return None
                
    
    def toJson(self):
        
        '''
        Converts this `View` and all of its components and their sub-components into a json-like `dict` dictionary.
        '''

        if self.bot in (None, ...):

            raise NotRegisteredError(self)
        
        jsonified = [
            
            row.toJson()
            for row in self.rows
            if row.components
            
        ]
        
        return jsonified
    
    def save(self):

        """
        Saves this `View` and its children to the bot's database.
        """

        db = self.bot.__gateway__.db

        if not db.viewExists(self.name):

            db.createView(self.name)

        self.update("msgs", [msg.id if type(msg) is Message else msg for msg in self.messages])
        self.update("nm", self.name)
        self.update("lst", self.last)

    def update(self, item, value):

        self.bot.__gateway__.db.updateView(self.name, item, value)

    def updateLast(self):

        self.last = time.time()
        self.save()

    def updateMessages(self, new: Message):

        self.messages.append(new)
        self.save()

    def delete(self):

        """
        Deletes the permanent `View` from your DataBase (lunardata.db) for whatever reason.
        """

        self.bot.__gateway__.db.deleteView(self.name)

    @property
    def messageIDs(self):
        return [message.id if type(message) is Message else int(message) for message in self.messages]
    
    def __str__(self):
        
        return f'<View name="{self.name}" components={self.length}>'
    
    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        
        return self.rows.__iter__()
    
    def __len__(self):

        return self.length
    
def button(name: str = None, customID: str = None, style: int = 1, emoji: str | int = None, row: int = None, view: View = None):
    
    '''
    A decorator that creates a new `Button` with the decorated function as its `Callback` and returns it.
    '''
    
    def decorator(decorated: Callable) -> Button:
        
        nonlocal name, customID, style, row
    
        return Button(
            
            name = name,
            customID = customID,
            style = style,
            emoji = emoji,
            row = row,
            callback = decorated
            
        )
        
    return decorator