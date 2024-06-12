from glxeveloop.loop.loop import Loop


class Builder:
    @staticmethod
    def loop(
        debug=None,
        hooks=None,
        queue=None,
        timer=None,
        running=None,
        start=None,
        stop=None,
        event_handler=None,
        sequence=None,
    ) -> object:
        new_loop = Loop()

        if debug and hasattr(new_loop, "debug"):
            new_loop.debug = debug
        if hooks and hasattr(new_loop, "hooks"):
            new_loop.hooks = hooks
        if queue and hasattr(new_loop, "queue"):
            new_loop.queue = queue
        if queue and hasattr(new_loop, "timer"):
            new_loop.timer = timer
        if running and hasattr(new_loop, "running"):
            new_loop.running = running
        if start and hasattr(new_loop, "start"):
            new_loop.start = start
        if stop and hasattr(new_loop, "stop"):
            new_loop.stop = stop
        if event_handler and hasattr(new_loop, "handle_event"):
            new_loop.handle_event = event_handler
        if sequence and hasattr(new_loop, "sequence"):
            new_loop.sequence = sequence

        return new_loop
