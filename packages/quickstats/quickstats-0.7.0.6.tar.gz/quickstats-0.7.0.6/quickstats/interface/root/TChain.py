from typing import Optional, Union, List, Dict
import numpy as np

from quickstats import semistaticmethod
from .TObject import TObject
from .TFile import TFile

class TChain(TObject):
    
    def __init__(self, treename:str,
                 source:Optional[Union[str, List[str]]],
                 **kwargs):
        super().__init__(treename=treename, source=source, **kwargs)
        
    def initialize(self, treename:str,
                   source:Optional[Union[str, List[str]]]):
        import ROOT
        obj = ROOT.TChain(treename)
        filenames = TFile.list_files(source)
        for filename in filenames:
            obj.AddFile(filename)
        self.obj = obj

    def get_entries(self, sel:Optional[str]=None):
        if sel:
            return self.obj.GetEntries(sel)
        return self.obj.GetEntries()
    
    # taken from https://root.cern/doc/master/classTChain.html#a98aec49da3a78d4298b7c40d5c1d79bb
    @semistaticmethod
    def parse_tree_filename(self, name:str):
        import ROOT
        url = ROOT.TUrl(name, True)
        if url.GetProtocol() != "file":
            filename = url.GetUrl()
        else:
            filename = url.GetFileAndOptions()
        query = None
        treename = None
        suffix = None
        fn = url.GetFile()
        # extract query
        options = url.GetOptions()
        if options and (len(options) > 0):
            query = f"?{options}"
        # extract treename
        anchor = url.GetAnchor()
        if anchor and (anchor[0] != '\0'):
            # support "?#tree_name" and "?query#tree_name"
            if (query or ("?#" in name)):
                if '=' in anchor:
                    query += '#'
                    query += anchor
                else:
                    treename = anchor
            else:
                # the anchor is part of the file name
                fn = url.GetFileAndOptions()
        suffix = url.GetFileAndOptions()
        # get options from suffix by removing the file name
        index = suffix.index(fn)
        if index != -1:
            suffix = suffix[:index] + suffix[index + len(fn):]
        # remove the options suffix from the original file name
        index = filename.index(suffix)
        if index != -1:
            filename = filename[:index] + filename[index + len(suffix):]
        
        # special case: [...]file.root/treename
        index = filename.rfind(".root")
        if index != -1:
            slash_index = filename.rfind('/')
            if (slash_index != -1) and (slash_index >= (index + len(".root"))):
                treename = filename[slash_index + 1:]
                filename = filename[:slash_index]
                suffix = f"/{treename}" + suffix
        results = {
            "filename": filename,
            "treename": treename,
            "query": query,
            "suffix": suffix
        }
        return results