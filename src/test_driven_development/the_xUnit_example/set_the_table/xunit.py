class TestCase:
    def __init__(self, name: str):
        self.name = name

    def run(self):
        self.set_up()
        method = getattr(self, self.name)
        method()

    def set_up(self):
        pass


class WasRun(TestCase):
    def test_method(self):
        self.was_run = 1

    def set_up(self):
        self.was_run = None
        self.was_set_up = 1


class TestCaseTest(TestCase):
    def set_up(self):
        self.test = WasRun("test_method")

    def test_runnning(self):
        self.test.run()
        assert self.test.was_run

    def test_set_up(self):
        self.test.run()
        assert self.test.was_set_up


TestCaseTest("test_runnning").run()
TestCaseTest("test_set_up").run()
