# mini-weka
Stripped down fork of [Weka](https://www.cs.waikato.ac.nz/ml/weka/) 3.9.x branch (HEAD) without package manager and user interface.
PMML support and certain XML support (e.g., for serialization) was removed as well to reduced
the number of dependencies. Finally, several classes got reverted to pre-MTJ matrix versions 
(PrincipalComponents, LinearRegression, GaussianProcesses, MultiVariateGaussianEstimator).
Overall, the changes achieved a pure Java library with minimal dependencies (only java-cup-runtime), making it a good candidate for inclusing in, e.g., Maven projects. Apart from the aforementioned classes, models (Java serialized objects) are compatible between standard Weka and this fork.


## Code base

The code base of *mini-weka* is synced (manually) with Weka's subversion repository, 
[trunk branch](https://svn.cms.waikato.ac.nz/svn/weka/trunk/) up to the following 
revision:

```
r15955   # svn revision
```

## Maven

Releases use the following versioning system:
```
X.Y.Z
```
* `X.Y` - the Weka major/minor release version
* `Z` - the Weka subversion repository revision that the code base was synced to

### Releases

Add the following dependency to your `pom.xml` to use the latest [release](https://search.maven.org/search?q=a:mini-weka) of *mini-weka*:

```xml
<dependency>
  <groupId>com.github.fracpete</groupId>
  <artifactId>mini-weka</artifactId>
  <version>3.9.15955</version>
</dependency>
```

* 3.9.15955 - equivalent to 3.9.6
* 3.9.15750 - equivalent to 3.9.5
* 3.9.15580 - post 3.9.4

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

### Run unit tests

* Switch to Java 8 as compiler
* Run unit tests as follows

  ```commandline
  mvn clean test
  ```

### Commit

* Once compilation and unit tests work, commit all changes
