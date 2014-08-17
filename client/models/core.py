import utils

class Test(object):
    """Represents all suites for a single test in an assignment."""

    def __init__(self, names=None, suites=None, points=0, note='',
            cache=''):
        self.names = names or []
        # Filter out empty suites.
        if suites:
            self.suites = [suite for suite in suites if suite]
        else:
            self.suites = []
        self.points = points
        self.note = utils.dedent(note)
        # TODO(albert): the notion of a cache was originally designed
        # only for code-based questions. Either generalize for other
        # test types, or move to subclasses.
        self.cache = utils.dedent(cache)

    @property
    def name(self):
        """Gets the canonical name of this test.

        RETURNS:
        str; the name of the test
        """
        if not self.names:
            return repr(self)
        return self.names[0]

    @property
    def count_cases(self):
        """Returns the number of test cases in this test."""
        return sum(len(suite) for suite in suites)

    @property
    def count_locked(self):
        """Returns the number of locked test cases in this test."""
        return [case.is_locked for suite in suites
                               for case in suite].count(True)

    def add_suite(self, suite):
        """Adds the given suite to this test's list of suites. If
        suite is empty, do nothing."""
        if suite:
            self.suites.append(suite)
            suite_num = len(self.suites) - 1
            for test_case in suite:
                test_case.test = self
                test_case.suite_num = suite_num

class TestCase(object):
    """Represents a single test case."""

    def __init__(self, input_str, outputs, test=None, **status):
        self._input_str = utils.dedent(input_str)
        self._outputs = outputs
        self.test = test
        self._status = status

    @property
    def is_locked(self):
        return self._status.get('lock', True)

    def set_locked(self, locked):
        self._status['lock'] = locked

    @property
    def outputs(self):
        return self._outputs

    def set_outputs(self, new_outputs):
        self._outputs = new_outputs

    @property
    def type(self):
        """Subclasses should implement a type tag."""
        return 'default'

class TestCaseAnswer(object):
    """Represents an answer for a single TestCase."""

    def __init__(self, answer, choices=None, explanation=''):
        self.answer = answer    # The correct answer, possibly encoded
        self.choices = choices or []
        self.explanation = explanation

    @property
    def is_multiple_choice(self):
        return len(self.choices) > 0

