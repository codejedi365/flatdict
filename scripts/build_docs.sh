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
    SPHINX_BUILD_EXE="$VENV_DIR/bin/sphinx-build"
    DIST_DOCS_DIR="$DIST_DIR/docs/html"

    if [ "${CI:-false}" = "true" ]; then
        SPHINX_BUILD_EXE="$(basename "$SPHINX_BUILD_EXE")"
    fi
}

function main() {
    set -eu -o pipefail

    cd "$PROJ_ROOT_DIR"

    if ! explicit_run_cmd_w_status_wrapper \
        "Verifying Python environment" \
        verify_python "$MINIMUM_PYTHON_VERSION";
    then
        info "Please run the dev setup script and activate the virtual environment first."
        return 1
    fi

    explicit_run_cmd_w_status_wrapper \
        "Verifying build dependencies exist" \
        python3 -m pip install -e ".[docs]" ">/dev/null"

    if [ ! -f "$SPHINX_BUILD_EXE" ] && ! is_command "$(basename "$SPHINX_BUILD_EXE")"; then
        printf '%s\n' "$(basename "$SPHINX_BUILD_EXE") was not found in environment!"
        return 1
    fi

    rm -rf docs/_build/html "$DIST_DOCS_DIR"

    explicit_run_cmd_w_status_wrapper \
        "Building documentation" \
        "$SPHINX_BUILD_EXE" docs/source "$DIST_DOCS_DIR"

    if [ -n "${GITHUB_OUTPUT:-}" ]; then
        printf "DIST_DOCS_DIR=%s\n" "$DIST_DOCS_DIR" >> "$GITHUB_OUTPUT"
    fi
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
