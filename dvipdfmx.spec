%define _texmf_main %{_datadir}/texmf
%define _texmf_conf %{_sysconfdir}/texmf

%define snapshot 20100328

Name:           dvipdfmx
Version:        0
Release:        %mkrel 0.1.%{snapshot}
Summary:        A DVI to PDF translator

Group:          Publishing
License:        GPLv2+
URL:            https://project.ktug.or.kr/dvipdfmx/
Source0:        http://project.ktug.or.kr/dvipdfmx/snapshot/latest/%{name}-%{snapshot}.tar.gz
Patch0:		dvipdfmx-20100328-ebb-to-ebbx.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot

BuildRequires:  kpathsea-devel libpng-devel zlib-devel libpaper-devel texlive-texmf
Requires:       texlive-texmf-fonts
Requires:       ghostscript
Requires(post): /usr/bin/mktexlsr
Requires(postun): /usr/bin/mktexlsr

%description
The dvipdfmx (formerly dvipdfm-cjk) project provides an eXtended version
of the dvipdfm, a DVI to PDF translator developed by Mark A. Wicks.

The primary goal of this project is to support multi-byte character
encodings and large character sets for East Asian languages. The secondary
goal is to support as many features as pdfTeX developed by Han The Thanh.

This project is a combined work of the dvipdfm-jpn project by Shunsaku
Hirata and its modified one, dvipdfm-kor, by Jin-Hwan Cho.


%prep
%setup -q -n %{name}-%{snapshot}
%patch0 -p1

%build
%configure
%make

# create customized cid-x.map for dvipdfmx (#418091)
cat <<EOF >> cid-x.map
%%
%% ASCII pTeX Examples
%%

%% Ryumin and GothicBBB found in PostScript printers:
rml  H !Ryumin-Light
gbm  H !GothicBBB-Medium
rmlv V !Ryumin-Light
gbmv V !GothicBBB-Medium
EOF


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

mkdir -p %{buildroot}%{_texmf_conf}/dvipdfmx
mv cid-x.map %{buildroot}%{_texmf_conf}/dvipdfmx/


%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/mktexlsr > /dev/null 2>&1 || :

%postun
/usr/bin/mktexlsr > /dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/dvipdfmx
%{_bindir}/extractbb
%{_bindir}/ebbx
%dir %{_texmf_conf}/dvipdfmx/
%config(noreplace) %{_texmf_conf}/dvipdfmx/cid-x.map
%{_texmf_main}/dvipdfmx
%{_texmf_main}/fonts/map/dvipdfmx/cid-x.map
%{_texmf_main}/fonts/map/glyphlist/glyphlist.txt
%{_texmf_main}/fonts/map/glyphlist/pdfglyphlist.txt
%{_texmf_main}/fonts/cmap/dvipdfmx/EUC-UCS2
%{_mandir}/man1/extractbb.1.*

