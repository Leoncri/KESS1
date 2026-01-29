class Event:

    def __init__(self):
        # callback functions of subscribors
        self._callbacks = []

    def subscribe(self, callbackFunction):
        self._callbacks.append(callbackFunction)

    def unsubscribe(self, callbackFunction):
        if callbackFunction in self._callbacks:
            self._callbacks.remove(callbackFunction)

    def notify(self, **kwargs):
        for callback in self._callbacks:
            callback(**kwargs)
