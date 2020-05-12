cat list.txt |  while read output
do
    ping -c 2 "$output" > /dev/null
    if [ $? -eq 0 ]; then
    echo  "$output is up"
    else
    echo "$output is down"
    fi
done
