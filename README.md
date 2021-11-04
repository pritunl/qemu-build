# build

```bash
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/j/jack-audio-connection-kit-1.9.19-1.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/l/libepoxy-1.5.9-1.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/l/liburing-2.0-2.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/epel/8/Everything/SRPMS/Packages/c/capstone-4.0.2-5.el8.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/epel/8/Everything/SRPMS/Packages/l/libnfs-4.0.0-1.el8.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/35/Everything/source/tree/Packages/q/qemu-6.1.0-9.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/q/qemu-sanity-check-1.1.6-5.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/v/virglrenderer-0.9.1-2.20210420git36391559.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/d/dtc-1.6.1-2.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/l/libslirp-4.6.1-2.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/e/edk2-20210527gite1999b264f1f-2.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/i/ipxe-20200823-7.git4bd064de.fc35.src.rpm
rpm -i https://yum.oracle.com/repo/OracleLinux/OL8/codeready/builder/x86_64/getPackageSource/SDL2-2.0.10-2.el8.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/34/Everything/SRPMS/Packages/l/libvirt-7.0.0-7.fc34.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/v/virt-manager-3.2.0-4.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/k/ksmtuned-0.1.0-8.fc35.src.rpm

rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    opc@123.123.123.123:/home/opc/rpmbuild/SOURCES/ /home/cloud/git/qemu-build/SOURCES/
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    opc@123.123.123.123:/home/opc/rpmbuild/SPECS/ /home/cloud/git/qemu-build/SPECS/

rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    /home/cloud/git/qemu-build/ opc@123.123.123.123:/home/cloud/rpmbuild/

scp /home/cloud/git/qemu-build/SPECS/qemu.spec opc@123.123.123.123:/home/opc/rpmbuild/SPECS/qemu.spec
scp /home/cloud/git/qemu-build/SPECS/qemu-sanity-check.spec opc@123.123.123.123:/home/opc/rpmbuild/SPECS/qemu-sanity-check.spec
scp /home/cloud/git/qemu-build/SPECS/libvirt.spec opc@123.123.123.123:/home/opc/rpmbuild/SPECS/libvirt.spec

cd ~/rpmbuild/SPECS/

sudo yum-builddep -y ~/rpmbuild/SPECS/libepoxy.spec
rpmbuild -ba libepoxy.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libepoxy-1.5.9-1.el8.x86_64.rpm ~/rpmbuild/RPMS/x86_64/libepoxy-devel-1.5.9-1.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/jack-audio-connection-kit.spec
rpmbuild -ba jack-audio-connection-kit.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/jack-audio-connection-kit-1.9.19-1.el8.x86_64.rpm ~/rpmbuild/RPMS/x86_64/jack-audio-connection-kit-dbus-1.9.19-1.el8.x86_64.rpm ~/rpmbuild/RPMS/x86_64/jack-audio-connection-kit-devel-1.9.19-1.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/virglrenderer.spec
rpmbuild -ba virglrenderer.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/virglrenderer-0.9.1-2.20210420git36391559.el8.x86_64.rpm ~/rpmbuild/RPMS/x86_64/virglrenderer-devel-0.9.1-2.20210420git36391559.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/liburing.spec
rpmbuild -ba liburing.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/liburing-2.0-2.el8.x86_64.rpm ~/rpmbuild/RPMS/x86_64/liburing-devel-2.0-2.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/qemu-sanity-check.spec
rpmbuild -ba qemu-sanity-check.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/qemu-sanity-check-nodeps-1.1.6-5.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/capstone.spec
rpmbuild -ba capstone.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/capstone-4.0.2-5.el8.x86_64.rpm ~/rpmbuild/RPMS/x86_64/capstone-devel-4.0.2-5.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/libslirp.spec
rpmbuild -ba libslirp.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libslirp-4.6.1-2.el8.x86_64.rpm ~/rpmbuild/RPMS/x86_64/libslirp-devel-4.6.1-2.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/libnfs.spec
rpmbuild -ba libnfs.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libnfs-4.0.0-1.el8.x86_64.rpm ~/rpmbuild/RPMS/x86_64/libnfs-devel-4.0.0-1.el8.x86_64.rpm ~/rpmbuild/RPMS/x86_64/libnfs-utils-4.0.0-1.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/dtc.spec
rpmbuild -ba dtc.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/dtc-1.6.1-2.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/SDL2.spec
rpmbuild -ba SDL2.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/SDL2-2.0.10-2.el8.x86_64.rpm ~/rpmbuild/RPMS/x86_64/SDL2-devel-2.0.10-2.el8.x86_64.rpm ~/rpmbuild/RPMS/x86_64/SDL2-static-2.0.10-2.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/edk2.spec
rpmbuild -ba edk2.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/edk2-tools-20210527gite1999b264f1f-2.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/ipxe.spec
rpmbuild -ba ipxe.spec

sudo yum-builddep -y ~/rpmbuild/SPECS/libvirt.spec
rpmbuild -ba libvirt.spec

sudo yum -y install xfsprogs-devel gtk3-devel vte291-devel
sudo yum-builddep -y ~/rpmbuild/SPECS/qemu.spec
rpmbuild -ba qemu.spec

sudo yum-builddep -y ~/rpmbuild/SPECS/virt-manager.spec
rpmbuild -ba virt-manager.spec

sudo yum-builddep -y ~/rpmbuild/SPECS/ksmtuned.spec
rpmbuild -ba ksmtuned.spec

cd ~/rpmbuild/RPMS/noarch/
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/x86_64/os/Packages/e/edk2-ovmf-20210527gite1999b264f1f-2.fc35.noarch.rpm
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/35/Everything/x86_64/Packages/s/seabios-1.14.0-6.fc35.noarch.rpm
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/x86_64/os/Packages/s/seabios-bin-1.14.0-5.fc35.noarch.rpm
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/35/Everything/x86_64/Packages/s/seavgabios-bin-1.14.0-6.fc35.noarch.rpm
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
mc mirror --remove --overwrite --md5 ~/repo repo-east/kvm-unstable
mc mirror --remove --overwrite --md5 ~/repo repo-west/kvm-unstable

sudo dnf -y remove gnome-boxes
sudo dnf module disable virt

sudo yum module provides sgabios-bin

sudo dnf module --all remove virt:ol

```
