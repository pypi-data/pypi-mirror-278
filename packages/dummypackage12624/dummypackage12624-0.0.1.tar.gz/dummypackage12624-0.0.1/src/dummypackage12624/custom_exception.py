class InvalidUserInput(Exception):
    def __init__(self, message: str = "Input is invalid"):
        self.message = message
        super().__init__(self.message)


# for linting just run command: "mypy src/" it will check any type error or anything