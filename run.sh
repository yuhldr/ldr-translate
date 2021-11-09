
curPath=$(readlink -f "$(dirname "$0")")
cd $curPath
nohup python ./ldrTranslate.py &