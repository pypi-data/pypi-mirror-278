from unittest import TestCase
from argparse_decorations import RootCommand, Command, SubCommand, Argument, init, parse, run, finish


class TestDecorations(TestCase):

    def tearDown(self):
        finish()


    def test_tests(self):
        self.assertTrue(True)


    def test_RootCommand(self):
        called = False

        @RootCommand
        def handler():
            nonlocal called
            called = True

        parse()

        run()

        self.assertTrue(called)


    def test_Command(self):
        called = False

        @Command('command')
        def handler():
            nonlocal called
            called = True

        parse(['command'])

        run()

        self.assertTrue(called)


    def test_call_handler_directly(self):
        @Command('command')
        def handler():
            return 31

        result = handler()

        self.assertEqual(result, 31)


    def test_SubCommand(self):
        called = False

        @Command('command')
        @SubCommand('add')
        def handler():
            nonlocal called
            called = True

        parse(['command', 'add'])

        run()

        self.assertTrue(called)


    def test_SubCommands_under_same_command(self):
        add_called = False
        sub_called = False

        @Command('command')
        @SubCommand('add')
        def add_handler():
            nonlocal add_called
            add_called = True

        @Command('command')
        @SubCommand('sub')
        def sub_handler():
            nonlocal sub_called
            sub_called = True

        parse(['command', 'add'])

        run()

        self.assertTrue(add_called)

        parse(['command', 'sub'])

        run()

        self.assertTrue(sub_called)


    def test_Argument(self):
        result = None

        @Command('add')
        @Argument('x', type=int)
        @Argument('y', type=int)
        def add(x, y):
            nonlocal result
            result = x + y

        parse(['add', '2', '3'])

        run()

        self.assertEqual(result, 5)

