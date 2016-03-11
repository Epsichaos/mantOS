#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/pi/manta_ws/src/diagnostics/diagnostic_analysis"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/pi/manta_ws/install_isolated/lib/python2.7/dist-packages:/home/pi/manta_ws/build_isolated/diagnostic_analysis/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/pi/manta_ws/build_isolated/diagnostic_analysis" \
    "/usr/bin/python" \
    "/home/pi/manta_ws/src/diagnostics/diagnostic_analysis/setup.py" \
    build --build-base "/home/pi/manta_ws/build_isolated/diagnostic_analysis" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/pi/manta_ws/install_isolated" --install-scripts="/home/pi/manta_ws/install_isolated/bin"
