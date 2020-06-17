#!/bin/bash

if [ -d $HOME/.local/lib/python*/site-packages ]; then
	for file in $HOME/.local/lib/python*/site-packages; do
		cp bin/configparse.py $file/
	done
else
	for file in /lib/python*; do
		sudo cp bin/configparse.py $file/
	done
fi

mkdir -p ~/.config/reportinator
mkdir -p ~/.config/reportinator/scripts ~/.config/reportinator/layouts
mkdir -p ~/.cache/reportinator
mkdir -p ~/.local/share/reportinator
chmod +x bin/run.py

if [[ $PATH == *"$HOME/.local/bin"* ]]; then
	cp bin/run.py ~/.local/bin/reportinator
else
	sudo cp bin/run.py /usr/bin/reportinator
fi

cp -r share/* ~/.local/share/reportinator/
cp -r config/* ~/.config/reportinator

python setup.py --cache "$HOME/.cache/reportinator" --installed "$HOME/.local/share/reportinator" --source "$PWD"
