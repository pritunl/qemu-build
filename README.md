# build

```bash
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/34/Everything/SRPMS/Packages/l/libepoxy-1.5.7-1.fc34.src.rpm

rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/34/Everything/source/tree/Packages/l/liburing-0.7-4.fc34.src.rpm

rpm -i https://download-ib01.fedoraproject.org/pub/epel/8/Everything/SRPMS/Packages/c/capstone-4.0.1-9.el8.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/epel/8/Everything/SRPMS/Packages/l/libnfs-4.0.0-1.el8.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/epel/8/Everything/SRPMS/Packages/l/libslirp-4.3.1-2.el8.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/q/qemu-6.0.0-1.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/33/Everything/source/tree/Packages/q/qemu-sanity-check-1.1.6-1.fc33.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/v/virglrenderer-0.9.1-1.20210420git36391559.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/34/Everything/source/tree/Packages/s/seabios-1.14.0-2.fc34.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/34/Everything/source/tree/Packages/d/dtc-1.6.0-4.fc34.src.rpm

rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    123.123.123.123:/home/cloud/rpmbuild/SOURCES/ /home/cloud/git/qemu-build/SOURCES/
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    123.123.123.123:/home/cloud/rpmbuild/SPECS/ /home/cloud/git/qemu-build/SPECS/

rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    /home/cloud/git/qemu-build/ 123.123.123.123:/home/cloud/rpmbuild/

scp /home/cloud/git/qemu-build/SPECS/qemu.spec 123.123.123.123:/home/cloud/rpmbuild/SPECS/qemu.spec

cd ~/rpmbuild/SPECS/

sudo yum-builddep -y ~/rpmbuild/SPECS/libepoxy.spec
rpmbuild -ba libepoxy.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libepoxy-1.5.7-1.el8.x86_64.rpm ~/rpmbuild/RPMS/x86_64/libepoxy-devel-1.5.7-1.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/virglrenderer.spec
rpmbuild -ba virglrenderer.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/virglrenderer-0.9.1-1.20210420git36391559.el8.x86_64.rpm ~/rpmbuild/RPMS/x86_64/virglrenderer-devel-0.9.1-1.20210420git36391559.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/liburing.spec
rpmbuild -ba liburing.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/liburing-0.7-4.el8.x86_64.rpm ~/rpmbuild/RPMS/x86_64/liburing-devel-0.7-4.el8.x86_64.rpm

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

sudo yum-builddep -y ~/rpmbuild/SPECS/seabios.spec
rpmbuild -ba seabios.spec

sudo yum-builddep -y ~/rpmbuild/SPECS/dtc.spec
rpmbuild -ba dtc.spec

wget https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/34/Everything/x86_64/os/Packages/e/edk2-ovmf-20200801stable-4.fc34.noarch.rpm
mv edk2-ovmf-20200801stable-4.fc34.noarch.rpm ~/repo/edk2-ovmf-20200801stable-4.fc34.noarch.rpm
```

# repo

```bash
rm -rf ~/repo
mkdir ~/repo
cp rpmbuild/RPMS/noarch/* ~/repo
cp rpmbuild/RPMS/x86_64/* ~/repo

rm ~/repo/qemu-sanity-check-*

rpm --resign ~/repo/*.rpm
createrepo ~/repo
mc mirror --remove --overwrite --md5 ~/repo repo-east/kvm
mc mirror --remove --overwrite --md5 ~/repo repo-west/kvm
```
