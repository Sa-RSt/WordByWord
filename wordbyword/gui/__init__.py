# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class Observable:
    def __init__(self):
        self._evt_handlers = []

    def on(self, evt, callback):
        '''
        Register a callback to a custom event 'evt'.
        The callback must accept a single parameter: the event object,
        which is the object passed to UIComponent.trigger().
        '''
        self._evt_handlers.append((evt, callback))
    
    def trigger(self, evt, obj=...):
        '''
        Call all callbacks associated by UIComponent.on() with the given custom event 'evt'.
        Returns a list with the return values of each callback.
        '''
        ret = []
        for ename, callback in self._evt_handlers:
            if ename == evt:
                if obj is ...:
                    ret.append(callback())
                else:
                    ret.append(callback(obj))
        
        if len(ret) == 0:
            raise AttributeError('No callbacks for event: ', evt)

        return ret

    def propagate_event_to(self, evt, comp_dst):
        '''
        Propagate all 'evt' events that are triggered in 'self' to the component 'comp_dst'.
        '''
        def event_propagation(obj):
            comp_dst.trigger(evt, obj)

        self.on(evt, event_propagation)


class UIComponent(ABC, Observable):
    def __init__(self):
        super(UIComponent, self).__init__()

    @abstractmethod
    def get_tk_widget(self):
        '''
        Return this component's tkinter widget.
        '''
        return NotImplemented
