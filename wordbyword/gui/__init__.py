from abc import ABC, abstractmethod

class UIComponent(ABC):
    @abstractmethod
    def get_tk_widget(self):
        '''
        Return this component's tkinter widget.
        '''
        return NotImplemented
