# GUI backend
# API for talking between GUI and backend

import json, threading

class gui:
    class state: # Class for all states in the settings.JSON file
        class active:
            def __init__(self):
                self.json_param = 'active'
                self.status = ''
        class mask:
            def __init__(self):
                self.json_param = 'mask'
                self.status = ''
        class camera_on:
            def __init__(self):
                self.json_param = 'camera-on'
                self.status = ''
        class auto_calibrate:
            def __init__(self):
                self.json_param = 'auto'
                self.status = ''
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
    
    def init_hook_listener(self): # Start hook listner
        threading.Thread(target=self.__hlistenthread).start()
    
    class get_state:
        def __init__(self, dict_):
            self.active = gui.state.active
            self.active.status = dict_[gui.state.active().json_param]
            
            self.mask = gui.state.mask
            self.mask.status = dict_[gui.state.mask().json_param]
            
            self.camera_on = gui.state.camera_on
            self.camera_on.status = dict_[gui.state.camera_on().json_param]
            
            self.auto_calibrate = gui.state.auto_calibrate
            self.auto_calibrate.status = dict_[gui.state.auto_calibrate().json_param]
    
    def get(self, state):
        return self.current_state[state]
    
    def set(self, state, value):
        fj = json.load(open(self.settings_file))
        fj[state.json_param] = value
        json.dump(fj, open(self.settings_file, 'w'))
    
    def __hlistenthread(self): # Thread for hooks
        while True: # loop
            get_s = gui.get_state(json.load(open(self.settings_file))) # Get current state of the settings file
            
            #print(get_s.active.status, self.current_state[gui.state.active])

            if get_s.active.status != self.current_state[gui.state.active]: # gui.state.active hooks will be called
                for callback in self.hooks[gui.state.active]:
                    if callback['pass_state']:
                        f = callback['function'] # Run callback function AND pass state
                        f(get_s.active.status)
                    else:
                        callback['function']() # Run callback function WITHOUT passing state
            
            if get_s.mask.status != self.current_state[gui.state.mask]: # gui.state.mask hooks will be called
                for callback in self.hooks[gui.state.mask]:
                    if callback['pass_state']:
                        f = callback['function'] # Run callback function AND pass state
                        f(get_s.mask.status)
                    else:
                        callback['function']() # Run callback function WITHOUT passing state
            
            if get_s.camera_on.status != self.current_state[gui.state.camera_on]: # gui.state.camera_on hooks will be called
                for callback in self.hooks[gui.state.camera_on]:
                    if callback['pass_state']:
                        f = callback['function'] # Run callback function AND pass state
                        f(get_s.camera_on.status)
                    else:
                        callback['function']() # Run callback function WITHOUT passing state
            
            if get_s.auto_calibrate.status != self.current_state[gui.state.auto_calibrate]: # gui.state.auto_calibrate hooks will be called
                for callback in self.hooks[gui.state.auto_calibrate]:
                    if callback['pass_state']:
                        f = callback['function'] # Run callback function AND pass state
                        f(get_s.auto_calibrate.status)
                    else:
                        callback['function']() # Run callback function WITHOUT passing state


            self.current_state[gui.state.active] = get_s.active.status
            self.current_state[gui.state.mask] = get_s.mask.status
            self.current_state[gui.state.camera_on] = get_s.camera_on.status
            self.current_state[gui.state.auto_calibrate] = get_s.auto_calibrate.status