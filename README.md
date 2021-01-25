########################################
# build
########################################
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/33/Everything/SRPMS/Packages/l/libepoxy-1.5.5-1.fc33.src.rpm

rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/33/Everything/SRPMS/Packages/l/liburing-0.7-3.fc33.src.rpm

rpm -i https://download-ib01.fedoraproject.org/pub/epel/8/Everything/SRPMS/Packages/c/capstone-4.0.1-9.el8.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/epel/8/Everything/SRPMS/Packages/l/libnfs-4.0.0-1.el8.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/epel/8/Everything/SRPMS/Packages/l/libslirp-4.3.1-2.el8.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/q/qemu-5.2.0-4.fc34.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/33/Everything/source/tree/Packages/q/qemu-sanity-check-1.1.6-1.fc33.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/33/Everything/source/tree/Packages/v/virglrenderer-0.8.2-2.20200212git7d204f39.fc33.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/33/Everything/SRPMS/Packages/s/seabios-1.14.0-1.fc33.src.rpm

rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    123.123.123.123:/home/cloud/rpmbuild/SOURCES/ /home/cloud/git/qemu-build/SOURCES/
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    123.123.123.123:/home/cloud/rpmbuild/SPECS/ /home/cloud/git/qemu-build/SPECS/

rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    /home/cloud/git/qemu-build/ 123.123.123.123:/home/cloud/rpmbuild/

cd ~/rpmbuild/SPECS/

sudo yum-builddep -y ~/rpmbuild/SPECS/libepoxy.spec
rpmbuild -ba libepoxy.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libepoxy-1.5.4-3.el8.x86_64.rpm
sudo yum -y install ~/rpmbuild/RPMS/x86_64/libepoxy-devel-1.5.4-3.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/virglrenderer.spec
rpmbuild -ba virglrenderer.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/virglrenderer-0.8.2-2.20200212git7d204f39.el8.x86_64.rpm
sudo yum -y install ~/rpmbuild/RPMS/x86_64/virglrenderer-devel-0.8.2-2.20200212git7d204f39.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/liburing.spec
rpmbuild -ba liburing.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/liburing-0.7-2.el8.x86_64.rpm
sudo yum -y install ~/rpmbuild/RPMS/x86_64/liburing-devel-0.7-2.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/qemu-sanity-check.spec
rpmbuild -ba qemu-sanity-check.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/qemu-sanity-check-nodeps-1.1.6-1.el8.x86_64.rpm

sudo yum -y install xfsprogs-devel gtk3-devel vte291-devel SDL2-devel
sudo yum-builddep -y ~/rpmbuild/SPECS/qemu.spec
rpmbuild -ba qemu.spec

sudo yum-builddep -y ~/rpmbuild/SPECS/capstone.spec
rpmbuild -ba capstone.spec

sudo yum-builddep -y ~/rpmbuild/SPECS/libslirp.spec
rpmbuild -ba libslirp.spec

sudo yum-builddep -y ~/rpmbuild/SPECS/libnfs.spec
rpmbuild -ba libnfs.spec

########################################
# repo
########################################
rm -rf ~/repo
mkdir ~/repo
cp rpmbuild/RPMS/noarch/* ~/repo
cp rpmbuild/RPMS/x86_64/* ~/repo

rm ~/repo/qemu-sanity-check-*

rpm --resign ~/repo/*.rpm
createrepo ~/repo
mc mirror --remove --overwrite --md5 ~/repo repo/kvm
