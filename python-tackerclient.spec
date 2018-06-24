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

%package -n python2-%{sclient}
Summary:    OpenStack tacker client
%{?python_provide:%python_provide python2-%{sclient}}

BuildRequires:  python2-devel
BuildRequires:  python2-mock
BuildRequires:  python2-fixtures
BuildRequires:  python2-flake8
BuildRequires:  python2-hacking
BuildRequires:  python2-keystoneclient
BuildRequires:  python2-oslo-log
BuildRequires:  python2-oslo-serialization
BuildRequires:  python2-pbr
BuildRequires:  python2-reno
BuildRequires:  python2-setuptools
BuildRequires:  python2-subunit
BuildRequires:  python2-testrepository
BuildRequires:  python2-testtools
BuildRequires:  python2-cliff
BuildRequires:  python2-mox

Requires:   python2-pbr >= 2.0.0
Requires:   python2-babel >= 2.3.4
Requires:   python2-cliff >= 2.8.0
Requires:   python2-iso8601 >= 0.1.11
Requires:   python2-keystoneclient >= 1:3.8.0
Requires:   python2-oslo-i18n >= 3.15.3
Requires:   python2-oslo-log >= 3.36.0
Requires:   python2-oslo-serialization >= 2.18.0
Requires:   python2-oslo-utils >= 3.33.0
Requires:   python2-requests >= 2.14.2
Requires:   python2-six >= 1.10.0
Requires:   python2-stevedore >= 1.20.0
Requires:   python2-osc-lib >= 1.8.0
Requires:   python2-netaddr >= 0.7.18
%if 0%{?fedora} > 0
Requires:   python2-simplejson >= 3.5.1
%else
Requires:   python-simplejson >= 3.5.1
%endif

%description -n python2-%{sclient}
OpenStack tacker client


%package -n python2-%{sclient}-tests-unit
Summary:    OpenStack taker client unit tests
Requires:   python2-%{sclient} = %{version}-%{release}

Requires:  python2-fixtures
Requires:  python2-flake8
Requires:  python2-hacking
Requires:  python2-oslo-log
Requires:  python2-oslo-serialization
Requires:  python2-pbr
Requires:  python2-setuptools
Requires:  python2-subunit
Requires:  python2-testtools
Requires:  python2-mock
Requires:  python2-testrepository
Requires:  python2-mox


%description -n python2-%{sclient}-tests-unit
OpenStack tacker client unit tests

This package contains the tacker client test files.


%package -n python-%{sclient}-doc
Summary:    OpenStack tacker client documentation

BuildRequires: python2-sphinx
BuildRequires: python2-openstackdocstheme

%description -n python-%{sclient}-doc
OpenStack tacker client documentation

This package contains the documentation for tacker client.

%if 0%{?with_python3}
%package -n python3-%{sclient}
Summary:    OpenStack tacker client
%{?python_provide:%python_provide python3-%{sclient}}

BuildRequires:  python3-devel
BuildRequires:  python3-cliff
BuildRequires:  python3-fixtures
BuildRequires:  python3-flake8
BuildRequires:  python3-hacking
BuildRequires:  python3-keystoneclient
BuildRequires:  python3-mox3
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-pbr
BuildRequires:  python3-reno
BuildRequires:  python3-setuptools
BuildRequires:  python3-subunit
BuildRequires:  python3-testrepository
BuildRequires:  python3-testtools
BuildRequires:  python3-mock


Requires:   python3-pbr >= 2.0.0
Requires:   python3-babel >= 2.3.4
Requires:   python3-cliff >= 2.8.0
Requires:   python3-iso8601 >= 0.1.11
Requires:   python3-keystoneclient >= 1:3.8.0
Requires:   python3-netaddr >= 0.7.18
Requires:   python3-oslo-i18n >= 3.15.3
Requires:   python3-oslo-log >= 3.36.0
Requires:   python3-oslo-serialization >= 2.18.0
Requires:   python3-oslo-utils >= 3.33.0
Requires:   python3-requests >= 2.14.2
Requires:   python3-simplejson >= 3.5.1
Requires:   python3-six >= 1.10.0
Requires:   python3-stevedore >= 1.20.0
Requires:   python3-osc-lib >= 1.8.0

%description -n python3-%{sclient}
OpenStack tacker client


%package -n python3-%{sclient}-tests-unit
Summary:    OpenStack tacker client unit tests
Requires:   python3-%{sclient} = %{version}-%{release}

Requires:  python3-fixtures
Requires:  python3-flake8
Requires:  python3-hacking
Requires:  python3-mox3
Requires:  python3-oslo-log
Requires:  python3-oslo-serialization
Requires:  python3-pbr
Requires:  python3-setuptools
Requires:  python3-subunit
Requires:  python3-testrepository
Requires:  python3-testtools
Requires:  python3-mock


%description -n python3-%{sclient}-tests-unit
OpenStack tacker client unit tests

This package contains the tacker client unit test files.

%endif # with_python3


%description
OpenStack tacker client.


%prep
%autosetup -n %{client}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%{__python2} setup.py build_sphinx -b man

%install

%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/%{executable}-%{python3_version}
ln -s ./%{executable}-%{python3_version} %{buildroot}%{_bindir}/%{executable}-3
%endif

%py2_install
install -p -D -m 644 -v doc/build/man/tacker.1 %{buildroot}%{_mandir}/man1/tacker.1
mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/%{executable}-%{python2_version}
ln -s ./%{executable}-%{python2_version} %{buildroot}%{_bindir}/%{executable}-2
ln -s ./%{executable}-2 %{buildroot}%{_bindir}/%{executable}

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{sclient}
%license LICENSE
%{python2_sitelib}/%{sclient}
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/%{sclient}/tests
%{_bindir}/%{executable}-%{python2_version}
%{_bindir}/%{executable}-2
%{_bindir}/%{executable}
%{_mandir}/man1/*

%files -n python2-%{sclient}-tests-unit
%license LICENSE
%{python2_sitelib}/%{sclient}/tests

%files -n python-%{sclient}-doc
%license LICENSE
%doc doc/build/html README.rst

%if 0%{?with_python3}
%files -n python3-%{sclient}
%license LICENSE
%{python3_sitelib}/%{sclient}
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/%{sclient}/tests
%{_bindir}/%{executable}-%{python3_version}
%{_bindir}/%{executable}-3

%files -n python3-%{sclient}-tests-unit
%license LICENSE
%{python3_sitelib}/%{sclient}/tests
%endif # with_python3

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/python-tackerclient/commit/?id=2156f7924d419d0fcf1249ce04ba54c6f113789c
