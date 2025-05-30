# GitHub Admonitions for MkDocs

Convert [GitHub admonitions](https://github.com/orgs/community/discussions/16925)
to [`mkdocs` admonitions](https://python-markdown.github.io/extensions/admonition/) 
when building docs, so that you can have admonitions on GitHub _and_ in the 
documentation from the same file.

Now also supporting GitLab admonitions ([alerts](https://docs.gitlab.com/user/markdown/#alerts), thanks @pismy!).

> [!TIP]
> This is an admonition. They are a useful tool to attract attention to information.

## Usage

To install the plugin:

```bash
python -m pip install mkdocs-github-admonitions-plugin
```

Then in your `mkdocs.yml` file, add the plugin:

```yaml
plugins:
  - gh-admonitions
```

Now you can write GitHub-compatible admonitions, and they will be 
automatically converted when used in [`mkdocs`][mm] pages.

## Why is this needed?

Both GitHub and [`mkdocs`][mm] support admonitions from their markdown flavors.
Unfortunately, their flavors are different. 
A GitHub admonition is written like this:

```
> [!TIP]
> This is the GitHub admonition syntax.
```

And [`mkdocs`][mm] admonitions are written like this:

```
!!! tip

    This is the mkdocs-materials admonition syntax.
```

So an admonition in your documentation will render correctly on either GitHub
or in your [`mkdocs`][mm] pages, but not both. With this plugin, you write 
the admonition once in GitHub syntax, and it will still show correctly in the
built [`mkdocs`][mm] pages!

## Limitations

The [`mkdocs`][mm] admonitions are much more powerful. They can feature
titles. They have more types, and you can add custom ones. You can render inline
admonitions. They can be collapsable, and be collapsed by default.
And much more. 

But since the GitHub syntax has none of that, this tool can not offer such
[`mkdocs`][mm] admonitions to be generated. All admonitions will be
converted to non-collapsed title-less admonitions.

GitHub admonitions feature two types which are not supported by [`mkdocs`][mm]:
`caution` and `important`. In converting these admonitions, we will preserve their title,
but use the `danger` and `warning` symbol and color, respectively.

## Examples

Here is a gallery with various admonitions.
They should show up correctly on the built documentation too!

> [!tip]
> This is normally formatted. Type in lower case. No extra spaces.
> It contains two lines in markdown, but only a soft linebreak.

>   [!CAUTION]    
> This admonition has:  
> 
>   - ALL CAPS in the type
>   - a list
> 
> Note that this admonition uses the "danger" symbol with "Caution" title.

> [!Important]
> This contains `inline` and
> ```python
> import this  # python code in ticks
> ```
>
>     and code block with spaces
>
> Note that this admonition uses the "warning" symbol with "Important" title.

> [!note]
> And this admonition contains an empty line
>
> That only has a `>` character in markdown.

> [!warning]
> Admonitions may contains quotes
> > Quotes always contain great wisdom. 

But pay attention! There may be admonitions which are really just code:
```text
> [!note]
> This is not an admonition.
```

## Disclaimer

This is an independent project and not affiliated with GitHub in any way.

[mm]: https://www.mkdocs.org
