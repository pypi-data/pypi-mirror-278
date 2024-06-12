import inspect
from .scriptexceptions import ScriptUserAbortException
class ScriptParams(object):
    def __init__(self, ask_gui = None):
        self._ask_gui = ask_gui
        self.argumentList = dict()
        self.on_add_object = None
    def add_object(self, objName, theObject):
        objName = objName.lower().strip()
        if objName=="_mngr_" or (objName is None) or len(objName)==0 or not objName.isidentifier():
            self.on_add_object("invalid object name '%s' " % objName, None)
            return
        elif theObject is None:
            self.on_add_object("Value for object %s is None" % objName, None)
            return
        self.argumentList[objName] = theObject
        if self.on_add_object is not None:
            self.on_add_object( objName, theObject )
    def add_objects(self, *args, **kwargs):
        for obj in args:
            if obj is None:
                continue
            try:
                if hasattr(obj, "name") and isinstance(obj.name, str):
                    self.add_object(obj.name, obj)
                elif hasattr(obj, "_name") and isinstance(obj._name, str):
                    self.add_object(obj._name, obj)
                elif hasattr(obj, "__name__") and isinstance(obj.__name__, str):
                    self.add_object(obj.__name__, obj)
            except AttributeError:
                self.on_add_object("No name found for object that was added", None)
                pass
        for key, value in kwargs.items():
            self.add_object(key, value)
    def get_param(self, param_name):
        if param_name in self.argumentList:
            return self.argumentList[param_name]
        else:
            return None
    def get_parameters(self, scriptObject, extraParams=None):
        if (extraParams is None) or (not isinstance(extraParams,dict)):
            extraParams = dict()
        missing = list()
        argnames = inspect.getfullargspec(scriptObject)[0]
        doctxt = inspect.getdoc( scriptObject )
        argvalues = list()
        for x in argnames:
            if x in self.argumentList:
                argvalues.append( self.argumentList[x] )
            elif x in extraParams:
                argvalues.append( extraParams[x] )
            elif self._ask_gui is not None:
                argvalues.append( self._find_missing_parameter(x, doctxt) )
            else:
                argvalues.append( None )
                missing.append(x)
        return (argvalues, missing)
    def _find_missing_parameter(self, paramName, docTxt ):
        result = None
        lines = docTxt.splitlines()
        for line in lines:
            if "@param " + paramName + " " in line:
                if ':' in line:
                    question = line[line.find(':')+1:].strip()
                else:
                    question = "Give parameter %s" % paramName
                try:
                    if '[num]' in line:
                        result = self._ask_gui.ask_number(question)
                    else:
                        result = self._ask_gui.ask(question)
                except ScriptUserAbortException as _:
                    pass
                break
        return result
