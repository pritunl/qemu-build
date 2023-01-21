# qemu-build

Build source for Pritunl KVM repository, currently provides QEMU v7.2.0 for RHEL9.

```bash
sudo tee /etc/yum.repos.d/pritunl-kvm.repo << EOF
[pritunl-kvm]
name=Pritunl KVM Repository
baseurl=https://repo.pritunl.com/kvm-unstable/oraclelinux/9/
gpgcheck=1
enabled=1
EOF

gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 1BB6FBB8D641BD9C6C0398D74D55437EC0508F5F
gpg --armor --export 1BB6FBB8D641BD9C6C0398D74D55437EC0508F5F > key.tmp; sudo rpm --import key.tmp; rm -f key.tmp
```

# build

```bash
sudo /usr/libexec/oci-growfs

sudo yum-config-manager --enable ol9_addons
sudo yum-config-manager --enable ol9_appstream
sudo yum-config-manager --enable ol9_codeready_builder

sudo yum -y install oracle-epel-release-el9
sudo yum-config-manager --enable ol9_developer_EPEL

sudo yum -y update
sudo yum -y remove cockpit cockpit-ws
sudo yum -y install rpm-build rpm-sign createrepo wget nano git
sudo yum -y install seabios seabios-bin seavgabios-bin
sudo yum -y groupinstall 'Development Tools'

sudo systemctl stop firewalld
sudo systemctl disable firewalld

mkdir rpmkeys
cd rpmkeys

wget https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/37/Everything/x86_64/Packages/d/distribution-gpg-keys-1.81-1.fc37.noarch.rpm
rpm2cpio ./distribution-gpg-keys-1.81-1.fc37.noarch.rpm | cpio -idmv
sudo rpm --import ./usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-*-primary

cd ..
rm -rf rpmkeys
mkdir rpmkeys
cd rpmkeys

wget https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/Packages/d/distribution-gpg-keys-1.81-1.fc38.noarch.rpm
rpm2cpio ./distribution-gpg-keys-1.81-1.fc38.noarch.rpm | cpio -idmv
sudo rpm --import ./usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-rawhide-primary

cd ..
rm -rf rpmkeys


wget https://yum.oracle.com/repo/OracleLinux/OL9/appstream/x86_64/getPackageSource/libepoxy-1.5.5-4.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/appstream/x86_64/getPackageSource/liburing-0.7-7.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/developer/EPEL/x86_64/getPackageSource/capstone-4.0.2-9.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL8/developer/EPEL/x86_64/getPackageSource/libnfs-4.0.0-1.el8.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL8/developer/EPEL/x86_64/getPackageSource/libslirp-4.3.1-2.el8.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/appstream/x86_64/getPackageSource/ipxe-20200823-9.git4bd064de.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/appstream/x86_64/getPackageSource/dtc-1.6.0-7.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/appstream/x86_64/getPackageSource/seabios-1.16.0-4.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/developer/kvm/utils/x86_64/getPackageSource/edk2-20220628-1.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL8/appstream/x86_64/getPackageSource/spice-0.14.3-4.el8.src.rpm

wget https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/37/Everything/source/tree/Packages/c/celt051-0.5.1.3-24.fc37.src.rpm
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/37/Everything/source/tree/Packages/l/libcacard-2.8.1-3.fc37.src.rpm
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/updates/37/Everything/source/tree/Packages/m/meson-0.63.3-1.fc37.src.rpm
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/v/virglrenderer-0.10.4-1.20230104git88b9fe3b.fc38.src.rpm
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/37/Everything/source/tree/Packages/q/qemu-sanity-check-1.1.6-7.fc37.src.rpm
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/q/qemu-7.2.0-4.fc38.src.rpm


rpm -K libepoxy-1.5.5-4.el9.src.rpm
rpm -K liburing-0.7-7.el9.src.rpm
rpm -K capstone-4.0.2-9.el9.src.rpm
rpm -K libnfs-4.0.0-1.el8.src.rpm
rpm -K libslirp-4.3.1-2.el8.src.rpm
rpm -K ipxe-20200823-9.git4bd064de.el9.src.rpm
rpm -K dtc-1.6.0-7.el9.src.rpm
rpm -K seabios-1.16.0-4.el9.src.rpm
rpm -K edk2-20220628-1.el9.src.rpm
rpm -K spice-0.14.3-4.el8.src.rpm
rpm -K libcacard-2.8.1-3.fc37.src.rpm
rpm -K celt051-0.5.1.3-24.fc37.src.rpm
rpm -K meson-0.63.3-1.fc37.src.rpm
rpm -K virglrenderer-0.10.4-1.20230104git88b9fe3b.fc38.src.rpm
rpm -K qemu-sanity-check-1.1.6-7.fc37.src.rpm
rpm -K qemu-7.2.0-4.fc38.src.rpm

sudo rpm -i libepoxy-1.5.5-4.el9.src.rpm
sudo rpm -i liburing-0.7-7.el9.src.rpm
sudo rpm -i capstone-4.0.2-9.el9.src.rpm
sudo rpm -i libnfs-4.0.0-1.el8.src.rpm
sudo rpm -i libslirp-4.3.1-2.el8.src.rpm
sudo rpm -i ipxe-20200823-9.git4bd064de.el9.src.rpm
sudo rpm -i dtc-1.6.0-7.el9.src.rpm
sudo rpm -i seabios-1.16.0-4.el9.src.rpm
sudo rpm -i edk2-20220628-1.el9.src.rpm
sudo rpm -i spice-0.14.3-4.el8.src.rpm
sudo rpm -i celt051-0.5.1.3-24.fc37.src.rpm
sudo rpm -i libcacard-2.8.1-3.fc37.src.rpm
sudo rpm -i meson-0.63.3-1.fc37.src.rpm
sudo rpm -i virglrenderer-0.10.4-1.20230104git88b9fe3b.fc38.src.rpm
sudo rpm -i qemu-sanity-check-1.1.6-7.fc37.src.rpm
sudo rpm -i qemu-7.2.0-4.fc38.src.rpm

sudo mv /root/rpmbuild ~/rpmbuild
sudo chown -R opc:opc ~/rpmbuild


rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    opc@123.123.123.123:/home/opc/*.rpm /home/cloud/git/qemu-build/SRPMS/
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    opc@123.123.123.123:/home/opc/rpmbuild/SOURCES/ /home/cloud/git/qemu-build/SOURCES/
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    opc@123.123.123.123:/home/opc/rpmbuild/SPECS/ /home/cloud/git/qemu-build/SPECS/

rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    /home/cloud/git/qemu-build/SOURCES/ opc@123.123.123.123:/home/opc/rpmbuild/SOURCES/
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    /home/cloud/git/qemu-build/SPECS/ opc@123.123.123.123:/home/opc/rpmbuild/SPECS/

scp /home/cloud/git/qemu-build/SPECS/qemu.spec opc@123.123.123.123:/home/opc/rpmbuild/SPECS/qemu.spec
scp /home/cloud/git/qemu-build/SPECS/qemu-sanity-check.spec opc@123.123.123.123:/home/opc/rpmbuild/SPECS/qemu-sanity-check.spec


cd ~/rpmbuild/SPECS/

sudo yum-builddep -y ~/rpmbuild/SPECS/libepoxy.spec
rpmbuild -ba libepoxy.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libepoxy-*.el9.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/libcacard.spec
rpmbuild -ba libcacard.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libcacard-*.el9.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/celt051.spec
rpmbuild -ba celt051.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/celt051-*.el9.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/spice.spec
rpmbuild -ba spice.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/spice-*.el9.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/virglrenderer.spec
rpmbuild -ba virglrenderer.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/virglrenderer-*.el9.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/liburing.spec
rpmbuild -ba liburing.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/liburing-*.el9.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/qemu-sanity-check.spec
rpmbuild -ba qemu-sanity-check.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/qemu-sanity-check-nodeps-*.el9.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/capstone.spec
rpmbuild -ba capstone.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/capstone-*.el9.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/libslirp.spec
rpmbuild -ba libslirp.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libslirp-*.el9.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/libnfs.spec
rpmbuild -ba libnfs.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libnfs-*.el9.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/dtc.spec
rpmbuild -ba dtc.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/dtc-*.el9.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/edk2.spec
rpmbuild -ba edk2.spec

sudo yum -y install ~/rpmbuild/RPMS/noarch/edk2-*.el9.noarch.rpm ~/rpmbuild/RPMS/x86_64/edk2-*.el9.x86_64.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/ipxe.spec
rpmbuild -ba ipxe.spec

sudo yum -y install ~/rpmbuild/RPMS/noarch/ipxe-*.el9.noarch.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/seabios.spec
rpmbuild -ba seabios.spec

sudo yum-builddep -y ~/rpmbuild/SPECS/meson.spec
rpmbuild -ba meson.spec

sudo yum -y install ~/rpmbuild/RPMS/noarch/meson-*.el9.noarch.rpm

sudo yum-builddep -y ~/rpmbuild/SPECS/qemu.spec
rpmbuild -ba qemu.spec
```

# repo

```bash
rm -rf ~/repo
mkdir ~/repo
cp rpmbuild/RPMS/noarch/* ~/repo
cp rpmbuild/RPMS/x86_64/* ~/repo
rm ~/repo/*debuginfo*
rm ~/repo/*debugsource*

rpm --resign ~/repo/*.rpm
createrepo ~/repo

mc mirror --remove --overwrite --md5 ~/repo repo-east/kvm-unstable/oraclelinux/9
mc mirror --remove --overwrite --md5 ~/repo repo-west/kvm-unstable/oraclelinux/9

mc mirror --remove --overwrite --md5 ~/repo repo-east/kvm-stable/oraclelinux/9
mc mirror --remove --overwrite --md5 ~/repo repo-west/kvm-stable/oraclelinux/9
```
