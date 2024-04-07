# Contributing

## Suggest

If you have idea/feature, you can [open an issue](https://github.com/captaincolonelfox/TeleTok/issues/new)
or [start a discussion](https://github.com/captaincolonelfox/TeleTok/discussions) and I
can try to implement it in my spare time

## Code

Or you can implement it yourself and [open a pull request](https://github.com/captaincolonelfox/TeleTok/pulls), though
maybe you want to [discuss](https://github.com/captaincolonelfox/TeleTok/discussions) the feature first

### Installing with dev dependencies

```shell
pip install -e ".[dev]"
```

### Checks before commit

Run those checks before commit

And test again, if you changed code to fix anything they find

If you are not sure, if you should implement suggested fix or not:
sometime we want to ignore some rules, not all of them are helpful, so just ask and we can discuss it

- linter

```shell
ruff check app
```

- typing

```shell
mypy app
```

- formatter

```shell
black --check app
```

