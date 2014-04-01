show:
	echo 'Run "make install" as root to install program!'
	
run:
	python reboot-required.py
install:
	sudo apt-get install transmission-gtk --assume-yes
	sudo cp reboot-required.py /usr/bin/reboot-required
	sudo chmod +x /usr/bin/reboot-required
	sudo link /usr/bin/reboot-required /etc/cron.daily/reboot-required
uninstall:
	sudo rm /usr/bin/reboot-required
	sudo rm /etc/cron.daily/reboot-required
installed-size:
	du -sx --exclude DEBIAN ./debian/
build:
	sudo make build-deb
build-deb:
	mkdir -p debian;
	mkdir -p debian/DEBIAN;
	mkdir -p debian/usr;
	mkdir -p debian/usr/bin;
	# make post and pre install scripts have the correct permissions
	chmod 775 debdata/*
	# copy over the binary
	cp -vf reboot-required.py ./debian/usr/bin/reboot-required
	# make the program executable
	chmod +x ./debian/usr/bin/reboot-required
	# start the md5sums file
	md5sum ./debian/usr/bin/reboot-required > ./debian/DEBIAN/md5sums
	# create md5 sums for all the config files transfered over
	sed -i.bak 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	rm -v ./debian/DEBIAN/md5sums.bak
	cp -rv debdata/. debian/DEBIAN/
	dpkg-deb --build debian
	cp -v debian.deb reboot-required_UNSTABLE.deb
	rm -v debian.deb
	rm -rv debian
