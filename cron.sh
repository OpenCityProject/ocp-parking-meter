
if ps aux | grep python > /dev/null
then
    echo "Running"
else
    echo "Stopped"
	echo -e '\xFE\x46' > /dev/ttyUSB0
fi