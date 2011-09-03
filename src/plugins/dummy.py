# -*- coding: utf-8 -*-

import random

from plugin import Plugin


class Dummy(Plugin):
    
    @property
    def name(self):
        return "Dummy"
    
    def setup(self):
        pass
    
    def teardown(self):
        pass
    
    def train(self, users):
        self._users = users
    
    def identify(self, frame, bbox, securityTol):
        user = None
        confidence = random.random()
        if self._users and confidence > 1 - securityTol:
            user = self._users.keys()[0]
        return confidence, user


class Dummy2(Plugin):
    
    @property
    def name(self):
        return "Dummy"
    
    def setup(self):
        pass
    
    def teardown(self):
        pass
    
    def train(self, users):
        pass
    
    def identify(self, frame, bbox, securityTol):
        return 0, None