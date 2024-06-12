from glxeveloop.properties.debug import DebugProperty
from glxeveloop.properties.hooks import HooksProperty
from glxeveloop.properties.queue import QueueProperty
from glxeveloop.properties.timer import TimerProperty
from glxeveloop.properties.running import RunningProperty
from glxeveloop.loop.start import Start
from glxeveloop.loop.stop import Stop
from glxeveloop.loop.handle_events import HandleEvents
from glxeveloop.loop.sequence import SequenceLoop


class Loop(
    DebugProperty,
    QueueProperty,
    HooksProperty,
    RunningProperty,
    TimerProperty,
    Start,
    Stop,
    HandleEvents,
    SequenceLoop,
):
    def __init__(self):
        DebugProperty.__init__(self)
        QueueProperty.__init__(self)
        HooksProperty.__init__(self)
        RunningProperty.__init__(self)
        TimerProperty.__init__(self)
        Start.__init__(self)
        Stop.__init__(self)
        HandleEvents.__init__(self)
        SequenceLoop.__init__(self)
