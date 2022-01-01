# build

```bash
sudo /usr/libexec/oci-growfs

sudo yum-config-manager --enable ol8_addons
sudo yum-config-manager --enable ol8_appstream
sudo yum-config-manager --enable ol8_codeready_builder

sudo yum -y install oracle-epel-release-el8
sudo yum-config-manager --enable ol8_developer_EPEL

sudo yum -y update
sudo yum -y remove cockpit cockpit-ws
sudo yum -y install rpm-build rpm-sign createrepo wget nano git
sudo yum -y groupinstall 'Development Tools'

sudo systemctl stop firewalld
sudo systemctl disable firewalld

rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/l/libepoxy-1.5.9-1.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/l/liburing-2.0-2.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/epel/8/Everything/SRPMS/Packages/c/capstone-4.0.2-5.el8.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/epel/8/Everything/SRPMS/Packages/l/libnfs-4.0.0-1.el8.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/l/libslirp-4.6.1-2.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/35/Everything/source/tree/Packages/m/meson-0.59.4-1.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/k/keyutils-1.6.1-3.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/i/ipxe-20200823-7.git4bd064de.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/e/edk2-20210527gite1999b264f1f-2.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/q/qemu-6.2.0-1.fc36.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/q/qemu-sanity-check-1.1.6-5.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/v/virglrenderer-0.9.1-2.20210420git36391559.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/d/dtc-1.6.1-2.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/35/Everything/source/tree/Packages/s/seabios-1.15.0-1.fc35.src.rpm
rpm -i https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/35/Everything/source/tree/Packages/k/ksmtuned-0.1.0-8.fc35.src.rpm

rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    opc@123.123.123.123:/home/opc/rpmbuild/SOURCES/ /home/cloud/git/qemu-build/SOURCES/
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    opc@123.123.123.123:/home/opc/rpmbuild/SPECS/ /home/cloud/git/qemu-build/SPECS/

rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    /home/cloud/git/qemu-build/ opc@123.123.123.123:/home/opc/rpmbuild/

scp /home/cloud/git/qemu-build/SPECS/meson.spec opc@123.123.123.123:/home/opc/rpmbuild/SPECS/meson.spec
scp /home/cloud/git/qemu-build/SPECS/qemu.spec opc@123.123.123.123:/home/opc/rpmbuild/SPECS/qemu.spec
scp /home/cloud/git/qemu-build/SPECS/qemu-sanity-check.spec opc@123.123.123.123:/home/opc/rpmbuild/SPECS/qemu-sanity-check.spec

cd ~/rpmbuild/SPECS/

sudo yum-builddep -y ~/rpmbuild/SPECS/libepoxy.spec
rpmbuild -ba libepoxy.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libepoxy-*.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/virglrenderer.spec
rpmbuild -ba virglrenderer.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/virglrenderer-*.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/liburing.spec
rpmbuild -ba liburing.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/liburing-*.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/qemu-sanity-check.spec
rpmbuild -ba qemu-sanity-check.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/qemu-sanity-check-nodeps-*.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/capstone.spec
rpmbuild -ba capstone.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/capstone-*.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/libslirp.spec
rpmbuild -ba libslirp.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libslirp-*.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/libnfs.spec
rpmbuild -ba libnfs.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libnfs-*.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/dtc.spec
rpmbuild -ba dtc.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/dtc-*.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/edk2.spec
rpmbuild -ba edk2.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/edk2-*.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/ipxe.spec
rpmbuild -ba ipxe.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/ipxe-*.el8.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/meson.spec
rpmbuild -ba meson.spec

sudo yum -y install ~/rpmbuild/RPMS/noarch/meson-*.el8.noarch.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/keyutils.spec
rpmbuild -ba keyutils.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/keyutils-*.el8.x86_64.rpm

sudo yum -y install https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/35/Everything/x86_64/Packages/s/seabios-1.15.0-1.fc35.noarch.rpm https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/35/Everything/x86_64/Packages/s/seabios-bin-1.15.0-1.fc35.noarch.rpm https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/35/Everything/x86_64/Packages/s/seavgabios-bin-1.15.0-1.fc35.noarch.rpm
sudo yum-builddep -y ~/rpmbuild/SPECS/seabios.spec
rpmbuild -ba seabios.spec

sudo yum-builddep -y ~/rpmbuild/SPECS/ksmtuned.spec
rpmbuild -ba ksmtuned.spec

sudo yum-builddep -y ~/rpmbuild/SPECS/qemu.spec
rpmbuild -ba qemu.spec
```

# repo

```bash
rm -rf ~/repo
mkdir ~/repo
cp rpmbuild/RPMS/noarch/* ~/repo
cp rpmbuild/RPMS/x86_64/* ~/repo

rpm --resign ~/repo/*.rpm
createrepo ~/repo
mc mirror --remove --overwrite --md5 ~/repo repo-east/kvm
mc mirror --remove --overwrite --md5 ~/repo repo-west/kvm
```
