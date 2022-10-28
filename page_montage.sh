#!/bin/bash

function _4m3_2m2()
{
    local mname="4m3_2m2"
    echo "montage $mname"
    command montage m3* -tile 2x -geometry +1+1 .ia.bmp
    command montage m2* -tile 2x -geometry +2+2 .ib.bmp
    command montage .i* -tile 1x -geometry +0+0 $1.bmp
}

function _2m3_4m2()
{
    local mname="2m3_4m2"
    echo "montage $mname"
    command montage m2* -tile 4x -geometry +4+4 .ia.bmp
    command montage m3* -tile 2x -geometry +2+2 .ib.bmp
    command montage .i* -tile 1x -geometry +0+0 $1.bmp
}

function _2m4()
{
    local mname="2m4"
    echo "montage $mname"
    command montage m4* -tile 1x -geometry +4+4 $1.bmp
}

function _1m6_2m2()
{
    local mname="1m6_2m2"
    echo "montage $mname"
    command montage m2* -tile 2x -geometry +4+4 .ia.bmp
    command montage m6* .i* -tile 1x -geometry +0+0 $1.bmp
}

function _m2()
{
    local mname="m2"
    echo "montage $mname"
    command montage m2* -tile 2x -geometry +4+4 $1.bmp
}

m6c=$(ls -ql m6* 2> /dev/null|wc -l)
m4c=$(ls -ql m4* 2> /dev/null|wc -l)
m3c=$(ls -ql m3* 2> /dev/null|wc -l)
m2c=$(ls -ql m2* 2> /dev/null|wc -l)
cmds=""
if ((m6c > 0))
then
    cmds="${cmds}_${m6c}m6"
fi
if ((m4c > 0))
then
    cmds="${cmds}_${m4c}m4"
fi
if ((m3c > 0))
then
    cmds="${cmds}_${m3c}m3"
fi
if ((m2c > 0))
then
    if ((m6c + m4c + m3c == 0))
    then
        cmds="_m2"
    else
        cmds="${cmds}_${m2c}m2"
    fi
fi

if (($# > 0))
then
    page_name="$1"
else
    page_name="p$cmds"
fi

command $cmds "$page_name"

exit 0
