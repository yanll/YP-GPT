
#sudo rm -rf ../.cache ../.dbgpts

#conda activate dbgpt_env
kill -9 `ps aux | grep 'dbgpt/app/dbgpt_server.py' | grep -v 'grep' | awk -F ' ' '{print $2}'`
sudo rm -rf ../tmp/log.log
nohup python dbgpt/app/dbgpt_server.py --port 5670 > ../tmp/log.log &
