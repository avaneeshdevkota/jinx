class Return(RuntimeError):

    def __init__(self, value):
        super().__init__(None, None, False, False)

        self.value = value
