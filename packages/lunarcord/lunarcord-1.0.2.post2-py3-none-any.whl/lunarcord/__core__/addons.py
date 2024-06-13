import inspect, datetime, sys, json, sqlite3, os, asyncio, sys, re, random, time
from typing import TypeVar, Generic, Callable, Iterator

from importlib.util import spec_from_file_location, module_from_spec

from string import ascii_letters as asciiLetters, digits
lettersAndDigits = asciiLetters + digits

T = TypeVar('T')

        
class SlashOption:
    def __init__(self, name: str = ..., description: str = ..., required: bool = True, options: list = ..., default = None):
        
        '''
        Represents a Slash Command option. This should be used for building bot Slash Commands.
        Below is a simple example of how this class can be used:
        
        ```
        @bot.slashCommand(description="Repeats your message.")
        async def say(
            interaction: Interaction,
            message: str = SlashOption(name="message", description="The message to repeat", default="No message provided.")
        ):
        
            await interaction.send(message)
        ```
        
        The above code demonstrates how you can use this class along with the `slashCommand` decorator in order to create the basic, famous "say" / "echo" command.
        Of course, you can use this class however you like in order to create slash command options as you like.
        The following is the list of all parameters you can use while creating an object of this class, and their explanations...
        
        Parameters
        ----------
        name: `str`
            The argument's name on discord. By default, this will be the same as the argument name in code.
        
        description: `str`
            The description seen on discord. If not given, a placeholder description is used.
            
        required: `bool`
            Whether this argument should be required (True) or optional (False). This is by default True (required).
            
        default: `Any`
            The value to be given to you when the command user doesn't really provide any value (this can only happen with optional/not required arguments; Required ones can never be empty).
        '''
        
        if name is ...:
            name = None
            
        if description is ...:
            description = None
            
        if options is ...:
            options = None
        
        self.name = name
        self.description = description
        self.options = options
        self.required = required
        self.default = default
        
    def setName(self, new: str = ...):
        
        if new is not ...:
            self.name = new
            
        return self
            
    def setDescription(self, new: str = ...):
        
        if new is not ...:
            self.description = new
            
        return self
            
    def makeOptional(self):
        
        self.required = False
        return self
        
    def makeRequired(self):
        
        self.required = True
        return self
        
    def setDefault(self, default = ...):
        
        if default is not ...:
            self.default = default
            
        return self
            
    def setOptions(self, options: list = ...):
        
        if options is ...:
            options = None
            
        self.options = options
        
        return self

class Utils:
    
    def argsCount(function):
        
        return len(Utils.arguments(function))
    
    def slashOptions(function, *, Types):
        
        # OPTION TYPES
        # 3: STRING
        # 4: INTEGER
        # 5: BOOLEAN
        # 6: USER
        # 7: CHANNEL
        # 8: ROLE
        # 9: MENTIONABLE
        # 10: NUMBER
        # 11: ATTACHMENT
        
        options = []
        
        params = Utils.arguments(function)
        allparams = params.copy()
        interaction = params.pop(0)
        
        User, Channel, Role, Member, Mentionable, Attachment = Types
        
        for param in params:
            
            paramtype = param.get('type')
            
            if paramtype is str:
                ftype = 3
                
            elif paramtype is int:
                ftype = 4
                
            elif paramtype is bool:
                ftype = 5
                
            elif paramtype is float:
                ftype = 10
                
            elif paramtype is Channel:
                ftype = 7
                
            elif paramtype in (User, Member):
                ftype = 6

            elif paramtype is Role:
                ftype = 8

            elif paramtype is Attachment:
                ftype = 11
                
            else:
                ftype = 3
                
            name = param.get('name')
            hint = param.get('default')
            
            if type(hint) is SlashOption:
                description = hint.description if hint.description is not None else 'No description provided'
                required = hint.required
                defaultval = hint.default
            else:
                description = 'No description provided'
                required = True
                defaultval = hint
            
            option = {'name': name, 'description': description, 'type': ftype, 'required': required, 'default': None}
            options.append(option)
            
        return options, allparams
        
    def istype(object, *types):
        return isinstance(object, types)
    
    def isstr(object):
        return Utils.istype(object, str)
    
    def isint(object):
        return Utils.istype(object, int)
    
    def isfloat(object):
        return Utils.istype(object, float)
    
    def isStringOrInt(object):
        return Utils.isstr(object) or Utils.isint(object)

    def isIntOrFloat(object):
        return Utils.isint(object) or Utils.isfloat(object)
    
    def isStringOrFloat(object):
        return Utils.isstr(object) or Utils.isfloat(object)
    
    def isStringIntOrFloat(object):
        return Utils.isstr(object) or Utils.isint(object) or Utils.isint(object)
    
    def toJson(object):
        try:
            jsonified = object.__json__()
        except:
            jsonified = {'error': 'NotJsonifiable'}
            
        return jsonified
    
    def manager(bot):
        return bot.__gateway__.manager
    
    def unixToIso(timestamp: int | float):
        return datetime.datetime.utcfromtimestamp(float(timestamp)).isoformat()
    
    def isoToUnix(timestamp: str):
        return datetime.datetime.fromisoformat(str(timestamp)).timestamp()
    
    def isAwaitable(function):
        return inspect.iscoroutinefunction(function)
    
    def arguments(function) -> list[dict]:
        
        signature = inspect.signature(function)
        params = list(signature.parameters.values())
        values = []
        
        for idx, param in enumerate(params):
            
            appears = str(param)
            name = [part.strip() for part in appears.split(':')]
            
            if len(name) == 1:
                appears = name[0]
                
            elif len(name) == 2:
                typehint = name[1]
                typehint = typehint.split('.')[-1]
                appears = f'{name}: {typehint}'
            
            data = {
                'name': param.name,
                'default': param.default,
                'required': param.default is param.empty,
                'type': param.annotation,
                'index': idx,
                'empty': param.empty,
                'isEmpty': lambda x: x is param.empty,
                'appears': appears,
                'isArgs': appears.startswith('*') and not appears.startswith('**'),
                'isKwargs': appears.startswith('**')
            }
            
            values.append(data)
            
        return values
    
    async def convert(value, annotation, empty, bot, default, source = None):
        
        if value is None:
            return value
        
        try:
            typename = type(annotation).__name__
        except:
            typename = None
            
        annotations = []
            
        if typename == 'UnionType':
            
            if hasattr(annotation, '__args__'):
                annotations = list(annotation.__args__)
                
            else:
                annotations = [annotation]
                
        else:
            
            annotations = [annotation]
            
        unfixed = type(value)
            
        for annotation in annotations:
            
            if unfixed == annotation:
                continue
            
            if hasattr(annotation, '__convert__'):
                
                try:
                    converter = annotation.__convert__
                    converterArgs = Utils.arguments(converter)
                    converterLen = len(converterArgs)
                    converterSupplies = [value]
                    
                    if converterLen > 1:
                        converterSupplies.append(empty)
                        
                    if converterLen > 2:
                        converterSupplies.append(bot)

                    if converterLen > 3:
                        converterSupplies.append(source)
                        
                    if Utils.isAwaitable(converter):
                        value = await converter(*converterSupplies)
                        
                    else:
                        value = converter(*converterSupplies)
                    
                except:
                    
                    #import traceback
                    #traceback.print_exc()
                    ...
                    
                if not value == empty:
                    break
                
            elif annotation in (str, int, float, list, tuple, dict, set):
                
                try:
                    value = annotation(value)
                    
                except:
                    ...
                
        if value == empty:
            value = default
            
        return value
    
    async def execute(function, *args, bot = None, params: list[dict] = None, **kwargs):
        
        if bot is not None:
            kwargs['bot'] = bot
        
        if len(args) == 1:
            args = [args[0]]
            
        else:
            args = list(args)
        
        if params is None:
            required: list[dict] = Utils.arguments(function)
            
        else:
            required: list[dict] = params
            
        passing: list = []
        
        for param in required:
            
            name: str = param.get('name')
            isRequired: bool = param.get('required')
            annotation: type = param.get('type')
            default = param.get('default')
            idx: int = param.get('index')
            empty: type = param.get('empty')
            isArgs: bool = param.get('isArgs')
            
            if type(default) is SlashOption:
                
                default = default.default
            
            if isArgs:
                
                value = args[idx:]
                value = [await Utils.convert(x, annotation, empty, bot, x, args[0]) for x in value]
                passing.extend(value)
                
            else:
            
                try:
                    value = args[idx]
                
                except:
                    value = default if default is not empty else None
                    
                if value is None and name in kwargs:
                    
                    value = kwargs.get(name)
                
                if type(value) is str and value.strip() == '':
                    value = None
                    
                value = await Utils.convert(value, annotation, empty, bot, default, args[0])
                
                passing.append(value)
        
        if Utils.isAwaitable(function):
            await function(*passing)
            
        else:
            function(*passing)
            
    def removeFirst(amount: int, string: str):
        
        if type(amount) is str:
            amount = len(amount)
        
        string: list = list(string)
        
        for x in range(amount):
            
            string.pop(0)
            
        return str(''.join(string))
    
    def removeLast(amount: int, string: str):
        
        if type(amount) is str:
            amount = len(amount)
        
        string: list = list(string)
        
        for x in range(amount):
            
            string.pop()
            
        return str(''.join(string))
    
    def floatParts(number: float):
        
        '''
        Splits a `float` to two parts - integer and decimal.
        '''
        
        if type(number) is not float:
            number = float(number)
            
        parts = str(number).split('.')
        
        integer = 0
        decimal = 0
        
        if len(parts) >= 1:
            integer = int(parts[0])
            
        if len(parts) >= 2:
            decimal = int(parts[1])
            
        return integer, float(f'0.{decimal}')
    
    def floatDecimal(number: float) -> int:
        '''
        Splits a `float` to two parts and returns the decimal (second part).
        '''
        
        integer, decimal = Utils.floatParts(number)
        return decimal
    
    def disableLine(code: list[str], line: int) -> list[str]:
        
        '''
        Disable a specific line from the given lines of code.
        Return the results as a list of strings representing lines.
        '''
        
        try:
            value = code[line]
            
        except:
            return code
        
        new = '# ' + value
        
        # new is value but
        # in a comment so
        # that value is
        # not executed.
        
        code[line] = new # Replace old value with new.
        
        return code # Return the final code.
    
    def disableLineWithFunction(code: list[str], function: Callable | str):
        
        '''
        Disable line(s) containing the given function.
        Return the updated code as a list of strings, representing lines.
        '''
        
        ignoring: list[int] = []
        
        if type(function) is not str:
            
            try:
                function = function.__name__
                
            except:
                return code
            
        done = False
        
        while not done:
            
            index = None
        
            for idx, line in enumerate(code):
                if function + '(' in line:
                    index = idx
                    
            if index is None or index in ignoring:
                
                done = True
                continue
            
            code = Utils.disableLine(code, index)
            ignoring.append(index)
                
        return code
    
    def removeDuplicates(iterable: list):
        
        '''
        Return a copy of the given list with all the duplicate values removed.
        '''
        
        return list(dict.fromkeys(iterable))
    
    def module(name: str, path: str, locations: list = None, exec: bool = True):

        spec = spec_from_file_location(name, path, submodule_search_locations=locations)
        module = module_from_spec(spec)

        if exec:
            spec.loader.exec_module(module)

        return module
    
    def getImports(lines: list[str]):

        imports: list[str] = []

        patterns = [
            r'^\s*import\s+.+',
            r'^\s*from\s+\S+\s+import\s+.+'
        ]

        combined = '|'.join(patterns)

        for line in lines:
            if re.match(combined, line):
                imports.append(line.removesuffix("\n"))

        return imports
    
    def getImportsRaw(lines):
        
        return "\n".join(Utils.getImports(lines))
    
    def functionToString(function: Callable, imports: bool = True):

        source = inspect.getsource(function)

        if not imports:
            return source
        
        mpath = inspect.getfile(function)
        mname = mpath.removesuffix(".py")
        module = Utils.module(mname, mpath, exec=False)
        msource = inspect.getsourcelines(module)[0]
        imports = Utils.getImportsRaw(msource)

        source = source.split("\n")

        if len(source) >= 0 and source[0].startswith("@"):
            source.pop(0) # Remove decorator

        source = "\n".join(source)

        return imports + "\n\n" + source
    
    def stringToFunction(string: str) -> Callable | None:

        sections = string.split("\n\n")
        imports = sections.pop(0)
        code = "\n\n".join(sections)

        exec(imports)
        before = locals()
        exec(code)
        after = locals()

        pairs = list(after.items())
        pairs.reverse()
        pairs = tuple(pairs)
        
        for key, value in pairs:

            if callable(value):

                return value
            
    def ending(amount: int):

        if amount == 1:
            return ""
        
        return "s"
    
    def generateString(length: int = 14, exceptions: list[int] = []):

        while True:

            string = "".join([random.choice(lettersAndDigits) for x in range(length)])

            if string not in exceptions:
                return string
    
class _(Exception):
    def __init__(self, start: str, message: str):
        self.start = start
        self.message = message
        
        sys.tracebacklimit = 0
        super().__init__(self.msg)
        
    @property
    def msg(self):
        return self.start + ' ' + self.message
    
class Debugger:
    def __init__(self, hide: bool = False, method: int = 2):
        self.method: int = method
        self.hide: bool = hide
        self.last: str = None
        self.logs: list = []
    
    @property
    def hiding(self):
        return self.hide
    
    @hiding.setter
    def hiding(self, value: bool):
        if isinstance(value, bool) and value in (False, True):
            self.hide = value
        else:
            return None
        
    def disable(self):
        
        self.hiding = True
        
    def enable(self):
        
        self.hiding = False
        
    def __send__(self, message: str, force: bool = False):
        if not self.hide or force:
            if self.method == 1: # Print
                print('[LUNARCORD] ' + str(message))
                
            elif self.method == 2:
                raise _('[LUNARCORD]', message)
            
            else:
                return
            
            self.last: str = message
            self.logs.append(message)
            
    def filter(self, message: str, replacer: str = '%p', values: tuple = ()):
        for value in values:
            value = str(value)
            message = message.replace(replacer, value, 1)
            
        return message
            
    def log(self, message: str, *values, force: bool = False):
        if len(values) == 1:
            values = [values[0]]
        
        message = self.filter(
            message,
            '%p',
            values
        )
        
        self.__send__(message, force)
        
class Signal:
    
    def __init__(self, *types):
        
        self.__arguments__ = types
        self.__argsCount__ = len(types)
        self.__connected__ = []
        self.data = None
        
    def connect(self, *functions):
        try:
            if hasattr(functions, '__iter__'):
                for function in functions:
                    try:
                        if callable(function):
                            self.__connected__.append(function)
                    except:
                        pass
        except:
            pass
        
    async def call(self, *supplies, ignored: list[Callable] = []):
        
        functions = self.__connected__
        
        for function in functions:
            
            if function in ignored:
                
                continue
            
            try:
                signature = inspect.signature(function)
                arguments = list(signature.parameters.keys())
                argsCount = len(arguments)
                supplied = []
                
                for s in supplies:
                    index = supplies.index(s)
                    if index + 1 <= argsCount:
                        signalArg = self.__arguments__[index]
                        if signalArg != type(s) and signalArg != object:
                            
                            try:
                                s = signalArg(s)
                                
                            except:
                                s = None
                                
                        supplied.append(s)
            except:
                continue
        
            unsupplied = argsCount - len(supplied)
            if unsupplied >= 1:
                for x in range(unsupplied):
                    supplied.append(None)
                    
            coro = function(*supplied)
            
            if Utils.isAwaitable(function):
                await coro
                
    def callSync(self, *supplies):
        '''
        Same as `Signal.call`, but ignores all `async def` functions so that you can also use this in a non-async context.
        '''
        
        functions = self.__connected__
        ignoring = [function for function in functions if Utils.isAwaitable(function)]
        
        for function in functions:
            
            if function in ignoring:
                
                continue
            
            try:
                signature = inspect.signature(function)
                arguments = list(signature.parameters.keys())
                argsCount = len(arguments)
                supplied = []
                
                for s in supplies:
                    index = supplies.index(s)
                    if index + 1 <= argsCount:
                        signalArg = self.__arguments__[index]
                        if signalArg != type(s) and signalArg != object:
                            
                            try:
                                s = signalArg(s)
                                
                            except:
                                s = None
                                
                        supplied.append(s)
            except:
                continue
        
            unsupplied = argsCount - len(supplied)
            if unsupplied >= 1:
                for x in range(unsupplied):
                    supplied.append(None)
                    
            function(*supplied)
            
    async def wait(self, loop: asyncio.AbstractEventLoop, timeout: float = None) -> tuple | None:
        
        '''
        Blocks your code until this signal has been called from anywhere.
        '''
        
        future = loop.create_future()
        
        def onComplete(*results):
            
            nonlocal future
            future.set_result(results)
            
        self.connect(onComplete)
        
        try:
            return await future

        finally:
            self.remove(onComplete)
        
        
    def disconnect(self, *functions):
        try:
            for function in functions:
                try:
                    self.__connected__.remove(function)
                except:
                    pass
        except:
            pass
        
    def updateArg(self, index, newType):
        try:
            self.__arguments__[index] = newType
        except:
            pass
        
    def argsList(self):
        return list(self.__arguments__)
    
    def connList(self):
        return list(self.__connected__)
        
    def removeArg(self, index):
        try:
            argList = self.argsList()
            del argList[index]
            argTuple = tuple(argList)
            self.__arguments__ = argTuple
            self.__argsCount__ -= 1
        except:
            pass
        
    def addArg(self, index, arg):
        try:
            argList = self.argsList()
            argList.insert(index, arg)
            argTuple = tuple(argList)
            self.__arguments__ = argTuple
            self.__argsCount__ += 1
        except:
            pass
        
    def appendArg(self, arg):
        try:
            self.addArg(self.__argsCount__, arg)
        except:
            pass
        
    def resetConns(self):
        for conn in self.conns():
            self.disconnect(conn)
            
    async def __call__(self, *supplies):
        
        return await self.call(*supplies)

    async def emit(self, *supplies): return await self.call(*supplies)
    def emitSync(self, *supplies): return self.callSync(*supplies)
    def add(self, *functions): return self.connect(*functions)
    def remove(self, *functions): return self.disconnect(*functions)
    def args(self): return self.argsList()
    def conns(self): return self.connList()
    def add(self, index, arg): return self.addArg(index, arg)
    def append(self, arg): return self.appendArg(arg)
    def reset(self): return self.resetConns()

class ComboSignal:

    """A signal that connects multiple signals altogether."""

    def __init__(self, *signals: Signal):

        setattr(self, "__container__", [])
        self.__container__.extend(signals)

    def __iter__(self) -> Iterator[Signal]:

        return self.__container__.__iter__()
    
    def connect(self, *callbacks: Callable):

        for signal in self:
            signal.connect(*callbacks)

    async def emit(self, *supplies):

        coros = []

        for signal in self:

            coros.append(
                signal.emit(*supplies)
            )

        await asyncio.gather(*coros)

    def emitSync(self, *supplies):

        for signal in self:
            signal.emitSync(*supplies)
    
class DatabaseHandler:
    
    def __init__(self, path: str):
        
        self.path: str = path
        self.tables: list = []
        self.phs: list = []
        
        self.connect(path=path)
        
    def connect(self, path: str):
        
        '''
        Create a new DataBase connection to the given `path`.
        '''
        
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        
    def close(self):
        
        '''
        Close the current DataBase connection.
        '''
        
        if self.connection:
            
            self.connection.close()
            self.connection = None
            
    def reconnect(self):
        
        '''
        Close and re-create a connection.
        '''
        
        self.close()
        
        self.connect(
            path = self.path
        )
        
    def createTable(self, name: str, types: dict[str, type]):
        
        '''
        Creates a new table with the given `name` and `types`.
        '''
        
        try:
        
            values = [f'{x} {self.typeToStr(types.get(x))}' for x in types]
            values = ', '.join(values + ['Data json'])
            self.cursor.execute(f'CREATE TABLE {name} ({values})')
            
        except:
            
            ...
            
        self.phs.append(f'{list(types.keys())[0]}, DATA')
        self.tables.append(name)
            
        return Table(self, name, types)
        
    def typeToStr(self, annotation: type):
        
        '''
        Converts `annotation` type to a string, eg `int` to `INTEGER`
        '''
        
        
        if annotation is int:
            return 'INTEGER'
        
        if annotation is str:
            return 'TEXT'
        
        return None
    
    def insertData(self, key: str, data, table: str = None):
        
        '''
        Insert a new `key` with data `data` for table `table`
        '''
        
        if table is None:
            
            try:
                table = self.tables[0]
                
            except:
                return None
            
        index = self.tables.index(table)
        ph = self.phs[index]
        
        string = self.toJson(data, ascii=False)
        
        self.execute(
            f'INSERT INTO {table} ({ph}) VALUES (?, ?)',
            key, string
        )
        
        self.commit() # Update all changes
        
    def loadData(self, key: str, table: str = None):
        
        '''
        Load data for `key` in table `table`
        '''
        
        if table is None:
            
            try:
                table = self.tables[0]
                
            except:
                return None
            
        index = self.tables.index(table)
        ph = self.phs[index]
        auth: str = ph.split(',')[0].strip()
        
        self.execute(
            f'SELECT * from {table} where {auth}=?',
            key
        )
        
        loaded = self.cursor.fetchall()
        return self.fromJson(loaded[0][1])
    
    def loadAll(self, table: str = None):
        
        '''
        Load all `key`s
        '''
        
        all = []
        
        if table is None:
            
            try:
                table = self.tables[0]
                
            except:
                return None
        
        self.execute(
            f'SELECT * from {table}'
        )
        
        data = self.cursor.fetchall()
        
        for loaded in data:
            
            all.append(
                self.fromJson(loaded[1])
            )
            
        return all
    
    def delete(self, key: str, table: str):
        
        '''
        Delete `key` from table of name `table`
        '''
        
        if table is None:
            
            try:
                table = self.tables[0]
                
            except:
                return None
            
        ph = self.phs[
            self.tables.index(table)
        ].split(',')[0].strip()
        
        self.execute(
            f'DELETE from {table} where {ph}=?',
            key
        )
        
        self.commit()
        
    def update(self, key: str, item: str, value, table: str = None):
        
        '''
        Replace the value for key `item` with the new `value`, where the target is `key` in `table`.
        '''
        
        if table is None:
            
            try:
                table = self.tables[0]
                
            except:
                return None
            
        phs = self.phs[
            self.tables.index(table)
        ].split(',')
        
        auth = phs[0].strip()
        data = phs[1].strip()
        
        current = self.loadData(key, table)
        current[item] = value
        
        self.execute(
            f'UPDATE {table} SET {data}=? where {auth}=?',
            self.toJson(current, ascii=False), key
        )
        
        self.commit()
        
        
    def toJson(self, data: dict | list, ascii: bool = True) -> str:
        
        '''
        Convert data to JavaScript Object Notation (JSON) string.
        '''
        
        return json.dumps(data, ensure_ascii=ascii)
    
    def fromJson(self, data: str) -> dict | list:
        
        '''
        Convert JavaScript Object Notation (JSON) string to pythonic data.
        '''
        
        return json.loads(data)
    
    def commit(self):
        
        '''
        Commit all changes to the connection.
        '''
        
        self.connection.commit()
        
    def execute(self, action: str, *params):
        
        '''
        Execute the given sqlite3 `action` with the additional `params`.
        '''
        
        if len(params) == 1:
            params = (params[0],)
        
        self.cursor.execute(action, params)
        
class Table:
    
    def __init__(self, db: DatabaseHandler, name: str, types: dict[str, type]):
        
        '''
        Represents a database table.
        '''
        
        self.db = db
        self.name = name
        self.types = types
        
    def insert(self, key: str, data = {}):
        
        '''
        Insert data to the table.
        '''
        
        self.db.insertData(
            key, data, self.name
        )
        
    def delete(self, key: str):
        
        '''
        Delete data of key `key`.
        '''
        
        self.db.delete(
            key, self.name
        )
        
    def update(self, key: str, item: str, value):
        
        '''
        Update `item` from data of key `key` with new `value`.
        '''
        
        self.db.update(
            key, item, value, self.name
        )
        
    def load(self, key: str):
        
        '''
        Load data for key `key`.
        '''
        
        return self.db.loadData(
            key, self.name
        )
        
    def loadAll(self):
        
        '''
        Load data for all keys.
        '''
        
        return self.db.loadAll(
            table = self.name
        )
    
    def exists(self, key: str):

        '''
        Check if key `key` really exists.
        '''

        try:
            self.load(key=key)
            return True
        except:
            return False
        
    def add(self, key: str, data = {}):

        '''
        Checks if `key` already exists. If not, inserts the `data`. Otherwise, ignores the operation.
        '''

        if not self.exists(key):
            self.insert(key, data)
        
class Database:
    
    def __init__(
        self, origin: str, path: str = None
    ):
        
        if path is None:
            path = 'lunardata.db'
            
        full: str = path
        
        if origin is not None:
            full: str = os.path.join(origin, path)
        
        self.manager = DatabaseHandler(full)
        
        self.channels = self.manager.createTable(
            'channels', {'id': int}
        )
        
        self.users = self.manager.createTable(
            'users', {'id': int}
        )

        self.views = self.manager.createTable(
            'views', {'name': str}
        )

        self.timers = self.manager.createTable(
            'timers', {'type': str}
        )

        for x in range(1):
            
            self.timers.add("loops", {})
            self.timers.add("cooldowns", {})
        
    def createChannel(self, id: int):
        
        self.channels.insert(
            key = id
        )
        
    def createUser(self, id: int):
        
        self.users.insert(
            key = id
        )
        
    def updateChannel(self, id: int, item: str, value):
        
        self.channels.update(
            key = id,
            item = item,
            value = value
        )
        
    def updateUser(self, id: int, item: str, value):
        
        self.users.update(
            key = id,
            item = item,
            value = value
        )
        
    def loadChannel(self, id: int):
        
        '''
        Load all saved data for a channel and return it or `None` if it is not found in the database
        '''
        
        try:
            return self.channels.load(
                key = id
            )
            
        except:
            return None
        
    def loadUser(self, id: int):
        
        '''
        Load all saved data for a user and return it or `None` if it is not found in the database
        '''
        
        try:
            return self.users.load(
                key = id
            )
            
        except:
            return None
        
    def loadChannels(self):
        
        return self.channels.loadAll()
    
    def loadUsers(self):
        
        return self.users.loadAll()
            
    def loadView(self, name: str):

        try:
            return self.views.load(
                key = name
            )
        
        except:
            return None
        
    def loadViews(self):

        return self.views.loadAll()
    
    def viewExists(self, name):

        return self.loadView(name) is not None
    
    def createView(self, name: str):

        self.views.insert(
            key = name
        )

    def deleteView(self, name: str):

        self.views.delete(
            key = name
        )
    
    def updateView(self, name, item, value):

        self.views.update(
            key = name,
            item = item,
            value = value
        )

    def loadLoops(self) -> dict:
        return self.timers.load("loops")
    
    def loadCooldowns(self) -> dict:
        return self.timers.load("cooldowns")
    
    def createLoop(self, name: str, timer: int | float):
        self.timers.update("loops", item=name, value=timer)

    def createCooldown(self, name: str, timer: int | float):
        self.timers.update("cooldowns", item=name, value=timer)

    def loadLoop(self, name: str) -> int | float:

        loops = self.loadLoops()

        for lname, timer in loops.items():
            if lname == name:
                return timer
            
    def loadCooldown(self, name: str) -> int | float:

        cds = self.loadCooldowns()

        for cdname, timer in cds.items():
            if cdname == name:
                return timer
    
class lunarlist(Generic[T], list):
    
    @property
    def length(self):
        '''
        The list's `length`. This is the same as doing `len(myList)` where `myList` is a `lunarlist`.
        '''
        
        return self.__len__()
    
    @property
    def list(self):
        '''
        A `list` equivalent of this `lunarlist`.
        '''
        
        return self.toList()
    
    @property
    def tuple(self):
        '''
        A `tuple` equivalent of this `lunarlist`.
        '''
        
        return self.toTuple()
    
    @property
    def set(self):
        '''
        A `set` equivalent of this `lunarlist`.
        '''
        
        return self.toSet()
    
    @property
    def reversed(self):
        '''
        A `reversed` copy of this `lunarlist`.
        '''
        
        copy = self.copy()
        copy.reverse()
        return copy
    
    def __init__(self, *arguments):
        
        '''
        A mutable, list-like sequence with additional methods and attributes.
        '''
        
        if len(arguments) == 1:
            arguments = [arguments[0]]
            
        else:
            arguments = list(arguments)
        
        super().__init__(arguments)
    
    def replace(self, old: T, new: T):
        
        '''
        Removes `old` value and adds `new` at its index.
        If `old` does not exist, a `ValueError` will be raised.
        '''
        
        try:
            idx = self.index(old)
        except:
            raise ValueError(f"'{old}' not in list")
        
        self.pop(idx)
        self.insert(idx, new)
        
    def toList(self) -> list:
        
        '''
        Converts this `lunarlist` to a built-in Python `list`.
        '''
        
        return list(self)
    
    def toTuple(self) -> tuple:
        
        '''
        Converts this `lunarlist` to a built-in Python `tuple`.
        '''
        
        return tuple(self)
    
    def toSet(self) -> set:
        
        '''
        Converts this `lunarlist` to a built-in Python `set`.
        '''
        
        return set(self)
    
    def convert(self, __type: type):
        
        '''
        Converts this `lunarlist` to an object of type `__type`.
        '''
        
        if __type is list:
            return self.toList()
        
        if __type is tuple:
            return self.toTuple()
        
        if __type is set:
            return self.toSet()
        
        if type(__type) is not type:
            raise TypeError(f'Invalid __type argument')
        
        raise ValueError(f'Cannot convert to \'{__type.__str__}\'')
    
    def appendSafe(self, value: T):
        
        '''
        Appends a value to the list, without worrying about if it already is in.
        '''
        
        super().append(value)
        
    def append(self, value: T):
        
        '''
        Append a value to the list, if it is not in it already.
        '''
        
        if value not in self:
            self.appendSafe(value)
            
    def reverseGet(self, value, default = None):
        
        '''
        Doing a reverse `lunarlist.get()` search, returns the index of the given object.
        '''
        
        for idx, x in enumerate(self):
            
            if x == value:
                
                return idx
            
        return default
    
    def __iter__(self) -> Iterator[T]:

        return super().__iter__()
    
class Time:
    
    def __init__(self, seconds: int | float = 0, minutes: int | float = 0, hours: int | float = 0, days: int | float = 0, weeks: int | float = 0, months: int | float = 0, years: int | float = 0):
        
        self.seconds: int | float = seconds
        
        self.seconds += Time.minutesToSeconds(minutes)
        self.seconds += Time.hoursToSeconds(hours)
        self.seconds += Time.daysToSeconds(days)
        self.seconds += Time.weeksToSeconds(weeks)
        self.seconds += Time.monthsToSeconds(months)
        self.seconds += Time.yearsToSeconds(years)
        
    @property
    def minutes(self):
        '''
        Converts this `Time` object to a `float` representing its time in minutes.
        '''
        
        return Time.secondsToMinutes(self.seconds)
    
    @property
    def hours(self):
        '''
        Converts this `Time` object to a `float` representing its time in hours.
        '''
        
        return Time.secondsToHours(self.seconds)
    
    @property
    def days(self):
        '''
        Converts this `Time` object to a `float` representing its time in days.
        '''
        
        return Time.secondsToDays(self.seconds)
    
    @property
    def weeks(self):
        '''
        Converts this `Time` object to a `float` representing its time in weeks.
        '''
        
        return Time.secondsToWeeks(self.seconds)
    
    @property
    def months(self):
        '''
        Converts this `Time` object to a `float` representing its time in months.
        '''
        
        return Time.secondsToMonths(self.seconds)
    
    @property
    def years(self):
        '''
        Converts this `Time` object to a `float` representing its time in years.
        '''
        
        return Time.secondsToHours(self.years)
        
    def __int__(self):
        return int(self.seconds)
    
    def __float__(self):
        return float(self.seconds)
    
    def __str__(self):
        return str(int(self))
    
    def format(self, formatter: str):
        
        minutes, seconds = Time.secondsToMinutesAndSeconds(self.seconds)
        
        return formatter.replace(
            '%s', str(seconds)
        ).replace(
            '%m', str(minutes)
        )
        
    @classmethod
    def minutesToSeconds(cls, minutes: int | float):
        
        return minutes * 60
    
    @classmethod
    def secondsToMinutes(cls, seconds: int | float):
        
        return seconds / 60
    
    @classmethod
    def hoursToSeconds(cls, hours: int | float):
        
        return hours * 60 * 60
    
    @classmethod
    def secondsToHours(cls, seconds: int | float):
        
        return seconds / 60 / 60
    
    @classmethod
    def daysToSeconds(cls, days: int | float):
        
        return days * 60 * 60 * 24
    
    @classmethod
    def secondsToDays(cls, seconds: int | float):
        
        return seconds / 60 / 60 / 24
    
    @classmethod
    def weeksToSeconds(cls, weeks: int | float):
        
        return weeks * 60 * 60 * 24 * 7
    
    @classmethod
    def secondsToWeeks(cls, seconds: int | float):
        
        return seconds / 60 / 60 / 24 / 7
    
    @classmethod
    def monthsToSeconds(cls, months: int | float):
        
        return months * 60 * 60 * 24 * 30
    
    @classmethod
    def secondsToMonths(cls, seconds: int | float):
        
        return seconds / 60 / 60 / 24 / 30
    
    @classmethod
    def yearsToSeconds(cls, years: int | float):
        
        return years * 60 * 60 * 24 * 365
    
    @classmethod
    def secondsToYears(cls, seconds: int | float):
        
        return seconds / 60 / 60 / 24 / 365
    
    @classmethod
    def minutesToHours(cls, minutes: int | float):
        
        return cls.secondsToHours(cls.minutesToSeconds(minutes))
    
    @classmethod
    def minutesToDays(cls, minutes: int | float):
        
        return cls.secondsToDays(cls.minutesToSeconds(minutes))
    
    @classmethod
    def minutesToWeeks(cls, minutes: int | float):
        
        return cls.secondsToWeeks(cls.minutesToSeconds(minutes))
    
    @classmethod
    def minutesToMonths(cls, minutes: int | float):
        
        return cls.secondsToMonths(cls.minutesToSeconds(minutes))
    
    @classmethod
    def minutesToYears(cls, minutes: int | float):
        
        return cls.secondsToYears(cls.minutesToSeconds(minutes))
    
    @classmethod
    def hoursToDays(cls, hours: int | float):
        
        return cls.secondsToDays(cls.hoursToSeconds(hours))
    
    @classmethod
    def hoursToMinutes(cls, hours: int | float):
        
        return cls.secondsToMinutes(cls.hoursToSeconds(hours)) 
    
    @classmethod
    def hoursToWeeks(cls, hours: int | float):
        
        return cls.secondsToWeeks(cls.hoursToSeconds(hours))
    
    @classmethod
    def hoursToMonths(cls, hours: int | float):
        
        return cls.secondsToMonths(cls.hoursToSeconds(hours))
    
    @classmethod
    def hoursToYears(cls, hours: int | float):
        
        return cls.secondsToYears(cls.hoursToSeconds(hours))

    @classmethod
    def daysToMinutes(cls, days: int | float):
        
        return cls.secondsToMinutes(cls.daysToSeconds(days))
        
    @classmethod
    def daysToHours(cls, days: int | float):
        
        return cls.secondsToHours(cls.daysToSeconds(days))
    
    @classmethod
    def daysToWeeks(cls, days: int | float):
        
        return cls.secondsToWeeks(cls.daysToSeconds(days))
    
    @classmethod
    def daysToMonths(cls, days: int | float):
        
        return cls.secondsToMonths(cls.daysToSeconds(days))
    
    @classmethod
    def daysToYears(cls, days: int | float):
        
        return cls.secondsToYears(cls.daysToSeconds(days))
    
    @classmethod
    def weeksToHours(cls, weeks: int | float):
        
        return cls.secondsToHours(cls.weeksToSeconds(weeks))
    
    @classmethod
    def weeksToMinutes(cls, weeks: int | float):
        
        return cls.secondsToMinutes(cls.weeksToSeconds(weeks))
    
    @classmethod
    def weeksToDays(cls, weeks: int | float):
        
        return cls.secondsToDays(cls.weeksToSeconds(weeks))
    
    @classmethod
    def weeksToMonths(cls, weeks: int | float):
        
        return cls.secondsToMonths(cls.weeksToSeconds(weeks))
    
    @classmethod
    def weeksToYears(cls, weeks: int | float):
        
        return cls.secondsToYears(cls.weeksToSeconds(weeks))
    
    @classmethod
    def monthsToHours(cls, months: int | float):
        
        return cls.secondsToMonths(cls.monthsToSeconds(months))
    
    @classmethod
    def monthsToMinutes(cls, months: int | float):
        
        return cls.secondsToMinutes(cls.monthsToSeconds(months))
    
    @classmethod
    def monthsToDays(cls, months: int | float):
        
        return cls.secondsToDays(cls.monthsToSeconds(months))
    
    @classmethod
    def monthsToWeeks(cls, months: int | float):
        
        return cls.secondsToWeeks(cls.monthsToSeconds(months))
    
    @classmethod
    def monthsToYears(cls, months: int | float):
        
        return cls.secondsToYears(cls.monthsToSeconds(months))
    
    @classmethod
    def yearsToHours(cls, years: int | float):
        
        return cls.secondsToHours(cls.yearsToSeconds(years))
    
    @classmethod
    def yearsToMinutes(cls, years: int | float):
        
        return cls.secondsToMinutes(cls.yearsToSeconds(years))
    
    @classmethod
    def yearsToDays(cls, years: int | float):
        
        return cls.secondsToDays(cls.yearsToSeconds(years))
    
    @classmethod
    def yearsToWeeks(cls, years: int | float):
        
        return cls.secondsToWeeks(cls.yearsToSeconds(years))
    
    @classmethod
    def yearsToMonths(cls, years: int | float):
        
        return cls.secondsToMonths(cls.yearsToSeconds(years))
    
    @classmethod
    def secondsToMinutesAndSeconds(cls, seconds: int | float) -> tuple[int, int]:
        
        minutes = float(cls.secondsToMinutes(seconds))
        integer, decimal = Utils.floatParts(minutes)
        
        if decimal > 0:
            decimal = cls.minutesToSeconds(decimal)
            
        return integer, round(decimal)
    
    @classmethod
    def secondsToHoursMinutesSeconds(cls, seconds: int | float) -> tuple[int, int]:
        
        minutes, seconds = cls.secondsToMinutesAndSeconds(seconds)
        integer, decimal = Utils.floatParts(float(cls.minutesToHours(minutes)))
        
        if decimal > 0:
            decimal = cls.hoursToMinutes(decimal)
            
        return integer, round(decimal), seconds
        
class Cooldown:

    """An object representing data for a command's cooldown."""

    def __init__(self, payload: dict[str]):

        self.ends: int | float = payload.get("ends")

    @classmethod
    def construct(cls, ends: int | float):

        """For internal use only. Constructs a new `Cooldown` object."""

        current = time.time()

        payload = {
            "ends": ends,
            "remains": ends - current,
            "active": ends is not None and current < ends
        }

        return cls(payload)
    
    @property
    def remaining(self) -> float:

        """The remaining time until the cooldown ends."""

        try:
            return self.ends - time.time()
        
        except:
            return 0.0
    
    @property
    def active(self):
        """Whether this cooldown is currently active."""
        return self.remaining > 0
    
    @property
    def timestamp(self):
        """A relative timestamp to use on Discord."""
        return f"<t:{int(self.ends)}:R>"
    
    def __str__(self):
        return self.timestamp
    
    def __repr__(self):
        return str(self)
    
    def __float__(self):
        return self.ends
    
    def __int__(self):
        return int(float(self))
    
    def __bool__(self):
        return self.active
    
'''time = Time(minutes=1, seconds=30)
print(time.secondsToHoursMinutesSeconds(3700))'''