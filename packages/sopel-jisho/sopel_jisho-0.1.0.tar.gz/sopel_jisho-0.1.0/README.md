# sopel-jisho

Sopel plugin to search Jisho.org, a Japanese/English dictionary.

## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:

```shell
$ pip install sopel-jisho
```

### Requirements

`sopel-jisho` requires Sopel 7.1+ and `requests`.

## Usage
Commands & arguments:

* `.jisho <search query>` (also available as `.ji`)
  * `<search query>`: the keyword(s) to search for on Jisho

## Notes

This plugin has beta-level functionality. It can search and display most
queries, but may not correctly deal with incomplete API responses (for example,
words that have no readings). That said, anything that doesn't behave as
expected should be reported in the plugin's [issue tracker][] if it isn't
already listed there (be sure to **also search closed issues!**).

Jisho's API is undocumented and subject to change, so there are sure to be edge
cases where the code receives something it doesn't expect. Some of these are
handled. Others aren't…yet. Report problematic queries to the issue tracker.

[issue tracker]: https://github.com/dgw/sopel-jisho/issues
