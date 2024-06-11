import quickstats

quickstats.core.methods._require_module("ROOT", quickstats.core.methods.is_root_installed)

from .macros import load_macros, load_macro
from .TObject import TObject
from .TArrayData import TArrayData
from .TH1 import TH1
from .TH2 import TH2
from .TF1 import TF1
from .TFile import TFile
from .TChain import TChain
from .RooAbsArg import RooAbsArg
from .RooRealVar import RooRealVar
from .RooAbsData import RooAbsData
from .RooDataSet import RooDataSet
from .RooCategory import RooCategory
from .RooAbsPdf import RooAbsPdf
from .RooArgSet import RooArgSet
from .RooMsgService import RooMsgService
from .ModelConfig import ModelConfig
from .RDataFrame import RDataFrame, RDataFrameBackend

load_macros()

quickstats.load_corelib()