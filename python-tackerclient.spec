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

%package -n python2-%{sclient}
Summary:    OpenStack tacker client
%{?python_provide:%python_provide python2-%{sclient}}

BuildRequires:  pyflakes
BuildRequires:  python2-devel
BuildRequires:  python2-mock
BuildRequires:  python-cliff
BuildRequires:  python-coverage
BuildRequires:  python-fixtures
BuildRequires:  python-flake8
BuildRequires:  python-hacking
BuildRequires:  python-keystoneclient
BuildRequires:  python-mox
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-serialization
BuildRequires:  python-pbr
BuildRequires:  python-pep8
BuildRequires:  python-reno
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-subunit
BuildRequires:  python-testrepository
BuildRequires:  python-testtools
BuildRequires:  git

Requires:   python-pbr >= 2.0.0
Requires:   python-babel >= 2.3.4
Requires:   python-cliff >= 2.8.0
Requires:   python-iso8601 >= 0.1.11
Requires:   python-keystoneclient >= 1:3.8.0
Requires:   python-netaddr >= 0.7.13
Requires:   python-oslo-i18n >= 2.1.0
Requires:   python-oslo-log >= 3.22.0
Requires:   python-oslo-serialization >= 1.10.0
Requires:   python-oslo-sphinx >= 4.7.0
Requires:   python-oslo-utils >= 3.20.0
Requires:   python-requests >= 2.10.0
Requires:   python-simplejson >= 2.2.0
Requires:   python-six >= 1.9.0
Requires:   python-stevedore >= 1.20.0

%description -n python2-%{sclient}
OpenStack tacker client


%package -n python2-%{sclient}-tests-unit
Summary:    OpenStack taker client unit tests
Requires:   python2-%{sclient} = %{version}-%{release}

Requires:  pyflakes
Requires:  python-coverage
Requires:  python-fixtures
Requires:  python-flake8
Requires:  python-hacking
Requires:  python-mox
Requires:  python-oslo-log
Requires:  python-oslo-serialization
Requires:  python-pbr
Requires:  python-pep8
Requires:  python-reno
Requires:  python-setuptools
Requires:  python-sphinx
Requires:  python-subunit
Requires:  python-testrepository
Requires:  python-testtools
Requires:  python2-mock


%description -n python2-%{sclient}-tests-unit
OpenStack tacker client unit tests

This package contains the tacker client test files.


%package -n python-%{sclient}-doc
Summary:    OpenStack tacker client documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description -n python-%{sclient}-doc
OpenStack tacker client documentation

This package contains the documentation for tacker client.

%if 0%{?with_python3}
%package -n python3-%{sclient}
Summary:    OpenStack tacker client
%{?python_provide:%python_provide python3-%{sclient}}

BuildRequires:  python3-pyflakes
BuildRequires:  python3-devel
BuildRequires:  python3-cliff
BuildRequires:  python3-coverage
BuildRequires:  python3-fixtures
BuildRequires:  python3-flake8
BuildRequires:  python3-hacking
BuildRequires:  python3-keystoneclient
BuildRequires:  python3-mox3
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-pbr
BuildRequires:  python3-pep8
BuildRequires:  python3-reno
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
BuildRequires:  python3-subunit
BuildRequires:  python3-testrepository
BuildRequires:  python3-testtools
BuildRequires:  python3-mock


Requires:   python3-pbr >= 2.0.0
Requires:   python3-babel >= 2.3.4
Requires:   python3-cliff >= 2.8.0
Requires:   python3-iso8601 >= 0.1.11
Requires:   python3-keystoneclient >= 1:3.8.0
Requires:   python3-netaddr >= 0.7.13
Requires:   python3-oslo-i18n >= 2.1.0
Requires:   python3-oslo-log >= 3.22.0
Requires:   python3-oslo-serialization >= 1.10.0
Requires:   python3-oslo-sphinx >= 4.7.0
Requires:   python3-oslo-utils >= 3.20.0
Requires:   python3-requests >= 2.10.0
Requires:   python3-simplejson >= 2.2.0
Requires:   python3-six >= 1.9.0
Requires:   python3-stevedore >= 1.20.0

%description -n python3-%{sclient}
OpenStack tacker client


%package -n python3-%{sclient}-tests-unit
Summary:    OpenStack tacker client unit tests
Requires:   python3-%{sclient} = %{version}-%{release}

Requires:  python3-pyflakes
Requires:  python3-coverage
Requires:  python3-fixtures
Requires:  python3-flake8
Requires:  python3-hacking
Requires:  python3-mox3
Requires:  python3-oslo-log
Requires:  python3-oslo-serialization
Requires:  python3-pbr
Requires:  python3-pep8
Requires:  python3-reno
Requires:  python3-setuptools
Requires:  python3-sphinx
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
sphinx-build -b html doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

sphinx-build -b man doc/source man

%install

%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/%{executable}-%{python3_version}
ln -s ./%{executable}-%{python3_version} %{buildroot}%{_bindir}/%{executable}-3
%endif

%py2_install
install -p -D -m 644 -v man/python-tackerclient.1 %{buildroot}%{_mandir}/man1/python-tackerclient.1
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
%doc html README.rst

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
* Thu Dec 22 2016 Dan Radez <dradez@redhat.com> - 0.7.0-2
- Copied from koji to RDO

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7.0-2
- Rebuild for Python 3.6

* Tue Sep 13 2016 Alfredo Moralejo <amoralej@redhat.com> - 0.7.0-1
- update to version 0.7.0

* Wed Jul 6 2016 Alfredo Moralejo <amoralej@redhat.com> - 0.4.0-1
- initial package
