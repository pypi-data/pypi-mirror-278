# Typehinted Classes for Cleo 2.x

The authors of the excellent [Cleo](https://github.com/python-poetry/cleo) library have declared a plan to overhaul Typing in Cleo 3.x, amongst the many other improvements listed in their [Writeup](https://github.com/python-poetry/cleo/issues/415).

In the meantime, some of the projects that I work on make use of Cleo 2.x, whose `Command.option()` and `Command.argument()` methods are annotated with `t.Any` and don't enforce returned types.

This library adds type-hinted, type-enforced wrappers for these methods as a holdover until Cleo 3.x is ready for use.

**If Cleo 3.x is out by the time you're reading this: You should probably be using that instead!**

# PyPi
https://pypi.org/project/typehints-cleo2/

# Installation
### With Poetry:
`poetry add typehints_cleo2`

### With pip:
`pip install typehints_cleo2`

# Example Usage
Modified example from Cleo's [README.md](https://github.com/python-poetry/cleo/blob/cca07a75f8e8cc9095221ab6e3e246baedaecf31/README.md?plain=1#L18)

```python
from cleo.helpers import argument, option

# Instead of `from cleo.commands.command import Command`
from typehints_cleo2 import TypeHintedCommand


# use TypeHintedCommand as a drop-in replacement for cleo's Command class
class GreetCommand(TypeHintedCommand):

    ...

    def handle(self):
        name: str = self.argument_str("name")  # Type-Hinted argument_str guarantees a string return
        ...

    ...

```

## Optional Arguments & Options

```python
class TestCommand(TypeHintedCommand):

    name = "test"
    description = "Test Command"
    arguments = [
        argument("test_argument", description="A test argument", optional=False),
        argument("test_argument2", description="A test argument", optional=True),
    ]
    options = [option("test_option", description="A test option")]

    ...

    def handle(self):
        arg1: str = self.argument_str("test_argument")
        arg2: str | None = self.argument_str_optional("test_argument2")
        opt1: str | bool = self.option_str("test_option")
        self.line(f"Test Command! -- Arg1: '{arg1}' -- Arg2: '{arg2}' -- Opt1: '{opt1}'")

    ...

```
```bash
poetry run python -m my_application test a_test_val

Output: Test Command! -- Arg1: 'a_test_val' -- Arg2: 'None' -- Opt1: 'False'
```
