#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (require some db)
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module

%define 	module	django-celery
Summary:	Celery integration for Django
Summary(pl.UTF-8):	Integracja Celery z Django
Name:		python-%{module}
Version:	3.3.1
Release:	3
License:	BSD
Group:		Development/Languages/Python
Source0:	https://files.pythonhosted.org/packages/source/d/django-celery/%{module}-%{version}.tar.gz
# Source0-md5:	935503afef427ae70400c6ec3b5791c8
Patch0:		django-celery-requires.patch
URL:		https://pypi.org/project/django-celery/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-celery >= 3.1.15
BuildRequires:	python-django >= 1.8
BuildRequires:	python-django-nose
BuildRequires:	python-mock
BuildRequires:	python-nose
BuildRequires:	python-nose-cover3
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-celery >= 3.1.15
BuildRequires:	python3-django >= 1.8
BuildRequires:	python3-django-nose
BuildRequires:	python3-nose
BuildRequires:	python3-nose-cover3
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python-celery
BuildRequires:	python-django >= 1.8
BuildRequires:	python-sphinxcontrib-issuetracker
BuildRequires:	sphinx-pdg-2
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Provides Celery integration for Django; Using Django ORM and cache
backend for storing results, autodiscovery of task modules for
applications listed in INSTALLED_APPS, and more.

%description -l pl.UTF-8
Pakiet dostarcza integrację Celery z Django - korzystanie z djangowego
ORM, backendu pamięci podręcznej do przechowywania wyników,
automatycznego wykrywania modułów zadań do aplikacji wymienionych w
INSTALLED_APPS itd.

%package -n python3-%{module}
Summary:	Celery integration for Django
Summary(pl.UTF-8):	Integracja Celery z Django
Group:		Development/Languages/Python

%description -n python3-%{module}
Provides Celery integration for Django; Using Django ORM and cache
backend for storing results, autodiscovery of task modules for
applications listed in INSTALLED_APPS, and more.

%description -n python3-%{module} -l pl.UTF-8
Pakiet dostarcza integrację Celery z Django - korzystanie z djangowego
ORM, backendu pamięci podręcznej do przechowywania wyników,
automatycznego wykrywania modułów zadań do aplikacji wymienionych w
INSTALLED_APPS itd.

%package apidocs
Summary:	API documentation for Python django-celery module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona django-celery
Group:		Documentation

%description apidocs
API documentation for Python django-celery module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona django-celery.

%prep
%setup -q -n %{module}-%{version}
%patch -P 0 -p1

# avoid network usage via sphinxcontrib-issuetracker during docs build
%{__sed} -i -e 's/Issue #\([0-9]\+\)/Issue ``#\1``/g' docs/changelog.rst

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/djcelery/tests
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/djcelery/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS Changelog FAQ LICENSE README.rst THANKS
%{py_sitescriptdir}/djcelery
%{py_sitescriptdir}/django_celery-%{version}-py*.egg-info
%endif

%if %{with python2}
%files -n python3-django-celery
%defattr(644,root,root,755)
%doc AUTHORS Changelog FAQ LICENSE README.rst THANKS
%{py3_sitescriptdir}/djcelery
%{py3_sitescriptdir}/django_celery-%{version}-py*.egg-info
%endif
