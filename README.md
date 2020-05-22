# mini-weka
Stripped down fork of Weka 3.9.4 without package manager and user interface.

## Code base

The code base of *mini-weka* is synced with Weka's subversion repository, `trunk`
branch up to the following revision:

```
r15559 - 2020-04-17 20:13:17 +1200 (Fri, 17 Apr 2020)
```


## Updating

### Update files
The code base can be synced with Weka's subversion branch using the `update.py`
Python script.

```
usage: update.py [-h] -w, --weka DIR -r, --revision REV [-s, --svn EXECUTABLE]
                 [-n, --dry_run] [-v, --verbose]

Analyzes the svn log from the specified revision on and then updates the code
accordingly. It stores the start/end svn revision in 'update.rev' after
execution.

optional arguments:
  -h, --help            show this help message and exit
  -w, --weka DIR        the directory with the Weka subversion repository
                        (HEAD)
  -r, --revision REV    the svn revision to start from
  -s, --svn EXECUTABLE  the svn executable to use if not on the path
  -n, --dry_run         whether to perform a dry run, i.e., only simulating
                        the update
  -v, --verbose         whether to be verbose with the output
```

Example:

```commandline
python3 update.py \
  -w /some/where/weka-HEAD/ \
  -r 15559 \ 
  -v
```

### Post-process files

* Files that should not end up in the code base need to be added to the 
  `BLACKLISTED_FILES` list
* Directories that should not end up in the code base need to be added to the
  `BLACKLISTED_PATHS`
* Remove any occurrences of the following annotations

  * `@ProgrammaticProperty`
  * `@FilePropertyMetadata`

### Run unit tests

* Switch to Java 8 as compiler
* Run unit tests as follows

  ```commandline
  mvn clean test
  ```

### Commit

* Once compilation and unit tests work, commit all changes
* Update the revision in this README
