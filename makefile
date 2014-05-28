show:
	echo 'Run "make install" as root to install program!'
	
run:
	python reboot-required.py
install: build
	sudo gdebi --non-interactive reboot-required_UNSTABLE.deb
uninstall:
	sudo apt-get purge reboot-required
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
	# Create the md5sums file
	find ./debian/ -type f -print0 | xargs -0 md5sum > ./debian/DEBIAN/md5sums
	# cut filenames of extra junk
	sed -i.bak 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	sed -i.bak 's/\\n*DEBIAN*\\n//g' ./debian/DEBIAN/md5sums
	sed -i.bak 's/\\n*DEBIAN*//g' ./debian/DEBIAN/md5sums
	rm -v ./debian/DEBIAN/md5sums.bak
	# figure out the package size	
	du -sx --exclude DEBIAN ./debian/ > Installed-Size.txt
	cp -rv debdata/. debian/DEBIAN/
	# build the package
	dpkg-deb --build debian
	cp -v debian.deb reboot-required_UNSTABLE.deb
	rm -v debian.deb
	rm -rv debian
