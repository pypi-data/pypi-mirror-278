# Odoo Addons Installer

The purpose of this lib is to watch environment variable and find [Odoo](https://github.com/odoo/odoo) extra addons_path.
The addons path can be `git` project (private or not, see [The protocole and the credential](#_private_git_project)) or local dir.

Install
=======

`pip install addons-installer --user` or from our registry
`pip install addons-installer --extra-index-url https://gitlab.ndp-systemes.fr/api/v4/projects/319/packages/pypi/simple`  or in your `requirement.txt` file

Fetch git project
=================

To add a `git` extra addons path you need to declare an environment variable `ADDONS_GIT_FOO`, where the value is the git project path **without the domain**.
To specify the domain you need to add a `ADDONS_GIT_FOO_SERVER=https://my.custom.git.vcs.com`, by default is `https://github.com` by convention.
In fact if you follow the convention you need to stop your configuration here.
See default value and convention if you want to fully customize the `git clone` commande that will be generated.

Convention
----------

### The branch to fetch `ADDONS_GIT_<NAME>_BRANCH`

The branch used will be in order of priority:

1.  The value of `ADDONS_GIT_<NAME>_BRANCH`
2.  The value of `ADDONS_GIT_DEFAULT_BRANCH` except `ADDONS_GIT_<NAME>_BRANCH == "NO_DEFAULT"`
3.  The value of `ODOO_VERSION` environment variable
4.  If `ODOO_PATH` exist then we look in the file `$ODOO_PATH/odoo/release.py` and get the `major_version` as value
5.  `"master"` if none above is valid.

### The server (domain name) of your git repository

By default, we use `https://github.com`.
You can specify a *default domain* with `ADDONS_GIT_DEFAULT_SERVER` if
you want.

Resolving the value by priority:

1.  The value of `ADDONS_GIT_<NAME>_SERVER`
2.  The value of `ADDONS_GIT_DEFAULT_SERVER` except `ADDONS_GIT_<NAME>_SERVER == "NO_DEFAULT"`
3.  `"https://github.com"` if none above is valid

### The protocole and the credential

By default `addons-installer` will use a `public` schema for the url. If the git project is private, you need to change
`ADDONS_GIT_<NAME>_PROTOCOLE` to `https`. Then you need to add the `ADDONS_GIT_<NAME>_HTTPS_LOGIN` and `ADDONS_GIT_<NAME>_HTTPS_PASSWORD` environment vars.

The `ssh` protocole isn’t supported
:warning: The lib will raise an `ValueError` if no credential is provided

Resolving the value by priority:

1.  The value of `ADDONS_GIT_<NAME>_PROTOCOLE`
2.  The value of `ADDONS_GIT_DEFAULT_PROTOCOLE` except `ADDONS_GIT_<NAME>_PROTOCOLE == "NO_DEFAULT"`
3.  `"public"` if none above is valid

Resolving the value by priority for credential:

1.  The value of `ADDONS_GIT_<NAME>_HTTPS_LOGIN`
2.  The value of `ADDONS_GIT_DEFAULT_HTTPS_LOGIN`
3.  `raise` `IllegalValueException`
4.  The value of `ADDONS_GIT_<NAME>_HTTPS_PASSWORD`
5.  The value of `ADDONS_GIT_DEFAULT_HTTPS_PASSWORD`
6.  `raise` `IllegalValueException`

### The clone path

Allow to specift the path where the project will be cloned.
This path can be absolute or not **(An absolute path is better for predictable behavior)**.

- `~` use the home of the current user
- `.` is your current working directory

Resolving the value by priority:

1. The value of `ADDONS_GIT_<NAME>_CLONE_PATH` (take the value as final destination)
2. The value of `ADDONS_GIT_DEFAULT_CLONE_PATH`. Take the value *base root path* where to clone.
   The final value will be `$ADDONS_GIT_DEFAULT_CLONE_PATH/<NAME>`.
3. The os temporary file. `/tmp` if you are under a GNU/Linux system

The pull option
---------------

Allow to add `git clone` custom option. by default we use `--depth=1 --quiet --single-branch`.
The value must be a **comma** or **space** separated value. `argparse` is used to parse the values.
If you want to fully erase the default value you should use `","` as value.
`""` will be handle as `False`.

Resolving the value by priority:
1. The value of `ADDONS_GIT_<NAME>_PULL_OPTION`
2. The value of `ADDONS_GIT_DEFAULT_PULL_OPTION`. Except `ADDONS_GIT_<NAME>_SERVER == "NO_DEFAULT"`
3. `--depth=1 --quiet --single-branch` if none above is valid

Use local directory
===================

You can add `addons-path` in the local filesystem with `ADDONS_LOCAL_<NAME>`.
There is only one configuration environment variable, `ADDONS_LOCAL_DEFAULT_BASE_PATH`.
`ADDONS_LOCAL_DEFAULT_BASE_PATH` allow you to specify the root path to see.

Exemple
-------

In this exemple

    /src
      |
      -- path1
      -- path2
    /other
      |
      -- sub
        |
        -- path3

To include `/src/path1`, `/src/path2` and `/other/sub/path3` you have choice.

Using `ADDONS_LOCAL_DEFAULT_BASE_PATH`:
1. `ADDONS_LOCAL_DEFAULT_BASE_PATH="/src"`
2. `ADDONS_LOCAL_PATH1="path1"`
3. `ADDONS_LOCAL_PATH2="path2"`
4. `ADDONS_LOCAL_PATH3="/other/sub/path2"`

Without `ADDONS_LOCAL_DEFAULT_BASE_PATH`:
1.  `ADDONS_LOCAL_PATH1="/src/path1"`
2.  `ADDONS_LOCAL_PATH2="/src/path2"`
3.  `ADDONS_LOCAL_PATH3="/other/sub/path2"`

### ADDONS_GIT_SUBDIR_OF and ADDONS_LOCAL_SUBDIR_OF

TODO: Explain this feat


Cli
===
The Cli gives an entrypoint called `addons-installer`
The Cli can be used to perform the installation of all addons declared in ENV vars, to specify which addons should be installed, or to retrieve the installing command without actually performing it.
We can use the `--profiles` option to pass profiles files that contains ENV var declaration
`addons-installer -help` to get usage

Developper local usage
======================
The library can be installed with ` pip install -e .`
Tests can be run with `python -m unittest discover`
Cli can be used with
```
export ADDONS_GIT_DEFAULT_SERVER="gitlab.com"; export ADDONS_GIT_MY_PROJECT="my-project"; export ADDONS_GIT_MY_PROJECT_PROTOCOLE="public";addons-installer -install --profiles toto,truc -i my_project --cmd-only
```
