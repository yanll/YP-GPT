
#sudo rm -rf ../.cache ../.dbgpts
kill -9 `ps aux | grep 'dbgpt/app/dbgpt_server.py' | grep -v 'grep' | awk -F ' ' '{print $2}'`
nohup python dbgpt/app/dbgpt_server.py > ../tmp/log.log &
