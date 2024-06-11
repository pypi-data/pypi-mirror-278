"""
conan_project commands for pmi cli.
"""

import typer
from rich import print
from rich.console import Console
from typing import Optional, List
from typing_extensions import Annotated

import sys
import os
import subprocess
import platform
from pathlib import Path

from pmicli.constants import ProjectType, BuildType, Arch, CompilerVersion
from pmicli.utils import run_cmd, print_options_table

console = Console()


def conan_install(
    source_folder, build_folder, build_type, arch, conan_install_args
):
    cmd = f'conan install "{source_folder}" --install-folder "{build_folder}" --output-folder "{build_folder}" -s build_type={build_type} -s arch={arch} '
    if conan_install_args:
        cmd += " ".join(conan_install_args)

    run_cmd(cmd, cwd=source_folder)


def conan_configure(source_folder, build_folder):
    cmd = (
        f'conan build "{source_folder}" --build-folder "{build_folder}" --configure'
    )
    run_cmd(cmd)


def generate_ide_start_script(source_folder, build_folder):
    if os.getenv("QT_CREATOR"):
        idepath = os.getenv("QT_CREATOR")
        script_path = os.path.join(build_folder, "start_qtcreator.cmd")
    elif os.getenv("CLION_BIN"):
        idepath = os.getenv("CLION_BIN")
        script_path = os.path.join(build_folder, "start_clion.cmd")

    if script_path and idepath:
        console.print(f"Added ide startup script to {script_path}", style="yellow")
        start_ide_script = (
            "@echo off\n\n"
            ":: This script was auto-generated using pmicli conan-project"
            "\n\n"
            "call conan\\conanrun.bat\n\n"
            f'start "" "{idepath}" "{source_folder}"'
        )

        with open(script_path, "w") as out:
            out.write(start_ide_script)


def start_ide(build_folder, project_type):
    os.chdir(build_folder)
    if project_type == ProjectType.vs:
        vs_solution = glob.glob("*.sln")[0]
        os.system(f"start {vs_solution}")
    elif os.getenv("QT_CREATOR"):
        os.system("call start_qtcreator.cmd")
    elif os.getenv("CLION_BIN"):
        os.system("call start_clion.cmd")


app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command("conan-project")
def conan_project(
    project_type: Annotated[
        ProjectType, typer.Argument(help="Which project to configure")
    ],
    source_folder: Annotated[
        Path,
        typer.Argument(
            help="Project source folder",
            exists=True,
            resolve_path=True,
            dir_okay=True,
            file_okay=False,
        ),
    ],
    build_folder: Annotated[
        Path,
        typer.Argument(
            help="Project build folder",
            resolve_path=True,
            dir_okay=True,
            file_okay=False,
        ),
    ],
    build_type: Annotated[
        List[BuildType],
        typer.Option(
            "--build-type",
            "-bt",
            help="Build type(s) to build for",
            rich_help_panel="build options",
        ),
    ] = [list(BuildType)[0]],
    arch: Annotated[
        Arch,
        typer.Option(
            help="Architecture to build for",
            rich_help_panel="build options",
        ),
    ] = list(Arch)[0],
    compiler_version: Annotated[
        CompilerVersion,
        typer.Option(
            "--compiler-version",
            "-cv",
            help="Compiler version",
            rich_help_panel="build options",
        ),
    ] = list(CompilerVersion)[0],
    update: Annotated[
        bool,
        typer.Option(
            "--update",
            "-u",
            help="Check remote server for package update even if they exist in local cache",
            rich_help_panel="Conan options",
        ),
    ] = False,
    open_ide: Annotated[
        bool,
        typer.Option(
            "--open",
            "-o",
            help="Open the generated project after configuration",
        ),
    ] = False,
    cmake_definitions: Annotated[
        str,
        typer.Option(
            "--cmake-definitions",
            "-d",
            help="Pass extra cmake definitions to cmake configure",
            rich_help_panel="build options",
        ),
    ] = "",
    profile: Annotated[
        str,
        typer.Option(
            "--profile",
            "-p",
            help="Use a custom conan build profile",
            rich_help_panel="Conan options",
        ),
    ] = None,
    build_missing: Annotated[
        bool,
        typer.Option(
            help="build all missing dependencies (specifically useful when using --require-override)",
            rich_help_panel="Conan options",
        ),
    ] = False,
    require_override: Annotated[
        List[str],
        typer.Option(
            help="Override one or multiple dependencies version to override",
            rich_help_panel="Conan options",
        ),
    ] = [],
    require_override_file: Annotated[
        Optional[typer.FileText],
        typer.Option(
            help="Same as --require-override option but accept a file as input",
            rich_help_panel="Conan options",
        ),
    ] = None,
    ctx: typer.Context = typer.Option(None, hidden=True),
):

    print_options_table(ctx)

    # convert rd, r, d to RelWithDebInfo, Release, Debug
    for index, item in enumerate(build_type):
        if build_type[index] == BuildType.rd:
            build_type[index] = BuildType.releasewithdebinfo
        if build_type[index] == BuildType.r:
            build_type[index] = BuildType.release
        if build_type[index] == BuildType.d:
            build_type[index] = BuildType.debug

    conan_install_args = []

    if platform.system() == "Windows" and project_type == ProjectType.vs:
        conan_install_args.append(
            "-e CMAKE_CONFIGURATION_TYPES={}".format(";".join(build_type))
        )
        os.environ["CC"] = "cl.exe"
        os.environ["CXX"] = "cl.exe"

    if update:
        conan_install_args.append("--update")

    if build_missing:
        conan_install_args.append("--build missing")

    if require_override_file:
        for line in require_override_file:
            if line.strip():
                require_override.append(line.strip())

    if require_override:
        for o in require_override:
            conan_install_args.append(f"--require-override {o}")

        # workaround needed by pmi_deploy_package until we find a better apparoch
        os.environ["CONAN_REQUIRE_OVERRIDES"] = ",".join(require_override)

    if not os.path.exists(build_folder):
        os.makedirs(build_folder)
    else:
        console.print(
            f"Updating existing build folder: {build_folder}", style="yellow"
        )

    if project_type == ProjectType.make or project_type == ProjectType.ninja:
        if len(build_type) > 1:
            console.print(
                f"Error: You cannot sepecify multiple build types for {project_type} projects",
                style="red",
            )
            raise typer.Exit(code=1)

    if not profile:
        if platform.system() == "Windows":
            if compiler_version == CompilerVersion.vs_16:
                profile = "vs2019"
            if compiler_version == CompilerVersion.vs_17:
                profile = "vs2022"
        else:
            profile = f"gcc{compiler_version.value}"

        if project_type == ProjectType.ninja:
            profile += "-ninja"

    if profile:
        if platform.system() == "Linux":
            # workaround: build and host profiles does not work correctly for linux builds
            # package id are not computed correctly on Linux when using host and build profiles
            conan_install_args.append(f"--profile {profile}")
        else:
            conan_install_args.append(
                f"--profile:host {profile} --profile:build {profile}"
            )

    if cmake_definitions:
        os.environ["PMI_EXTRA_CMAKE_DEFINITIONS"] = cmake_definitions

    # delete old conanfile.hash as we will run conan install anyway
    # conanfile.hash and conandata.hash are used by pmi_cmake_modules to check if build folder is outdated
    conanfile_hash = os.path.join(build_folder, "conanfile.hash")
    conandata_hash = os.path.join(build_folder, "conandata.hash")
    if os.path.exists(conanfile_hash):
        os.remove(conanfile_hash)
    if os.path.exists(conandata_hash):
        os.remove(conandata_hash)

    # install conan dependencies
    for _build_type in build_type:
        conan_install(
            source_folder,
            build_folder,
            _build_type.value,
            arch.value,
            conan_install_args,
        )

    # configure project
    conan_configure(source_folder, build_folder)

    if platform.system() == "Windows":
        if args.project == ProjectType.make or args.project == ProjectType.ninja:
            generate_ide_start_script(source_folder, build_folder)

        if open_ide:
            start_ide(build_folder, project_type)


if __name__ == "__main__":
    app()
