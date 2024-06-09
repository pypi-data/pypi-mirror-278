#! /usr/bin/env bash

function CV_clean() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        abcli_show_usage "CV clean" \
            "clean CV."
        return
    fi

    pushd $abcli_path_git/CV/src >/dev/null
    rm *.aux
    rm *.dvi
    rm *.log
    rm *.out
    rm *.ps
    popd >/dev/null
    return

}
