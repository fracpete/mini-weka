import argparse
import logging
import shutil
import subprocess
import traceback

SVN_PREFIX = "/trunk/weka/"
""" the prefix in svn paths """

BLACKLISTED_FILES=[
    # maven
    "/trunk/weka/pom.xml",
    # MTJ related changes
    "/trunk/weka/src/main/java/weka/attributeSelection/PrincipalComponents.java",
    "/trunk/weka/src/test/resources/wekarefs/weka/attributeSelection/PrincipalComponentsTest.ref",
    "/trunk/weka/src/main/java/weka/classifiers/functions/GaussianProcesses.java",
    "/trunk/weka/src/test/resources/wekarefs/weka/classifiers/functions/GaussianProcessesTest.ref",
    "/trunk/weka/src/main/java/weka/classifiers/functions/LinearRegression.java",
    "/trunk/weka/src/test/resources/wekarefs/weka/classifiers/functions/LinearRegressionTest.ref",
    "/trunk/weka/src/main/java/weka/estimators/MultivariateGaussianEstimator.java",
    "/trunk/weka/src/main/java/weka/filters/unsupervised/attribute/PrincipalComponents.java",
    "/trunk/weka/src/test/resources/wekarefs/weka/filters/unsupervised/attribute/PrincipalComponentsTest.ref",
    "/trunk/weka/src/test/resources/wekarefs/weka/classifiers/rules/M5RulesTest.ref",
    "/trunk/weka/src/test/resources/wekarefs/weka/classifiers/trees/M5PTest.ref",
    # package management related
    "/trunk/weka/src/main/java/weka/core/Utils.java",
    "/trunk/weka/src/main/java/weka/core/ResourceUtils.java",
    "/trunk/weka/src/main/java/weka/core/WekaPackageLibIsolatingClassLoader.java",
    "/trunk/weka/src/main/java/weka/core/WekaPackageManager.java",
    "/trunk/weka/src/main/java/weka/core/WekaPackageClassLoaderManager.java",
    # javadoc
    "/trunk/weka/src/main/java/weka/core/AllJavadoc.java",
    "/trunk/weka/src/main/java/weka/core/Javadoc.java",
    "/trunk/weka/src/main/java/weka/core/TechnicalInformationHandlerJavadoc.java",
    "/trunk/weka/src/main/java/weka/core/OptionHandlerJavadoc.java",
    "/trunk/weka/src/main/java/weka/core/GlobalInfoJavadoc.java",
    # obsolete tests
    "/trunk/weka/src/test/java/weka/test/WekaTestSuite.java",
    "/trunk/weka/src/test/java/weka/classifiers/AllTests.java",
    "/trunk/weka/src/test/java/weka/classifiers/functions/supportVector/AllTests.java",
    "/trunk/weka/src/test/java/weka/classifiers/pmml/consumer/AllTests.java",
    "/trunk/weka/src/test/java/weka/attributeSelection/AllTests.java",
    "/trunk/weka/src/test/java/weka/AllTests.java",
    "/trunk/weka/src/test/java/weka/filters/AllTests.java",
    "/trunk/weka/src/test/java/weka/filters/AllFilterTest.java",
    "/trunk/weka/src/test/java/weka/clusterers/AllTests.java",
    "/trunk/weka/src/test/java/weka/associations/AllTests.java",
    "/trunk/weka/src/test/java/weka/core/AllTests.java",
    "/trunk/weka/src/test/java/weka/core/OptionHandlersTests.java",
    "/trunk/weka/src/test/java/weka/core/tokenizers/AllTests.java",
    "/trunk/weka/src/test/java/weka/core/neighboursearch/AllTests.java",
    "/trunk/weka/src/test/java/weka/core/converters/AllTests.java",
    "/trunk/weka/src/test/java/weka/datagenerators/AllTests.java",
]

BLACKLISTED_PATHS=[
    # gui related classes
    "/trunk/weka/src/main/java/weka/gui",
    # package management
    "/trunk/weka/src/main/java/weka/core/packageManagement",
    # scripts
    "/trunk/weka/src/main/scripts",
    # pmml
    "/trunk/weka/src/main/java/weka/classifiers/pmml",
    "/trunk/weka/src/main/java/weka/core/pmml",
    "/trunk/weka/src/test/java/weka/classifiers/pmml",
    "/trunk/weka/src/test/resources/wekarefs/weka/classifiers/pmml",
    # other
    "/trunk/weka/src/main/java/weka/core/json",
    "/trunk/weka/src/main/java/weka/core/logging",
    "/trunk/weka/src/main/java/weka/core/metastore",
    "/trunk/weka/src/main/java/weka/core/xml",
    "/trunk/weka/src/main/java/weka/classifiers/xml",
]

POM_VERSION_TAG = "<!-- mini-weka-version -->"
""" Comment tag in pom.xml to identify the version """

POM_VERSION_TEMPLATE = "  <version>3.9.%i-SNAPSHOT</version><!-- mini-weka-version -->\n"
""" Template for inserting the new version """

README_REVISION_COMMENT = "# svn revision"
""" The comment to identify the line with the revision """

README_REVISION_TEMPLATE = "r%i   # svn revision\n"
""" The template for the revision in the README """

README_VERSION_TAG = "<!-- mini-weka-version -->"
""" The tag to identify the line with the revision """

README_VERSION_TEMPLATE = "  <version>3.9.%i-SNAPSHOT</version><!-- mini-weka-version -->\n"
""" The template for the version in the README """

logger = logging.getLogger("mini-weka-update")
""" the logging instance to use """


def output_process_info(res):
    """
    Outputs process information.

    :param res: the complete process
    :type res: subprocess.CompletedProcess
    """
    logger.debug("command: %s" % " ".join(res.args))
    if len(res.stdout) > 0:
        logger.debug("stdout:\n%s" % res.stdout.decode("UTF-8"))
    if len(res.stderr) > 0:
        logger.debug("stderr:\n%s" % res.stderr.decode("UTF-8"))


def update_pom(revision):
    """
    Updates the pom.xml with the revision.

    :param revision: the final revision
    :type revision: int
    """

    logger.info("Updating pom.xml")
    with open("./pom.xml", "r") as pom_file:
        lines = pom_file.readlines()
    for i in range(len(lines)):
        if POM_VERSION_TAG in lines[i]:
            lines[i] = POM_VERSION_TEMPLATE % revision
    with open("./pom.xml", "w") as pom_file:
        pom_file.writelines(lines)


def update_readme(revision):
    """
    Updates the README.md with the revision.

    :param revision: the final revision
    :type revision: int
    """

    logger.info("Updating README.md")
    with open("./README.md", "r") as pom_file:
        lines = pom_file.readlines()
    for i in range(len(lines)):
        if README_REVISION_COMMENT in lines[i]:
            lines[i] = README_REVISION_TEMPLATE % revision
        if README_VERSION_TAG in lines[i]:
            lines[i] = README_VERSION_TEMPLATE % revision
    with open("./README.md", "w") as pom_file:
        pom_file.writelines(lines)


def requires_post_processing(source):
    """
    Determines whether the file requires post-processing.
    Looks for: @ProgrammaticProperty, @FilePropertyMetadata

    :param source: the file to check
    :type source: str
    :return: True if the file requires post-processing
    :rtype: bool
    """
    result = False
    with open(source, "r") as source_file:
        lines = source_file.readlines()
    for line in lines:
        if "@ProgrammaticProperty" in line:
            result = True
            break
        if "@FilePropertyMetadata" in line:
            result = True
            break
    return result


def post_process(source, target):
    """
    Post-processes the source content before writing it to its target.

    :param source: the source file
    :type source: str
    :param target: the target file
    :type target: str
    """

    logger.info("Post-processing %s" % source)

    with open(source, "r") as source_file:
        lines = source_file.readlines()

    filtered = []
    is_open = False
    for i in range(len(lines)):
        if is_open:
            if lines[i].strip().endswith(")"):
                is_open = False
                continue
        # remove import of annotations
        if "import " in lines[i]:
            if "weka.gui.FilePropertyMetadata;" in lines[i]:
                continue
            if "weka.gui.ProgrammaticProperty;" in lines[i]:
                continue
        # remove annotations itself
        if "@ProgrammaticProperty" in lines[i]:
            continue
        if "@FilePropertyMetadata" in lines[i]:
            if lines[i].strip().endswith(")"):
                continue
            else:
                is_open = True
                continue
        filtered.append(lines[i])

    with open(target, "w") as target_file:
        target_file.writelines(filtered)



def process_paths(weka, paths, dry_run, verbose):
    """
    The paths in the svn log to process.

    :param weka: the directory with the Weka subversion checkout (HEAD)
    :type weka: str
    :param paths: the list of svn paths to process
    :type paths: list
    :param dry_run: whether to perform a dry-run, i.e., simulation
    :type dry_run: bool
    :param verbose: whether to be verbose with the output
    :type verbose: bool
    :return: the number of files updated
    :rtype: int
    """

    result = 0

    for path in paths:
        # skip all paths that we don't care about
        if not path.startswith(SVN_PREFIX):
            continue

        # check whether path is blacklisted
        blacklisted = False
        # check files
        if path in BLACKLISTED_FILES:
            if verbose:
                logger.info("Blacklisted: %s" % path)
            blacklisted = True
        # check paths
        if not blacklisted:
            for dir in BLACKLISTED_PATHS:
                if path.startswith(dir):
                    if verbose:
                        logger.info("Blacklisted: %s" % path)
                    blacklisted = True
                    break
        if blacklisted:
            continue

        if dry_run:
            logger.info("Update required: %s" % path)
        else:
            logger.info("Updating: %s" % path)

        # generate filenames
        source = weka + path[len("/trunk"):]  # exclude "/trunk"
        target = "./" + path[len(SVN_PREFIX):].replace("wekarefs", "")
        if verbose:
            logger.info("%s\n->%s" % (source, target))
        result += 1

        # copy file
        if not dry_run:
            try:
                if requires_post_processing(source):
                    post_process(source, target)
                else:
                    shutil.copyfile(source, target)
            except:
                logger.severe("Failed to copy %s to %s\n%s" % (source, target, traceback.format_exc()))

    return result


def update(weka, revision, svn=None, dry_run=False, verbose=False):
    """
    Updates the code base startin from the specified revision.

    :param weka: the directory with the Weka subversion checkout (HEAD)
    :type weka: str
    :param revision: the revision to start from
    :type revision: int
    :param svn: the svn executable, if not found on PATH; None to use default
    :type svn: str
    :param dry_run: whether to perform a dry-run, i.e., simulation
    :type dry_run: bool
    :param verbose: whether to be verbose with the output
    :type verbose: bool
    """

    if svn is None:
        svn = "svn"
    logger.info("svn executable: %s" % svn)

    # update Weka
    logger.info("Updating Weka code base: %s" % weka)
    res = subprocess.run([svn, "update"], cwd=weka, capture_output=True)
    if res.returncode != 0:
        raise IOError("Failed to update Weka code base!\nStdout:\n%s\nStderr:\n%s" % (res.stdout, res.stderr))
    elif verbose:
        output_process_info(res)

    # current revision
    revision_head = -1
    logger.info("Determining revision of HEAD")
    res = subprocess.run([svn, "info"], cwd=weka, capture_output=True)
    if res.returncode != 0:
        raise IOError("Failed to run svn info!\nStdout:\n%s\nStderr:\n%s" % (res.stdout, res.stderr))
    elif verbose:
        lines = res.stdout.decode("UTF-8").split("\n")
        for line in lines:
            if "Revision:" in line:
                parts = line.split(":")
                if len(parts) == 2:
                    revision_head = int(parts[1].strip())

    # generate log
    logger.info("SVN log since: %i" % revision)
    res = subprocess.run([svn, "log", "-r", "%i:HEAD" % revision, "-v"], cwd=weka, capture_output=True)
    if res.returncode != 0:
        raise IOError("Failed to generate svn log!\nStdout:\n%s\nStderr:\n%s" % (res.stdout, res.stderr))
    elif verbose:
        output_process_info(res)

    # process log
    log = res.stdout.decode("UTF-8")
    entries = log.split("------------------------------------------------------------------------")
    num_files = 0
    for entry in entries:
        if "Changed paths:" in entry:
            parts = entry.split("Changed paths:")
            if len(parts) == 2:
                lines = parts[1].strip().split("\n")
                paths = []
                for line in lines:
                    if (len(line.strip()) > 0) and (SVN_PREFIX + "/src" in line):
                        paths.append(line[line.find("/"):])
                # process paths
                if len(paths) > 0:
                    num_files += process_paths(weka, paths, dry_run, verbose)

    logger.info("Number of files that needed updating: %s" % num_files)

    if not dry_run:
        update_pom(revision_head)
        update_readme(revision_head)
        rev_filename = "./update.rev"
        logger.info("Storing revision information in: %s" % rev_filename)
        with open(rev_filename, "w") as ref_file:
            ref_file.write("%i:%i" % (revision, revision_head))


def main(args=None):
    """
    Runs the update. Use -h to see all options.

    :param args: the command-line arguments to use, uses sys.argv if None
    :type args: list
    """

    parser = argparse.ArgumentParser(
        description='Analyzes the svn log from the specified revision on and then updates the code accordingly.\n'
                    + "It stores the start/end svn revision in 'update.rev' after execution.")
    parser.add_argument("-w, --weka", metavar="DIR", dest="weka", required=True, help="the directory with the Weka subversion repository (HEAD)")
    parser.add_argument("-r, --revision", metavar="REV", dest="revision", type=int, required=True, help="the svn revision to start from")
    parser.add_argument("-s, --svn", metavar="EXECUTABLE", dest="svn", help="the svn executable to use if not on the path")
    parser.add_argument("-n, --dry_run", action="store_true", dest="dry_run", help="whether to perform a dry run, i.e., only simulating the update")
    parser.add_argument("-v, --verbose", action="store_true", dest="verbose", help="whether to be verbose with the output")
    parsed = parser.parse_args(args=args)

    logging.basicConfig()
    logger.setLevel(logging.DEBUG)

    update(parsed.weka, parsed.revision, svn=parsed.svn, dry_run=parsed.dry_run, verbose=parsed.verbose)


def sys_main():
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    :rtype: int
    """

    try:
        main()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(traceback.format_exc())


