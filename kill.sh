#/bin/bash

ps -ef | grep runtaskserver.py | grep -v 'grep' | awk '{print $2}' | xargs kill -9
