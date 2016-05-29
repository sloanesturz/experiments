for i in {0..2}
do
    cd $(mktemp -d);
    twistd -n web -p $((8000 + i)) --path=${HOME}/experiments/dash-data 2>&1 > /dev/null &
done

echo "Server's running!"
