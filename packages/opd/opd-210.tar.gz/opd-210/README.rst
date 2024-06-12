NAME

::

    OPD - Original Programmer Daemon

SYNOPSIS

::

    opdctl <cmd> [key=val] [key==val]
    opdctl [-a] [-c] [-v]
    opd

DESCRIPTION

::

    OPD is a python3 library implementing the 'opd' package. It
    provides all the tools to program a bot, such as disk perisistence
    for configuration files, event handler to handle the client/server
    connection, code to introspect modules for commands, deferred
    exception handling to not crash on an error, a parser to parse
    commandline options and values, etc.

    OPD provides a demo bot, it can connect to IRC, fetch and
    display RSS feeds, take todo notes, keep a shopping list
    and log text. You can also copy/paste the service file and run
    it under systemd for 24/7 presence in a IRC channel.

    OPD is Public Domain.

INSTALL

::

    $ pipx install opd
    $ pipx ensurepath

USAGE

::

    without any argument the program starts itself as a daemon

    $ opd
    $

    use opdctl to configure the daemon

    $ opdctl cmd
    cmd,err,mod,req,thr,ver
    $

    the -c option starts a console

    $ opdctl -c
    >

    the -v option turns on verbose    

    $ opdctl -cv
    OPD CV started Sat Feb 10 13:50:56 2024
    > 

    use mod= to load additional modules

    $ opdctl mod=irc,rss
    $

    the ``mod`` command shows a list of modules

    $ opdctl mod
    cmd,err,irc,log,mod,rss,tdo,thr
    $

    the -a option will load all available modules

CONFIGURATION

::

    irc

    $ opdctl cfg server=<server>
    $ opdctl cfg channel=<channel>
    $ opdctl cfg nick=<nick>

    sasl

    $ opdctl pwd <nsvnick> <nspass>
    $ opdctl cfg password=<frompwd>

    rss

    $ opdctl rss <url>
    $ opdctl dpl <url> <item1,item2>
    $ opdctl rem <url>
    $ opdctl nme <url> <name>

COMMANDS

::

    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    log - log some text
    met - add a user
    mre - displays cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    rss - add a feed
    thr - show the running threads

SYSTEMD

::

    save the following in /etc/systemd/system/opd.service and
    replace "<user>" with the user running pipx

    [Unit]
    Description=Original Programmer Daemon
    Requires=network.target
    After=network.target

    [Service]
    Type=simple
    User=<user>
    Group=<user>
    WorkingDirectory=/home/<user>/.opd
    ExecStart=/home/<user>/.local/pipx/venvs/opd/bin/opd
    RemainAfterExit=yes

    [Install]
    WantedBy=default.target

    then run this

    $ mkdir ~/.opd
    $ sudo systemctl enable opd --now

    default channel/server is #opd on localhost

FILES

::

    ~/.opd
    ~/.local/bin/opd
    ~/.local/bin/opdctl
    ~/.local/pipx/venvs/opd/*

AUTHOR

::

    Bart Thate <bthate@dds.nl>

COPYRIGHT

::

    OPD is Public Domain.
