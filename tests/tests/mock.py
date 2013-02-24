class TestFunc:
    
    called = False
    
    def __call__(self):
        self.called = True
