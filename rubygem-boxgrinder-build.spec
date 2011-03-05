%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname boxgrinder-build
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8

Summary: A tool for creating appliances from simple plain text files
Name: rubygem-%{gemname}
Version: 0.9.0
Release: 1%{?dist}
Group: Development/Languages
License: LGPLv3+
URL: http://boxgrinder.org/
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: ruby(abi) = %{rubyabi}
Requires: rubygem(boxgrinder-core) >= 0.2.1
Requires: rubygem(boxgrinder-core) < 0.3.0
Requires: ruby-libguestfs
Requires: parted
Requires: e2fsprogs

BuildRequires: rubygem(rake)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(boxgrinder-core) >= 0.2.1
BuildRequires: rubygem(boxgrinder-core) < 0.3.0
BuildRequires: rubygem(echoe)
BuildRequires: ruby-libguestfs

# EBS and S3

Requires: rubygem(amazon-ec2)
# Fixes blankslate error
Requires: rubygem(builder)
Requires: rubygem(aws)
Requires: euca2ools >= 1.3.1-4

BuildRequires: rubygem(amazon-ec2)
BuildRequires: rubygem(aws)
# Fixes blankslate error
BuildRequires: rubygem(builder)

# SFTP

Requires: rubygem(net-sftp)
Requires: rubygem(net-ssh)
Requires: rubygem(progressbar)

BuildRequires: rubygem(net-sftp)
BuildRequires: rubygem(net-ssh)
BuildRequires: rubygem(progressbar)

# RPM-BASED

Requires: appliance-tools
Requires: yum-utils

# EC2

Requires: rsync
Requires: wget
Requires: util-linux

BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

Obsoletes: rubygem(boxgrinder-build-ebs-delivery-plugin)
Obsoletes: rubygem(boxgrinder-build-s3-delivery-plugin)
Obsoletes: rubygem(boxgrinder-build-local-delivery-plugin)
Obsoletes: rubygem(boxgrinder-build-sftp-delivery-plugin)

Obsoletes: rubygem(boxgrinder-build-centos-os-plugin)
Obsoletes: rubygem(boxgrinder-build-rhel-os-plugin)
Obsoletes: rubygem(boxgrinder-build-fedora-os-plugin)
Obsoletes: rubygem(boxgrinder-build-rpm-based-os-plugin)

Obsoletes: rubygem(boxgrinder-build-ec2-platform-plugin)
Obsoletes: rubygem(boxgrinder-build-vmware-platform-plugin)
Obsoletes: rubygem(boxgrinder-build-virtualbox-platform-plugin)

%description
A tool for creating appliances from simple plain text files for various
virtual environments

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep

%build

%install
rm -rf %{buildroot}
rm -rf %{_builddir}%{gemdir}

mkdir -p %{_builddir}%{gemdir}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{gemdir}

gem install --local --install-dir %{_builddir}%{gemdir} \
            --force --rdoc %{SOURCE0}
mv %{_builddir}%{gemdir}/bin/* %{buildroot}/%{_bindir}
find %{_builddir}%{geminstdir}/bin -type f | xargs chmod a+x
cp -r %{_builddir}%{gemdir}/* %{buildroot}/%{gemdir}

%check
pushd %{_builddir}/%{geminstdir}
rake spec
popd

%files
%defattr(-, root, root, -)
%{_bindir}/boxgrinder-build
%dir %{geminstdir}
%{geminstdir}/bin
%{geminstdir}/lib
%doc %{geminstdir}/CHANGELOG
%doc %{geminstdir}/LICENSE
%doc %{geminstdir}/README.md
%doc %{geminstdir}/Manifest
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-, root, root, -)
%{geminstdir}/spec
%{geminstdir}/Rakefile
%{geminstdir}/rubygem-%{gemname}.spec
%{geminstdir}/%{gemname}.gemspec
%{gemdir}/doc/%{gemname}-%{version}

%changelog

* Tue Mar 01 2011 <msavy@redhat.com> - 0.9.0-1
- Upstream release: 0.8.2
- [BGBUILD-103] README to indicate supported operating systems / requirements
- [BGBUILD-169] S3 plugin temporary work-around for EL5
- [BGBUILD-174] Move plugins to boxgrinder-build gem
- [BGBUILD-175] Rewrite boxgrinder CLI to remove thor dependency
- [BGBUILD-81] post command execution w/ setarch breaks commands which are scripts
- [BGBUILD-173] Include setarch package in default package list for RPM-based OSes
- [BGBUILD-177] Fedora 13 builds have enabled firewall although they shouldn't have it

* Tue Feb 16 2011  <mgoldman@redhat.com> - 0.8.1-1
- Upstream release: 0.8.1
- [BGBUILD-141] Long delay after "Preparing guestfs" message when creating new image
- [BGBUILD-150] Cyclical inclusion dependencies in appliance definition files are not detected/handled
- [BGBUILD-165] Use version in dependencies in gem and in RPM only where necessary

* Tue Jan 04 2011  <mgoldman@redhat.com> - 0.8.0-1
- Upstream release: 0.8.0
- Added BuildRoot tag to build for EPEL 5
- [BGBUILD-128] Allow to specify plugin configuration using CLI
- [BGBUILD-134] Replace rubygem-commander with rubygem-thor
- [BGBUILD-79] Allow to use BoxGrinder Build as a library
- [BGBUILD-127] Use appliance definition object instead of a file when using BG as a library
- [BGBUILD-68] Global .boxgrinder/config or rc style file for config
- [BGBUILD-131] Check if OS is supported before executing the plugin
- [BGBUILD-72] Add support for growing (not pre-allocated) disks for KVM/Xen
- [BGBUILD-133] Support a consolidated configuration file
- [BGBUILD-138] enablerepo path is not escaped when calling repoquery
- [BGBUILD-147] Allow to list installed plugins and version information

* Mon Dec 20 2010  <mgoldman@redhat.com> - 0.7.1-1
- Upstream release: 0.7.1
- [BGBUILD-123] Remove RPM database recreation code
- [BGBUILD-124] Guestfs fails while mounting multiple partitions with '_' prefix

* Fri Dec 17 2010  <mgoldman@redhat.com> - 0.7.0-1
- Updated to upstream version: 0.7.0
- [BGBUILD-113] Allow to specify supported file formats for operating system plugin
- [BGBUILD-73] Add support for kickstart files
- [BGBUILD-80] VMware .tgz Bundle Should Expand Into Subdirectory, Not Current Directory
- [BGBUILD-118] Enable SElinux in guestfs
- [BGBUILD-119] Fix SElinux issues on EC2 appliances

* Thu Dec 02 2010  <mgoldman@redhat.com> - 0.6.5-1
- Updated to new upstream release: 0.6.5

* Mon Nov 22 2010  <mgoldman@redhat.com> - 0.6.4-3
- Changelog rewritten
- Added Require: parted and e2fsprogs

* Sat Nov 20 2010  <mgoldman@redhat.com> - 0.6.4-2
- Small set of spec file adjustments

* Mon Nov 15 2010  <mgoldman@redhat.com> - 0.6.4-1
- Updated to new upstream release: 0.6.4
- Removed BuildRoot tag
- Adjusted Requires and BuildRequires
- Different approach for testing
- [BGBUILD-98] Use hashery gem
- [BGBUILD-99] Timeout exception is not catched on non-EC2 platfrom in GuestFSHelper
- [BGBUILD-92] Enable --trace switch by default
- [BGBUILD-91] Log exceptions to log file

* Tue Nov 09 2010  <mgoldman@redhat.com> - 0.6.3-1
- [BGBUILD-94] Check if set_network call is avaialbe in libguestfs
- Added 'check' section that executes tests

* Wed Nov 03 2010  <mgoldman@redhat.com> - 0.6.2-1
- [BGBUILD-84] Don't use in libguestfs qemu-kvm where hardware accleration isn't available

* Mon Oct 18 2010  <mgoldman@redhat.com> - 0.6.1-1
- Initial package
