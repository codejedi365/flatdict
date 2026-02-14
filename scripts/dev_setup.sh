#!/bin/bash

set -eu -o pipefail

function load_env() {
    set -eu -o pipefail

    if [ "${UTILITIES_SH_LOADED:-false}" = "false" ]; then
        local __FILE__=""
        __FILE__="$(realpath "${BASH_SOURCE[0]}")"

        local __DIR__=""
        __DIR__="$(realpath "$(dirname "$__FILE__")")"

        local ROOT_DIR=""
        ROOT_DIR="$(realpath "$(dirname "$__DIR__")")"

        # shellcheck source=scripts/utils.sh
        source "$ROOT_DIR/scripts/utils.sh"

        load_base_env
    fi

    PIP_EXE="$VENV_DIR/bin/pip"
    BUILD_SCRIPT="$SCRIPTS_DIR/build.sh"
}

function show_base_usage() {
    set -eu
    stdout "Usage: $(basename "$__FILE__") [OPTIONS]"
    stdout ""
    stdout "A command line tool to automate the development environment setup for the project."
    stdout ""
    stdout "Options:"
    stdout "  --build     Run the build script after setting up the development environment"
    stdout "  --clean     Remove the virtual environment before setting up a new one"
    stdout "  --help      Show this help message and exit"
    stdout ""
}

function main() {
    set -eu -o pipefail

    # Defaults
    local CLEAN="false"
    local RUN_BUILD="false"
    export PIP_DISABLE_PIP_VERSION_CHECK="true"

    local -r args=("$@")
    local arg=""

    if [ -n "${args[*]:-}" ]; then
        for arg in "${args[@]}"; do
            case "$arg" in
                --help)
                    show_base_usage
                    return 0
                    ;;
                --clean)
                    CLEAN="true"
                    ;;
                --build)
                    RUN_BUILD="true"
                    ;;
                *)
                    error "Unknown argument: $arg"
                    show_base_usage
                    return 1
                    ;;
            esac
        done
    fi

    cd "$PROJ_ROOT_DIR" || exit 1

    if [ "$CLEAN" = "true" ]; then
        rm -rf "${VENV_DIR:?}"
    fi

    local VENV_EXISTS="false"
    if [ -f "$VENV_DIR/pyvenv.cfg" ]; then
        VENV_EXISTS="true"
    fi

    if [ "$VENV_EXISTS" = "false" ]; then
        python3_exe=""
        if is_command asdf; then
            info "Finding the python3 executable from asdf..."
            if ! python3_exe="$(realpath "$(asdf which python)")"; then
                warning "Unable to determine python version from asdf"
            else
                info "asdf python3 executable: $python3_exe"
            fi
        fi

        if [ -z "$python3_exe" ]; then
            info "Finding the system python3 executable from PATH..."
            if ! python3_exe="$(realpath "$(which python3)")"; then
                error "Unable to find python3 executable on system!"
                return 1
            fi
            info "Found python3 executable: $python3_exe"
        fi

        verify_python_version "$python3_exe" "$MINIMUM_PYTHON_VERSION"

        explicit_run_cmd_w_status_wrapper \
            "Creating virtual environment for project" \
            "$python3_exe" -m venv "$VENV_DIR"
    fi

    if ! [ -f "$PIP_EXE" ]; then
        error "Unable to find pip executable at '$PIP_EXE'."
        return 1
    fi

    explicit_run_cmd_w_status_wrapper \
        "Updating virtual environment default build tools" \
        "$PIP_EXE" install --upgrade pip setuptools wheel

    local pip_args=("-e" ".[build,dev,docs,test]")

    explicit_run_cmd_w_status_wrapper \
        "Installing editable project and development dependencies" \
        "$PIP_EXE" install "${pip_args[@]}";

    if [ "$VENV_EXISTS" = "false" ]; then
        local localized_venv_path="${VENV_DIR/$PROJ_ROOT_DIR/<proj_dir>}"
        stdout "######################################################################"
        stdout "#                                                                    #"
        stdout "#  Virtual environment created successfully! Activate it with:       #"
        stdout "#                                                                    #"
        stdout "#      source $localized_venv_path/bin/activate                          #"
        stdout "#                                                                    #"
        stdout "#  Then you can import the package with:                             #"
        stdout "#                                                                    #"
        stdout "#      from cj365.flatdict import FlatDict, FlatterDict              #"
        stdout "#                                                                    #"
        stdout "######################################################################"
    fi

    if [ "$RUN_BUILD" = "true" ]; then
        export PATH="$VENV_DIR/bin:$PATH"
        explicit_run_cmd_w_status_wrapper \
            "Building project" \
            bash "$BUILD_SCRIPT"
    fi

    info "Project Development Setup...DONE"
}

########################################################################
# CONDITIONAL AUTO-EXECUTE                                             #
########################################################################

if ! (return 0 2>/dev/null); then
    # Since this script is not being sourced, run the main function
    unset -v UTILITIES_SH_LOADED  # Ensure utils are reloaded when called from another script
    load_env
    main "$@"
fi
