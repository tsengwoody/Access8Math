# Integrating the add-on template in your add-on

## Pre-requisites

1. Create a repository, for example on GitHub, providing readme and license files.
1. Clone the repository:

  ```sh
  git clone https://github.com/{repoName}.git
  ```

1. In the folder where your add-on repository is cloned, create an `addon` submolder and store the code for your add-on.

1. Go to the folder where your repository was cloned:

  ```sh
  cd {repoFolder}
  ```

1. Commit your changes:

  ```sh
  git add .
  git commit -m "Initial commit"
  ```

1. Add the template as a remote:

  ```sh
  git remote add template https://github.com/nvaccess/addonTemplate.git
  ```

1. Fetch the add-on template:

  ```sh
  git fetch template
  ```

## Updating an Existing Add-on

As AddonTemplate evolves, it receives improvements, bug fixes, new GitHub workflows, and build system updates.

You can merge the latest template changes into your repository instead of manually copying updated files.

This document explains the recommended update procedure.

> [!NOTE]
> Updating from AddonTemplate only affects your project's infrastructure (build scripts, GitHub workflows, configuration files, etc.). It does **not** modify your add-on's source code.

## Before you begin

Before updating your repository:

- Ensure your working tree is clean.

  ```sh
  git status
  ```

- Commit or stash any pending changes.

- It is recommended to perform the update on a dedicated branch.

If anything goes wrong before the merge commit is created, if you haven't passed the `--squash- flag, you can safely cancel the operation using:

```sh
git merge --abort
```

## Adding the template repository

If you have not already done so, add AddonTemplate as a remote:

```sh
git remote add template https://github.com/nvaccess/AddonTemplate.git
```

Then fetch the latest changes:

```sh
git fetch template
```

## Merging the latest template

Merge the latest version of AddonTemplate:

```sh
git merge template/master --allow-unrelated-histories --squash
```

The `--allow-unrelated-histories` option is required because your add-on repository and AddonTemplate do not share a common Git history.

The `--squash` flags will add changes from the template as a unique commit, instead of several ones, what may be useful to keep a cleaner history on your repository.

At this stage, Git may report merge conflicts.

This is completely normal.

## Understanding merge conflicts

During the merge, Git attempts to combine the contents of both repositories automatically.

When Git cannot determine which version should be kept, it reports a merge conflict.

A conflict does **not** mean that something went wrong.
It simply means that some files require manual review.

## Resolving the merge

### Using the restore command

The `restore` command can be used to update files on your working directory, i.e., the folder where your add-on repository was cloned.
The `--source` flag is used to determine where files to be restored can be found.

### Keep your add-on documentation

Your add-on documentation should not be replaced by the template.

To keep your `.md` files from your add-on repository, ensuring they aren't replaced with files from the template, you can use the following command:

```sh
git restore *.md --source=HEAD
```

### Remove the template documentation

The `docs/` directory belongs to AddonTemplate itself.

It is not intended to become part of your add-on repository.

Remove it:

```
git rm -r docs
```

Or use the restore command:

```sh
git restore docs --source=HEAD
```

### Resolve buildVars.py

`buildVars.py` usually contains merge conflicts because it includes both:

- information specific to your add-on;
- variables introduced by newer versions of AddonTemplate.

Review the file carefully.

In general:

- keep your add-on metadata;
- preserve your version number;
- keep your custom settings;
- add any new variables introduced by the template.

### Resolve pyproject.toml

`pyproject.toml` is another file that commonly requires manual review.

Keep your project-specific configuration while incorporating any new settings required by the updated template.

### Other files

For most remaining files, the version provided by AddonTemplate is generally the correct one.

Typical examples include:

- `.github/`
- `.gitignore`
- `manifest.ini.tpl`
- `manifest-translated.ini.tpl`
- `site_scons/`
- `sconstruct`

Review any conflicts if necessary before completing the merge.

## Completing the merge

Once all conflicts have been resolved, check if the add-on can be built properly:

```sh
uv sync  # Update dependencies
uv run scons  # Build the add-on
```


If all is right, stage the modified files:

```sh
git add .
```

Then create the merge commit:

```sh
git commit
```

## Summary

| File or directory | Recommended action |
|-------------------|--------------------|
| `README.md` | Keep the add-on version |
| `CHANGELOG.md` | Keep the add-on version |
| `docs/` | Remove |
| `buildVars.py` | Merge manually |
| `pyproject.toml` | Merge manually |
| Other template files | Usually accept the template version |

## Troubleshooting

### I don't understand a merge conflict

Merge conflicts are expected when updating from a newer version of AddonTemplate.

Most conflicts occur in `buildVars.py` and `pyproject.toml`.

Review the conflicting sections carefully and combine the changes from both versions.

### I want to cancel the update

If you have not yet committed the merge, and you haven't passed the `--squash` flag to `git merge`, you can restore your repository to its previous state:

```sh
git merge --abort
```

If you passed the `--squash` flag, `git merge --abort` won't work.
In this case, you can use the restore command:

```sh
git restore  . --staged  # Discard changes added to the staging area (after using `git add .`)
```

```sh
git restore . --source=HEAD  # Restores the working directory to the last commit made in your add-on repository
```

If you committed changes, you can use:

```sh
git reset --hard {cleanBranch}
```
