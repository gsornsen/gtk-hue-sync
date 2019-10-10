# gtk-hue-sync

CONFIG_DIR=${HOME}/.config/gtk-hue-sync
INSTALL_DIR=/usr/bin
BUILD_DIR=dist
DEB_BUILD_DIR=${BUILD_DIR}/.debian
# BUILD_NUMBER can be overridden by passing in a build number
# 		$ make deb BUILD_NUMBER=1.2.3
BUILD_NUMBER=0.0.1
GIT_HASH=$(shell git rev-parse --short HEAD)
# Assets to include in Debian file
ASSETS=${BUILD_DIR}/gtk-hue-sync ${BUILD_DIR}/config.yaml

# Meta data for DEBIAN/control
PACKAGE_NAME=gtk-hue-sync
# PACKAGE_NAME can be overriden by passing in a name
#		$ make deb BUILD_NUMBER=1.2.3 PACKAGE_NAME=gtk-hue-sync-dev
VERSION=${BUILD_NUMBER}
ARCHITECTURE=amd64
MAINTAINER=gerald@sornsen.io
PRIORITY=optional
DESCRIPTION=Set Hue lights to dominant color on primary display

make:
	pyinstaller -F src/gtk-hue-sync.py -p src/ --workpath /tmp --specpath /tmp
	cp -rv config.yaml  dist

.PHONY: deb
deb: make prerm postinst control
	@ mkdir -p ${DEB_BUILD_DIR}/usr/bin
	@ cp -rv ${ASSETS} ${DEB_BUILD_DIR}/usr/bin
	@ mv ${DEB_BUILD_DIR}/usr/bin/config.yaml ${DEB_BUILD_DIR}/usr/bin/gtk-hue-sync-config.yaml
	@ dpkg-deb --build ${DEB_BUILD_DIR} ${BUILD_DIR}/${PACKAGE_NAME}-${VERSION}.deb

# Write the control file
.PHONY: control
control:
	@ echo "Package: ${PACKAGE_NAME}\n\
	Architecture: ${ARCHITECTURE}\n\
	Maintainer: ${MAINTAINER}\n\
	Priority: ${PRIORITY}\n\
	Version: ${VERSION}\n\
	Installed-size: `du -s ${DEB_BUILD_DIR} | cut -f1`\n\
	Description: ${DESCRIPTION}\n" > ${DEB_BUILD_DIR}/DEBIAN/control

# Write prerm script
.PHONY: prerm
prerm:
	@ mkdir -p ${DEB_BUILD_DIR}/DEBIAN
	@ printf '#!/bin/bash\n\
	sudo rm -rf $${INSTALL_DIR}/gtk-hue-sync\n\
	sudo rm -rf $${CONFIG_DIR}' > ${DEB_BUILD_DIR}/DEBIAN/prerm
	@ chmod +x ${DEB_BUILD_DIR}/DEBIAN/prerm

# Write postinst script
.PHONY: postinst
postinst:
	@ printf '#!/bin/bash\n\
	mkdir -p $${HOME}/.config/gtk-hue-sync\n\
	sudo mv /usr/bin/gtk-hue-sync-config.yaml $${HOME}/.config/gtk-hue-sync/config.yaml\n\
	sudo chown -R $${SUDO_USER}:$${SUDO_USER} $${HOME}/.config/gtk-hue-sync\n\' > ${DEB_BUILD_DIR}/DEBIAN/postinst
	@ chmod +x ${DEB_BUILD_DIR}/DEBIAN/postinst


# Install build dependencies
.PHONY: apt
apt:
	sudo apt-get update
	sudo apt-get install libgirepository1.0-dev libcairo2-dev pkg-config gir1.2-gtk-3.0 virtualenv build-essential

# Install Travis CI/CD specific apt dependencies
.PHONY: travis-apt
travis-apt:
	# The minimal VM travis spins up needs some X11 dependencies
	sudo apt-get install x11-common x11-utils

# Set up python virtual environment
.PHONY: virtualenv
virtualenv:
	virtualenv -p python3 env

# Install python dependencies in virtual environment
.PHONY: pip
pip:
	env/bin/pip3 install -r requirements.txt

.PHONY: env
env: apt virtualenv pip

.PHONY: travis-env
travis-env: travis-apt env

# Clean up after any recipe
.PHONY: clean
clean:
	rm -rf env
	rm -rf dist
	rm -rf /tmp/*.spec
	rm -rf /tmp/gtk-hue-sync
	rm -rf /tmp/hue-python-rgb-converter
	rm -rf src/__pycache__
	rm -rf src/*.pyc

# Make and install from source
.PHONY: install
install:
	make
	sudo cp -rv dist/gtk-hue-sync ${INSTALL_DIR}
	mkdir -p ${CONFIG_DIR}
	cp -rv config.yaml ${CONFIG_DIR}

# Uninstall source installation
.PHONY: uninstall
uninstall:
	sudo rm -rf ${INSTALL_DIR}/gtk-hue-sync
	rm -rf ${CONFIG_DIR}

# Run tests
.PHONY: test
test:
	pytest src/tests
