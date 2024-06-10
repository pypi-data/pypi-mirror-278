import logging, os, time
import yaml
class ScriptInfo(object):
    logger = logging.getLogger('happyscript')
    def __init__(self, testlist):
        self.clear()
        self.__dict__["xx_testlist"] = testlist
    def clear(self):
        self.__dict__["xx_info"] = dict()
        self.__dict__["xx_serials"] = list()
        self.__dict__["xx_filename"] = None
        self.__dict__["xx_dirty"] = False
        self.__dict__["xx_lastupdate"] = time.time()
    def set_serials(self, serials):
        self.xx_serials.clear()
        if serials is not None:
            for sn in serials:
                self.add_serial(sn)
    def add_serial(self, *serials):
        for serial in serials:
            if isinstance(serial, str):
                self.xx_serials.append(serial.strip() )
            else:
                self.logger.error("Given serial is invalid : '%s'" % str(serial) )
                self.xx_serials.append("")
            self.xx_dirty = True
            self.update_file()
    def set_filename(self, fname):
        self.xx_filename = fname
        self.xx_dirty = True
    def write_file(self, fname = None):
        if fname is None:
            fname = self.xx_filename
        if fname is None:
            return
        fname = os.path.splitext(fname)[0] + ".yml"
        file = open(fname, "w")
        if len(self.serials)>0:
            serials_dict = { 'serials': self.serials }
            yaml.dump(serials_dict, file)
        if len(self.xx_info)>0:
            yaml.dump(self.xx_info, file)
        file.close()
    def update_file(self, force=False):
        if len(self.xx_info)==0 and len(self.serials)==0:
            return
        t = time.time()
        if force or (self.xx_dirty and (t - self.xx_lastupdate > 2)):
            self.xx_dirty = False
            self.xx_lastupdate = t
            self.write_file()
    @property
    def serials(self):
        return self.xx_serials.copy()
    def __getattr__(self, attr):
        if attr in self.xx_info:
            return self.xx_info[attr]
        else:
            return None
    def __setattr__(self, attr, value):
        if attr in self.__dict__:
            super().__setattr__(attr, value)
        else:
            self.add(attr, value)
    def get_passed_tests(self, include = None, exclude = None):
        if self.xx_testlist is None:
            return list()
        return self.xx_testlist.get_tests(True, include, exclude)
    def get_failed_tests(self, include = None, exclude = None):
        if self.xx_testlist is None:
            return list() if include is None else include
        return self.xx_testlist.get_tests(False, include, exclude)
    def add(self, objName, theObject):
        if not isinstance(objName, str) or not objName.isidentifier():
            self.logger.error("Given name for information is not a valid identifier : '%s'" % str(objName) )
            return
        self.xx_dirty = True
        objName = objName.lower().strip()
        self.xx_info[objName] = theObject
        self.update_file()
