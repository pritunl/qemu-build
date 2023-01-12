%global _hardened_build 1

%global _for_fedora_koji_builds 0

# uncomment and add '%' to use the prereltag for pre-releases
# %%global prereltag qa3

##-----------------------------------------------------------------------------
## All argument definitions should be placed here and keep them sorted
##

# asan
# if you wish to compile an rpm with address sanitizer...
# rpmbuild -ta glusterfs-6.0.tar.gz --with asan
%{?_with_asan:%global _with_asan --enable-asan}

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%global _with_asan %{nil}
%endif

# bd
# if you wish to compile an rpm without the BD map support...
# rpmbuild -ta glusterfs-6.0.tar.gz --without bd
%{?_without_bd:%global _without_bd --disable-bd-xlator}

%if ( 0%{?rhel} && 0%{?rhel} > 7 )
%global _without_bd --without-bd
%endif

# cmocka
# if you wish to compile an rpm with cmocka unit testing...
# rpmbuild -ta glusterfs-6.0.tar.gz --with cmocka
%{?_with_cmocka:%global _with_cmocka --enable-cmocka}

# debug
# if you wish to compile an rpm with debugging...
# rpmbuild -ta glusterfs-6.0.tar.gz --with debug
%{?_with_debug:%global _with_debug --enable-debug}

# epoll
# if you wish to compile an rpm without epoll...
# rpmbuild -ta glusterfs-6.0.tar.gz --without epoll
%{?_without_epoll:%global _without_epoll --disable-epoll}

# fusermount
# if you wish to compile an rpm without fusermount...
# rpmbuild -ta glusterfs-6.0.tar.gz --without fusermount
%{?_without_fusermount:%global _without_fusermount --disable-fusermount}

# geo-rep
# if you wish to compile an rpm without geo-replication support, compile like this...
# rpmbuild -ta glusterfs-6.0.tar.gz --without georeplication
%{?_without_georeplication:%global _without_georeplication --disable-georeplication}

# ipv6default
# if you wish to compile an rpm with IPv6 default...
# rpmbuild -ta glusterfs-6.0.tar.gz --with ipv6default
%{?_with_ipv6default:%global _with_ipv6default --with-ipv6-default}

# libtirpc
# if you wish to compile an rpm without TIRPC (i.e. use legacy glibc rpc)
# rpmbuild -ta glusterfs-6.0.tar.gz --without libtirpc
%{?_without_libtirpc:%global _without_libtirpc --without-libtirpc}

# Do not use libtirpc on EL6, it does not have xdr_uint64_t() and xdr_uint32_t
# Do not use libtirpc on EL7, it does not have xdr_sizeof()
%if ( 0%{?rhel} && 0%{?rhel} <= 7 )
%global _without_libtirpc --without-libtirpc
%endif


# ocf
# if you wish to compile an rpm without the OCF resource agents...
# rpmbuild -ta glusterfs-6.0.tar.gz --without ocf
%{?_without_ocf:%global _without_ocf --without-ocf}

# rdma
# if you wish to compile an rpm without rdma support, compile like this...
# rpmbuild -ta glusterfs-6.0.tar.gz --without rdma
%{?_without_rdma:%global _without_rdma --disable-ibverbs}

# No RDMA Support on 32-bit ARM
%ifarch armv7hl
%global _without_rdma --disable-ibverbs
%endif

# server
# if you wish to build rpms without server components, compile like this
# rpmbuild -ta glusterfs-6.0.tar.gz --without server
%{?_without_server:%global _without_server --without-server}

# disable server components forcefully as rhel <= 6
%if ( 0%{?rhel} )
%if (!(( "%{?dist}" == ".el6rhs" ) || ( "%{?dist}" == ".el7rhs" ) || ( "%{?dist}" == ".el7rhgs" ) || ( "%{?dist}" == ".el8rhgs" )))
%global _without_server --without-server
%endif
%endif

%global _without_extra_xlators 1
%global _without_regression_tests 1

# syslog
# if you wish to build rpms without syslog logging, compile like this
# rpmbuild -ta glusterfs-6.0.tar.gz --without syslog
%{?_without_syslog:%global _without_syslog --disable-syslog}

# disable syslog forcefully as rhel <= 6 doesn't have rsyslog or rsyslog-mmcount
# Fedora deprecated syslog, see
#  https://fedoraproject.org/wiki/Changes/NoDefaultSyslog
# (And what about RHEL7?)
%if ( 0%{?fedora} && 0%{?fedora} >= 20 ) || ( 0%{?rhel} && 0%{?rhel} <= 6 )
%global _without_syslog --disable-syslog
%endif

# tsan
# if you wish to compile an rpm with thread sanitizer...
# rpmbuild -ta glusterfs-6.0.tar.gz --with tsan
%{?_with_tsan:%global _with_tsan --enable-tsan}

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%global _with_tsan %{nil}
%endif

# valgrind
# if you wish to compile an rpm to run all processes under valgrind...
# rpmbuild -ta glusterfs-6.0.tar.gz --with valgrind
%{?_with_valgrind:%global _with_valgrind --enable-valgrind}

##-----------------------------------------------------------------------------
## All %%global definitions should be placed here and keep them sorted
##

# selinux booleans whose defalut value needs modification
# these booleans will be consumed by "%%selinux_set_booleans" macro.
%if ( 0%{?rhel} && 0%{?rhel} >= 8 )
%global selinuxbooleans rsync_full_access=1 rsync_client=1
%endif

%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} > 6 )
%global _with_systemd true
%endif

%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 7 )
%global _with_firewalld --enable-firewalld
%endif

%if 0%{?_tmpfilesdir:1}
%global _with_tmpfilesdir --with-tmpfilesdir=%{_tmpfilesdir}
%else
%global _with_tmpfilesdir --without-tmpfilesdir
%endif

# without server should also disable some server-only components
%if 0%{?_without_server:1}
%global _without_events --disable-events
%global _without_georeplication --disable-georeplication
%global _without_tiering --disable-tiering
%global _without_ocf --without-ocf
%endif

%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} > 7 )
%global _usepython3 1
%global _pythonver 3
%else
%global _usepython3 0
%global _pythonver 2
%endif

# From https://fedoraproject.org/wiki/Packaging:Python#Macros
%if ( 0%{?rhel} && 0%{?rhel} <= 6 )
%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(python2 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%global _rundir %{_localstatedir}/run
%endif

%if ( 0%{?_with_systemd:1} )
%global service_enable()   /bin/systemctl --quiet enable %1.service || : \
%{nil}
%global service_start()   /bin/systemctl --quiet start %1.service || : \
%{nil}
%global service_stop()    /bin/systemctl --quiet stop %1.service || :\
%{nil}
%global service_install() install -D -p -m 0644 %1.service %{buildroot}%2 \
%{nil}
# can't seem to make a generic macro that works
%global glusterd_svcfile   %{_unitdir}/glusterd.service
%global glusterfsd_svcfile %{_unitdir}/glusterfsd.service
%global glusterta_svcfile %{_unitdir}/gluster-ta-volume.service
%global glustereventsd_svcfile %{_unitdir}/glustereventsd.service
%global glusterfssharedstorage_svcfile %{_unitdir}/glusterfssharedstorage.service
%else
%global service_enable()  /sbin/chkconfig --add %1 >/dev/null 2>&1 || : \
%{nil}
%global systemd_preun() /sbin/chkconfig --del %1 >/dev/null 2>&1 || : \
%{nil}
%global systemd_postun_with_restart() /sbin/service %1 condrestart >/dev/null 2>&1 || : \
%{nil}
%global service_start()   /sbin/service %1 start >/dev/null 2>&1 || : \
%{nil}
%global service_stop()    /sbin/service %1 stop >/dev/null 2>&1 || : \
%{nil}
%global service_install() install -D -p -m 0755 %1.init %{buildroot}%2 \
%{nil}
# can't seem to make a generic macro that works
%global glusterd_svcfile   %{_sysconfdir}/init.d/glusterd
%global glusterfsd_svcfile %{_sysconfdir}/init.d/glusterfsd
%global glustereventsd_svcfile %{_sysconfdir}/init.d/glustereventsd
%endif

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

# We do not want to generate useless provides and requires for xlator
# .so files to be set for glusterfs packages.
# Filter all generated:
#
# TODO: RHEL5 does not have a convenient solution
%if ( 0%{?rhel} == 6 )
# filter_setup exists in RHEL6 only
%filter_provides_in %{_libdir}/glusterfs/%{version}/
%global __filter_from_req %{?__filter_from_req} | grep -v -P '^(?!lib).*\.so.*$'
%filter_setup
%else
# modern rpm and current Fedora do not generate requires when the
# provides are filtered
%global __provides_exclude_from ^%{_libdir}/glusterfs/%{version}/.*$
%endif


##-----------------------------------------------------------------------------
## All package definitions should be placed here in alphabetical order
##
Summary:          Distributed File System
%if ( 0%{_for_fedora_koji_builds} )
Name:             glusterfs
Version:          3.8.0
Release:          0.2%{?prereltag:.%{prereltag}}%{?dist}
%else
Name:             glusterfs
Version:          6.0
Release:          57.4%{?dist}
ExcludeArch:      i686
%endif
License:          GPLv2 or LGPLv3+
URL:              http://docs.gluster.org/
%if ( 0%{_for_fedora_koji_builds} )
Source0:          http://bits.gluster.org/pub/gluster/glusterfs/src/glusterfs-%{version}%{?prereltag}.tar.gz
Source1:          glusterd.sysconfig
Source2:          glusterfsd.sysconfig
Source7:          glusterfsd.service
Source8:          glusterfsd.init
%else
Source0:          glusterfs-6.0.tar.gz
%endif

Requires(pre):    shadow-utils
%if ( 0%{?_with_systemd:1} )
BuildRequires:    systemd
%endif

Requires:         %{name}-libs%{?_isa} = %{version}-%{release}
%if ( 0%{?_with_systemd:1} )
%{?systemd_requires}
%endif
%if 0%{?_with_asan:1} && !( 0%{?rhel} && 0%{?rhel} < 7 )
BuildRequires:    libasan
%endif
%if 0%{?_with_tsan:1} && !( 0%{?rhel} && 0%{?rhel} < 7 )
BuildRequires:    libtsan
%endif
BuildRequires:    git
BuildRequires:    bison flex
BuildRequires:    gcc make libtool
BuildRequires:    ncurses-devel readline-devel
BuildRequires:    libxml2-devel openssl-devel
BuildRequires:    libaio-devel libacl-devel
BuildRequires:    python%{_pythonver}-devel
%if ( 0%{?rhel} && 0%{?rhel} < 8 )
BuildRequires:    python-ctypes
%endif
%if ( 0%{?_with_ipv6default:1} ) || ( 0%{!?_without_libtirpc:1} ) || ( 0%{?rhel} && ( 0%{?rhel} >= 8 ) )
BuildRequires:    libtirpc-devel
%endif
%if ( 0%{?fedora} && 0%{?fedora} > 27 ) || ( 0%{?rhel} && 0%{?rhel} > 7 )
BuildRequires:    rpcgen
%endif
BuildRequires:    userspace-rcu-devel >= 0.7
%if ( 0%{?rhel} && 0%{?rhel} <= 6 )
BuildRequires:    automake
%endif
BuildRequires:    libuuid-devel
%if ( 0%{?_with_cmocka:1} )
BuildRequires:    libcmocka-devel >= 1.0.1
%endif
%if ( 0%{!?_without_tiering:1} )
BuildRequires:    sqlite-devel
%endif
%if ( 0%{!?_without_georeplication:1} )
BuildRequires:    libattr-devel
%endif

%if (0%{?_with_firewalld:1})
BuildRequires:    firewalld
%endif

Obsoletes:        hekafs
Obsoletes:        %{name}-common < %{version}-%{release}
Obsoletes:        %{name}-core < %{version}-%{release}
Obsoletes:        %{name}-ufo
%if ( 0%{!?_with_gnfs:1} )
Obsoletes:        %{name}-gnfs
%endif
%if ( 0%{?rhel} < 7 )
Obsoletes:        %{name}-ganesha
%endif
Provides:         %{name}-common = %{version}-%{release}
Provides:         %{name}-core = %{version}-%{release}

# Patch0001: 0001-Update-rfc.sh-to-rhgs-3.5.0.patch
Patch0002: 0002-glusterd-fix-op-versions-for-RHS-backwards-compatabi.patch
Patch0003: 0003-rpc-set-bind-insecure-to-off-by-default.patch
Patch0004: 0004-glusterd-spec-fixing-autogen-issue.patch
Patch0005: 0005-libglusterfs-glusterd-Fix-compilation-errors.patch
Patch0006: 0006-build-remove-ghost-directory-entries.patch
Patch0007: 0007-build-add-RHGS-specific-changes.patch
Patch0008: 0008-secalert-remove-setuid-bit-for-fusermount-glusterfs.patch
Patch0009: 0009-build-introduce-security-hardening-flags-in-gluster.patch
Patch0010: 0010-spec-fix-add-pre-transaction-scripts-for-geo-rep-and.patch
Patch0011: 0011-rpm-glusterfs-devel-for-client-builds-should-not-dep.patch
Patch0012: 0012-build-add-pretrans-check.patch
Patch0013: 0013-glusterd-fix-info-file-checksum-mismatch-during-upgr.patch
Patch0014: 0014-build-spec-file-conflict-resolution.patch
Patch0015: 0015-build-randomize-temp-file-names-in-pretrans-scriptle.patch
Patch0016: 0016-glusterd-parallel-readdir-Change-the-op-version-of-p.patch
Patch0017: 0017-glusterd-Revert-op-version-for-cluster.max-brick-per.patch
Patch0018: 0018-cli-Add-message-for-user-before-modifying-brick-mult.patch
Patch0019: 0019-build-launch-glusterd-upgrade-after-all-new-bits-are.patch
Patch0020: 0020-spec-unpackaged-files-found-for-RHEL-7-client-build.patch
Patch0021: 0021-cli-glusterfsd-remove-copyright-information.patch
Patch0022: 0022-cli-Remove-upstream-doc-reference.patch
Patch0023: 0023-hooks-remove-selinux-hooks.patch
Patch0024: 0024-glusterd-Make-localtime-logging-option-invisible-in-.patch
Patch0025: 0025-build-make-RHGS-version-available-for-server.patch
Patch0026: 0026-glusterd-Introduce-daemon-log-level-cluster-wide-opt.patch
Patch0027: 0027-glusterd-change-op-version-of-fips-mode-rchecksum.patch
Patch0028: 0028-glusterd-Reset-op-version-for-features.shard-deletio.patch
Patch0029: 0029-glusterd-Reset-op-version-for-features.shard-lru-lim.patch
Patch0030: 0030-selinux-glusterd-add-features.selinux-to-glusterd-vo.patch
Patch0031: 0031-glusterd-turn-off-selinux-feature-in-downstream.patch
Patch0032: 0032-glusterd-update-gd-op-version-to-3_7_0.patch
Patch0033: 0033-build-add-missing-explicit-package-dependencies.patch
Patch0034: 0034-glusterd-introduce-a-new-op-version-for-rhgs-3.4.3.patch
Patch0035: 0035-glusterd-tag-rebalance-mgmt_v3-command-to-op-version.patch
Patch0036: 0036-build-add-conditional-dependency-on-server-for-devel.patch
Patch0037: 0037-cli-change-the-warning-message.patch
Patch0038: 0038-spec-avoid-creation-of-temp-file-in-lua-script.patch
Patch0039: 0039-cli-fix-query-to-user-during-brick-mux-selection.patch
Patch0040: 0040-build-Remove-unsupported-test-cases-failing-consiste.patch
Patch0041: 0041-tests-geo-rep-Build-failed-in-Jenkins-for-test-bug-1.patch
Patch0042: 0042-spec-client-server-Builds-are-failing-on-rhel-6.patch
Patch0043: 0043-inode-don-t-dump-the-whole-table-to-CLI.patch
Patch0044: 0044-cluster-ec-Don-t-enqueue-an-entry-if-it-is-already-h.patch
Patch0045: 0045-glusterd-fix-txn-id-mem-leak.patch
Patch0046: 0046-protocol-client-Do-not-fallback-to-anon-fd-if-fd-is-.patch
Patch0047: 0047-client-rpc-Fix-the-payload-being-sent-on-the-wire.patch
Patch0048: 0048-gfapi-Unblock-epoll-thread-for-upcall-processing.patch
Patch0049: 0049-transport-socket-log-shutdown-msg-occasionally.patch
Patch0050: 0050-geo-rep-Fix-syncing-multiple-rename-of-symlink.patch
Patch0051: 0051-spec-update-rpm-install-condition.patch
Patch0052: 0052-geo-rep-IPv6-support.patch
Patch0053: 0053-Revert-packaging-ganesha-remove-glusterfs-ganesha-su.patch
Patch0054: 0054-Revert-glusterd-storhaug-remove-ganesha.patch
Patch0055: 0055-Revert-storhaug-HA-first-step-remove-resource-agents.patch
Patch0056: 0056-common-ha-fixes-for-Debian-based-systems.patch
Patch0057: 0057-ganesha-scripts-Remove-export-entries-from-ganesha.c.patch
Patch0058: 0058-glusterd-ganesha-During-volume-delete-remove-the-gan.patch
Patch0059: 0059-glusterd-ganesha-throw-proper-error-for-gluster-nfs-.patch
Patch0060: 0060-ganesha-scripts-Stop-ganesha-process-on-all-nodes-if.patch
Patch0061: 0061-ganesha-allow-refresh-config-and-volume-export-unexp.patch
Patch0062: 0062-glusterd-ganesha-perform-removal-of-ganesha.conf-on-.patch
Patch0063: 0063-glusterd-ganesha-update-cache-invalidation-properly-.patch
Patch0064: 0064-glusterd-ganesha-return-proper-value-in-pre_setup.patch
Patch0065: 0065-ganesha-scripts-remove-dependency-over-export-config.patch
Patch0066: 0066-glusterd-ganesha-add-proper-NULL-check-in-manage_exp.patch
Patch0067: 0067-ganesha-minor-improvments-for-commit-e91cdf4-17081.patch
Patch0068: 0068-common-ha-surviving-ganesha.nfsd-not-put-in-grace-on.patch
Patch0069: 0069-common-ha-enable-and-disable-selinux-ganesha_use_fus.patch
Patch0070: 0070-packaging-glusterfs-ganesha-update-sometimes-fails-s.patch
Patch0071: 0071-common-ha-enable-and-disable-selinux-gluster_use_exe.patch
Patch0072: 0072-ganesha-ha-don-t-set-SELinux-booleans-if-SELinux-is-.patch
Patch0073: 0073-build-remove-ganesha-dependency-on-selinux-policy.patch
Patch0074: 0074-common-ha-enable-pacemaker-at-end-of-setup.patch
Patch0075: 0075-common-ha-Fix-an-incorrect-syntax-during-setup.patch
Patch0076: 0076-glusterd-ganesha-change-voltype-for-ganesha.enable-i.patch
Patch0077: 0077-glusterd-ganesha-create-remove-export-file-only-from.patch
Patch0078: 0078-common-ha-scripts-pass-the-list-of-servers-properly-.patch
Patch0079: 0079-common-ha-All-statd-related-files-need-to-be-owned-b.patch
Patch0080: 0080-glusterd-ganesha-Skip-non-ganesha-nodes-properly-for.patch
Patch0081: 0081-ganesha-ha-ensure-pacemaker-is-enabled-after-setup.patch
Patch0082: 0082-build-Add-dependency-on-netstat-for-glusterfs-ganesh.patch
Patch0083: 0083-common-ha-enable-and-disable-selinux-ganesha_use_fus.patch
Patch0084: 0084-glusterd-Fix-duplicate-client_op_version-in-info-fil.patch
Patch0085: 0085-Revert-all-remove-code-which-is-not-being-considered.patch
Patch0086: 0086-Revert-tiering-remove-the-translator-from-build-and-.patch
Patch0087: 0087-ganesha-fixing-minor-issues-after-the-backport-from-.patch
Patch0088: 0088-tier-fix-failures-noticed-during-tier-start-and-tier.patch
Patch0089: 0089-glusterd-gNFS-On-post-upgrade-to-3.2-disable-gNFS-fo.patch
Patch0090: 0090-Revert-build-conditionally-build-legacy-gNFS-server-.patch
Patch0091: 0091-glusterd-gNFS-explicitly-set-nfs.disable-to-off-afte.patch
Patch0092: 0092-logging-Fix-GF_LOG_OCCASSIONALLY-API.patch
Patch0093: 0093-glusterd-Change-op-version-of-cache-invalidation-in-.patch
Patch0094: 0094-glusterd-load-ctime-in-the-client-graph-only-if-it-s.patch
Patch0095: 0095-cluster-afr-Remove-local-from-owners_list-on-failure.patch
Patch0096: 0096-core-Brick-is-not-able-to-detach-successfully-in-bri.patch
Patch0097: 0097-glusterd-tier-while-doing-an-attach-tier-the-self-he.patch
Patch0098: 0098-mgmt-shd-Implement-multiplexing-in-self-heal-daemon.patch
Patch0099: 0099-client-fini-return-fini-after-rpc-cleanup.patch
Patch0100: 0100-clnt-rpc-ref-leak-during-disconnect.patch
Patch0101: 0101-shd-mux-Fix-coverity-issues-introduced-by-shd-mux-pa.patch
Patch0102: 0102-rpc-transport-Missing-a-ref-on-dict-while-creating-t.patch
Patch0103: 0103-dht-NULL-check-before-setting-error-flag.patch
Patch0104: 0104-afr-shd-Cleanup-self-heal-daemon-resources-during-af.patch
Patch0105: 0105-core-Log-level-changes-do-not-effect-on-running-clie.patch
Patch0106: 0106-libgfchangelog-use-find_library-to-locate-shared-lib.patch
Patch0107: 0107-gfapi-add-function-to-set-client-pid.patch
Patch0108: 0108-afr-add-client-pid-to-all-gf_event-calls.patch
Patch0109: 0109-glusterd-Optimize-glusterd-handshaking-code-path.patch
Patch0110: 0110-tier-shd-glusterd-with-shd-mux-the-shd-volfile-path-.patch
Patch0111: 0111-glusterd-fix-loading-ctime-in-client-graph-logic.patch
Patch0112: 0112-geo-rep-fix-incorrectly-formatted-authorized_keys.patch
Patch0113: 0113-spec-Glusterd-did-not-start-by-default-after-node-re.patch
Patch0114: 0114-core-fix-hang-issue-in-__gf_free.patch
Patch0115: 0115-core-only-log-seek-errors-if-SEEK_HOLE-SEEK_DATA-is-.patch
Patch0116: 0116-cluster-ec-fix-fd-reopen.patch
Patch0117: 0117-spec-Remove-thin-arbiter-package.patch
Patch0118: 0118-tests-mark-thin-arbiter-test-ta.t-as-bad.patch
Patch0119: 0119-glusterd-provide-a-way-to-detach-failed-node.patch
Patch0120: 0120-glusterd-shd-Keep-a-ref-on-volinfo-until-attach-rpc-.patch
Patch0121: 0121-spec-glusterfs-devel-for-client-build-should-not-dep.patch
Patch0122: 0122-posix-ctime-Fix-stat-time-attributes-inconsistency-d.patch
Patch0123: 0123-ctime-Fix-log-repeated-logging-during-open.patch
Patch0124: 0124-spec-remove-duplicate-references-to-files.patch
Patch0125: 0125-glusterd-define-dumpops-in-the-xlator_api-of-gluster.patch
Patch0126: 0126-cluster-dht-refactor-dht-lookup-functions.patch
Patch0127: 0127-cluster-dht-Refactor-dht-lookup-functions.patch
Patch0128: 0128-glusterd-Fix-bulkvoldict-thread-logic-in-brick-multi.patch
Patch0129: 0129-core-handle-memory-accounting-correctly.patch
Patch0130: 0130-tier-test-new-tier-cmds.t-fails-after-a-glusterd-res.patch
Patch0131: 0131-tests-dht-Test-that-lookups-are-sent-post-brick-up.patch
Patch0132: 0132-glusterd-remove-duplicate-occurrence-of-features.sel.patch
Patch0133: 0133-glusterd-enable-fips-mode-rchecksum-for-new-volumes.patch
Patch0134: 0134-performance-write-behind-remove-request-from-wip-lis.patch
Patch0135: 0135-geo-rep-fix-incorrectly-formatted-authorized_keys.patch
Patch0136: 0136-glusterd-fix-inconsistent-global-option-output-in-vo.patch
Patch0137: 0137-shd-glusterd-Serialize-shd-manager-to-prevent-race-c.patch
Patch0138: 0138-glusterd-Add-gluster-volume-stop-operation-to-gluste.patch
Patch0139: 0139-ec-shd-Cleanup-self-heal-daemon-resources-during-ec-.patch
Patch0140: 0140-cluster-ec-Reopen-shouldn-t-happen-with-O_TRUNC.patch
Patch0141: 0141-socket-ssl-fix-crl-handling.patch
Patch0142: 0142-lock-check-null-value-of-dict-to-avoid-log-flooding.patch
Patch0143: 0143-packaging-Change-the-dependency-on-nfs-ganesha-to-2..patch
Patch0144: 0144-cluster-ec-honor-contention-notifications-for-partia.patch
Patch0145: 0145-core-Capture-process-memory-usage-at-the-time-of-cal.patch
Patch0146: 0146-dht-Custom-xattrs-are-not-healed-in-case-of-add-bric.patch
Patch0147: 0147-glusterd-bulkvoldict-thread-is-not-handling-all-volu.patch
Patch0148: 0148-cluster-dht-Lookup-all-files-when-processing-directo.patch
Patch0149: 0149-glusterd-Optimize-code-to-copy-dictionary-in-handsha.patch
Patch0150: 0150-libglusterfs-define-macros-needed-for-cloudsync.patch
Patch0151: 0151-mgmt-glusterd-Make-changes-related-to-cloudsync-xlat.patch
Patch0152: 0152-storage-posix-changes-with-respect-to-cloudsync.patch
Patch0153: 0153-features-cloudsync-Added-some-new-functions.patch
Patch0154: 0154-cloudsync-cvlt-Cloudsync-plugin-for-commvault-store.patch
Patch0155: 0155-cloudsync-Make-readdirp-return-stat-info-of-all-the-.patch
Patch0156: 0156-cloudsync-Fix-bug-in-cloudsync-fops-c.py.patch
Patch0157: 0157-afr-frame-Destroy-frame-after-afr_selfheal_entry_gra.patch
Patch0158: 0158-glusterfsd-cleanup-Protect-graph-object-under-a-lock.patch
Patch0159: 0159-glusterd-add-an-op-version-check.patch
Patch0160: 0160-geo-rep-Geo-rep-help-text-issue.patch
Patch0161: 0161-geo-rep-Fix-rename-with-existing-destination-with-sa.patch
Patch0162: 0162-geo-rep-Fix-sync-method-config.patch
Patch0163: 0163-geo-rep-Fix-sync-hang-with-tarssh.patch
Patch0164: 0164-cluster-ec-Fix-handling-of-heal-info-cases-without-l.patch
Patch0165: 0165-tests-shd-Add-test-coverage-for-shd-mux.patch
Patch0166: 0166-glusterd-svc-glusterd_svcs_stop-should-call-individu.patch
Patch0167: 0167-glusterd-shd-Optimize-the-glustershd-manager-to-send.patch
Patch0168: 0168-cluster-dht-Fix-directory-perms-during-selfheal.patch
Patch0169: 0169-Build-Fix-spec-to-enable-rhel8-client-build.patch
Patch0170: 0170-geo-rep-Convert-gfid-conflict-resolutiong-logs-into-.patch
Patch0171: 0171-posix-add-storage.reserve-size-option.patch
Patch0172: 0172-ec-fini-Fix-race-with-ec_fini-and-ec_notify.patch
Patch0173: 0173-glusterd-store-fips-mode-rchecksum-option-in-the-inf.patch
Patch0174: 0174-xlator-log-Add-more-logging-in-xlator_is_cleanup_sta.patch
Patch0175: 0175-ec-fini-Fix-race-between-xlator-cleanup-and-on-going.patch
Patch0176: 0176-features-shard-Fix-crash-during-background-shard-del.patch
Patch0177: 0177-features-shard-Fix-extra-unref-when-inode-object-is-.patch
Patch0178: 0178-Cluster-afr-Don-t-treat-all-bricks-having-metadata-p.patch
Patch0179: 0179-tests-Fix-split-brain-favorite-child-policy.t-failur.patch
Patch0180: 0180-ganesha-scripts-Make-generate-epoch.py-python3-compa.patch
Patch0181: 0181-afr-log-before-attempting-data-self-heal.patch
Patch0182: 0182-geo-rep-fix-mountbroker-setup.patch
Patch0183: 0183-glusterd-svc-Stop-stale-process-using-the-glusterd_p.patch
Patch0184: 0184-tests-Add-gating-configuration-file-for-rhel8.patch
Patch0185: 0185-gfapi-provide-an-api-for-setting-statedump-path.patch
Patch0186: 0186-cli-Remove-brick-warning-seems-unnecessary.patch
Patch0187: 0187-gfapi-statedump_path-add-proper-version-number.patch
Patch0188: 0188-features-shard-Fix-integer-overflow-in-block-count-a.patch
Patch0189: 0189-features-shard-Fix-block-count-accounting-upon-trunc.patch
Patch0190: 0190-Build-removing-the-hardcoded-usage-of-python3.patch
Patch0191: 0191-Build-Update-python-shebangs-based-on-version.patch
Patch0192: 0192-build-Ensure-gluster-cli-package-is-built-as-part-of.patch
Patch0193: 0193-spec-fixed-python-dependency-for-rhel6.patch
Patch0194: 0194-stack-Make-sure-to-have-unique-call-stacks-in-all-ca.patch
Patch0195: 0195-build-package-glusterfs-ganesha-for-rhel7-and-above.patch
Patch0196: 0196-posix-ctime-Fix-ctime-upgrade-issue.patch
Patch0197: 0197-posix-fix-crash-in-posix_cs_set_state.patch
Patch0198: 0198-cluster-ec-Prevent-double-pre-op-xattrops.patch
Patch0199: 0199-upcall-Avoid-sending-notifications-for-invalid-inode.patch
Patch0200: 0200-gfapi-fix-incorrect-initialization-of-upcall-syncop-.patch
Patch0201: 0201-geo-rep-Fix-permissions-for-GEOREP_DIR-in-non-root-s.patch
Patch0202: 0202-shd-mux-Fix-race-between-mux_proc-unlink-and-stop.patch
Patch0203: 0203-glusterd-shd-Change-shd-logfile-to-a-unique-name.patch
Patch0204: 0204-glusterd-conditionally-clear-txn_opinfo-in-stage-op.patch
Patch0205: 0205-glusterd-Can-t-run-rebalance-due-to-long-unix-socket.patch
Patch0206: 0206-glusterd-ignore-user.-options-from-compatibility-che.patch
Patch0207: 0207-glusterd-fix-use-after-free-of-a-dict_t.patch
Patch0208: 0208-mem-pool-remove-dead-code.patch
Patch0209: 0209-core-avoid-dynamic-TLS-allocation-when-possible.patch
Patch0210: 0210-mem-pool.-c-h-minor-changes.patch
Patch0211: 0211-libglusterfs-Fix-compilation-when-disable-mempool-is.patch
Patch0212: 0212-core-fix-memory-allocation-issues.patch
Patch0213: 0213-cluster-dht-Strip-out-dht-xattrs.patch
Patch0214: 0214-geo-rep-Upgrading-config-file-to-new-version.patch
Patch0215: 0215-posix-modify-storage.reserve-option-to-take-size-and.patch
Patch0216: 0216-Test-case-fixe-for-downstream-3.5.0.patch
Patch0217: 0217-uss-Fix-tar-issue-with-ctime-and-uss-enabled.patch
Patch0218: 0218-graph-shd-Use-glusterfs_graph_deactivate-to-free-the.patch
Patch0219: 0219-posix-add-posix_set_ctime-in-posix_ftruncate.patch
Patch0220: 0220-graph-shd-Use-top-down-approach-while-cleaning-xlato.patch
Patch0221: 0221-protocol-client-propagte-GF_EVENT_CHILD_PING-only-fo.patch
Patch0222: 0222-cluster-dht-Fixed-a-memleak-in-dht_rename_cbk.patch
Patch0223: 0223-change-get_real_filename-implementation-to-use-ENOAT.patch
Patch0224: 0224-core-replace-inet_addr-with-inet_pton.patch
Patch0225: 0225-tests-utils-Fix-py2-py3-util-python-scripts.patch
Patch0226: 0226-geo-rep-fix-gluster-command-path-for-non-root-sessio.patch
Patch0227: 0227-glusterd-svc-update-pid-of-mux-volumes-from-the-shd-.patch
Patch0228: 0228-locks-enable-notify-contention-by-default.patch
Patch0229: 0229-glusterd-Show-the-correct-brick-status-in-get-state.patch
Patch0230: 0230-Revert-glusterd-svc-update-pid-of-mux-volumes-from-t.patch
Patch0231: 0231-Revert-graph-shd-Use-top-down-approach-while-cleanin.patch
Patch0232: 0232-cluster-afr-Fix-incorrect-reporting-of-gfid-type-mis.patch
Patch0233: 0233-Revert-graph-shd-Use-glusterfs_graph_deactivate-to-f.patch
Patch0234: 0234-Revert-glusterd-shd-Change-shd-logfile-to-a-unique-n.patch
Patch0235: 0235-Revert-glusterd-svc-Stop-stale-process-using-the-glu.patch
Patch0236: 0236-Revert-shd-mux-Fix-race-between-mux_proc-unlink-and-.patch
Patch0237: 0237-Revert-ec-fini-Fix-race-between-xlator-cleanup-and-o.patch
Patch0238: 0238-Revert-xlator-log-Add-more-logging-in-xlator_is_clea.patch
Patch0239: 0239-Revert-ec-fini-Fix-race-with-ec_fini-and-ec_notify.patch
Patch0240: 0240-Revert-glusterd-shd-Optimize-the-glustershd-manager-.patch
Patch0241: 0241-Revert-glusterd-svc-glusterd_svcs_stop-should-call-i.patch
Patch0242: 0242-Revert-tests-shd-Add-test-coverage-for-shd-mux.patch
Patch0243: 0243-Revert-glusterfsd-cleanup-Protect-graph-object-under.patch
Patch0244: 0244-Revert-ec-shd-Cleanup-self-heal-daemon-resources-dur.patch
Patch0245: 0245-Revert-shd-glusterd-Serialize-shd-manager-to-prevent.patch
Patch0246: 0246-Revert-glusterd-shd-Keep-a-ref-on-volinfo-until-atta.patch
Patch0247: 0247-Revert-afr-shd-Cleanup-self-heal-daemon-resources-du.patch
Patch0248: 0248-Revert-shd-mux-Fix-coverity-issues-introduced-by-shd.patch
Patch0249: 0249-Revert-client-fini-return-fini-after-rpc-cleanup.patch
Patch0250: 0250-Revert-mgmt-shd-Implement-multiplexing-in-self-heal-.patch
Patch0251: 0251-tests-Fix-bug-1717819-metadata-split-brain-detection.patch
Patch0252: 0252-glusterd-do-not-mark-skip_locking-as-true-for-geo-re.patch
Patch0253: 0253-core-fix-deadlock-between-statedump-and-fd_anonymous.patch
Patch0254: 0254-Detach-iot_worker-to-release-its-resources.patch
Patch0255: 0255-Revert-tier-shd-glusterd-with-shd-mux-the-shd-volfil.patch
Patch0256: 0256-features-snapview-server-use-the-same-volfile-server.patch
Patch0257: 0257-geo-rep-Test-case-for-upgrading-config-file.patch
Patch0258: 0258-geo-rep-Fix-mount-broker-setup-issue.patch
Patch0259: 0259-gluster-block-tuning-perf-options.patch
Patch0260: 0260-ctime-Set-mdata-xattr-on-legacy-files.patch
Patch0261: 0261-features-utime-Fix-mem_put-crash.patch
Patch0262: 0262-glusterd-ctime-Disable-ctime-by-default.patch
Patch0263: 0263-tests-fix-ctime-related-tests.patch
Patch0264: 0264-gfapi-Fix-deadlock-while-processing-upcall.patch
Patch0265: 0265-fuse-add-missing-GF_FREE-to-fuse_interrupt.patch
Patch0266: 0266-geo-rep-Fix-mount-broker-setup-issue.patch
Patch0267: 0267-posix-ctime-Fix-race-during-lookup-ctime-xattr-heal.patch
Patch0268: 0268-rpc-transport-have-default-listen-port.patch
Patch0269: 0269-ec-fix-truncate-lock-to-cover-the-write-in-tuncate-c.patch
Patch0270: 0270-cluster-ec-inherit-healing-from-lock-when-it-has-inf.patch
Patch0271: 0271-cluster-ec-fix-EIO-error-for-concurrent-writes-on-sp.patch
Patch0272: 0272-cluster-ec-Always-read-from-good-mask.patch
Patch0273: 0273-cluster-ec-Fix-reopen-flags-to-avoid-misbehavior.patch
Patch0274: 0274-cluster-ec-Update-lock-good_mask-on-parent-fop-failu.patch
Patch0275: 0275-cluster-ec-Create-heal-task-with-heal-process-id.patch
Patch0276: 0276-features-utime-always-update-ctime-at-setattr.patch
Patch0277: 0277-geo-rep-Fix-Config-Get-Race.patch
Patch0278: 0278-geo-rep-Fix-worker-connection-issue.patch
Patch0279: 0279-posix-In-brick_mux-brick-is-crashed-while-start-stop.patch
Patch0280: 0280-performance-md-cache-Do-not-skip-caching-of-null-cha.patch
Patch0281: 0281-ctime-Fix-incorrect-realtime-passed-to-frame-root-ct.patch
Patch0282: 0282-geo-rep-Fix-the-name-of-changelog-archive-file.patch
Patch0283: 0283-ctime-Fix-ctime-issue-with-utime-family-of-syscalls.patch
Patch0284: 0284-posix-log-aio_error-return-codes-in-posix_fs_health_.patch
Patch0285: 0285-glusterd-glusterd-service-is-getting-timed-out-on-sc.patch
Patch0286: 0286-glusterfs.spec.in-added-script-files-for-machine-com.patch
Patch0287: 0287-cluster-ec-Fail-fsync-flush-for-files-on-update-size.patch
Patch0288: 0288-cluster-ec-Fix-coverity-issues.patch
Patch0289: 0289-cluster-ec-quorum-count-implementation.patch
Patch0290: 0290-glusterd-tag-disperse.quorum-count-for-31306.patch
Patch0291: 0291-cluster-ec-Mark-release-only-when-it-is-acquired.patch
Patch0292: 0292-rpc-Update-address-family-if-it-is-not-provide-in-cm.patch
Patch0293: 0293-glusterd-IPV6-hostname-address-is-not-parsed-correct.patch
Patch0294: 0294-eventsapi-Set-IPv4-IPv6-family-based-on-input-IP.patch
Patch0295: 0295-ctime-rebalance-Heal-ctime-xattr-on-directory-during.patch
Patch0296: 0296-glusterfind-pre-command-failure-on-a-modify.patch
Patch0297: 0297-rpmbuild-fixing-the-build-errors-with-2a905a8ae.patch
Patch0298: 0298-geo-rep-fix-sub-command-during-worker-connection.patch
Patch0299: 0299-geo-rep-performance-improvement-while-syncing-rename.patch
Patch0300: 0300-cli-remove-the-warning-displayed-when-remove-brick-s.patch
Patch0301: 0301-posix-Brick-is-going-down-unexpectedly.patch
Patch0302: 0302-cluster-ec-prevent-filling-shd-log-with-table-not-fo.patch
Patch0303: 0303-posix-heketidbstorage-bricks-go-down-during-PVC-crea.patch
Patch0304: 0304-cluster-dht-Correct-fd-processing-loop.patch
Patch0305: 0305-glusterd-rebalance-start-should-fail-when-quorum-is-.patch
Patch0306: 0306-cli-fix-distCount-value.patch
Patch0307: 0307-ssl-fix-RHEL8-regression-failure.patch
Patch0308: 0308-dht-Rebalance-causing-IO-Error-File-descriptor-in-ba.patch
Patch0309: 0309-geo-rep-Fix-config-upgrade-on-non-participating-node.patch
Patch0310: 0310-tests-test-case-for-non-root-geo-rep-setup.patch
Patch0311: 0311-geo-rep-Fix-Permission-denied-traceback-on-non-root-.patch
Patch0312: 0312-Scripts-quota_fsck-script-KeyError-contri_size.patch
Patch0313: 0313-extras-Cgroup-CPU-Mem-restriction-are-not-working-on.patch
Patch0314: 0314-glusterd-tier-is_tier_enabled-inserted-causing-check.patch
Patch0315: 0315-geo-rep-Fix-py2-py3-compatibility-in-repce.patch
Patch0316: 0316-spec-fixed-python-prettytable-dependency-for-rhel6.patch
Patch0317: 0317-Update-rfc.sh-to-rhgs-3.5.1.patch
Patch0318: 0318-Update-rfc.sh-to-rhgs-3.5.1.patch
Patch0319: 0319-features-snapview-server-obtain-the-list-of-snapshot.patch
Patch0320: 0320-gf-event-Handle-unix-volfile-servers.patch
Patch0321: 0321-Adding-white-spaces-to-description-of-set-group.patch
Patch0322: 0322-glusterd-display-correct-rebalance-data-size-after-g.patch
Patch0323: 0323-cli-display-detailed-rebalance-info.patch
Patch0324: 0324-extras-hooks-Add-SELinux-label-on-new-bricks-during-.patch
Patch0325: 0325-extras-hooks-Install-and-package-newly-added-post-ad.patch
Patch0326: 0326-tests-subdir-mount.t-is-failing-for-brick_mux-regrss.patch
Patch0327: 0327-glusterfind-integrate-with-gfid2path.patch
Patch0328: 0328-glusterd-Add-warning-and-abort-in-case-of-failures-i.patch
Patch0329: 0329-cluster-afr-Heal-entries-when-there-is-a-source-no-h.patch
Patch0330: 0330-mount.glusterfs-change-the-error-message.patch
Patch0331: 0331-features-locks-Do-special-handling-for-op-version-3..patch
Patch0332: 0332-Removing-one-top-command-from-gluster-v-help.patch
Patch0333: 0333-rpc-Synchronize-slot-allocation-code.patch
Patch0334: 0334-dht-log-getxattr-failure-for-node-uuid-at-DEBUG.patch
Patch0335: 0335-tests-RHEL8-test-failure-fixes-for-RHGS.patch
Patch0336: 0336-spec-check-and-return-exit-code-in-rpm-scripts.patch
Patch0337: 0337-fuse-Set-limit-on-invalidate-queue-size.patch
Patch0338: 0338-glusterfs-fuse-Reduce-the-default-lru-limit-value.patch
Patch0339: 0339-geo-rep-fix-integer-config-validation.patch
Patch0340: 0340-rpc-event_slot_alloc-converted-infinite-loop-after-r.patch
Patch0341: 0341-socket-fix-error-handling.patch
Patch0342: 0342-Revert-hooks-remove-selinux-hooks.patch
Patch0343: 0343-extras-hooks-syntactical-errors-in-SELinux-hooks-sci.patch
Patch0344: 0344-Revert-all-fixes-to-include-SELinux-hook-scripts.patch
Patch0345: 0345-read-ahead-io-cache-turn-off-by-default.patch
Patch0346: 0346-fuse-degrade-logging-of-write-failure-to-fuse-device.patch
Patch0347: 0347-tools-glusterfind-handle-offline-bricks.patch
Patch0348: 0348-glusterfind-Fix-py2-py3-issues.patch
Patch0349: 0349-glusterfind-python3-compatibility.patch
Patch0350: 0350-tools-glusterfind-Remove-an-extra-argument.patch
Patch0351: 0351-server-Mount-fails-after-reboot-1-3-gluster-nodes.patch
Patch0352: 0352-spec-fixed-missing-dependencies-for-glusterfs-clouds.patch
Patch0353: 0353-build-glusterfs-ganesha-pkg-requires-python3-policyc.patch
Patch0354: 0354-core-fix-memory-pool-management-races.patch
Patch0355: 0355-core-Prevent-crash-on-process-termination.patch
Patch0356: 0356-Update-rfc.sh-to-rhgs-3.5.1-rhel-8.patch
Patch0357: 0357-ganesha-ha-updates-for-pcs-0.10.x-i.e.-in-Fedora-29-.patch
Patch0358: 0358-inode-fix-wrong-loop-count-in-__inode_ctx_free.patch
Patch0359: 0359-dht-gf_defrag_process_dir-is-called-even-if-gf_defra.patch
Patch0360: 0360-rpc-Make-ssl-log-more-useful.patch
Patch0361: 0361-snap_scheduler-python3-compatibility-and-new-test-ca.patch
Patch0362: 0362-write-behind-fix-data-corruption.patch
Patch0363: 0363-common-ha-cluster-status-shows-FAILOVER-when-actuall.patch
Patch0364: 0364-dht-fixing-rebalance-failures-for-files-with-holes.patch
Patch0365: 0365-build-geo-rep-requires-relevant-selinux-permission-f.patch
Patch0366: 0366-snapshot-fix-python3-issue-in-gcron.patch
Patch0367: 0367-dht-Handle-setxattr-and-rm-race-for-directory-in-reb.patch
Patch0368: 0368-Update-rfc.sh-to-rhgs-3.5.2.patch
Patch0369: 0369-cluster-ec-Return-correct-error-code-and-log-message.patch
Patch0370: 0370-dht-Do-opendir-selectively-in-gf_defrag_process_dir.patch
Patch0371: 0371-common-ha-cluster-status-shows-FAILOVER-when-actuall.patch
Patch0372: 0372-posix-fix-seek-functionality.patch
Patch0373: 0373-build-geo-rep-sub-pkg-requires-policycoreutils-pytho.patch
Patch0374: 0374-open-behind-fix-missing-fd-reference.patch
Patch0375: 0375-features-shard-Send-correct-size-when-reads-are-sent.patch
Patch0376: 0376-features-shard-Fix-crash-during-shards-cleanup-in-er.patch
Patch0377: 0377-syncop-improve-scaling-and-implement-more-tools.patch
Patch0378: 0378-Revert-open-behind-fix-missing-fd-reference.patch
Patch0379: 0379-glusterd-add-missing-synccond_broadcast.patch
Patch0380: 0380-features-shard-Aggregate-size-block-count-in-iatt-be.patch
Patch0381: 0381-dht-add-null-check-in-gf_defrag_free_dir_dfmeta.patch
Patch0382: 0382-features-shard-Aggregate-file-size-block-count-befor.patch
Patch0383: 0383-common-ha-ganesha-ha.sh-bad-test-for-rhel-centos-for.patch
Patch0384: 0384-Update-rfc.sh-to-rhgs-3.5.3.patch
Patch0385: 0385-glusterd-start-glusterd-automatically-on-abnormal-sh.patch
Patch0386: 0386-glusterd-increase-the-StartLimitBurst.patch
Patch0387: 0387-To-fix-readdir-ahead-memory-leak.patch
Patch0388: 0388-rpc-Cleanup-SSL-specific-data-at-the-time-of-freeing.patch
Patch0389: 0389-posix-Avoid-diskpace-error-in-case-of-overwriting-th.patch
Patch0390: 0390-glusterd-deafult-options-after-volume-reset.patch
Patch0391: 0391-glusterd-unlink-the-file-after-killing-the-process.patch
Patch0392: 0392-glusterd-Brick-process-fails-to-come-up-with-brickmu.patch
Patch0393: 0393-afr-restore-timestamp-of-files-during-metadata-heal.patch
Patch0394: 0394-man-gluster-Add-volume-top-command-to-gluster-man-pa.patch
Patch0395: 0395-Cli-Removing-old-log-rotate-command.patch
Patch0396: 0396-Updating-gluster-manual.patch
Patch0397: 0397-mgmt-brick-mux-Avoid-sending-two-response-when-attac.patch
Patch0398: 0398-ec-change-error-message-for-heal-commands-for-disper.patch
Patch0399: 0399-glusterd-coverity-fixes.patch
Patch0400: 0400-cli-throw-a-warning-if-replica-count-greater-than-3.patch
Patch0401: 0401-cli-change-the-warning-message.patch
Patch0402: 0402-afr-wake-up-index-healer-threads.patch
Patch0403: 0403-Fix-spurious-failure-in-bug-1744548-heal-timeout.t.patch
Patch0404: 0404-tests-Fix-spurious-failure.patch
Patch0405: 0405-core-fix-return-of-local-in-__nlc_inode_ctx_get.patch
Patch0406: 0406-afr-support-split-brain-CLI-for-replica-3.patch
Patch0407: 0407-geo-rep-Improving-help-message-in-schedule_georep.py.patch
Patch0408: 0408-geo-rep-Fix-ssh-port-validation.patch
Patch0409: 0409-system-posix-acl-update-ctx-only-if-iatt-is-non-NULL.patch
Patch0410: 0410-afr-prevent-spurious-entry-heals-leading-to-gfid-spl.patch
Patch0411: 0411-tools-glusterfind-validate-session-name.patch
Patch0412: 0412-gluster-smb-add-smb-parameter-when-access-gluster-by.patch
Patch0413: 0413-extras-hooks-Remove-smb.conf-parameter-allowing-gues.patch
Patch0414: 0414-cluster-syncop-avoid-duplicate-unlock-of-inodelk-ent.patch
Patch0415: 0415-dht-Fix-stale-layout-and-create-issue.patch
Patch0416: 0416-tests-fix-spurious-failure-of-bug-1402841.t-mt-dir-s.patch
Patch0417: 0417-events-fix-IPv6-memory-corruption.patch
Patch0418: 0418-md-cache-avoid-clearing-cache-when-not-necessary.patch
Patch0419: 0419-cluster-afr-fix-race-when-bricks-come-up.patch
Patch0420: 0420-scripts-quota_fsck-script-TypeError-d-format-not-dic.patch
Patch0421: 0421-Improve-logging-in-EC-client-and-lock-translator.patch
Patch0422: 0422-cluster-afr-Prioritize-ENOSPC-over-other-errors.patch
Patch0423: 0423-ctime-Fix-ctime-inconsisteny-with-utimensat.patch
Patch0424: 0424-afr-make-heal-info-lockless.patch
Patch0425: 0425-tests-Fix-spurious-self-heald.t-failure.patch
Patch0426: 0426-geo-rep-Fix-for-Transport-End-Point-not-connected-is.patch
Patch0427: 0427-storage-posix-Fixing-a-coverity-issue.patch
Patch0428: 0428-glusterd-ganesha-fixing-resource-leak-in-tear_down_c.patch
Patch0429: 0429-dht-rebalance-fixing-failure-occurace-due-to-rebalan.patch
Patch0430: 0430-Fix-some-Null-pointer-dereference-coverity-issues.patch
Patch0431: 0431-glusterd-check-for-same-node-while-adding-bricks-in-.patch
Patch0432: 0432-glusterd-Fix-coverity-defects-put-coverity-annotatio.patch
Patch0433: 0433-socket-Resolve-ssl_ctx-leak-for-a-brick-while-only-m.patch
Patch0434: 0434-glusterd-ganesha-fix-Coverity-CID-1405785.patch
Patch0435: 0435-glusterd-coverity-fix.patch
Patch0436: 0436-glusterd-coverity-fixes.patch
Patch0437: 0437-glusterd-prevent-use-after-free-in-glusterd_op_ac_se.patch
Patch0438: 0438-dht-sparse-files-rebalance-enhancements.patch
Patch0439: 0439-cluster-afr-Delay-post-op-for-fsync.patch
Patch0440: 0440-glusterd-snapshot-Improve-log-message-during-snapsho.patch
Patch0441: 0441-fuse-occasional-logging-for-fuse-device-weird-write-.patch
Patch0442: 0442-fuse-correctly-handle-setxattr-values.patch
Patch0443: 0443-fuse-fix-high-sev-coverity-issue.patch
Patch0444: 0444-mount-fuse-Fixing-a-coverity-issue.patch
Patch0445: 0445-feature-changelog-Avoid-thread-creation-if-xlator-is.patch
Patch0446: 0446-bitrot-Make-number-of-signer-threads-configurable.patch
Patch0447: 0447-core-brick_mux-brick-crashed-when-creating-and-delet.patch
Patch0448: 0448-Posix-Use-simple-approach-to-close-fd.patch
Patch0449: 0449-test-Test-case-brick-mux-validation-in-cluster.t-is-.patch
Patch0450: 0450-tests-basic-ctime-enable-ctime-before-testing.patch
Patch0451: 0451-extras-Modify-group-virt-to-include-network-related-.patch
Patch0452: 0452-Tier-DHT-Handle-the-pause-case-missed-out.patch
Patch0453: 0453-glusterd-add-brick-command-failure.patch
Patch0454: 0454-features-locks-avoid-use-after-freed-of-frame-for-bl.patch
Patch0455: 0455-locks-prevent-deletion-of-locked-entries.patch
Patch0456: 0456-add-clean-local-after-grant-lock.patch
Patch0457: 0457-cluster-ec-Improve-detection-of-new-heals.patch
Patch0458: 0458-features-bit-rot-stub-clean-the-mutex-after-cancelli.patch
Patch0459: 0459-features-bit-rot-Unconditionally-sign-the-files-duri.patch
Patch0460: 0460-cluster-ec-Remove-stale-entries-from-indices-xattrop.patch
Patch0461: 0461-geo-replication-Fix-IPv6-parsing.patch
Patch0462: 0462-Issue-with-gf_fill_iatt_for_dirent.patch
Patch0463: 0463-cluster-ec-Change-handling-of-heal-failure-to-avoid-.patch
Patch0464: 0464-storage-posix-Remove-nr_files-usage.patch
Patch0465: 0465-posix-Implement-a-janitor-thread-to-close-fd.patch
Patch0466: 0466-cluster-ec-Change-stale-index-handling.patch
Patch0467: 0467-build-Added-dependency-for-glusterfs-selinux.patch
Patch0468: 0468-build-Update-the-glusterfs-selinux-version.patch
Patch0469: 0469-cluster-ec-Don-t-trigger-heal-for-stale-index.patch
Patch0470: 0470-extras-snap_scheduler-changes-in-gluster-shared-stor.patch
Patch0471: 0471-nfs-ganesha-gluster_shared_storage-fails-to-automoun.patch
Patch0472: 0472-geo-rep-gluster_shared_storage-fails-to-automount-on.patch
Patch0473: 0473-glusterd-Fix-Add-brick-with-increasing-replica-count.patch
Patch0474: 0474-features-locks-posixlk-clear-lock-should-set-error-a.patch
Patch0475: 0475-fuse-lock-interrupt-fix-flock_interrupt.t.patch
Patch0476: 0476-mount-fuse-use-cookies-to-get-fuse-interrupt-record-.patch
Patch0477: 0477-glusterd-snapshot-Snapshot-prevalidation-failure-not.patch
Patch0478: 0478-DHT-Fixing-rebalance-failure-on-issuing-stop-command.patch
Patch0479: 0479-ganesha-ha-revised-regex-exprs-for-status.patch
Patch0480: 0480-DHT-Rebalance-Ensure-Rebalance-reports-status-only-o.patch
Patch0481: 0481-RHGS-3.5.3-rebuild-to-ship-with-RHEL.patch
Patch0482: 0482-logger-Always-print-errors-in-english.patch
Patch0483: 0483-afr-more-quorum-checks-in-lookup-and-new-entry-marki.patch
Patch0484: 0484-glusterd-rebalance-status-displays-stats-as-0-after-.patch
Patch0485: 0485-cli-rpc-conditional-init-of-global-quota-rpc-1578.patch
Patch0486: 0486-glusterd-brick-sock-file-deleted-log-error-1560.patch
Patch0487: 0487-Events-Log-file-not-re-opened-after-logrotate.patch
Patch0488: 0488-glusterd-afr-enable-granular-entry-heal-by-default.patch
Patch0489: 0489-glusterd-fix-bug-in-enabling-granular-entry-heal.patch
Patch0490: 0490-Segmentation-fault-occurs-during-truncate.patch
Patch0491: 0491-glusterd-mount-directory-getting-truncated-on-mounti.patch
Patch0492: 0492-afr-lookup-Pass-xattr_req-in-while-doing-a-selfheal-.patch
Patch0493: 0493-geo-rep-Note-section-is-required-for-ignore_deletes.patch
Patch0494: 0494-glusterd-start-the-brick-on-a-different-port.patch
Patch0495: 0495-geo-rep-descriptive-message-when-worker-crashes-due-.patch
Patch0496: 0496-posix-Use-MALLOC-instead-of-alloca-to-allocate-memor.patch
Patch0497: 0497-socket-Use-AES128-cipher-in-SSL-if-AES-is-supported-.patch
Patch0498: 0498-geo-rep-Fix-corner-case-in-rename-on-mkdir-during-hy.patch
Patch0499: 0499-gfapi-give-appropriate-error-when-size-exceeds.patch
Patch0500: 0500-features-shard-Convert-shard-block-indices-to-uint64.patch
Patch0501: 0501-Cli-Removing-old-syntax-of-tier-cmds-from-help-menu.patch
Patch0502: 0502-dht-fixing-a-permission-update-issue.patch
Patch0503: 0503-gfapi-Suspend-synctasks-instead-of-blocking-them.patch
Patch0504: 0504-io-stats-Configure-ios_sample_buf_size-based-on-samp.patch
Patch0505: 0505-trash-Create-inode_table-only-while-feature-is-enabl.patch
Patch0506: 0506-posix-Attach-a-posix_spawn_disk_thread-with-glusterf.patch
Patch0507: 0507-inode-make-critical-section-smaller.patch
Patch0508: 0508-fuse-fetch-arbitrary-number-of-groups-from-proc-pid-.patch
Patch0509: 0509-core-configure-optimum-inode-table-hash_size-for-shd.patch
Patch0510: 0510-glusterd-brick_mux-Optimize-friend-handshake-code-to.patch
Patch0511: 0511-features-shard-Missing-format-specifier.patch
Patch0512: 0512-glusterd-shared-storage-mount-fails-in-ipv6-environm.patch
Patch0513: 0513-afr-mark-pending-xattrs-as-a-part-of-metadata-heal.patch
Patch0514: 0514-afr-event-gen-changes.patch
Patch0515: 0515-cluster-afr-Heal-directory-rename-without-rmdir-mkdi.patch
Patch0516: 0516-afr-return-EIO-for-gfid-split-brains.patch
Patch0517: 0517-gfapi-glfs_h_creat_open-new-API-to-create-handle-and.patch
Patch0518: 0518-glusterd-Fix-for-shared-storage-in-ipv6-env.patch
Patch0519: 0519-glusterfs-events-Fix-incorrect-attribute-access-2002.patch
Patch0520: 0520-performance-open-behind-seek-fop-should-open_and_res.patch
Patch0521: 0521-open-behind-fix-missing-fd-reference.patch
Patch0522: 0522-lcov-improve-line-coverage.patch
Patch0523: 0523-open-behind-rewrite-of-internal-logic.patch
Patch0524: 0524-open-behind-fix-call_frame-leak.patch
Patch0525: 0525-open-behind-implement-create-fop.patch
Patch0526: 0526-Quota-quota_fsck.py-converting-byte-string-to-string.patch
Patch0527: 0527-Events-Socket-creation-after-getaddrinfo-and-IPv4-an.patch
Patch0528: 0528-Extras-Removing-xattr_analysis-script.patch
Patch0529: 0529-geo-rep-prompt-should-work-for-ignore_deletes.patch
Patch0530: 0530-gfapi-avoid-crash-while-logging-message.patch
Patch0531: 0531-Glustereventsd-Default-port-change-2091.patch
Patch0532: 0532-glusterd-fix-for-starting-brick-on-new-port.patch
Patch0533: 0533-glusterd-Rebalance-cli-is-not-showing-correct-status.patch
Patch0534: 0534-glusterd-Resolve-use-after-free-bug-2181.patch
Patch0535: 0535-multiple-files-use-dict_allocate_and_serialize-where.patch
Patch0536: 0536-dht-Ongoing-IO-is-failed-during-volume-shrink-operat.patch
Patch0537: 0537-cluster-afr-Fix-race-in-lockinfo-f-getxattr.patch
Patch0538: 0538-afr-fix-coverity-issue-introduced-by-90cefde.patch
Patch0539: 0539-extras-disable-lookup-optimize-in-virt-and-block-gro.patch
Patch0540: 0540-extras-Disable-write-behind-for-group-samba.patch
Patch0541: 0541-glusterd-volgen-Add-functionality-to-accept-any-cust.patch
Patch0542: 0542-xlaotrs-mgmt-Fixing-coverity-issue-1445996.patch
Patch0543: 0543-glusterd-handle-custom-xlator-failure-cases.patch
Patch0900: 0900-rhel-9.0-beta-build-fixing-gcc-10-and-LTO-errors.patch
Patch0901: 0901-contrib-remove-contrib-sunrpc-xdr_sizeof.c.patch

%description
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package includes the glusterfs binary, the glusterfsd daemon and the
libglusterfs and glusterfs translator modules common to both GlusterFS server
and client framework.

%package api
Summary:          GlusterFS api library
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-client-xlators%{?_isa} = %{version}-%{release}
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}

%description api
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the glusterfs libgfapi library.

%package api-devel
Summary:          Development Libraries
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-devel%{?_isa} = %{version}-%{release}
Requires:         libacl-devel
Requires:         %{name}-api%{?_isa} = %{version}-%{release}

%description api-devel
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the api include files.

%package cli
Summary:          GlusterFS CLI
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}

%description cli
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the GlusterFS CLI application and its man page

%package cloudsync-plugins
Summary:          Cloudsync Plugins
BuildRequires:    libcurl-devel
Requires:         glusterfs-libs = %{version}-%{release}

%description cloudsync-plugins
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides cloudsync plugins for archival feature.

%package devel
Summary:          Development Libraries
Requires:         %{name}%{?_isa} = %{version}-%{release}
# Needed for the Glupy examples to work
%if ( 0%{!?_without_extra_xlators:1} )
Requires:         %{name}-extra-xlators%{?_isa} = %{version}-%{release}
%endif
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}
%if ( 0%{!?_without_server:1} )
Requires:         %{name}-server%{?_isa} = %{version}-%{release}
%endif

%description devel
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the development libraries and include files.

%if ( 0%{!?_without_extra_xlators:1} )
%package extra-xlators
Summary:          Extra Gluster filesystem Translators
# We need python-gluster rpm for gluster module's __init__.py in Python
# site-packages area
Requires:         python%{_pythonver}-gluster = %{version}-%{release}
Requires:         python%{_pythonver}

%description extra-xlators
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides extra filesystem Translators, such as Glupy,
for GlusterFS.
%endif

%package fuse
Summary:          Fuse client
BuildRequires:    fuse-devel
Requires:         attr
Requires:         psmisc

Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-client-xlators%{?_isa} = %{version}-%{release}

Obsoletes:        %{name}-client < %{version}-%{release}
Provides:         %{name}-client = %{version}-%{release}
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}

%description fuse
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides support to FUSE based clients and inlcudes the
glusterfs(d) binary.

%if ( 0%{!?_without_server:1} && 0%{?rhel} > 6 )
%package ganesha
Summary:          NFS-Ganesha configuration
Group:            Applications/File

Requires:         %{name}-server%{?_isa} = %{version}-%{release}
Requires:         nfs-ganesha-selinux >= 2.7.3
Requires:         nfs-ganesha-gluster >= 2.7.3
Requires:         pcs, dbus
%if ( 0%{?rhel} && 0%{?rhel} == 6 )
Requires:         cman, pacemaker, corosync
%endif

%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} > 5 )
# we need portblock resource-agent in 3.9.5 and later.
Requires:         resource-agents >= 3.9.5
Requires:         net-tools
%endif

%if ( 0%{?fedora} && 0%{?fedora} > 25  || ( 0%{?rhel} && 0%{?rhel} > 6 ) )
%if ( 0%{?rhel} && 0%{?rhel} < 8 )
Requires: selinux-policy >= 3.13.1-160
Requires(post):   policycoreutils-python
Requires(postun): policycoreutils-python
%else
Requires(post):   policycoreutils-python-utils
Requires(postun): policycoreutils-python-utils
%endif
%endif

%description ganesha
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the configuration and related files for using
NFS-Ganesha as the NFS server using GlusterFS
%endif

%if ( 0%{!?_without_georeplication:1} )
%package geo-replication
Summary:          GlusterFS Geo-replication
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-server%{?_isa} = %{version}-%{release}
Requires:         python%{_pythonver}
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
Requires:         python-prettytable
%else
Requires:         python%{_pythonver}-prettytable
%endif
Requires:         python%{_pythonver}-gluster = %{version}-%{release}

Requires:         rsync
Requires:         util-linux
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}
# required for setting selinux bools
%if ( 0%{?rhel} && 0%{?rhel} >= 8 )
Requires(post):      policycoreutils-python-utils
Requires(postun):    policycoreutils-python-utils
Requires:            selinux-policy-targeted
Requires(post):      selinux-policy-targeted
BuildRequires:       selinux-policy-devel
%endif

%description geo-replication
GlusterFS is a distributed file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

This package provides support to geo-replication.
%endif

%package libs
Summary:          GlusterFS common libraries

%description libs
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the base GlusterFS libraries

%package -n python%{_pythonver}-gluster
Summary:          GlusterFS python library
Requires:         python%{_pythonver}
%if ( ! %{_usepython3} )
%{?python_provide:%python_provide python-gluster}
Provides:         python-gluster = %{version}-%{release}
Obsoletes:        python-gluster < 3.10
%endif

%description -n python%{_pythonver}-gluster
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package contains the python modules of GlusterFS and own gluster
namespace.

%if ( 0%{!?_without_rdma:1} )
%package rdma
Summary:          GlusterFS rdma support for ib-verbs
%if ( 0%{?fedora} && 0%{?fedora} > 26 )
BuildRequires:    rdma-core-devel
%else
BuildRequires:    libibverbs-devel
BuildRequires:    librdmacm-devel >= 1.0.15
%endif
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}

%description rdma
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides support to ib-verbs library.
%endif

%if ( 0%{!?_without_regression_tests:1} )
%package regression-tests
Summary:          Development Tools
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-fuse%{?_isa} = %{version}-%{release}
Requires:         %{name}-server%{?_isa} = %{version}-%{release}
## thin provisioning support
Requires:         lvm2 >= 2.02.89
Requires:         perl(App::Prove) perl(Test::Harness) gcc util-linux-ng
Requires:         python%{_pythonver}
Requires:         attr dbench file git libacl-devel net-tools
Requires:         nfs-utils xfsprogs yajl psmisc bc

%description regression-tests
The Gluster Test Framework, is a suite of scripts used for
regression testing of Gluster.
%endif

%if ( 0%{!?_without_ocf:1} )
%package resource-agents
Summary:          OCF Resource Agents for GlusterFS
License:          GPLv3+
BuildArch:        noarch
# this Group handling comes from the Fedora resource-agents package
# for glusterd
Requires:         %{name}-server = %{version}-%{release}
# depending on the distribution, we need pacemaker or resource-agents
Requires:         %{_prefix}/lib/ocf/resource.d

%description resource-agents
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the resource agents which plug glusterd into
Open Cluster Framework (OCF) compliant cluster resource managers,
like Pacemaker.
%endif

%if ( 0%{!?_without_server:1} )
%package server
Summary:          Clustered file-system server
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-cli%{?_isa} = %{version}-%{release}
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}
%if ( 0%{?fedora} && 0%{?fedora} >= 30  || ( 0%{?rhel} && 0%{?rhel} >= 8 ) )
Requires:         glusterfs-selinux >= 1.0-1
%endif
# some daemons (like quota) use a fuse-mount, glusterfsd is part of -fuse
Requires:         %{name}-fuse%{?_isa} = %{version}-%{release}
# self-heal daemon, rebalance, nfs-server etc. are actually clients
Requires:         %{name}-api%{?_isa} = %{version}-%{release}
Requires:         %{name}-client-xlators%{?_isa} = %{version}-%{release}
# lvm2 for snapshot, and nfs-utils and rpcbind/portmap for gnfs server
Requires:         lvm2
Requires:         nfs-utils
%if ( 0%{?_with_systemd:1} )
%{?systemd_requires}
%else
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/service
Requires(preun):  /sbin/chkconfig
Requires(postun): /sbin/service
%endif
%if (0%{?_with_firewalld:1})
# we install firewalld rules, so we need to have the directory owned
%if ( 0%{!?rhel} )
# not on RHEL because firewalld-filesystem appeared in 7.3
# when EL7 rpm gets weak dependencies we can add a Suggests:
Requires:         firewalld-filesystem
%endif
%endif
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 )
Requires:         rpcbind
%else
Requires:         portmap
%endif
%if ( 0%{?rhel} && 0%{?rhel} <= 6 )
Requires:         python-argparse
%endif
%if ( 0%{?fedora} && 0%{?fedora} > 27 ) || ( 0%{?rhel} && 0%{?rhel} > 7 )
Requires:         python%{_pythonver}-pyxattr
%else
Requires:         pyxattr
%endif
%if (0%{?_with_valgrind:1})
Requires:         valgrind
%endif

%description server
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the glusterfs server daemon.
%endif

%package client-xlators
Summary:          GlusterFS client-side translators
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}

%description client-xlators
GlusterFS is a distributed file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the translators needed on any GlusterFS client.

%if ( 0%{!?_without_events:1} )
%package events
Summary:          GlusterFS Events
Requires:         %{name}-server%{?_isa} = %{version}-%{release}
Requires:         python%{_pythonver}
Requires:         python%{_pythonver}-gluster = %{version}-%{release}
%if ( 0%{?rhel} && 0%{?rhel} < 8 )
Requires:         python-requests
%else
Requires:         python%{_pythonver}-requests
%endif
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
Requires:         python-prettytable
Requires:         python-argparse
%else
Requires:         python%{_pythonver}-prettytable
%endif
%if ( 0%{?_with_systemd:1} )
%{?systemd_requires}
%endif

%description events
GlusterFS Events

%endif

%prep
%setup -q -n %{name}-%{version}%{?prereltag}

# sanitization scriptlet for patches with file renames
ls %{_topdir}/SOURCES/*.patch | sort | \
while read p
do
    # if the destination file exists, its most probably stale
    # so we must remove it
    rename_to=( $(grep -i 'rename to' $p | cut -f 3 -d ' ') )
    if [ ${#rename_to[*]} -gt 0 ]; then
        for f in ${rename_to[*]}
        do
            if [ -f $f ]; then
                rm -f $f
            elif [ -d $f ]; then
                rm -rf $f
            fi
        done
    fi

    SOURCE_FILES=( $(egrep '^\-\-\- a/' $p | cut -f 2- -d '/') )
    DEST_FILES=( $(egrep '^\+\+\+ b/' $p | cut -f 2- -d '/') )
    EXCLUDE_DOCS=()
    for idx in ${!SOURCE_FILES[@]}; do
        # skip the doc
        source_file=${SOURCE_FILES[$idx]}
        dest_file=${DEST_FILES[$idx]}
        if [[ "$dest_file" =~ ^doc/.+ ]]; then
            if [ "$source_file" != "dev/null" ] && [ ! -f "$dest_file" ]; then
                # if patch is being applied to a doc file and if the doc file
                # hasn't been added so far then we need to exclude it
                EXCLUDE_DOCS=( ${EXCLUDE_DOCS[*]} "$dest_file" )
            fi
        fi
    done
    EXCLUDE_DOCS_OPT=""
    for doc in ${EXCLUDE_DOCS}; do
        EXCLUDE_DOCS_OPT="--exclude=$doc $EXCLUDE_DOCS_OPT"
    done

    # HACK to fix build
    bn=$(basename $p)
    if [ "$bn" == "0085-Revert-all-remove-code-which-is-not-being-considered.patch" ]; then
        (patch -p1 -u -F3 < $p || :)
        if [ -f libglusterfs/Makefile.am.rej ]; then
            sed -i -e 's/^SUBDIRS = src/SUBDIRS = src src\/gfdb/g;s/^CLEANFILES = /CLEANFILES =/g' libglusterfs/Makefile.am
        fi
    elif [ "$bn" == "0053-Revert-packaging-ganesha-remove-glusterfs-ganesha-su.patch" ]; then
        (patch -p1 < $p || :)
    elif [ "$bn" == "0055-Revert-storhaug-HA-first-step-remove-resource-agents.patch" ]; then
        (patch -p1 < $p || :)
    elif [ "$bn" == "0090-Revert-build-conditionally-build-legacy-gNFS-server-.patch" ]; then
        (patch -p1 < $p || :)
    elif [ "$bn" == "0117-spec-Remove-thin-arbiter-package.patch" ]; then
        (patch -p1 < $p || :)
    elif [ "$bn" == "0023-hooks-remove-selinux-hooks.patch" ]; then
        (patch -p1 < $p || :)
    elif [ "$bn" == "0042-spec-client-server-Builds-are-failing-on-rhel-6.patch" ]; then
        (patch -p1 < $p || :)
    else
        # apply the patch with 'git apply'
        git apply -p1 --exclude=rfc.sh \
                      --exclude=.gitignore \
                      --exclude=.testignore \
                      --exclude=MAINTAINERS \
                      --exclude=extras/checkpatch.pl \
                      --exclude=build-aux/checkpatch.pl \
                      --exclude='tests/*' \
                      ${EXCLUDE_DOCS_OPT} \
                      $p
    fi

done

echo "fixing python shebangs..."
%if ( %{_usepython3} )
    for i in `find . -type f -exec bash -c "if file {} | grep 'Python script, ASCII text executable' >/dev/null; then echo {}; fi" ';'`; do
        sed -i -e 's|^#!/usr/bin/python.*|#!%{__python3}|' -e 's|^#!/usr/bin/env python.*|#!%{__python3}|' $i
    done
%else
    for f in api events extras geo-replication libglusterfs tools xlators; do
        find $f -type f -exec sed -i 's|/usr/bin/python3|/usr/bin/python2|' {} \;
    done
%endif

%build

# In RHEL7 few hardening flags are available by default, however the RELRO
# default behaviour is partial, convert to full
%if ( 0%{?rhel} && 0%{?rhel} >= 7 )
LDFLAGS="$RPM_LD_FLAGS -Wl,-z,relro,-z,now"
export LDFLAGS
%else
%if ( 0%{?rhel} && 0%{?rhel} == 6 )
CFLAGS="$RPM_OPT_FLAGS -fPIE -DPIE"
LDFLAGS="$RPM_LD_FLAGS -pie -Wl,-z,relro,-z,now"
%else
#It appears that with gcc-4.1.2 in RHEL5 there is an issue using both -fPIC and
 # -fPIE that makes -z relro not work; -fPIE seems to undo what -fPIC does
CFLAGS="$CFLAGS $RPM_OPT_FLAGS"
LDFLAGS="$RPM_LD_FLAGS -Wl,-z,relro,-z,now"
%endif
export CFLAGS
export LDFLAGS
%endif

./autogen.sh && %configure \
        %{?_with_asan} \
        %{?_with_cmocka} \
        %{?_with_debug} \
        %{?_with_firewalld} \
        %{?_with_tmpfilesdir} \
        %{?_with_tsan} \
        %{?_with_valgrind} \
        %{?_without_epoll} \
        %{?_without_events} \
        %{?_without_fusermount} \
        %{?_without_georeplication} \
        %{?_without_ocf} \
        %{?_without_rdma} \
        %{?_without_server} \
        %{?_without_syslog} \
        %{?_without_tiering} \
        %{?_with_ipv6default} \
        %{?_without_libtirpc}

# fix hardening and remove rpath in shlibs
%if ( 0%{?fedora} && 0%{?fedora} > 17 ) || ( 0%{?rhel} && 0%{?rhel} > 6 )
sed -i 's| \\\$compiler_flags |&\\\$LDFLAGS |' libtool
%endif
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|' libtool

make %{?_smp_mflags}

%check
make check

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
%if ( 0%{!?_without_server:1} )
%if ( 0%{_for_fedora_koji_builds} )
install -D -p -m 0644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/sysconfig/glusterd
install -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/sysconfig/glusterfsd
%else
install -D -p -m 0644 extras/glusterd-sysconfig \
    %{buildroot}%{_sysconfdir}/sysconfig/glusterd
%endif
%endif

mkdir -p %{buildroot}%{_localstatedir}/log/glusterd
mkdir -p %{buildroot}%{_localstatedir}/log/glusterfs
mkdir -p %{buildroot}%{_localstatedir}/log/glusterfsd
mkdir -p %{buildroot}%{_rundir}/gluster

# Remove unwanted files from all the shared libraries
find %{buildroot}%{_libdir} -name '*.a' -delete
find %{buildroot}%{_libdir} -name '*.la' -delete

# Remove installed docs, the ones we want are included by %%doc, in
# /usr/share/doc/glusterfs or /usr/share/doc/glusterfs-x.y.z depending
# on the distribution
%if ( 0%{?fedora} && 0%{?fedora} > 19 ) || ( 0%{?rhel} && 0%{?rhel} > 6 )
rm -rf %{buildroot}%{_pkgdocdir}/*
%else
rm -rf %{buildroot}%{_defaultdocdir}/%{name}
mkdir -p %{buildroot}%{_pkgdocdir}
%endif
head -50 ChangeLog > ChangeLog.head && mv ChangeLog.head ChangeLog
cat << EOM >> ChangeLog

More commit messages for this ChangeLog can be found at
https://forge.gluster.org/glusterfs-core/glusterfs/commits/v%{version}%{?prereltag}
EOM

# Remove benchmarking and other unpackaged files
# make install always puts these in %%{_defaultdocdir}/%%{name} so don't
# use %%{_pkgdocdir}; that will be wrong on later Fedora distributions
rm -rf %{buildroot}%{_defaultdocdir}/%{name}/benchmarking
rm -f %{buildroot}%{_defaultdocdir}/%{name}/glusterfs-mode.el
rm -f %{buildroot}%{_defaultdocdir}/%{name}/glusterfs.vim

%if ( 0%{!?_without_server:1} )
# Create working directory
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd

# Update configuration file to /var/lib working directory
sed -i 's|option working-directory /etc/glusterd|option working-directory %{_sharedstatedir}/glusterd|g' \
    %{buildroot}%{_sysconfdir}/glusterfs/glusterd.vol
%endif

# Install glusterfsd .service or init.d file
%if ( 0%{!?_without_server:1} )
%if ( 0%{_for_fedora_koji_builds} )
%service_install glusterfsd %{glusterfsd_svcfile}
%endif
%endif

install -D -p -m 0644 extras/glusterfs-logrotate \
    %{buildroot}%{_sysconfdir}/logrotate.d/glusterfs

# ganesha ghosts
%if ( 0%{!?_without_server:1} && 0%{?rhel} > 6 )
mkdir -p %{buildroot}%{_sysconfdir}/ganesha
touch %{buildroot}%{_sysconfdir}/ganesha/ganesha-ha.conf
mkdir -p %{buildroot}%{_localstatedir}/run/gluster/shared_storage/nfs-ganesha/
touch %{buildroot}%{_localstatedir}/run/gluster/shared_storage/nfs-ganesha/ganesha.conf
touch %{buildroot}%{_localstatedir}/run/gluster/shared_storage/nfs-ganesha/ganesha-ha.conf
%endif

%if ( 0%{!?_without_georeplication:1} )
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/geo-replication
touch %{buildroot}%{_sharedstatedir}/glusterd/geo-replication/gsyncd_template.conf
install -D -p -m 0644 extras/glusterfs-georep-logrotate \
    %{buildroot}%{_sysconfdir}/logrotate.d/glusterfs-georep
%endif

%if ( 0%{!?_without_server:1} )
touch %{buildroot}%{_sharedstatedir}/glusterd/glusterd.info
touch %{buildroot}%{_sharedstatedir}/glusterd/options
subdirs=(add-brick create copy-file delete gsync-create remove-brick reset set start stop)
for dir in ${subdirs[@]}; do
    mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/"$dir"/{pre,post}
done
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/glustershd
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/peers
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/vols
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/nfs/run
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/bitd
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/quotad
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/scrub
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/snaps
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/ss_brick
touch %{buildroot}%{_sharedstatedir}/glusterd/nfs/nfs-server.vol
touch %{buildroot}%{_sharedstatedir}/glusterd/nfs/run/nfs.pid
%endif

find ./tests ./run-tests.sh -type f | cpio -pd %{buildroot}%{_prefix}/share/glusterfs

## Install bash completion for cli
install -p -m 0744 -D extras/command-completion/gluster.bash \
    %{buildroot}%{_sysconfdir}/bash_completion.d/gluster

%if ( 0%{!?_without_server:1} )
echo "RHGS 3.5" > %{buildroot}%{_datadir}/glusterfs/release
%endif

%clean
rm -rf %{buildroot}

##-----------------------------------------------------------------------------
## All %%post should be placed here and keep them sorted
##
%post
/sbin/ldconfig
%if ( 0%{!?_without_syslog:1} )
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 )
%systemd_postun_with_restart rsyslog
%endif
%endif
exit 0

%post api
/sbin/ldconfig

%if ( 0%{!?_without_events:1} )
%post events
%service_enable glustereventsd
%endif

%if ( 0%{!?_without_server:1} )
%if ( 0%{?fedora} && 0%{?fedora} > 25 || ( 0%{?rhel} && 0%{?rhel} > 6 ) )
%post ganesha
semanage boolean -m ganesha_use_fusefs --on
exit 0
%endif
%endif

%if ( 0%{!?_without_georeplication:1} )
%post geo-replication
%if ( 0%{?rhel} && 0%{?rhel} >= 8 )
%selinux_set_booleans %{selinuxbooleans}
%endif
if [ $1 -ge 1 ]; then
    %systemd_postun_with_restart glusterd
fi
exit 0
%endif

%post libs
/sbin/ldconfig

%if ( 0%{!?_without_server:1} )
%post server
# Legacy server
%service_enable glusterd
%if ( 0%{_for_fedora_koji_builds} )
%service_enable glusterfsd
%endif
# ".cmd_log_history" is renamed to "cmd_history.log" in GlusterFS-3.7 .
# While upgrading glusterfs-server package form GlusterFS version <= 3.6 to
# GlusterFS version 3.7, ".cmd_log_history" should be renamed to
# "cmd_history.log" to retain cli command history contents.
if [ -f %{_localstatedir}/log/glusterfs/.cmd_log_history ]; then
    mv %{_localstatedir}/log/glusterfs/.cmd_log_history \
       %{_localstatedir}/log/glusterfs/cmd_history.log
fi

# Genuine Fedora (and EPEL) builds never put gluster files in /etc; if
# there are any files in /etc from a prior gluster.org install, move them
# to /var/lib. (N.B. Starting with 3.3.0 all gluster files are in /var/lib
# in gluster.org RPMs.) Be careful to copy them on the off chance that
# /etc and /var/lib are on separate file systems
if [ -d /etc/glusterd -a ! -h %{_sharedstatedir}/glusterd ]; then
    mkdir -p %{_sharedstatedir}/glusterd
    cp -a /etc/glusterd %{_sharedstatedir}/glusterd
    rm -rf /etc/glusterd
    ln -sf %{_sharedstatedir}/glusterd /etc/glusterd
fi

# Rename old volfiles in an RPM-standard way.  These aren't actually
# considered package config files, so %%config doesn't work for them.
if [ -d %{_sharedstatedir}/glusterd/vols ]; then
    for file in $(find %{_sharedstatedir}/glusterd/vols -name '*.vol'); do
        newfile=${file}.rpmsave
        echo "warning: ${file} saved as ${newfile}"
        cp ${file} ${newfile}
    done
fi

# add marker translator
# but first make certain that there are no old libs around to bite us
# BZ 834847
if [ -e /etc/ld.so.conf.d/glusterfs.conf ]; then
    rm -f /etc/ld.so.conf.d/glusterfs.conf
    /sbin/ldconfig
fi

%if (0%{?_with_firewalld:1})
    %firewalld_reload
%endif

%endif

##-----------------------------------------------------------------------------
## All %%pre should be placed here and keep them sorted
##
%pre
getent group gluster > /dev/null || groupadd -r gluster
getent passwd gluster > /dev/null || useradd -r -g gluster -d %{_rundir}/gluster -s /sbin/nologin -c "GlusterFS daemons" gluster
exit 0

##-----------------------------------------------------------------------------
## All %%preun should be placed here and keep them sorted
##
%if ( 0%{!?_without_events:1} )
%preun events
if [ $1 -eq 0 ]; then
    if [ -f %glustereventsd_svcfile ]; then
        %service_stop glustereventsd
        %systemd_preun glustereventsd
    fi
fi
exit 0
%endif

%if ( 0%{!?_without_server:1} )
%preun server
if [ $1 -eq 0 ]; then
    if [ -f %glusterfsd_svcfile ]; then
        %service_stop glusterfsd
    fi
    %service_stop glusterd
    if [ -f %glusterfsd_svcfile ]; then
        %systemd_preun glusterfsd
    fi
    %systemd_preun glusterd
fi
if [ $1 -ge 1 ]; then
    if [ -f %glusterfsd_svcfile ]; then
        %systemd_postun_with_restart glusterfsd
    fi
    %systemd_postun_with_restart glusterd
fi
exit 0
%endif

##-----------------------------------------------------------------------------
## All %%postun should be placed here and keep them sorted
##
%postun
%if ( 0%{!?_without_syslog:1} )
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 )
%systemd_postun_with_restart rsyslog
%endif
%endif

%if ( 0%{!?_without_server:1} )
%postun server
%if (0%{?_with_firewalld:1})
    %firewalld_reload
%endif
exit 0
%endif

%if ( 0%{!?_without_server:1} )
%if ( 0%{?fedora} && 0%{?fedora} > 25  || ( 0%{?rhel} && 0%{?rhel} > 6 ) )
%postun ganesha
semanage boolean -m ganesha_use_fusefs --off
exit 0
%endif
%endif

##-----------------------------------------------------------------------------
## All %%trigger should be placed here and keep them sorted
##
%if ( 0%{!?_without_server:1} )
%if ( 0%{?fedora} && 0%{?fedora} > 25  || ( 0%{?rhel} && 0%{?rhel} > 6 ) )
%trigger ganesha -- selinux-policy-targeted
semanage boolean -m ganesha_use_fusefs --on
exit 0
%endif
%endif

##-----------------------------------------------------------------------------
## All %%triggerun should be placed here and keep them sorted
##
%if ( 0%{!?_without_server:1} )
%if ( 0%{?fedora} && 0%{?fedora} > 25  || ( 0%{?rhel} && 0%{?rhel} > 6 ) )
%triggerun ganesha -- selinux-policy-targeted
semanage boolean -m ganesha_use_fusefs --off
exit 0
%endif
%endif

##-----------------------------------------------------------------------------
## All %%files should be placed here and keep them grouped
##
%files
%doc ChangeLog COPYING-GPLV2 COPYING-LGPLV3 INSTALL README.md THANKS COMMITMENT
%{_mandir}/man8/*gluster*.8*
%if ( 0%{!?_without_server:1} )
%exclude %{_mandir}/man8/gluster.8*
%endif
%dir %{_localstatedir}/log/glusterfs
%if ( 0%{!?_without_rdma:1} )
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/rpc-transport/rdma*
%endif
%if 0%{?!_without_server:1}
%dir %{_datadir}/glusterfs
%dir %{_datadir}/glusterfs/scripts
     %{_datadir}/glusterfs/scripts/post-upgrade-script-for-quota.sh
     %{_datadir}/glusterfs/scripts/pre-upgrade-script-for-quota.sh
%endif
%{_datadir}/glusterfs/scripts/identify-hangs.sh
%{_datadir}/glusterfs/scripts/collect-system-stats.sh
%{_datadir}/glusterfs/scripts/log_accounting.sh
# xlators that are needed on the client- and on the server-side
%dir %{_libdir}/glusterfs
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/auth
     %{_libdir}/glusterfs/%{version}%{?prereltag}/auth/addr.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/auth/login.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/rpc-transport
     %{_libdir}/glusterfs/%{version}%{?prereltag}/rpc-transport/socket.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/debug
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/debug/error-gen.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/debug/delay-gen.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/debug/io-stats.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/debug/sink.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/debug/trace.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/access-control.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/barrier.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/cdc.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/changelog.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/utime.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/gfid-access.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/namespace.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/read-only.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/shard.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/snapview-client.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/worm.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/cloudsync.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/meta.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/io-cache.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/io-threads.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/md-cache.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/open-behind.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/quick-read.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/read-ahead.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/readdir-ahead.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/stat-prefetch.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/write-behind.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/nl-cache.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/system
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/system/posix-acl.so
%dir %attr(0775,gluster,gluster) %{_rundir}/gluster
%if 0%{?_tmpfilesdir:1} && 0%{!?_without_server:1}
%{_tmpfilesdir}/gluster.conf
%endif
%if ( 0%{?_without_extra_xlators:1} )
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/quiesce.so
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/playground/template.so
%endif
%if ( 0%{?_without_regression_tests:1} )
%exclude %{_datadir}/glusterfs/run-tests.sh
%exclude %{_datadir}/glusterfs/tests
%endif
%if 0%{?_without_server:1}
%if ( 0%{?_with_systemd:1} )
%exclude %{_datadir}/glusterfs/scripts/control-cpu-load.sh
%exclude %{_datadir}/glusterfs/scripts/control-mem.sh
%endif
%endif

%if ( 0%{?_without_server:1} || 0%{?rhel} < 7 )
#exclude ganesha related files for rhel 6 and client builds
%exclude %{_sysconfdir}/ganesha/ganesha-ha.conf.sample
%exclude %{_libexecdir}/ganesha/*
%exclude %{_prefix}/lib/ocf/resource.d/heartbeat/*
%if ( 0%{!?_without_server:1} )
%{_sharedstatedir}/glusterd/hooks/1/start/post/S31ganesha-start.sh
%endif
%endif

%exclude %{_datadir}/glusterfs/scripts/setup-thin-arbiter.sh

%if ( 0%{?_without_server:1} )
%exclude %{_sysconfdir}/glusterfs/thin-arbiter.vol
%endif

%files api
%exclude %{_libdir}/*.so
# libgfapi files
%{_libdir}/libgfapi.*
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mount
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mount/api.so

%files api-devel
%{_libdir}/pkgconfig/glusterfs-api.pc
%{_libdir}/libgfapi.so
%dir %{_includedir}/glusterfs
%dir %{_includedir}/glusterfs/api
     %{_includedir}/glusterfs/api/*

%files cli
%{_sbindir}/gluster
%{_mandir}/man8/gluster.8*
%{_sysconfdir}/bash_completion.d/gluster

%files cloudsync-plugins
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/cloudsync-plugins
     %{_libdir}/glusterfs/%{version}%{?prereltag}/cloudsync-plugins/cloudsyncs3.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/cloudsync-plugins/cloudsynccvlt.so

%files devel
%dir %{_includedir}/glusterfs
     %{_includedir}/glusterfs/*
%exclude %{_includedir}/glusterfs/api
%exclude %{_libdir}/libgfapi.so
%{_libdir}/*.so
%if ( 0%{?_without_server:1} )
%exclude %{_libdir}/pkgconfig/libgfchangelog.pc
%exclude %{_libdir}/libgfchangelog.so
%if ( 0%{!?_without_tiering:1} )
%exclude %{_libdir}/pkgconfig/libgfdb.pc
%endif
%else
%{_libdir}/pkgconfig/libgfchangelog.pc
%if ( 0%{!?_without_tiering:1} )
%{_libdir}/pkgconfig/libgfdb.pc
%endif
%endif

%files client-xlators
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/cluster
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/cluster/*.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/protocol
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/protocol/client.so

%if ( 0%{!?_without_extra_xlators:1} )
%files extra-xlators
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/quiesce.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/playground
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/playground/template.so
%endif

%files fuse
# glusterfs is a symlink to glusterfsd, -server depends on -fuse.
%{_sbindir}/glusterfs
%{_sbindir}/glusterfsd
%config(noreplace) %{_sysconfdir}/logrotate.d/glusterfs
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mount
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mount/fuse.so
/sbin/mount.glusterfs
%if ( 0%{!?_without_fusermount:1} )
%{_bindir}/fusermount-glusterfs
%endif

%if ( 0%{!?_without_georeplication:1} )
%files geo-replication
%config(noreplace) %{_sysconfdir}/logrotate.d/glusterfs-georep

%{_sbindir}/gfind_missing_files
%{_sbindir}/gluster-mountbroker
%dir %{_libexecdir}/glusterfs
%dir %{_libexecdir}/glusterfs/python
%dir %{_libexecdir}/glusterfs/python/syncdaemon
     %{_libexecdir}/glusterfs/gsyncd
     %{_libexecdir}/glusterfs/python/syncdaemon/*
     %{_libexecdir}/glusterfs/gverify.sh
     %{_libexecdir}/glusterfs/set_geo_rep_pem_keys.sh
     %{_libexecdir}/glusterfs/peer_gsec_create
     %{_libexecdir}/glusterfs/peer_mountbroker
     %{_libexecdir}/glusterfs/peer_mountbroker.py*
     %{_libexecdir}/glusterfs/gfind_missing_files
     %{_libexecdir}/glusterfs/peer_georep-sshkey.py*
%{_sbindir}/gluster-georep-sshkey

       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/geo-replication
%ghost      %attr(0644,-,-) %{_sharedstatedir}/glusterd/geo-replication/gsyncd_template.conf
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/gsync-create
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/gsync-create/post
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/gsync-create/post/S56glusterd-geo-rep-create-post.sh
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/gsync-create/pre

%dir %{_datadir}/glusterfs
%dir %{_datadir}/glusterfs/scripts
     %{_datadir}/glusterfs/scripts/get-gfid.sh
     %{_datadir}/glusterfs/scripts/slave-upgrade.sh
     %{_datadir}/glusterfs/scripts/gsync-upgrade.sh
     %{_datadir}/glusterfs/scripts/generate-gfid-file.sh
     %{_datadir}/glusterfs/scripts/gsync-sync-gfid
     %{_datadir}/glusterfs/scripts/schedule_georep.py*
%endif

%files libs
%{_libdir}/*.so.*
%exclude %{_libdir}/libgfapi.*
%if ( 0%{!?_without_tiering:1} )
# libgfdb is only needed server-side
%exclude %{_libdir}/libgfdb.*
%endif

%files -n python%{_pythonver}-gluster
# introducing glusterfs module in site packages.
# so that all other gluster submodules can reside in the same namespace.
%if ( %{_usepython3} )
%dir %{python3_sitelib}/gluster
     %{python3_sitelib}/gluster/__init__.*
     %{python3_sitelib}/gluster/__pycache__
     %{python3_sitelib}/gluster/cliutils
%else
%dir %{python2_sitelib}/gluster
     %{python2_sitelib}/gluster/__init__.*
     %{python2_sitelib}/gluster/cliutils
%endif

%if ( 0%{!?_without_rdma:1} )
%files rdma
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/rpc-transport
     %{_libdir}/glusterfs/%{version}%{?prereltag}/rpc-transport/rdma*
%endif

%if ( 0%{!?_without_regression_tests:1} )
%files regression-tests
%dir %{_datadir}/glusterfs
     %{_datadir}/glusterfs/run-tests.sh
     %{_datadir}/glusterfs/tests
%exclude %{_datadir}/glusterfs/tests/vagrant
%endif

%if ( 0%{!?_without_server:1} && 0%{?rhel} > 6 )
%files ganesha
%dir %{_libexecdir}/ganesha
%{_sysconfdir}/ganesha/ganesha-ha.conf.sample
%{_libexecdir}/ganesha/*
%{_prefix}/lib/ocf/resource.d/heartbeat/*
%{_sharedstatedir}/glusterd/hooks/1/start/post/S31ganesha-start.sh
%ghost      %attr(0644,-,-) %config(noreplace) %{_sysconfdir}/ganesha/ganesha-ha.conf
%ghost %dir %attr(0755,-,-) %{_localstatedir}/run/gluster/shared_storage/nfs-ganesha
%ghost      %attr(0644,-,-) %config(noreplace) %{_localstatedir}/run/gluster/shared_storage/nfs-ganesha/ganesha.conf
%ghost      %attr(0644,-,-) %config(noreplace) %{_localstatedir}/run/gluster/shared_storage/nfs-ganesha/ganesha-ha.conf
%endif

%if ( 0%{!?_without_ocf:1} )
%files resource-agents
# /usr/lib is the standard for OCF, also on x86_64
%{_prefix}/lib/ocf/resource.d/glusterfs
%endif

%if ( 0%{!?_without_server:1} )
%files server
%doc extras/clear_xattrs.sh
%{_datadir}/glusterfs/scripts/xattr_analysis.py*
%{_datadir}/glusterfs/scripts/quota_fsck.py*
# sysconf
%config(noreplace) %{_sysconfdir}/glusterfs
%exclude %{_sysconfdir}/glusterfs/thin-arbiter.vol
%exclude %{_sysconfdir}/glusterfs/eventsconfig.json
%config(noreplace) %{_sysconfdir}/sysconfig/glusterd
%if ( 0%{_for_fedora_koji_builds} )
%config(noreplace) %{_sysconfdir}/sysconfig/glusterfsd
%endif

# init files
%glusterd_svcfile
%if ( 0%{_for_fedora_koji_builds} )
%glusterfsd_svcfile
%endif
%if ( 0%{?_with_systemd:1} )
%glusterfssharedstorage_svcfile
%endif

# binaries
%{_sbindir}/glusterd
%{_sbindir}/glfsheal
%{_sbindir}/gf_attach
%{_sbindir}/gluster-setgfid2path
# {_sbindir}/glusterfsd is the actual binary, but glusterfs (client) is a
# symlink. The binary itself (and symlink) are part of the glusterfs-fuse
# package, because glusterfs-server depends on that anyway.

# Manpages
%{_mandir}/man8/gluster-setgfid2path.8*

# xlators
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/arbiter.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/bit-rot.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/bitrot-stub.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/sdfs.so
%if ( 0%{!?_without_tiering:1} )
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/changetimerecorder.so
     %{_libdir}/libgfdb.so.*
%endif
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/index.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/locks.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/posix*
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/snapview-server.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/marker.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/quota*
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/selinux.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/trash.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/upcall.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/leases.so
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/nfs*
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mgmt
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mgmt/glusterd.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/protocol
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/protocol/server.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/storage
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/storage/posix.so
%dir %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance
     %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/performance/decompounder.so

# snap_scheduler
%{_sbindir}/snap_scheduler.py
%{_sbindir}/gcron.py
%{_sbindir}/conf.py

# /var/lib/glusterd, e.g. hookscripts, etc.
%ghost      %attr(0644,-,-) %config(noreplace) %{_sharedstatedir}/glusterd/glusterd.info
%ghost      %attr(0600,-,-) %config(noreplace) %{_sharedstatedir}/glusterd/options
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/bitd
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/groups
            %attr(0644,-,-) %{_sharedstatedir}/glusterd/groups/virt
            %attr(0644,-,-) %{_sharedstatedir}/glusterd/groups/metadata-cache
            %attr(0644,-,-) %{_sharedstatedir}/glusterd/groups/gluster-block
            %attr(0644,-,-) %{_sharedstatedir}/glusterd/groups/nl-cache
            %attr(0644,-,-) %{_sharedstatedir}/glusterd/groups/db-workload
            %attr(0644,-,-) %{_sharedstatedir}/glusterd/groups/distributed-virt
            %attr(0644,-,-) %{_sharedstatedir}/glusterd/groups/samba
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/glusterfind
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/glusterfind/.keys
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/glustershd
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick/post
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick/post/disabled-quota-root-xattr-heal.sh
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick/post/S13create-subdir-mounts.sh
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick/pre
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick/pre/S28Quota-enable-root-xattr-heal.sh
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/create
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/create/post
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/create/pre
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/copy-file
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/copy-file/post
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/copy-file/pre
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/delete
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/delete/post
                            %{_sharedstatedir}/glusterd/hooks/1/delete/post/S57glusterfind-delete-post
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/delete/pre
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/remove-brick
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/remove-brick/post
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/remove-brick/pre
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/reset
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/reset/post
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/reset/pre
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/set
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/set/post
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/set/post/S30samba-set.sh
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/set/post/S32gluster_enable_shared_storage.sh
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/set/pre
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/start
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/start/post
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/start/post/S29CTDBsetup.sh
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/start/post/S30samba-start.sh
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/start/pre
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/stop
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/stop/post
       %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/stop/pre
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/stop/pre/S30samba-stop.sh
            %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/stop/pre/S29CTDB-teardown.sh
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/nfs
%ghost      %attr(0600,-,-) %{_sharedstatedir}/glusterd/nfs/nfs-server.vol
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/nfs/run
%ghost      %attr(0600,-,-) %{_sharedstatedir}/glusterd/nfs/run/nfs.pid
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/peers
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/quotad
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/scrub
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/snaps
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/ss_brick
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/vols

# Extra utility script
%dir %{_libexecdir}/glusterfs
     %{_datadir}/glusterfs/release
%dir %{_datadir}/glusterfs/scripts
     %{_datadir}/glusterfs/scripts/stop-all-gluster-processes.sh
%if ( 0%{?_with_systemd:1} )
     %{_libexecdir}/glusterfs/mount-shared-storage.sh
     %{_datadir}/glusterfs/scripts/control-cpu-load.sh
     %{_datadir}/glusterfs/scripts/control-mem.sh
%endif

# Incrementalapi
     %{_libexecdir}/glusterfs/glusterfind
%{_bindir}/glusterfind
     %{_libexecdir}/glusterfs/peer_add_secret_pub

%if ( 0%{?_with_firewalld:1} )
%{_prefix}/lib/firewalld/services/glusterfs.xml
%endif
# end of server files
%endif

# Events
%if ( 0%{!?_without_events:1} )
%files events
%config(noreplace) %{_sysconfdir}/glusterfs/eventsconfig.json
%dir %{_sharedstatedir}/glusterd
%dir %{_sharedstatedir}/glusterd/events
%dir %{_libexecdir}/glusterfs
     %{_libexecdir}/glusterfs/gfevents
     %{_libexecdir}/glusterfs/peer_eventsapi.py*
%{_sbindir}/glustereventsd
%{_sbindir}/gluster-eventsapi
%{_datadir}/glusterfs/scripts/eventsdash.py*
%if ( 0%{?_with_systemd:1} )
%{_unitdir}/glustereventsd.service
%else
%{_sysconfdir}/init.d/glustereventsd
%endif
%endif

##-----------------------------------------------------------------------------
## All %pretrans should be placed here and keep them sorted
##
%if 0%{!?_without_server:1}
%pretrans -p <lua>
if not posix.access("/bin/bash", "x") then
    -- initial installation, no shell, no running glusterfsd
    return 0
end

-- TODO: move this completely to a lua script
-- For now, we write a temporary bash script and execute that.

script = [[#!/bin/sh
pidof -c -o %PPID -x glusterfsd &>/dev/null

if [ $? -eq 0 ]; then
   pushd . > /dev/null 2>&1
   for volume in /var/lib/glusterd/vols/*; do cd $volume;
       vol_type=`grep '^type=' info | awk -F'=' '{print $2}'`
       volume_started=`grep '^status=' info | awk -F'=' '{print $2}'`
       if [ $vol_type -eq 0 ] && [ $volume_started -eq 1 ] ; then
          echo "ERROR: Distribute volumes detected. In-service rolling upgrade requires distribute volume(s) to be stopped."
          echo "ERROR: Please stop distribute volume(s) before proceeding... exiting!"
          exit 1;
       fi
   done

   popd > /dev/null 2>&1
   echo "WARNING: Updating glusterfs requires its processes to be killed. This action does NOT incur downtime."
   echo "WARNING: Ensure to wait for the upgraded server to finish healing before proceeding."
   echo "WARNING: Refer upgrade section of install guide for more details"
   echo "Please run # service glusterd stop; pkill glusterfs; pkill glusterfsd; pkill gsyncd.py;"
   exit 1;
fi
]]

ok, how, val = os.execute(script)
rc = val or ok
if not (rc == 0) then
   error("Detected running glusterfs processes", rc)
end



%pretrans api -p <lua>
if not posix.access("/bin/bash", "x") then
    -- initial installation, no shell, no running glusterfsd
    return 0
end

-- TODO: move this completely to a lua script
-- For now, we write a temporary bash script and execute that.

script = [[#!/bin/sh
pidof -c -o %PPID -x glusterfsd &>/dev/null

if [ $? -eq 0 ]; then
   pushd . > /dev/null 2>&1
   for volume in /var/lib/glusterd/vols/*; do cd $volume;
       vol_type=`grep '^type=' info | awk -F'=' '{print $2}'`
       volume_started=`grep '^status=' info | awk -F'=' '{print $2}'`
       if [ $vol_type -eq 0 ] && [ $volume_started -eq 1 ] ; then
          exit 1;
       fi
   done

   popd > /dev/null 2>&1
   exit 1;
fi
]]

ok, how, val = os.execute(script)
rc = val or ok
if not (rc == 0) then
   error("Detected running glusterfs processes", rc)
end



%pretrans api-devel -p <lua>
if not posix.access("/bin/bash", "x") then
    -- initial installation, no shell, no running glusterfsd
    return 0
end

-- TODO: move this completely to a lua script
-- For now, we write a temporary bash script and execute that.

script = [[#!/bin/sh
pidof -c -o %PPID -x glusterfsd &>/dev/null

if [ $? -eq 0 ]; then
   pushd . > /dev/null 2>&1
   for volume in /var/lib/glusterd/vols/*; do cd $volume;
       vol_type=`grep '^type=' info | awk -F'=' '{print $2}'`
       volume_started=`grep '^status=' info | awk -F'=' '{print $2}'`
       if [ $vol_type -eq 0 ] && [ $volume_started -eq 1 ] ; then
          exit 1;
       fi
   done

   popd > /dev/null 2>&1
   exit 1;
fi
]]

ok, how, val = os.execute(script)
rc = val or ok
if not (rc == 0) then
   error("Detected running glusterfs processes", rc)
end



%pretrans cli -p <lua>
if not posix.access("/bin/bash", "x") then
    -- initial installation, no shell, no running glusterfsd
    return 0
end

-- TODO: move this completely to a lua script
-- For now, we write a temporary bash script and execute that.

script = [[#!/bin/sh
pidof -c -o %PPID -x glusterfsd &>/dev/null

if [ $? -eq 0 ]; then
   pushd . > /dev/null 2>&1
   for volume in /var/lib/glusterd/vols/*; do cd $volume;
       vol_type=`grep '^type=' info | awk -F'=' '{print $2}'`
       volume_started=`grep '^status=' info | awk -F'=' '{print $2}'`
       if [ $vol_type -eq 0 ] && [ $volume_started -eq 1 ] ; then
          exit 1;
       fi
   done

   popd > /dev/null 2>&1
   exit 1;
fi
]]

ok, how, val = os.execute(script)
rc = val or ok
if not (rc == 0) then
   error("Detected running glusterfs processes", rc)
end


%pretrans client-xlators -p <lua>
if not posix.access("/bin/bash", "x") then
    -- initial installation, no shell, no running glusterfsd
    return 0
end

-- TODO: move this completely to a lua script
-- For now, we write a temporary bash script and execute that.

script = [[#!/bin/sh
pidof -c -o %PPID -x glusterfsd &>/dev/null

if [ $? -eq 0 ]; then
   pushd . > /dev/null 2>&1
   for volume in /var/lib/glusterd/vols/*; do cd $volume;
       vol_type=`grep '^type=' info | awk -F'=' '{print $2}'`
       volume_started=`grep '^status=' info | awk -F'=' '{print $2}'`
       if [ $vol_type -eq 0 ] && [ $volume_started -eq 1 ] ; then
          exit 1;
       fi
   done

   popd > /dev/null 2>&1
   exit 1;
fi
]]

ok, how, val = os.execute(script)
rc = val or ok
if not (rc == 0) then
   error("Detected running glusterfs processes", rc)
end


%pretrans fuse -p <lua>
if not posix.access("/bin/bash", "x") then
    -- initial installation, no shell, no running glusterfsd
    return 0
end

-- TODO: move this completely to a lua script
-- For now, we write a temporary bash script and execute that.

script = [[#!/bin/sh
pidof -c -o %PPID -x glusterfsd &>/dev/null

if [ $? -eq 0 ]; then
   pushd . > /dev/null 2>&1
   for volume in /var/lib/glusterd/vols/*; do cd $volume;
       vol_type=`grep '^type=' info | awk -F'=' '{print $2}'`
       volume_started=`grep '^status=' info | awk -F'=' '{print $2}'`
       if [ $vol_type -eq 0 ] && [ $volume_started -eq 1 ] ; then
          exit 1;
       fi
   done

   popd > /dev/null 2>&1
   exit 1;
fi
]]

ok, how, val = os.execute(script)
rc = val or ok
if not (rc == 0) then
   error("Detected running glusterfs processes", rc)
end



%if ( 0%{!?_without_georeplication:1} )
%pretrans geo-replication -p <lua>
if not posix.access("/bin/bash", "x") then
    -- initial installation, no shell, no running glusterfsd
    return 0
end

-- TODO: move this completely to a lua script
-- For now, we write a temporary bash script and execute that.

script = [[#!/bin/sh
pidof -c -o %PPID -x glusterfsd &>/dev/null

if [ $? -eq 0 ]; then
   pushd . > /dev/null 2>&1
   for volume in /var/lib/glusterd/vols/*; do cd $volume;
       vol_type=`grep '^type=' info | awk -F'=' '{print $2}'`
       volume_started=`grep '^status=' info | awk -F'=' '{print $2}'`
       if [ $vol_type -eq 0 ] && [ $volume_started -eq 1 ] ; then
          exit 1;
       fi
   done

   popd > /dev/null 2>&1
   exit 1;
fi
]]

ok, how, val = os.execute(script)
rc = val or ok
if not (rc == 0) then
   error("Detected running glusterfs processes", rc)
end
%endif



%pretrans libs -p <lua>
if not posix.access("/bin/bash", "x") then
    -- initial installation, no shell, no running glusterfsd
    return 0
end

-- TODO: move this completely to a lua script
-- For now, we write a temporary bash script and execute that.

script = [[#!/bin/sh
pidof -c -o %PPID -x glusterfsd &>/dev/null

if [ $? -eq 0 ]; then
   pushd . > /dev/null 2>&1
   for volume in /var/lib/glusterd/vols/*; do cd $volume;
       vol_type=`grep '^type=' info | awk -F'=' '{print $2}'`
       volume_started=`grep '^status=' info | awk -F'=' '{print $2}'`
       if [ $vol_type -eq 0 ] && [ $volume_started -eq 1 ] ; then
          exit 1;
       fi
   done

   popd > /dev/null 2>&1
   exit 1;
fi
]]

ok, how, val = os.execute(script)
rc = val or ok
if not (rc == 0) then
   error("Detected running glusterfs processes", rc)
end



%if ( 0%{!?_without_rdma:1} )
%pretrans rdma -p <lua>
if not posix.access("/bin/bash", "x") then
    -- initial installation, no shell, no running glusterfsd
    return 0
end

-- TODO: move this completely to a lua script
-- For now, we write a temporary bash script and execute that.

script = [[#!/bin/sh
pidof -c -o %PPID -x glusterfsd &>/dev/null

if [ $? -eq 0 ]; then
   pushd . > /dev/null 2>&1
   for volume in /var/lib/glusterd/vols/*; do cd $volume;
       vol_type=`grep '^type=' info | awk -F'=' '{print $2}'`
       volume_started=`grep '^status=' info | awk -F'=' '{print $2}'`
       if [ $vol_type -eq 0 ] && [ $volume_started -eq 1 ] ; then
          exit 1;
       fi
   done

   popd > /dev/null 2>&1
   exit 1;
fi
]]

ok, how, val = os.execute(script)
rc = val or ok
if not (rc == 0) then
   error("Detected running glusterfs processes", rc)
end
%endif



%if ( 0%{!?_without_ocf:1} )
%pretrans resource-agents -p <lua>
if not posix.access("/bin/bash", "x") then
    -- initial installation, no shell, no running glusterfsd
    return 0
end

-- TODO: move this completely to a lua script
-- For now, we write a temporary bash script and execute that.

script = [[#!/bin/sh
pidof -c -o %PPID -x glusterfsd &>/dev/null

if [ $? -eq 0 ]; then
   pushd . > /dev/null 2>&1
   for volume in /var/lib/glusterd/vols/*; do cd $volume;
       vol_type=`grep '^type=' info | awk -F'=' '{print $2}'`
       volume_started=`grep '^status=' info | awk -F'=' '{print $2}'`
       if [ $vol_type -eq 0 ] && [ $volume_started -eq 1 ] ; then
          exit 1;
       fi
   done

   popd > /dev/null 2>&1
   exit 1;
fi
]]

ok, how, val = os.execute(script)
rc = val or ok
if not (rc == 0) then
   error("Detected running glusterfs processes", rc)
end
%endif



%pretrans server -p <lua>
if not posix.access("/bin/bash", "x") then
    -- initial installation, no shell, no running glusterfsd
    return 0
end

-- TODO: move this completely to a lua script
-- For now, we write a temporary bash script and execute that.

script = [[#!/bin/sh
pidof -c -o %PPID -x glusterfsd &>/dev/null

if [ $? -eq 0 ]; then
   pushd . > /dev/null 2>&1
   for volume in /var/lib/glusterd/vols/*; do cd $volume;
       vol_type=`grep '^type=' info | awk -F'=' '{print $2}'`
       volume_started=`grep '^status=' info | awk -F'=' '{print $2}'`
       if [ $vol_type -eq 0 ] && [ $volume_started -eq 1 ] ; then
          exit 1;
       fi
   done

   popd > /dev/null 2>&1
   exit 1;
fi
]]

ok, how, val = os.execute(script)
rc = val or ok
if not (rc == 0) then
   error("Detected running glusterfs processes", rc)
end

%posttrans server
pidof -c -o %PPID -x glusterd &> /dev/null
if [ $? -eq 0 ]; then
    kill -9 `pgrep -f gsyncd.py` &> /dev/null

    killall --wait -SIGTERM glusterd &> /dev/null

    if [ "$?" != "0" ]; then
        echo "killall failed while killing glusterd"
    fi

    glusterd --xlator-option *.upgrade=on -N

    #Cleaning leftover glusterd socket file which is created by glusterd in
    #rpm_script_t context.
    rm -rf /var/run/glusterd.socket

    # glusterd _was_ running, we killed it, it exited after *.upgrade=on,
    # so start it again
    %service_start glusterd
else
    glusterd --xlator-option *.upgrade=on -N

    #Cleaning leftover glusterd socket file which is created by glusterd in
    #rpm_script_t context.
    rm -rf /var/run/glusterd.socket
fi

%endif

%changelog
* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 6.0-57.4
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Sun Aug 1 2021 Tamar Shacked <tshacked@redhat.com> - 6.0-56.4
- remove unneeded file with ambiguous licence
- fixes bug bz#1939340

* Mon Jul 26 2021 Tamar Shacked <tshacked@redhat.com> - 6.0-56.3
- Rebase with latest RHGS-3.5.4
- Fix changlog chronological order by removing unneeded changelogs
- fixes bug bz#1939340

* Thu May 06 2021 Gluster Jenkins <dkhandel+glusterjenkins@redhat.com> - 6.0-56.2
- fixes bugs bz#1953901

* Thu Apr 22 2021 Gluster Jenkins <dkhandel+glusterjenkins@redhat.com> - 6.0-56.1
- fixes bugs bz#1927235

* Wed Apr 14 2021 Gluster Jenkins <dkhandel+glusterjenkins@redhat.com> - 6.0-56
- fixes bugs bz#1948547

* Fri Mar 19 2021 Gluster Jenkins <dkhandel+glusterjenkins@redhat.com> - 6.0-55
- fixes bugs bz#1939372

* Wed Mar 03 2021 Gluster Jenkins <dkhandel+glusterjenkins@redhat.com> - 6.0-54
- fixes bugs bz#1832306 bz#1911292 bz#1924044

* Thu Feb 11 2021 Gluster Jenkins <dkhandel+glusterjenkins@redhat.com> - 6.0-53
- fixes bugs bz#1224906 bz#1691320 bz#1719171 bz#1814744 bz#1865796

* Thu Jan 28 2021 Gluster Jenkins <dkhandel+glusterjenkins@redhat.com> - 6.0-52
- fixes bugs bz#1600459 bz#1719171 bz#1830713 bz#1856574

* Mon Dec 28 2020 Gluster Jenkins <dkhandel+glusterjenkins@redhat.com> - 6.0-51
- fixes bugs bz#1640148 bz#1856574 bz#1910119

* Tue Dec 15 2020 Gluster Jenkins <dkhandel+glusterjenkins@redhat.com> - 6.0-50
- fixes bugs bz#1224906 bz#1412494 bz#1612973 bz#1663821 bz#1691320 
  bz#1726673 bz#1749304 bz#1752739 bz#1779238 bz#1813866 bz#1814744 bz#1821599 
  bz#1832306 bz#1835229 bz#1842449 bz#1865796 bz#1878077 bz#1882923 bz#1885966 
  bz#1890506 bz#1896425 bz#1898776 bz#1898777 bz#1898778 bz#1898781 bz#1898784 
  bz#1903468

* Wed Nov 25 2020 Gluster Jenkins <dkhandel+glusterjenkins@redhat.com> - 6.0-49
- fixes bugs bz#1286171

* Tue Nov 10 2020 Gluster Jenkins <dkhandel+glusterjenkins@redhat.com> - 6.0-48
- fixes bugs bz#1895301

* Thu Nov 05 2020 Gluster Jenkins <dkhandel+glusterjenkins@redhat.com> - 6.0-47
- fixes bugs bz#1286171 bz#1821743 bz#1837926

* Wed Oct 21 2020 Gluster Jenkins <dkhandel+glusterjenkins@redhat.com> - 6.0-46
- fixes bugs bz#1873469 bz#1881823

* Wed Sep 09 2020 Deepshikha Khandelwal <dkhandel@redhat.com> - 6.0-45
- fixes bugs bz#1785714

* Thu Sep 03 2020 Deepshikha Khandelwal <dkhandel@redhat.com> - 6.0-44
- fixes bugs bz#1460657

* Thu Sep 03 2020 Deepshikha Khandelwal <dkhandel@redhat.com> - 6.0-43
- fixes bugs bz#1460657

* Wed Sep 02 2020 Deepshikha Khandelwal <dkhandel@redhat.com> - 6.0-42
- fixes bugs bz#1785714

* Tue Aug 25 2020 Deepshikha Khandelwal <dkhandel@redhat.com> - 6.0-41
- fixes bugs bz#1785714 bz#1851424 bz#1851989 bz#1852736 bz#1853189 bz#1855966

* Tue Jul 21 2020 Deepshikha Khandelwal <dkhandel@redhat.com> - 6.0-40
- fixes bugs bz#1812789 bz#1844359 bz#1847081 bz#1854165

* Wed Jun 17 2020 Deepshikha Khandelwal <dkhandel@redhat.com> - 6.0-39
- fixes bugs bz#1844359 bz#1845064

* Wed Jun 10 2020 Rinku Kothiya <rkothiya@redhat.com> - 6.0-38
- fixes bugs bz#1234220 bz#1286171 bz#1487177 bz#1524457 bz#1640573 
  bz#1663557 bz#1667954 bz#1683602 bz#1686897 bz#1721355 bz#1748865 bz#1750211 
  bz#1754391 bz#1759875 bz#1761531 bz#1761932 bz#1763124 bz#1763129 bz#1764091 
  bz#1775637 bz#1776901 bz#1781550 bz#1781649 bz#1781710 bz#1783232 bz#1784211 
  bz#1784415 bz#1786516 bz#1786681 bz#1787294 bz#1787310 bz#1787331 bz#1787994 
  bz#1790336 bz#1792873 bz#1794663 bz#1796814 bz#1804164 bz#1810924 bz#1815434 
  bz#1836099 bz#1837467 bz#1837926 bz#1838479 bz#1839137 bz#1844359

* Fri May 29 2020 Rinku Kothiya <rkothiya@redhat.com> - 6.0-37
- fixes bugs bz#1840794

* Wed May 27 2020 Rinku Kothiya <rkothiya@redhat.com> - 6.0-36
- fixes bugs bz#1812789 bz#1823423

* Fri May 22 2020 Rinku Kothiya <rkothiya@redhat.com> - 6.0-35
- fixes bugs bz#1810516 bz#1830713 bz#1836233

* Sun May 17 2020 Rinku Kothiya <rkothiya@redhat.com> - 6.0-34
- fixes bugs bz#1802013 bz#1823706 bz#1825177 bz#1830713 bz#1831403 bz#1833017

* Wed Apr 29 2020 Rinku Kothiya <rkothiya@redhat.com> - 6.0-33
- fixes bugs bz#1812789 bz#1813917 bz#1823703 bz#1823706 bz#1825195

* Sat Apr 04 2020 Rinku Kothiya <rkothiya@redhat.com> - 6.0-32
- fixes bugs bz#1781543 bz#1812789 bz#1812824 bz#1817369 bz#1819059

* Tue Mar 17 2020 Rinku Kothiya <rkothiya@redhat.com> - 6.0-31
- fixes bugs bz#1802727

* Thu Feb 20 2020 Rinku Kothiya <rkothiya@redhat.com> - 6.0-30.1
- fixes bugs bz#1800703

* Sat Feb 01 2020 Rinku Kothiya <rkothiya@redhat.com> - 6.0-30
- fixes bugs bz#1775564 bz#1794153

* Thu Jan 23 2020 Rinku Kothiya <rkothiya@redhat.com> - 6.0-29
- fixes bugs bz#1793035

* Tue Jan 14 2020 Rinku Kothiya <rkothiya@redhat.com> - 6.0-28
- fixes bugs bz#1789447

* Mon Jan 13 2020 Rinku Kothiya <rkothiya@redhat.com> - 6.0-27
- fixes bugs bz#1789447

* Fri Jan 10 2020 Rinku Kothiya <rkothiya@redhat.com> - 6.0-26
- fixes bugs bz#1763208 bz#1788656

* Mon Dec 23 2019 Rinku Kothiya <rkothiya@redhat.com> - 6.0-25
- fixes bugs bz#1686800 bz#1763208 bz#1779696 bz#1781444 bz#1782162

* Thu Nov 28 2019 Rinku Kothiya <rkothiya@redhat.com> - 6.0-24
- fixes bugs bz#1768786

* Thu Nov 21 2019 Rinku Kothiya <rkothiya@redhat.com> - 6.0-23
- fixes bugs bz#1344758 bz#1599802 bz#1685406 bz#1686800 bz#1724021 
  bz#1726058 bz#1727755 bz#1731513 bz#1741193 bz#1758923 bz#1761326 bz#1761486 
  bz#1762180 bz#1764095 bz#1766640

* Thu Nov 14 2019 Rinku Kothiya <rkothiya@redhat.com> - 6.0-22
- fixes bugs bz#1771524 bz#1771614

* Fri Oct 25 2019 Rinku Kothiya <rkothiya@redhat.com> - 6.0-21
- fixes bugs bz#1765555

* Wed Oct 23 2019 Rinku Kothiya <rkothiya@redhat.com> - 6.0-20
- fixes bugs bz#1719171 bz#1763412 bz#1764202

* Thu Oct 17 2019 Rinku Kothiya <rkothiya@redhat.com> - 6.0-19
- fixes bugs bz#1760939

* Wed Oct 16 2019 Rinku Kothiya <rkothiya@redhat.com> - 6.0-18
- fixes bugs bz#1758432

* Fri Oct 11 2019 Rinku Kothiya <rkothiya@redhat.com> - 6.0-17
- fixes bugs bz#1704562 bz#1758618 bz#1760261

* Wed Oct 09 2019 Rinku Kothiya <rkothiya@redhat.com> - 6.0-16
- fixes bugs bz#1752713 bz#1756325

* Fri Sep 27 2019 Rinku Kothiya <rkothiya@redhat.com> - 6.0-15
- fixes bugs bz#1726000 bz#1731826 bz#1754407 bz#1754790 bz#1755227

* Fri Sep 20 2019 Sunil Kumar Acharya <sheggodu@redhat.com> - 6.0-14
- fixes bugs bz#1719171 bz#1728673 bz#1731896 bz#1732443 bz#1733970 
  bz#1745107 bz#1746027 bz#1748688 bz#1750241 bz#1572163

* Fri Aug 23 2019 Rinku Kothiya <rkothiya@redhat.com> - 6.0-13
- fixes bugs bz#1729915 bz#1732376 bz#1743611 bz#1743627 bz#1743634 bz#1744518

* Fri Aug 09 2019 Sunil Kumar Acharya <sheggodu@redhat.com> - 6.0-12
- fixes bugs bz#1730914 bz#1731448 bz#1732770 bz#1732792 bz#1733531 
  bz#1734305 bz#1734534 bz#1734734 bz#1735514 bz#1737705 bz#1732774
  bz#1732793

* Tue Aug 06 2019 Sunil Kumar Acharya <sheggodu@redhat.com> - 6.0-11
- fixes bugs bz#1733520 bz#1734423

* Fri Aug 02 2019 Sunil Kumar Acharya <sheggodu@redhat.com> - 6.0-10
- fixes bugs bz#1713890

* Tue Jul 23 2019 Sunil Kumar Acharya <sheggodu@redhat.com> - 6.0-9
- fixes bugs bz#1708064 bz#1708180 bz#1715422 bz#1720992 bz#1722757

* Tue Jul 16 2019 Sunil Kumar Acharya <sheggodu@redhat.com> - 6.0-8
- fixes bugs bz#1698435 bz#1712591 bz#1715447 bz#1720488 bz#1722209
  bz#1722512 bz#1724089 bz#1726991 bz#1727785 bz#1729108

* Fri Jun 28 2019 Sunil Kumar Acharya <sheggodu@redhat.com> - 6.0-7
- fixes bugs bz#1573077 bz#1600918 bz#1703423 bz#1704207 bz#1708064
  bz#1709301 bz#1713664 bz#1716760 bz#1717784 bz#1720163 bz#1720192
  bz#1720551 bz#1721351 bz#1721357 bz#1721477 bz#1722131 bz#1722331
  bz#1722509 bz#1722801 bz#1720248

* Fri Jun 14 2019 Sunil Kumar Acharya <sheggodu@redhat.com> - 6.0-6
- fixes bugs bz#1668001 bz#1708043 bz#1708183 bz#1710701 
  bz#1719640 bz#1720079 bz#1720248 bz#1720318 bz#1720461

* Tue Jun 11 2019 Sunil Kumar Acharya <sheggodu@redhat.com> - 6.0-5
- fixes bugs bz#1573077 bz#1694595 bz#1703434 bz#1714536 bz#1714588 
  bz#1715407 bz#1715438 bz#1705018

* Fri Jun 07 2019 Rinku Kothiya <rkothiya@redhat.com> - 6.0-4
- fixes bugs bz#1480907 bz#1702298 bz#1703455 bz#1704181 bz#1707246
  bz#1708067 bz#1708116 bz#1708121 bz#1709087 bz#1711249 bz#1711296 
  bz#1714078 bz#1714124 bz#1716385 bz#1716626 bz#1716821 bz#1716865 bz#1717927

* Tue May 14 2019 Rinku Kothiya <rkothiya@redhat.com> - 6.0-3
- fixes bugs bz#1583585 bz#1671862 bz#1702686 bz#1703434 bz#1703753 
  bz#1703897 bz#1704562 bz#1704769 bz#1704851 bz#1706683 bz#1706776 bz#1706893

* Thu Apr 25 2019 Milind Changire <mchangir@redhat.com> - 6.0-2
- fixes bugs bz#1471742 bz#1652461 bz#1671862 bz#1676495 bz#1691620 
  bz#1696334 bz#1696903 bz#1697820 bz#1698436 bz#1698728 bz#1699709 bz#1699835 
  bz#1702240

* Mon Apr 08 2019 Milind Changire <mchangir@redhat.com> - 6.0-1
- rebase to upstream glusterfs at v6.0
- fixes bugs bz#1493284 bz#1578703 bz#1600918 bz#1670415 bz#1691620 
  bz#1693935 bz#1695057

