# -*- coding: utf-8 -*-

from plugin import Plugin


__all__ = ["FaceRecognizer"]


class FaceRecognizer(object):

    def __init__(self, pluginsPath):
        self._techniques = {}
        self._selectedTechniqueName = None
        self._securityTol = 0
        self._users = {}

        self.loadPluginsFrom(pluginsPath)

    def loadPluginsFrom(self, newPath):
        self.selectTechniqueByName(None)
        self._techniques = {}
        if newPath:
            Plugin.load(newPath)
            for p in Plugin.getInstances():
                origName = p.name.strip()
                if not origName:
                    continue
                name = origName
                i = 1
                while self._techniques.has_key(name):
                    name = "%s %d" % (origName, i)
                    i += 1
                self._techniques[name] = p

    @property
    def techniquesNames(self):
        return self._techniques.keys()

    @property
    def selectedTechniqueName(self):
        return self._selectedTechniqueName

    @property
    def selectedTechnique(self):
        if self._selectedTechniqueName is None:
            return None
        return self._techniques[self._selectedTechniqueName]

    def selectTechniqueByName(self, techniqueName):
        if techniqueName is None:
            if self.selectedTechnique is not None:
                self.selectedTechnique.teardown()
            self._selectedTechniqueName = None
        else:
            techniqueName = techniqueName.strip()
            if not techniqueName:
                return
            if self._techniques.has_key(techniqueName) and \
                    self._selectedTechniqueName != techniqueName:
                if self.selectedTechnique is not None:
                    self.selectedTechnique.teardown()
                self._selectedTechniqueName = techniqueName
                self.selectedTechnique.setup()
                self.selectedTechnique.train(self._users)

    @property
    def securityTol(self):
        return self._securityTol

    @securityTol.setter
    def securityTol(self, newValue):
        if newValue < 0 or newValue > 1:
            raise ValueError("'securityTol' must be in [0, 1] interval.")
        self._securityTol = newValue

    @property
    def users(self):
        return self._users.keys()

    def addUser(self, user, enrollment):
        user = user.strip()
        if not user:
            return
        if self.userExists(user):
            raise ValueError("Duplicated user.")
        self._users[user] = enrollment
        if self.selectedTechnique is not None:
            self.selectedTechnique.train(self._users)

    def removeUser(self, user):
        user = user.strip()
        if not (user and self.userExists(user)):
            return
        self._users[user].delete()
        del self._users[user]
        if self.selectedTechnique is not None:
            self.selectedTechnique.train(self._users)

    def userExists(self, user):
        return self._users.has_key(user.strip())

    def identify(self, frame, bbox):
        technique = self.selectedTechnique
        if not technique:
            return 0, None
        confidence, user = technique.identify(frame, bbox, self.securityTol)

        assert confidence >= 0 and confidence <= 1, "The confidence must be " \
            "in [0, 1] interval."
        assert user is None or self.userExists(user), \
            "The returned user '%s' isn't known. Check the consistency of " \
            "the '%s' technique." % (user, self.selectedTechniqueName)

        return confidence, user