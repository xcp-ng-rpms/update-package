Name:    update-package
Summary: Build host update packages
Version: 2.0.0
Release: 1
License: BSD
Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/%{name}/archive?at=v%{version}&format=tar.gz&prefix=%{name}-%{version}#/%{name}.tar.gz
BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: systemd-units

Requires: createrepo expect genisoimage gnupg2 python-libarchive-c python-setuptools rpm rpm-build rpm-sign syslinux
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Creates ISO images from a collection of RPMs.

%package hotfix
Summary: Build host hotfix updates

Requires: update-package yum-utils

%description hotfix
Creates hotfix updates from a collection of RPMs.

%package signing
Summary: Signing request tools

Requires: git python-setuptools

%description signing
Requests the signing server to sign releases and updates

%package sign-server
Summary: Signing server for updates

Requires: createrepo expect genisoimage gnupg2 python-libarchive-c python-setuptools rpm rpm-build rpm-sign syslinux

%description sign-server
Signs media and updates with release keys.

%package gpg
Summary: GnuPG proxy for update signing server

Requires: gnupg2 python-setuptools

%description gpg
Performs signing operations requested by the update signing server.

%prep
%autosetup -p1

%build
sed -e "s/use_scm_version=True/version='%{version}'/" setup.py >setup.no_scm.py
%{__python2} setup.no_scm.py build

%install
%{__python2} setup.no_scm.py install --root %{buildroot}
%{__install} -d -m 755 %{buildroot}/%{_unitdir}
%{__install} -m 644 sign-server.service %{buildroot}/%{_unitdir}
%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 644 sign-server.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/sign-server

%post sign-server
%systemd_post sign-server.service

%preun sign-server
%systemd_preun sign-server.service

%postun sign-server
%systemd_postun_with_restart sign-server.service

%files
%{_bindir}/build-update
%{_bindir}/compare-repositories
%{_bindir}/fetch-package-sources
%{_bindir}/manage-signing-keys
%{_bindir}/repack-update
%{_bindir}/unpack-update
%{_bindir}/update-info
%{_bindir}/create-group-file
%{python_sitelib}/query_update/__init__.py*
%{python_sitelib}/query_update/compare_repositories.py*
%{python_sitelib}/update_package/build_update.py*
%{python_sitelib}/update_package/fetch_package_sources.py*
%{python_sitelib}/update_package/manage_signing_keys.py*
%{python_sitelib}/update_package/__init__.py*
%{python_sitelib}/update_package/buildcommon.py*
%{python_sitelib}/update_package/common.py*
%{python_sitelib}/update_package/repack_update.py*
%{python_sitelib}/update_package/unpack_update.py*
%{python_sitelib}/update_package/update_info.py*
%{python_sitelib}/update_package/*.spec
%{python_sitelib}/update_package/create_group_file.py*

%{python_sitelib}/update_package-*.egg-info

%files hotfix
%{_bindir}/build-hotfix-update
%{_bindir}/create-group-file
%{_bindir}/create-update-doc
%{_bindir}/list-binary-packages
%{_bindir}/update-resource
%{python_sitelib}/update_package/build_hotfix_update.py*
%{python_sitelib}/update_package/create_group_file.py*
%{python_sitelib}/update_package/create_update_doc.py*
%{python_sitelib}/update_package/list_binary_packages.py*
%{python_sitelib}/update_package/generate-livepatch-precheck
%{python_sitelib}/update_package/livepatch_info.py*
%{python_sitelib}/update_package/livepatch.mk
%{python_sitelib}/update_package/update.mk
%{python_sitelib}/update_package/resource.py*

%files signing
%{_bindir}/request-sign-build
%{_bindir}/request-sign-cr
%{_bindir}/request-sign-update
%{python_sitelib}/sign_update/__init__.py*
%{python_sitelib}/sign_update/request_sign_build.py*
%{python_sitelib}/sign_update/request_sign_cr.py*
%{python_sitelib}/sign_update/request_sign_update.py*
%{python_sitelib}/sign_update/*.json
%exclude %{python_sitelib}/sign_update/request_sign_hotfix.py*

%files sign-server
%{_bindir}/gpg-proxy
%{_bindir}/manage-pub-keys
%{_bindir}/sign-media
%{_bindir}/sign-server
%{_bindir}/sign-source
%{_bindir}/sign-update
%config(noreplace) %attr(600, -, -) %{_sysconfdir}/sysconfig/sign-server
%{python_sitelib}/update_package/__init__.py*
%{python_sitelib}/update_package/common.py*
%{python_sitelib}/update_package/gpg_proxy_client.py*
%{python_sitelib}/update_package/manage_pub_keys.py*
%{python_sitelib}/update_package/server_common.py*
%{python_sitelib}/update_package/sign_media.py*
%{python_sitelib}/update_package/sign_server.py*
%{python_sitelib}/update_package/sign_source.py*
%{python_sitelib}/update_package/sign_update.py*

%{python_sitelib}/update_package-*.egg-info

%{_unitdir}/sign-server.service

%files gpg
%{_bindir}/gpg-proxy-sign
%{_bindir}/manage-signing-keys
%{python_sitelib}/update_package/__init__.py*
%{python_sitelib}/update_package/gpg_proxy_server.py*
%{python_sitelib}/update_package/manage_signing_keys.py*

%{python_sitelib}/update_package-*.egg-info

%changelog
* Fri Aug 31 2018 Simon Rowe <simon.rowe@citrix.com> - 2.0.0-1
- CA-293995: Ensure xmllint call is quoted
- Remove slipstreaming tools
- Add support for multiple precheck scripts

* Wed May 09 2018 Alex Brett <alex.brett@citrix.com> - 1.12.6-1
- Don't expect to find DDK files in the build in request-sign-cr

* Wed May 02 2018 Alex Brett <alex.brett@citrix.com> - 1.12.5-1
- Add ability to only sign inspur in request-sign-cr

* Tue May 01 2018 Alex Brett <alex.brett@citrix.com> - 1.12.4-1
- Fixes for Inspur signing in request-sign-cr

* Tue Apr 17 2018 Simon Rowe <simon.rowe@citrix.com> - 1.12.3-1
- CA-284645: exclude lpe from source ISO

* Mon Mar 05 2018 Simon Rowe <simon.rowe@citrix.com> - 1.12.2-1
- Print names of packages being dowloaded

* Wed Feb 28 2018 Simon Rowe <simon.rowe@citrix.com> - 1.12.1-1
- CA-284517: ensure the request is a JSON object first

* Sat Feb 24 2018 Kun Ma <kun.ma@citrix.com> - 1.12.0-1
- CA-284306: Ask for auth when querying JIRA

* Thu Feb 15 2018 Alex Brett <alex.brett@citrix.com> - 1.11.0-1
- Add request-sign-cr tool

* Wed Jan 24 2018 Simon Rowe <simon.rowe@citrix.com> - 1.10.3-1
- Download source packages using urlgrabber

* Fri Jan 19 2018 Simon Rowe <simon.rowe@citrix.com> - 1.10.2-1
- Download source packages using requests
- Use ephemeral temporary directory for each yum operation
- CP-26579: pass NO_SRC_REPOS to fetch-package-sources
- CP-26579: add --no-sources argument

* Thu Jan 18 2018 Simon Rowe <simon.rowe@citrix.com> - 1.10.1-1
- CP-26579: include build dependencies in source ISO
- Adding the SDK to the list of files which get copied
- Add Partner Engineering key to Inspur release
- Check both host and port when comparing URLs 

* Fri Nov 10 2017 Simon Rowe <simon.rowe@citrix.com> - 1.10.0-1
- Add project definition for Inverness
- Add support for deliverables service
- CA-254970: fixing the assumption that the presence of '/' means a value is a URL

* Thu Oct 26 2017 Simon Rowe <simon.rowe@citrix.com> - 1.9.18-1
- Add target to create full source ISO Inspur builds

* Mon Oct 23 2017 Simon Rowe <simon.rowe@citrix.com> - 1.9.17-1
- Use Python rpm module to sign packages
- CP-24763: Updated request-sign-update to recognise Honolulu and Inverness
- Remove hard-coded version in setup.py
- CA-268655: Find livepatches even with a release name

* Mon Oct 09 2017 Alex Brett <alex.brett@citrix.com> - 1.9.16-1
- Rename ely-lcm.json to xs7-lcm.json

* Mon Oct 09 2017 Simon Rowe <simon.rowe@citrix.com> - 1.9.15-1
- Reduce space consumption by slipstream-updates-source

* Fri Oct 06 2017 Simon Rowe <simon.rowe@citrix.com> - 1.9.14-1
- Adding template for the Partner Engineering key

* Fri Sep 29 2017 Simon Rowe <simon.rowe@citrix.com> - 1.9.13-1
- CA-267665: replace chroot with --installroot
- CA-264473: exclude 32-bit packages by default
- CP-24672: Add server_common.py 

* Wed Sep 27 2017 Simon Rowe <simon.rowe@citrix.com> - 1.9.12-1
- CP-24433: added compare-repositories

* Fri Sep 08 2017 Simon Rowe <simon.rowe@citrix.com> - 1.9.11-1
- CA-265277: Merge livepatch and license check scripts
- CA-265099: Recognize xen-ely-livepatch as a livepatch RPM

* Tue Aug 22 2017 Simon Rowe <simon.rowe@citrix.com> - 1.9.10-1
- CP-24080: add update-stream to the XML document

* Mon Aug 21 2017 Simon Rowe <simon.rowe@citrix.com> - 1.9.9-1
- CA-263558: slipstream-updates: remove old hypervisor
- CA-260672: only try to sign packages if there are some
- CA-261183: get_gpg_key_pass is located in update_package.common

* Wed Jul 26 2017 Callum McIntyre <callum.mcintyre@citrix.com> - 1.9.8-1
- Revert 'Use libarchive to extract the initrd'
- Support both bzip2 and gzip compressed initrd

* Fri Jul 21 2017 Callum McIntyre <callum.mcintyre@citrix.com> - 1.9.7-1
- Use rpm_query for install size
- Silence RPM signature warnings
- Add Packages as an ignore directory
- [CP-23583] Use libarchive to extract the initrd

* Wed Jul 19 2017 Callum McIntyre <callum.mcintyre@citrix.com> - 1.9.6-1
- CA-260183: Also delete XenCenterSetup.exe from installer

* Tue Jul 18 2017 Callum McIntyre <callum.mcintyre@citrix.com> - 1.9.5-1
- CP-22958: add homogeneity arguments to update build scripts
- CA-260183: Copy XenCenter.msi into installer

* Wed Jul 05 2017 Simon Rowe <simon.rowe@citrix.com> - 1.9.4-1
- CA-254443: Add support for EXCLUDE_SOURCE_PACKAGES
- CA-253958: clean up following updates
- CA-258305: add epoch to update package requires

* Fri Jun 30 2017 Simon Rowe <simon.rowe@citrix.com> - 1.9.3-1
- CA-257048: add EXTRA_SOURCE_PACKAGES list

* Thu Jun 29 2017 Simon Rowe <simon.rowe@citrix.com> - 1.9.2-1
- CA-253958: default BASE_REQUIRES to kernel-uname-r for driverDisks
- [CA-258071] Add copy rules for xenserver-pv-tools
- CA-255199] Add support for copying latest XenCenter into installer

* Fri Jun 23 2017 Simon Rowe <simon.rowe@citrix.com> - 1.9.1-1
- Adding driver version to iso name label for driver updates
- [CP-22948] Remove stamp file of updates that are not rolled up

* Fri Jun 16 2017 Simon Rowe <simon.rowe@citrix.com> - 1.9.0-1
- CP-22840: Do not rollup previous livepatch packages
- CP-22958: set enforce-homogeneity for hotfixes & servicePacks
- [CP-22948] Add a rolled-up-by arg to create_update_doc
- [CP-22782] Handle grub-efi package
- [CP-22732] Special case for handling kernel

* Mon Jun 12 2017 Simon Rowe <simon.rowe@citrix.com> - 1.8.11-1
- [CA-256540] Pass new ISO labels to slipstreaming scripts
- [CP-22732] Handle kernel + xen-hypervisor packages

* Fri Jun 09 2017 Simon Rowe <simon.rowe@citrix.com> - 1.8.10-1
- CA-256487: ignore RPM directories when copying directories
- CA-256504: run slipstream-updates as root

* Wed Jun 07 2017 Simon Rowe <simon.rowe@citrix.com> - 1.8.9-1
- CA-256340: cope with Provides without an EVR
- CA-256353: Obsolete the control packages of rollups

* Thu Jun 01 2017 Simon Rowe <simon.rowe@citrix.com> - 1.8.8-1
- CP-22251: make --base-requires optional for build-hotfix-update
- CA-255511: fail curl commands
- CP-22251: add dependency on PRECHECK_SCRIPT
- CP-22509: servicePack, add build number

* Thu May 25 2017 Simon Rowe <simon.rowe@citrix.com> - 1.8.7-1
- CA-255177: append basename to destination URL 

* Wed May 24 2017 Simon Rowe <simon.rowe@citrix.com> - 1.8.6-1
- CA-255034: remove existing public keys

* Tue May 23 2017 Simon Rowe <simon.rowe@citrix.com> - 1.8.5-1
- CA-251625: generate a stamp file without key attribute
- CA-254040: only generate provides file when source is present
- CA-254045: only include stamp files in hotfixes

* Fri May 19 2017 Simon Rowe <simon.rowe@citrix.com> - 1.8.4-1
- CA-254029: create a globals file for slipstreamed ISOs

* Tue May 09 2017 Simon Rowe <simon.rowe@citrix.com> - 1.8.3-1
- CA-253151: treat servicePacks in a similar manner to hotfixes

* Mon May 08 2017 Simon Rowe <simon.rowe@citrix.com> - 1.8.2-1
- CA-253461: determine rollups recursively

* Fri May 05 2017 Simon Rowe <simon.rowe@citrix.com> - 1.8.1-1
- CA-251605: include rollup source packages

* Fri Apr 28 2017 Alex Brett <alex.brett@citrix.com> - 1.8.0-1
- CP-20970 Add copy_file and copy_dir support to signing server

* Fri Apr 21 2017 Simon Rowe <simon.rowe@citrix.com> - 1.7.6-1
- CP-21419: Add mail alerts to signing server

* Thu Apr 13 2017 Simon Rowe <simon.rowe@citrix.com> - 1.7.5-1
- Include livepatch repos as extra UPDATE_REPOs

* Wed Apr 12 2017 Simon Rowe <simon.rowe@citrix.com> - 1.7.4-1
- Fix building an update when binpkgs ISO is empty

* Thu Apr 06 2017 Simon Rowe <simon.rowe@citrix.com> - 1.7.3-1
- sign-media: make --key optional

* Thu Mar 30 2017 Simon Rowe <simon.rowe@citrix.com> - 1.7.1-1
- Auto generate slipstreamed ISOs

* Wed Mar 29 2017 Simon Rowe <simon.rowe@citrix.com> - 1.7.0-1
- CP-21354: add tool to slipstream source ISOs
- [CA-246375] Correct how relationship lines are written for packages
- CP-21572: build an additional binaries ISO
- CP-21359: remove delta from GA size calculation
- CP-21158: Generate groups file for driver disks

* Thu Mar 23 2017 Simon Rowe <simon.rowe@citrix.com> - 1.6.6-1
- CA-248365: rewrite pretrans script in Lua
- CP-21070: Add livepatch metadata to XML document

* Tue Mar 14 2017 Simon Rowe <simon.rowe@citrix.com> - 1.6.3-1
- Remove hard dependency on xenserver-specs

* Mon Mar 06 2017 Simon Rowe <simon.rowe@citrix.com> - 1.6.1-1
- Fix text error for REMOVE_SCRIPT description
- CP-20944: Repack update rpm use new description
- CP-20904: Add rollsup stampfile in update-info
- CA-245843: add update prefix to relationships

* Wed Feb 22 2017 Simon Rowe <simon.rowe@citrix.com> - 1.6.0-1
- Add unpack and repack tools

* Fri Feb 17 2017 Simon Rowe <simon.rowe@citrix.com> - 1.5.5-1
- Add livepatch support

* Thu Feb 16 2017 Simon Rowe <simon.rowe@citrix.com> - 1.5.3-1
- Use existing yum repositories

* Wed Feb 15 2017 Kun Ma <kun.ma@citrix.com> - 1.5.2-1
- Add update_info.py into build_update package

* Tue Feb 14 2017 Simon Rowe <simon.rowe@citrix.com> - 1.5.1-1
- CA-243752: signing-server crashes: 'retries referenced before assignment'

* Mon Feb 13 2017 Simon Rowe <simon.rowe@citrix.com> - 1.5.0-1
- Change makefile to be generic rather than hotfix-specific

* Wed Feb 08 2017 Simon Rowe <simon.rowe@citrix.com> - 1.4.2-1
- Fix hotfix building for non-root users

* Tue Feb 07 2017 Simon Rowe <simon.rowe@citrix.com> - 1.4.1-1
- Added signing subpackage

* Fri Jan 27 2017 Simon Rowe <simon.rowe@citrix.com> - 1.4.0-1
- Added hotfix subpackage

* Sun Jan 22 2017 Simon Rowe <simon.rowe@citrix.com> - 1.3.4-1
- Fix expect timeouts
- Added source signing tool

* Tue Jan 17 2017 Simon Rowe <simon.rowe@citrix.com> - 1.3.2-1
- Escape key UIDs between GnuPG client and server

* Mon Jan 16 2017 Simon Rowe <simon.rowe@citrix.com> - 1.3.1-1
- Add systemd sign-server service

* Fri Jan 13 2017 Simon Rowe <simon.rowe@citrix.com> - 1.3.0-1
- Added key signing tools

* Thu Jan 12 2017 Simon Rowe <simon.rowe@citrix.com> - 1.2.0-1
- Added signing subpackages

* Tue Sep 13 2016 Simon Rowe <simon.rowe@citrix.com> - 1.0.0-1
- Initial packaging
