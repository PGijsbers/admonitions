# Admonitions

Convert Github admonitions to `mkdocs-material` admonitions when building docs,
so that you can have admonitions on Github _and_ in the documentation from the
same file.

> [!TIP]
> This is an admonition. They are a useful tool to attract attention to information.

# Usage

To install the plugin:

```bash
python -m pip install gh-admonitions
```

Then in your `mkdocs.yml` file, add the plugin:

```yaml
plugins:
  - gh-admonitions
```

Now you can write Github-compatible admonitions, and they will be 
automatically converted when used in `mkdocs-material` pages.

## The Problem

Both Github and `mkdocs-material` support admonitions from their markdown flavors.
Unfortunately, their flavors are different. 
A Github admonition is written like this:

```
> [!TIP]
> This is the Github admonition syntax.
```

And `mkdocs-material` admonitions are written like this:

```
!!! tip

    This is the mkdocs-materials admonition syntax.
```

So now whenever you have markdown documentation that should be readable both
on Github and from built documentation, using either style means it will show
up as 

## Limitations

The `mkdocs-materials` admonitions are much more powerful. They can feature
titles. They have more types and you can add custom ones. You can in-line
admonitions. They can be collapsable, and be collapsed by default.
And much more. 

But since the Github syntax has none of that, this tool can not offer such
`mkdocs-material` admonitions to be generated. All admonitions will be
converted to non-collapsed title-less admonitions.



