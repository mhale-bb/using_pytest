---

# Using pytest to write effective software tests

This presentation provides an overview of the concepts exposed by the pytest
module alongside a guided tour that implements those concepts in test code.

All of the "slides" and source code can be found in the linked repository, and
there's a branch for each presentation session so you can go back and read the
diffs after the fact.

To follow along "live," you can fork this repository and run the initialization
script at the top of the directory.

* [GitHub repository](https://github.com/mhale-bb/using_pytest)
* [Email](mailto:mhale@idealintegrations.net)












---

# Why test?

As used in this talk, when I say "test," I am using the following definitions:

**test:**

1. _(verb):_ the act of verifying the expected functionality of a system using
             automated tools.
2. _(noun):_ an automated tool that verifies an expectation of a system.

Tests answer the fundamental question: does this system do what I expect it to
do, given the inputs provided?

This question is always present when working with a system, whether it is
written down or it lives in your head.

Testing, as a practice, simply takes this question and codifies it into a
program.








---

# Testing with pytest

`pytest` is at least two things:

* `pytest` is a test runner. It gathers up all of the tests in your project and
  executes them, then presents the results.
* `pytest` is a Python module. It provides an interface that you can use in
  your tests to improve their design.

The `pytest` test runner can be used to execute tests that aren't written with
any `pytest` module functionality, such as tests that use the `unittest` module
from the standard library.














---

# Test files and tests

Test files look like `test_*.py` or `*_test.py`, and `pytest` is configured by
default to find all such files in your project's test directory (`tests`, in
this case).

Each test in a test file is a function or method prefixed with `test`. Methods
can also be grouped into classes prefixed with `Test`. `pytest` will execute
each test it finds in each test file, and display the results.

For example:

```python test_stuff.py
def test_something():
    ...
```










---

# Practical example 1: Starting from scratch

We're starting with a brand new project, and the `tests` directory is noticably
empty.

We'll make our first test file in the `tests` directory, called `test_foo.py`.

To demonstrate `pytest`, we'll add a simple test in `test_foo.py`:

```python tests/test_foo.py
def test_math_works():
    x = 1
    y = 1
    assert x + y == 1 # This will fail
```

Note that this test doesn't need to import anything from `pytest`. It's just
regular Python code, with a regular `assert` statement.

The names of your tests don't matter until you know what it is you're testing.
At the beginning, they can be any nonsense phrase. You can always squash your
commits later.




---

# Practical example 1: Starting from scratch (cont.)

Now that we know what a failing test looks like, let's make it pass:

```python tests/test_foo.py
def test_math_works():
    x = 1
    y = 1
    assert x + y == 2
```

Our first example is directly executing the code that it's testing. Normally
though, we want to test the code that's actually defined in our module.













---

# Practical example 2: Testing code in our module

We still haven't decided what this module should be doing. For this talk, we'll
have it perform some simple math operations.

This is the point at which you are required to think about the public interface
of your module. How do you want users to consume this code? Since this is
supposed to be doing math, maybe it should expose some mathy functions?

```python tests/test_using_pytest.py
import using_pytest

def test_add():
    x = 1
    y = 2
    assert using_pytest.add(x, y) == 3

def test_multiply():
    x = 4
    y = 6
    assert using_pytest.multiply(x, y) == 24
```




---

# Practical example 2: Testing code in our module (cont.)

There is one very important reason for demonstrating that a test will fail
before you write the code that makes it pass: Showing a failing test is how we
test the tests.

If we accidentally wrote a test that never fails, but we wrote it after
implementing the functionality in our module, how would we tell the difference
between a broken test and well-functioning module code?

```python using_pytest/__init__.py
def add(x, y):
    return x + y

def multiply(x, y):
    return x * y
```









---

# Practical example 2: Testing code in our module (cont.)

Note some of the things that these tests are describing:

* Our module provides functions `add()` and `multiply()`
* These functions each take at least 2 positional parameters
* We expect them to return results appropriate to the arguments provided

These are some of the module's requirements that need to be tested, but these
tests are not exhaustive. Think about some other requirements that we could
include in our tests:

* What happens if we call `add()` or `multiply()` with non-number arguments?
* Can we call them with just one argument? Three or more? Only two?
* Can they handle negative numbers?

All of these questions are about the public interface of the module, and should
be answered with tests.








---

# Test fixtures

`pytest` provides a method of supplying tests with necessary input, called
"fixtures." These are decorated functions that are passed into tests via
parameters of the same name.

If a test accepts a parameter with the same name as a fixture, the test will
receive the results of calling that fixture.

Fixtures are extremely flexible:

* Fixtures can depend on other fixtures
* Fixtures can be scoped as necessary
* Tests can use more than one fixture at a time
* Fixtures can be reused, facilitating test isolation











---

# Practical example 3: Test fixutres

Let's add a fixture:

```python tests/test_using_pytest.py
import pytest
import using_pytest

@pytest.fixture
def data():
    return [3, 4]

def test_add_data(data):
    assert using_pytest.add(*data) == 7

def test_multiply_data(data):
    assert using_pytest.multiply(*data) == 12
```








---

# Parameterization

Just like normal code, test code can be refactored to deduplicate test logic.
Instead of running dozens of copies of effectively the same test, we can
define a test to operate on parameters passed at runtime.

`pytest` provides two main interfaces for parameterizing tests:

* Parameterized fixtures
* The `pytest.mark.parametrize` decorator

While either can be used to parameterize a test, they work a bit differently:

* A parameterized fixture will automatically re-run any tests which depend on
  it, providing them a different parameter each time. The tests don't need to
  encode the knowledge that they will be re-run.
* Tests decorated with `pytest.mark.parametrize` will automatically execute
  once for each parameter, passing in the parameters as-is.

In general:

* Use parameterized fixtures when the test data is being used across multiple
  tests, or when you need to apply additional logic to the parameter values.
* Use the parameterize decorator when the test data is only being used for that
  specific test.

---

# Practical example 4: Parameterizing the tests

We can refactor the earlier tests we wrote to instead use a parameterized
fixture:

```python tests/test_using_pytest.py
import pytest
import using_pytest

@pytest.fixture(params=[
    (1, 2),
    (4, 6),
])
def data(request):
    return request.param

def test_add(data):
    x, y = data
    assert using_pytest.add(x, y) == x + y

def test_multiply(data):
    x, y = data
    assert using_pytest.multiply(x, y) == x * y
```


---

# Exceptions

While we've tested the happy paths, we also want to test for exceptions.
`pytest` provides a simple way to test that an exception was raised:
`pytest.raises()`. If the specified exception is raised, the test passes; if it
_isn't_ raised, the test _fails_.

For example:

```python
import pytest

def test_foo():
    x = {'key': 'val'}
    with pytest.raises(KeyError): # This test will pass
        _ = x['DNE']

def test_foo2():
    x = {'key': 'val'}
    with pytest.raises(KeyError): # This test will fail
        _ = x['key']
```




---

# Practical example 5: Exceptional mathematics

Let's say we call our math functions with non-number input. What should our
code do?

Well, given the functions require numbers to work, we should probably raise a
`TypeError` if arguments of the wrong type are passed as input:

```python tests/test_using_pytest
# ... eariler file content elided ...

def test_add_non_numbers():
    with pytest.raises(TypeError):
        using_pytest.add("non", "numbers")

def test_multiply_non_numbers():
    with pytest.raises(TypeError):
        using_pytest.multiply("non", "numbers")
```







---

# Practical example 5: Exceptional mathematics (cont.)

Why is it important that we be sure what exceptions we expect to see raised
from our code?

Exceptions are part of the public interface that a module provides.

If strange exceptions are thrown, consumers of the module will have to deal
with it.

If the specific type of exception thrown by a function changes, that is a
change to your public interface. It could even be a breaking change.

For example, when I try to use a dictionary key that doesn't exist, I get a
`KeyError`. If that ever changes, every piece of code that checks for a
`KeyError` in that situation will break.

Your own code should make similar guarantees, and it should provide a stable
interface for its exceptions.







---

# Conclusion

`pytest` is a powerful test runner and testing library that facilitates easier
and simpler testing for Python modules. Using `pytest` effectively can have a
positive impact on not only code correctness, but also module design.

Comments? Let me know.

Questions?



















