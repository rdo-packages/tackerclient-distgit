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

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global client python-tackerclient
%global sclient tackerclient
%global executable tacker

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
%{?python_provide:%python_provide python2-%{sclient}}

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
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-cliff
BuildRequires:  python%{pyver}-mox

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
Requires:  python%{pyver}-mox


%description -n python%{pyver}-%{sclient}-tests-unit
OpenStack tacker client unit tests

This package contains the tacker client test files.


%package -n python%{pyver}-%{sclient}-doc
Summary:    OpenStack tacker client documentation
%{?python_provide:%python_provide python%{pyver}-%{sclient}-doc}

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme

%description -n python%{pyver}-%{sclient}-doc
OpenStack tacker client documentation

This package contains the documentation for tacker client.

%description
OpenStack tacker client.

%prep
%autosetup -n %{client}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%{pyver_build}

# generate html docs
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

sphinx-build-%{pyver} -W -b man doc/source doc/build/man

%install

%{pyver_install}
install -p -D -m 644 -v doc/build/man/tacker.1 %{buildroot}%{_mandir}/man1/tacker.1

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{executable} %{buildroot}%{_bindir}/%{executable}-%{pyver}

%check
export OS_TEST_PATH='./tackerclient/tests/unit'
stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{sclient}
%license LICENSE
%{pyver_sitelib}/%{sclient}
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/%{sclient}/tests
%{_bindir}/%{executable}-%{pyver}
%{_bindir}/%{executable}
%{_mandir}/man1/*

%files -n python%{pyver}-%{sclient}-tests-unit
%license LICENSE
%{pyver_sitelib}/%{sclient}/tests

%files -n python%{pyver}-%{sclient}-doc
%license LICENSE
%doc doc/build/html README.rst

%changelog

