class QuizColab:
    def __init__(self) -> None:
        pass

    def parse(self, message):
        if message == 'help':
            return self.helper_box()

    def helper_box(self):
        return '''
        Help
        ----
        
        '''
