# fzf-tree

Wrap [fzf](https://github.com/junegunn/fzf) with a tool to explore any tree-like structure.


# Motivation

One often comes across tree structures when programming. This tool attempts to make it easy to create tools to explore these tree structures.

It tries to follow the [Unix philosophy](http://www.faqs.org/docs/artu/ch01s06.html):
small programs that communicate via pipelines and new-line separated streams.
It is hoped that such an approach makes it easier to understand and debug the interface to this tool.


# Usage

`fzf-tree` takes two arguments: a root node from which to start exploration and
the name of an executable which finds the children of a node.

Some examples:

```
# Explore the root filesystem
fzf-tree / ls
```

In practice, one may need to write a wrapper script to create output useable by `fzf-tree`.
An example of such a script is contained in the examples directory.

# Testing

The interactive nature of this tool makes testing quite a lot of work - though this tool could be tested with expect. `tox.ini` ensures that the tool can at least be started.

# Alternatives and prior work

The author has written similar interfaces using [rofi](https://github.com/DaveDavenport/rofi)
 as part of other tools.
