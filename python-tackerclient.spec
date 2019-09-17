# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global client python-tackerclient
%global sclient tackerclient
%global executable tacker
%global with_doc 1

Name:       %{client}
Version:    XXX
Release:    XXX
Summary:    OpenStack Tacker client
License:    ASL 2.0
URL:        http://launchpad.net/%{client}/

Source0:    http://tarballs.openstack.org/%{client}/%{client}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  git

%package -n python%{pyver}-%{sclient}
Summary:    OpenStack tacker client
%{?python_provide:%python_provide python%{pyver}-%{sclient}}
%if %{pyver} == 3
Obsoletes: python2-%{sclient} < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-flake8
BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-keystoneclient
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-oslo-serialization
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-reno
BuildRequires:  python%{pyver}-requests-mock
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-cliff

Requires:   python%{pyver}-pbr >= 2.0.0
Requires:   python%{pyver}-babel >= 2.3.4
Requires:   python%{pyver}-cliff >= 2.8.0
Requires:   python%{pyver}-iso8601 >= 0.1.11
Requires:   python%{pyver}-keystoneclient >= 1:3.8.0
Requires:   python%{pyver}-oslo-i18n >= 3.15.3
Requires:   python%{pyver}-oslo-log >= 3.36.0
Requires:   python%{pyver}-oslo-serialization >= 2.18.0
Requires:   python%{pyver}-oslo-utils >= 3.33.0
Requires:   python%{pyver}-requests >= 2.14.2
Requires:   python%{pyver}-six >= 1.10.0
Requires:   python%{pyver}-stevedore >= 1.20.0
Requires:   python%{pyver}-osc-lib >= 1.8.0
Requires:   python%{pyver}-netaddr >= 0.7.18
# Handle python2 exception
%if %{pyver} == 2
Requires:   python-simplejson >= 3.5.1
%else
Requires:   python%{pyver}-simplejson >= 3.5.1
%endif

%description -n python%{pyver}-%{sclient}
OpenStack tacker client


%package -n python%{pyver}-%{sclient}-tests-unit
Summary:    OpenStack taker client unit tests
Requires:   python%{pyver}-%{sclient} = %{version}-%{release}

Requires:  python%{pyver}-fixtures
Requires:  python%{pyver}-flake8
Requires:  python%{pyver}-hacking
Requires:  python%{pyver}-oslo-log
Requires:  python%{pyver}-oslo-serialization
Requires:  python%{pyver}-pbr
Requires:  python%{pyver}-setuptools
Requires:  python%{pyver}-subunit
Requires:  python%{pyver}-testtools
Requires:  python%{pyver}-mock
Requires:  python%{pyver}-stestr

%description -n python%{pyver}-%{sclient}-tests-unit
OpenStack tacker client unit tests

This package contains the tacker client test files.


%if 0%{?with_doc}
%package -n python-%{sclient}-doc
Summary:    OpenStack tacker client documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-osc-lib
BuildRequires: python%{pyver}-ddt
BuildRequires: python%{pyver}-openstackdocstheme

%description -n python-%{sclient}-doc
OpenStack tacker client documentation

This package contains the documentation for tacker client.
%endif

%description
OpenStack tacker client.

%prep
%autosetup -n %{client}-%{upstream_version} -S git

# Fix rpmlint warning for CRLF line termination
sed -i 's/\r$//' ./doc/source/cli/vnf_package_commands.rst ./doc/source/cli/commands.rst

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

sphinx-build-%{pyver} -W -b man doc/source doc/build/man
%endif

%install

%{pyver_install}

%if 0%{?with_doc}
install -p -D -m 644 -v doc/build/man/tacker.1 %{buildroot}%{_mandir}/man1/tacker.1
%endif

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{executable} %{buildroot}%{_bindir}/%{executable}-%{pyver}

%check
export OS_TEST_PATH='./tackerclient/tests/unit'
PYTHON=%{pyver_bin} stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{sclient}
%license LICENSE
%{pyver_sitelib}/%{sclient}
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/%{sclient}/tests
%{_bindir}/%{executable}-%{pyver}
%{_bindir}/%{executable}

%if 0%{?with_doc}
%{_mandir}/man1/*
%endif

%files -n python%{pyver}-%{sclient}-tests-unit
%license LICENSE
%{pyver_sitelib}/%{sclient}/tests

%if 0%{?with_doc}
%files -n python-%{sclient}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/python-tackerclient/commit/?id=f4839f308ab341bbb4a8faa818b0d6eba2048819
