def set_multithread(multithread:bool):
    import ROOT
    if (not ROOT.IsImplicitMTEnabled()) and (multithread):
        ROOT.EnableImplicitMT()
    elif (ROOT.IsImplicitMTEnabled()) and (not multithread):
        ROOT.DisableImplicitMT()

class RMultithreadEnv(object):
    def __init__(self, enable_multithread:bool):
        import ROOT
        self.original_multithread_state = ROOT.IsImplicitMTEnabled()
        self.new_multithread_state = enable_multithread
      
    def __enter__(self):
        import ROOT
        if (not self.original_multithread_state) and self.new_multithread_state:
            ROOT.EnableImplicitMT()
        elif (self.original_multithread_state) and (not self.new_multithread_state):
            ROOT.DisableImplicitMT()
        return self
  
    def __exit__(self, *args):
        import ROOT
        if (not self.original_multithread_state) and self.new_multithread_state:
            ROOT.DisableImplicitMT()
        elif (self.original_multithread_state) and (not self.new_multithread_state):
            ROOT.EnableImplicitMT()