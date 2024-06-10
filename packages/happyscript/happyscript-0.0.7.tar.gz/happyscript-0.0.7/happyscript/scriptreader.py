import os, inspect, traceback
import wx
import importlib.util
class ScriptReader:
    def __init__(self, script_dir, group_name = None):
        if group_name is None:
            group_name = os.path.basename(script_dir)
        self.group_name = group_name
        self._script_dir = script_dir
        self.func_help = dict()
        self.func_obj = dict()
        self.mdl = dict()
        self.func_names = dict()
    def reload( self ):
        self.func_help.clear()
        self.func_obj.clear()
        self.mdl.clear()
        self.func_names.clear()
        print("Reading scripts from " + self._script_dir)
        files = os.listdir(self._script_dir)
        msg = ""
        for x in files:
            if not x.endswith(".py") or x=="__init__.py":
                continue
            print( "---> " + x )
            error = self.read_single_file(x)
            if error:
                msg = msg + "\n" + error
        if len(msg)>0:
            msg = "There were (more) errors :" + msg
            wx.MessageBox( msg, "Error importing files", wx.OK | wx.ICON_WARNING )
    def read_single_file(self, filename):
        fullfilename = os.path.join(self._script_dir, filename)
        try:
            child = None
            modname = os.path.splitext(filename)[0]
            spec = importlib.util.spec_from_file_location(modname, fullfilename)
            mdl = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mdl)
            self.mdl[modname] = mdl
            self.func_names[modname] = list()
            for x in inspect.getmembers(mdl, inspect.isfunction):
                funcname = x[0]
                doctxt = inspect.getdoc( x[1] )
                if not doctxt:
                    continue
                if not ("@public" in doctxt) and not ("\\public" in doctxt):
                    continue
                doctxt = doctxt.replace("@public","").replace("\\public","")
                if doctxt:
                    self.func_help["%s.%s" % (modname,funcname)] = doctxt
                else:
                    self.func_help["%s.%s" % (modname,funcname)] = "No help"
                self.func_obj["%s.%s" % (modname,funcname)] = x[1]
                self.func_names[modname].append(funcname)
        except:
            msg = traceback.format_exc()
            wx.MessageBox( msg, "Error importing file %s" % (fullfilename), wx.OK | wx.ICON_WARNING )
        for fname in list(self.func_names.keys()):
            if len(self.func_names[fname]) == 0:
                del self.func_names[fname]
        return None
    def get_file_list(self):
        if len(self.func_names)==0:
            return list()
        result = sorted(self.func_names.keys())
        return result
    def get_func_names(self, filename):
        if not filename in self.func_names:
            return list()
        return sorted(self.func_names[filename])
    def get_help(self, filename, funcname):
        itemname = "%s.%s" % (filename, funcname)
        if itemname in self.func_help:
            return self.func_help[itemname]
        else:
            return "No help for %s.%s" % (filename, funcname)
    def get_func(self, filename, funcname):
        itemname = "%s.%s" % (filename, funcname)
        if itemname in self.func_obj:
            return self.func_obj[itemname]
        else:
            return None
