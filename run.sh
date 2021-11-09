
curPath=$(readlink -f "$(dirname "$0")")
cd $curPath
echo $curPath
nohup python ./ldrTranslate.py &