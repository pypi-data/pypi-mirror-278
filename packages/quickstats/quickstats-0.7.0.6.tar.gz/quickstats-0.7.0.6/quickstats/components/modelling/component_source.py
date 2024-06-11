from typing import Optional, Union, List

import ROOT

from quickstats import PathManager
from quickstats.components import ROOTObject
from quickstats.interface.root import RooRealVar

class ComponentSource(ROOTObject):
    
    """

    class ModelType(DescriptiveEnum):
        SIGNAL     = (0, "Signal Model")
        BACKGROUND = (1, "Background Model")
        AUXILIARY  = (2, "Auxiliary Model")
    
                
    @property
    def model_type(self) -> ModelType:
        return self._model_type
    
    @model_type.setter
    def model_type(self, value:Union[str, ModelType]):
        if isinstance(value, ModelType):
            self._model_type = value
        else:
            self._model_type = ModelType.parse(value)
    """
    
    @property
    def observable(self) -> RooRealVar:
        return self._observable
    
    @observable.setter
    def observable(self, value:Union[RooRealVar, ROOT.RooRealVar, dict, str]):
        if value is None:
            self._observable = None
        elif isinstance(value, RooRealVar):
            self._observable = value
        else:
            self._observable = RooRealVar()
            self._observable.parse(value)
    
    def __init__(self, input_paths:Optional[Union[PathManager, str, List[str]]]=None,
                 observable:Optional[Union[RooRealVar, ROOT.RooRealVar, dict, str]]=None,
                 verbosity:Optional[Union[int, str]]="INFO"):
        super().__init__(verbosity=verbosity)
        
        self.path_manager = PathManager()
        self.observable   = observable
        self.set_input_paths(input_paths)

    def set_input_paths(self, paths:Optional[Union[PathManager, str, List[str]]]=None):
        if paths is None:
            return 
        if isinstance(paths, PathManager):
            self.path_manager = path
            return
        if isinstance(paths, str):
            files = {'0': paths}
        elif isinstance(paths, list):
            files = {str(i) : file for i, file in enumerate(value)}
        self.path_manager.update_files(files)
    
    def get_resolved_input_paths(self, **file_kwargs):
        if not self.path_manager.files:
            raise RuntimeError("Input path(s) not set.")
        resolved_paths = []
        for name in self.path_manager.files:
            resolved_path = self.path_manager.get_file(name, check_exist=True, **file_kwargs)
            resolved_paths.append(resolved_path)
        return resolved_paths
        
    def set_observable(self, observable:Union[RooRealVar, ROOT.RooRealVar]):
        self.observable = observable