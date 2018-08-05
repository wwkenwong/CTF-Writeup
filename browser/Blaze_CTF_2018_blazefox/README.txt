This is a standard build of firefox nightly pulled on 4/6.

How it was built:
    Following https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Build_Instructions/Simple_Firefox_build/Linux_and_MacOS_build_preparation

    python bootstrap.py
    hg clone https://hg.mozilla.org/mozilla-central
    hg checkout ee6283795f41
    hg import blaze.patch --no-commit
    ./mach build

The larger download contains the built firefox and the docker env.

We run it in the docker container with
    /firefox/dist/bin/firefox --headless <url>
The container has a profile to disable sandboxing, you're welcome

The flag is in /flag in the container.

