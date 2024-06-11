#
#  Copyright (C) 2021 Protein Metrics Inc. - All Rights Reserved.
#  Unauthorized copying or distribution of this file, via any medium is strictly prohibited.
#  Confidential.
#
#  Author: Walid Boussafa (boussaffa.walid@outlook.com)
#

import os
import yaml
import datetime
import shutil
import textwrap
from conans import tools
import subprocess

#####################
#  HELPER FUNCTIONS #
#####################


def folder_size(folder):
    try:
        byteOutput = subprocess.check_output(f"du -sh {folder}", shell=True)
        return byteOutput.decode("UTF-8").rstrip()
    except subprocess.CalledProcessError as e:
        print(f"Error: failed to run `du -sh {folder}`:\n", e.output)
        return None


def _is_ci_build():
    return tools.get_env("PMI_CI_BUILD", False)


def _is_current_recipe(conanfile):
    return tools.get_env("CONAN_PACKAGE_NAME") == conanfile.name


def _save_conan_dirs(conanfile):
    if not _is_current_recipe(conanfile):
        return

    if "test_package" in str(conanfile.source_folder):
        # we dont want to save test_package build folder in _conan_build_dirs.txt
        return

    # save conan build dirs to be able to report test results in jenkins with xunit plugin
    WORKSPACE = tools.get_env("WORKSPACE")
    assert WORKSPACE, "WORKSPACE is not defined"
    with open(os.path.join(WORKSPACE, "build", "_conan_build_dirs.txt"), "a") as f:
        f.write(str(conanfile.build_folder) + "\n")

    with open(os.path.join(WORKSPACE, "build", "_conan_source_dirs.txt"), "a") as f:
        f.write(str(conanfile.source_folder) + "\n")

    with open(
        os.path.join(WORKSPACE, "build", "_conan_package_dirs.txt"), "a"
    ) as f:
        f.write(str(conanfile.package_folder) + "\n")


# fix bad yaml indentation
# https://stackoverflow.com/questions/25108581/python-yaml-dump-bad-indentation
class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


#
# generate pmi_package_info.yaml in package folder
#
def _pmi_generate_package_info(output, conanfile):
    _package_info = dict()

    # create pmi_package_info.yaml
    _package_info["name"] = str(conanfile.name)
    _package_info["version"] = str(conanfile.version)
    _package_info["creation_date"] = datetime.datetime.utcnow().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    _ci_info = _get_ci_info()
    for i in _ci_info.keys():
        _package_info[i] = _ci_info[i]

    if hasattr(conanfile, "cpp_build_duration"):
        _package_info["cpp_build_duration"] = conanfile.cpp_build_duration
    if hasattr(conanfile, "autotest_duration"):
        _package_info["autotest_duration"] = conanfile.autotest_duration
    _package_info["settings"] = dict()
    _package_info["options"] = dict()

    for setting in conanfile.settings.items():
        _package_info["settings"][setting[0]] = setting[1]

    for option in conanfile.options.items():
        _package_info["options"][option[0]] = option[1]

    return _package_info


def _get_ci_info():
    _ci_info = dict()
    _ci_info["full_package_name"] = tools.get_env("CONAN_FULL_PACKAGE_NAME")
    _ci_info["branch_name"] = tools.get_env("BRANCH_NAME")
    _ci_info["git_commit"] = tools.get_env("GIT_COMMIT")
    _ci_info["git_triggering_commit"] = tools.get_env("GIT_TRIGGERING_COMMIT")
    _ci_info["build_number"] = tools.get_env("BUILD_NUMBER")
    _ci_info["build_url"] = tools.get_env("BUILD_URL")
    _ci_info["job_name"] = tools.get_env("JOB_NAME")
    _ci_info["artifacts_url"] = _ci_info["build_url"] + "artifact"
    _ci_info["artifacts_url_s3"] = (
        f's3://pmi-jenkins/artifacts/{_ci_info["job_name"]}/{_ci_info["build_number"]}/artifacts/'
    )

    return _ci_info


def _save_package_info(output, conanfile):
    _package_info = _pmi_generate_package_info(output, conanfile)

    changelog_dir = os.path.join(conanfile.package_folder, "changelog")
    tools.mkdir(changelog_dir)

    package_info_file = os.path.join(changelog_dir, "pmi_package_info.yaml")
    with open(package_info_file, "w") as outfile:
        yaml.dump(
            _package_info,
            outfile,
            Dumper=MyDumper,
            default_flow_style=False,
            sort_keys=False,
        )

    # include conan build log
    conan_run_log = os.path.join(conanfile.build_folder, "conan_run.log")
    if os.path.isfile(conan_run_log):
        shutil.copy(conan_run_log, changelog_dir)


#
# generate git changelog for current package and collect changelogs from all deps
#
def _pmi_generate_changelog(output, conanfile):
    changelog_dir = os.path.join(conanfile.package_folder, "changelog")
    tools.mkdir(changelog_dir)
    #
    # Generate git changelog for current package
    #
    if os.path.isdir(os.path.join(conanfile.source_folder, ".git")):
        output.info(
            f"Generating git changelog for conan package {conanfile.ref.name}"
        )
        git = tools.Git(folder=conanfile.source_folder)
        git_log = git.run('log --pretty=format:"%cd - %h - %s" --since=4.weeks')
        tools.save(os.path.join(changelog_dir, "changelog.txt"), git_log)
    else:
        output.warn("This is not a git repo! skip changelog generation")

    #
    # collect changelog from deps
    #
    for require, dependency in conanfile.dependencies.items():
        if not require.build and not require.test:
            deps_changelog_dir = os.path.join(
                dependency.package_folder, "changelog"
            )
            if os.path.isdir(deps_changelog_dir):
                output.info(
                    f"Collecting changelog from conan package {dependency.ref.name}"
                )
                changelog_dst = os.path.join(changelog_dir, dependency.ref.name)
                os.makedirs(changelog_dst, exist_ok=True)
                files = ["changelog.txt", "pmi_package_info.yaml"]
                for f in files:
                    if os.path.exists(os.path.join(deps_changelog_dir, f)):
                        shutil.copy(
                            os.path.join(deps_changelog_dir, f), changelog_dst
                        )


#
# generate pmi license file
#
def _pmi_generate_license(output, conanfile):
    licenses_folder = os.path.join(conanfile.package_folder, "licenses")
    tools.mkdir(licenses_folder)

    license_txt = textwrap.dedent(
        """\
         * Copyright (C) 2012-2023 Protein Metrics, LLC. - All Rights Reserved.
         * Unauthorized copying or distribution of this file, via any medium is strictly prohibited.
         * Confidential.
    """
    )

    output.info(f"Generating PMI license file in {licenses_folder}")
    tools.save(os.path.join(licenses_folder, "LICENSE"), license_txt)


#####################
#   CONAN HOOKS     #
#####################


def pre_build(output, conanfile, **kwargs):
    assert conanfile, "conanfile is not defined in pre_build"
    if not _is_ci_build():
        output.warn("This is not a CI build! skip _save_conan_build_dirs!")
        return
    else:
        output.warn("This is a CI build! _save_conan_build_dirs!")
        _save_conan_dirs(conanfile)


def post_build(output, conanfile, **kwargs):
    assert conanfile
    if not _is_ci_build():
        return

    # output.info(f"Build folder size: {folder_size(conanfile.build_folder)}")


def post_package(output, conanfile, conanfile_path, **kwargs):
    assert conanfile, "conanfile is not defined in post_package"
    if not _is_ci_build():
        output.warn(
            "This is not a CI build! skip _save_package_info and _pmi_generate_changelog!"
        )
        return

    # output.info(f"Package folder size: {folder_size(conanfile.package_folder)}")

    _save_package_info(output, conanfile)
    _pmi_generate_changelog(output, conanfile)
    _pmi_generate_license(output, conanfile)


def pre_upload_recipe(output, conanfile_path, reference, remote, **kwargs):
    if not _is_ci_build() or not reference:
        return

    if "pmi_pyreq" in tools.get_env("CONAN_PACKAGE_NAME"):
        return

    if tools.get_env("CONAN_PACKAGE_NAME") not in reference.full_str():
        return

    _ci_info_file = os.path.join(
        os.path.dirname(conanfile_path), "pmi_ci_info.yaml"
    )
    if os.path.exists(_ci_info_file):
        return

    _ci_info = _get_ci_info()
    with open(_ci_info_file, "w", newline="\n") as outfile:
        output.info(f"Saving ci info to {_ci_info_file}")
        yaml.dump(
            _ci_info,
            outfile,
            Dumper=MyDumper,
            default_flow_style=False,
            sort_keys=False,
        )
