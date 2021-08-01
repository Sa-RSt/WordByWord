# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class UIComponent(ABC):
    def __init__(self):
        self.__evt_handlers = []

    @abstractmethod
    def get_tk_widget(self):
        '''
        Return this component's tkinter widget.
        '''
        return NotImplemented
    
    def on(self, evt, callback):
        '''
        Register a callback to a custom event 'evt'.
        The callback must accept a single parameter: the event object,
        which is the object passed to UIComponent.trigger().
        '''
        self.__evt_handlers.append((evt, callback))
    
    def trigger(self, evt, obj=...):
        '''
        Call all callbacks associated by UIComponent.on() with the given custom event 'evt'.
        Returns a list with the return values of each callback.
        '''
        ret = []
        for ename, callback in self.__evt_handlers:
            if ename == evt:
                if obj is ...:
                    ret.append(callback())
                else:
                    ret.append(callback(obj))
        return ret
