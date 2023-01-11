Name: liburing
Version: 1.0.7
Release: 3%{?dist}
Summary: Linux-native io_uring I/O access library
License: LGPLv2+
Source: %{name}-%{version}.tar.bz2
URL: http://brick.kernel.dk/snaps/%{name}-%{version}.tar.bz2
BuildRequires: gcc
Patch0: liburing-always-build-with-fPIC.patch

%description
Provides native async IO for the Linux kernel, in a fast and efficient
manner, for both buffered and O_DIRECT.

%package devel
Summary: Development files for Linux-native io_uring I/O access library
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package provides header files to include and libraries to link with
for the Linux-native io_uring.

%prep
%autosetup -p1

%build
./configure --prefix=%{_prefix} --libdir=/%{_libdir} --libdevdir=/%{_libdir} --mandir=%{_mandir} --includedir=%{_includedir}

%make_build V=1

%install
%make_install

%files
%attr(0755,root,root) %{_libdir}/liburing.so.*
%doc COPYING

%files devel
%{_includedir}/liburing/
%{_includedir}/liburing.h
%{_libdir}/liburing.so
%{_libdir}/liburing.a
%{_libdir}/pkgconfig/*
%{_mandir}/man2/*

%changelog
* Thu Aug 20 2020 Jeff Moyer <jmoyer@redhat.com> - 1.0.7-3.el8
- Build with V=1 so that the build logs are useful.
- Related: rhbz#1862551

* Thu Aug 20 2020 Jeff Moyer <jmoyer@redhat.com> - 1.0.7-2.el8
- Fix versioning.  The installed library is 1.0.7, make the rpm match.
- bump release number for build, which includes -fPIC fix
- Related: rhbz#1862551

* Fri Jul 31 2020 Jeff Moyer <jmoyer@redhat.com> - 0.7-1.el8
- Update to upstream version 0.7.
- Resolves: 1862551

* Wed Nov  6 2019 Jeff Moyer <jmoyer@redhat.com> - 0.2-2.el8
- bump release to trigger gating tests
- Related: bz#1724804

* Thu Oct 31 2019 Jeff Moyer <jmoyer@redhat.com> - 0.2-1
- Initial rhel8 package.
- Resolves: bz#1724804

* Tue Jan 8 2019 Jens Axboe <axboe@kernel.dk> - 0.1
- Initial version
