# gtk-hue-sync

CONFIG_DIR=${HOME}/.config/gtk-hue-sync
INSTALL_DIR=/usr/bin

make:
	pyinstaller -F src/gtk-hue-sync.py -p src/ --workpath /tmp --specpath /tmp

.PHONY: apt
apt:
	sudo apt-get update
	sudo apt-get install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 git virtualenv

.PHONY: travis-apt
travis-apt:
	sudo apt-get update
	sudo apt install virtualenv gcc

.PHONY: virtualenv
virtualenv:
	virtualenv -p python3.7 env

.PHONY: pip
pip:
	env/bin/pip3.7 install -r requirements.txt

.PHONY: env
env: apt virtualenv pip

.PHONY: travis-env
travis-env: travis-apt virtualenv pip

.PHONY: clean
clean:
	rm -rf env
	rm -rf dist
	rm -rf /tmp/*.spec
	rm -rf /tmp/gtk-hue-sync
	rm -rf /tmp/hue-python-rgb-converter
	rm -rf src/__pycache__
	rm -rf src/*.pyc

.PHONY: install
install:
	make
	sudo cp -rv dist/gtk-hue-sync ${INSTALL_DIR}
	mkdir -p ${CONFIG_DIR}
	cp -rv config.yaml ${CONFIG_DIR}

.PHONY: uninstall
uninstall:
	sudo rm -rf ${INSTALL_DIR}/gtk-hue-sync
	rm -rf ${CONFIG_DIR}



