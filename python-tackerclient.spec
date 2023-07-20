%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global client python-tackerclient
%global sclient tackerclient
%global executable tacker
%global with_doc 1

Name:       %{client}
Version:    XXX
Release:    XXX
Summary:    OpenStack Tacker client
License:    Apache-2.0
URL:        http://launchpad.net/%{client}/

Source0:    http://tarballs.openstack.org/%{client}/%{client}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{client}/%{client}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:  git-core

%package -n python3-%{sclient}
Summary:    OpenStack tacker client
Obsoletes: python2-%{sclient} < %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
%description -n python3-%{sclient}
OpenStack tacker client


%package -n python3-%{sclient}-tests-unit
Summary:    OpenStack taker client unit tests
Requires:   python3-%{sclient} = %{version}-%{release}

Requires:  python3-fixtures
Requires:  python3-flake8
Requires:  python3-hacking
Requires:  python3-oslo-log
Requires:  python3-oslo-serialization
Requires:  python3-pbr
Requires:  python3-setuptools
Requires:  python3-subunit
Requires:  python3-testtools
Requires:  python3-mock
Requires:  python3-stestr

%description -n python3-%{sclient}-tests-unit
OpenStack tacker client unit tests

This package contains the tacker client test files.


%if 0%{?with_doc}
%package -n python-%{sclient}-doc
Summary:    OpenStack tacker client documentation

%description -n python-%{sclient}-doc
OpenStack tacker client documentation

This package contains the documentation for tacker client.
%endif

%description
OpenStack tacker client.

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{client}-%{upstream_version} -S git -p1

# Fix rpmlint warning for CRLF line termination
sed -i 's/\r$//' ./doc/source/cli/vnf_package_commands.rst ./doc/source/cli/commands.rst

# Use assertCountEqual instead of assertItemsEqual until
# https://review.opendev.org/c/openstack/python-tackerclient/+/791095 is in next tag release
sed -i 's/assertItemsEqual/assertCountEqual/g' tackerclient/tests/unit/osc/v1/test_vnflcm_op_occs.py

# Skip flaky test test_take_action_with_filter
sed -i '/^import sys/a import unittest' tackerclient/tests/unit/osc/v1/test_vnflcm_op_occs.py
sed -i '/test_take_action_with_filter/i \    @unittest.skip(reason="Skip flaky test until its fixed upstream lp#1919350")' tackerclient/tests/unit/osc/v1/test_vnflcm_op_occs.py


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

sphinx-build -W -b man doc/source doc/build/man
%endif


%if 0%{?with_doc}
install -p -D -m 644 -v doc/build/man/tacker.1 %{buildroot}%{_mandir}/man1/tacker.1
%endif

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{executable} %{buildroot}%{_bindir}/%{executable}-3

%check
%tox -e %{default_toxenv}

%files -n python3-%{sclient}
%license LICENSE
%{python3_sitelib}/%{sclient}
%{python3_sitelib}/*.dist-info
%exclude %{python3_sitelib}/%{sclient}/tests
%{_bindir}/%{executable}-3
%{_bindir}/%{executable}

%if 0%{?with_doc}
%{_mandir}/man1/*
%endif

%files -n python3-%{sclient}-tests-unit
%license LICENSE
%{python3_sitelib}/%{sclient}/tests

%if 0%{?with_doc}
%files -n python-%{sclient}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
