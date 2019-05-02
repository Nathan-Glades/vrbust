# GUI backend
# API for talking between GUI and backend

import json, threading

class gui:
    class state: # Class for all states in the settings.JSON file
        class active:
            json_param = 'active'
            status = ''
        class mask:
            json_param = 'mask'
            status = ''
        class camera_on:
            json_param = 'camera-on'
            status = ''
        class auto_calibrate:
            json_param = 'auto'
            status = ''
    def __init__(self): # called on class initiation
        self.values = json.load(open('settings.json')) # Values of the JSON file
        self.current_state = {
            gui.state.active: '',
            gui.state.mask: '',
            gui.state.camera_on: '',
            gui.state.auto_calibrate: ''
        }
        self.hooks = {
            gui.state.active: [],
            gui.state.mask: [],
            gui.state.camera_on: [],
            gui.state.auto_calibrate: []
        }
        self.settings_file = 'settings.json'
    
    def add_hook(self, state, callback, pass_state): # Add hook
        self.hooks[state].append({"function": callback, "pass_state": pass_state})
        # State = waiting for selected state to be changed (gui.state.)
        # Callback = function called when state is changed (function)
        # Pass state = state of hook will be passed to called function
    
    def init_hook_listner(self): # Start hook listner
        threading.Thread(target=self.__hlistenthread, args=(self,))
    
    class get_state():
        def __init__(self, dict_):
            self.active = gui.state.active
            self.active.status = dict_[gui.state.active.json_param]
            
            self.mask = gui.state.mask
            self.mask.status = dict_[gui.state.mask.json_param]
            
            self.camera_on = gui.state.camera_on
            self.camera_on.status = dict_[gui.state.camera_on.json_param]
            
            self.auto_calibrate = gui.state.auto_calibrate
            self.auto_calibrate.status = dict_[gui.state.auto_calibrate.json_param]
    
    def __hlistenthread(self): # Thread for hooks
        while True: # loop
            get_s = gui.get_state(json.load(open(self.settings_file))) # Get current state of the settings file

            if get_s.active != self.current_state[gui.state.active]: # gui.state.active hooks will be called
                for callback in self.hooks[gui.state.active]:
                    if callback['pass_state']:
                        callback['function'](self.current_state[gui.state.active].status) # Run callback function AND pass state
                    else:
                        callback['function']() # Run callback function WITHOUT passing state


