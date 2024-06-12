'''
A lunarcord extension for scheduling time-consuming tasks to be ran in a separate `Thread` without blocking your code or your bot.
Below is an example implementation showing what can be done with this extension:

```
from lunarcord import tasks, Bot
import asyncio

bot = Bot()

@tasks.task()
async def myTask():

    print("Before sleep")
    await asyncio.sleep(100) # Sleeps for 100 seconds.
    print("After sleep")
    
@tasks.loop(every=10)
async def myLoop(iteration: int):

    myChannel = await bot.fetchChannel(12345678)
    await myChannel.send(f"Iteration number **{iteration}**.")
    
bot.run("TOKEN")
```

The task ("myTask") created above prints something, waits for 100 seconds, then prints another message. If a `Task` was not used for this, your bot would run AFTER the waiting had finished. From the other hand, those two tasks (waiting and starting the bot) are done in parallel thanks to the usage of a lunarcord task.
Another reason you may want to make use of a `Task` is because you want to run an `async def` function (with `await`), which is not possible in non-async context.

The "myLoop" loop created in the example is a lunarcord `Loop`. This is a subclass of lunarcord's `Task` class that allows you to schedule a task to be ran not once, not twice, but forever until it has been stopped, every `every` (look at the decorator's `every=100` argument) seconds.
This is like using a `while True` loop, with the difference, again, that this does not block the rest of your code.
For more examples, read more about `Tasks` in lunarcord's official docs (`SOON`).
'''

import threading, asyncio, time
from .__core__.types import Registrable, Bot
from .__core__.addons import Utils, Signal
from typing import TypeVar, Generic, Iterable

T = TypeVar('T')

class CallableLike(Generic[T]): ...
class TimeLike(Generic[T]): ...
class NameLike(Generic[T]): ...
class BotLike(Generic[T]): ...
class BoolLike(Generic[T]): ...

class Function: ...
class Method: ...
class Class: ...

class Task(Registrable):
    
    '''
    A task that can be ran in a separate thread of control so that it doesn't block other processes.
    '''
    
    def __init__(self, activity: CallableLike[Function | Method | Class], name: NameLike[str] = None, autorun: BoolLike[bool] = True, bot: BotLike[Bot] = None):
        
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
        
        if name is None:
            
            name = activity.__name__
        
        self.bot: BotLike = None
        self.activity: CallableLike = activity
        self.thread: threading.Thread = None
        self.running: bool = False
        self.name: NameLike = name
        self.auto: bool = bool(autorun)
        
        if bot:
            
            self.__register__(bot)
            
    async def run(self, *args, **kwargs):
        
        '''
        Runs the activity of this `Task` in an async and blocking manner, something that is not advisable.
        '''
        
        while self.running:
            ... # Block until the current execution is finished.
        
        func = self.activity
        self.running = True
        
        await Utils.execute(
            function = func,
            bot = self.bot,
            client = self.bot,
            *args,
            **kwargs
        )
        
        self.running = False
        
    def start(self):
        
        '''
        Starts the Task's activity in another thread without blocking other running Tasks. This requires the task to be registered to a bot.
        '''
        
        if self.bot is not None:
            
            runner = self.bot.__gateway__.runInThread
            
            self.thread = runner(
                self.run,
                name = self.name
            )
    
    def __register__(self, bot: Bot, name: str = ...):
        
        if bot:
            
            self.bot = bot
            self.bot.__gateway__.tasks.append(self)
            
            if self.auto:
                self.start()
            
    def __unregister__(self):
        
        if self.bot:
            self.bot = None
            
    def __reregister__(self):
        
        if self.bot:
            
            bot = self.bot
            self.__unregister__()
            self.__register__(bot)

    def __str__(self):
        return self.name
            
    def __repr__(self):
        return f'<Task name={self.name} activity={self.activity} running={self.running}>'
    
    def __call__(self, *args, **kwargs):
        
        '''
        Start execution of the task, in another thread of course. Even if your activity function is a coroutine function (`async def` function), this does not need to be awaited.
        '''
        
        return self.start(
            *args,
            **kwargs
        )
        
class Loop(Task):
    
    '''
    A task that is ran every once in a while without blocking the rest of your code.
    '''
    
    def __init__(self, activity: CallableLike[Function | Method | Class], name: NameLike[str], every: TimeLike[int | float], iterable: Iterable = None, bot: BotLike[Bot] = None):
        
        '''
        Creates a `Loop` that executes your `activity` in a non-blocking manner.
        
        Parameters
        ----------
        activity: `CallableLike`
            A function, method or class (or anything that has a `__call__` attribute) to be called every once in a while.
            
        name: `NameLike`
            A string or convertible to string (anything that has a `__str__` attribute) to name this `Loop`/`Task`.
            
        every: `TimeLike`
            An int, float or convertible to float (anything that has a `__float__` attribute) to wait before executing the activity every time.
            
        iterable: `Iterable`
            An iterable (for example a `list`) to pass items from in every iteration. This can be useful for automatically updating the bot's activity, and not only.
            
        bot: `BotLike`
            A `Bot` that should take care of this looping task and its activity. If not given, the task can't start.
        '''
        
        super().__init__(
            
            activity = activity,
            name = name,
            autorun = True,
            bot = bot
            
        )
        
        self.delay: float = every
        self.next: float = ...
        self.iterable: Iterable = iterable
        
        if not hasattr(self.iterable, '__iter__'): # Is not an iterable
            
            self.iterable = None # Mark it as None (not given)
        
        try:
            
            if self.delay < 0.3:
                self.delay = 0.3
                
            self.delay = float(every)
            
        except:
            
            self.delay = 1.0
            
        self.iterations: int = 0
        self.onStoppedSignal = Signal()
        
    async def run(self, *args, **kwargs):

        restart = False
        
        if self.running:   
            self.stop()
             
        self.running = True
        self.next = time.time()

        try:
            existing, oldDelay = self.bot.__gateway__.db.loadLoop(self.name)
        except:
            existing, oldDelay = None, self.delay

        if existing and type(existing) in (int, float):
            self.next = existing
        
        while self.running:

            await asyncio.sleep(0.1)

            if self.delay != oldDelay:

                restart = True
                self.stop()
                break

            try: self.bot.__gateway__.db.createLoop(self.name, (self.next, self.delay))
            except: self.stop(); break

            signal = self.onStoppedSignal
            await self.sleep(until=self.next, signal=signal)
            
            if self.iterable:
                
                index = (self.iterations + 1) % len(self.iterable)
                
                try:
                    
                    value = self.iterable[index]
                    kwargs['item'] = value
                    #args.append(value)
                    
                except:
                    
                    ...
            
            await Utils.execute(
                
                function = self.activity,
                bot = self.bot,
                client = self.bot,
                iteration = self.iterations,
                iter = self.iterations,
                *args,
                **kwargs
                
            )
            
            self.iterations += 1
            self.next = time.time() + self.delay

        if restart:

            await self.run(*args, **kwargs)
            
    async def sleep(self, seconds: float = None, until: float = None, signal: Signal = None):
        
        '''
        Helper method that sleeps for `seconds` or until `signal` is called. If `until` is given, sleeps until the given time in unix timestamp has passed.
        '''

        if until is None:

            if seconds is None:
                return
            
            until = time.time() + seconds

        if signal is None:
            signal = Signal()

        if seconds is None:
            tries = float("inf")
        else:
            tries = seconds * 10
        
        finished = False
        attempts = 0
        
        def callback():
            
            nonlocal finished
            finished = True
            
        signal.connect(callback)
        
        while not finished:
            
            if attempts == tries or time.time() > until:
                
                finished = True
                break
                
            await asyncio.sleep(.1)
            attempts += 1

    @property
    def name(self) -> str | None:

        return getattr(self, "__name__") if hasattr(self, "__name__") else None
    
    @name.setter
    def name(self, new: str):
        if self.__checkName__(new):
            setattr(self, "__name__", new)
            
    def stop(self):
        
        '''
        Kills and stops this loop forever, preventing it from running.
        '''
        
        self.onStoppedSignal.callSync()
        self.running = False

    def __register__(self, bot: Bot, name: str = ...):

        self.bot: Bot = bot
        self.__checkName__(self.name)

        if self not in self.bot.__gateway__.loops:
            self.bot.__gateway__.loops.append(self)

        if self.auto:
            self.start()
        
    def __unregister__(self):

        if self in self.bot.__gateway__.loops:
            self.bot.__gateway__.loops.remove(self)
        
        self.stop()
        self.bot = None

    def __checkName__(self, name: str) -> bool:

        if self.bot is None:
            return True
        
        for loop in self.bot.__gateway__.loops:

            if loop.name == name:

                raise NameError("Can't have two or more loops of the same name")
            
        return True
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<Loop name=\"{self.name}\" every={self.delay} running={self.running}"
            
            
            
def __createTask__(bot: BotLike[Bot], activity: CallableLike[Function | Method | Class], name: NameLike[str] = None, autorun: BoolLike[bool] = True):
    
    task = Task(activity, name, autorun)
    
    if bot:
        
        try:
            
            bot.register(task)
            
        except:
            
            ...
            
    return task

def __createLoop__(bot: BotLike[Bot], activity: CallableLike[Function | Method | Class], name: NameLike[str], every: TimeLike[int | float], iterable: Iterable):
    
    loop = Loop(activity, name, every, iterable)
    
    if bot:
        
        try:
            
            bot.register(loop)
            
        except:
            
            ...
            
    return loop

def task(name: NameLike[str] = None, autorun: BoolLike[bool] = True, bot: BotLike[Bot] = None):
    
    '''
    Create a new task and start its execution in another thread. If `bot` is not provided and this is never registered from a cog or with `Bot.register()`, the task will never be ran. As long as the task is registered to some bot, the given bot will take care of it immediately.
    
    Parameters
    ----------
    name: `str`
        A name for this task. If not given, it'll be generated using the activity's name.
        
    autorun: `bool`
        If this is set to `False`, the task will not be executed by the bot automatically, but by you (eg. if the activity name is `myActivity`, then `myActivity()`)
        
    bot: `Bot`
        The bot that should take care of this task and its activity. If not given, the task can't start.
    '''
    
    def create(activity):
        
        nonlocal name, autorun
    
        return __createTask__(
            bot = bot,
            activity = activity,
            name = name,
            autorun = autorun
        )
        
    return create

def loop(name: NameLike[str] = None, every: TimeLike[int | float] = 1, iterable: Iterable = None, bot: BotLike[Bot] = None):
    
    '''
    Create a new loop and start it in another thread. If `bot` is not provided and this is never registered from a cog or with `Bot.register()`, the loop will never start. As long as this loop is registered to some bot, the bot will take care of it immediately.
    
    Parameters
    ----------
    name: `NameLike`
        A name for this task. If not given, it'll be generated using the activity's name.
        
    every: `TimeLike`
        Seconds to wait before every execution of the loop's activity.
        
    iterable: `Iterable`
        An iterable (for example a `list`) to pass items from in every iteration. This can be useful for automatically updating the bot's activity, and not only.
                
    bot: `BotLike`
        The bot that should take care of this loop and run its activity. If not given, the loop won't start.

    '''
    
    def create(activity):
        
        nonlocal name, every
    
        return __createLoop__(
            bot = bot,
            activity = activity,
            name = name,
            every = every,
            iterable = iterable
        )
        
    return create