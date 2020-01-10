%if 0%{?fedora}
%global with_wayland 1
%global with_broadway 1
%endif

%global glib2_version 2.49.4
%global pango_version 1.37.3
%global atk_version 2.15.1
%global cairo_version 1.14.0
%global gdk_pixbuf_version 2.30.0
%global xrandr_version 1.5.0
%global wayland_version 1.9.91
%global wayland_protocols_version 1.7
%global epoxy_version 1.0

%global bin_version 3.0.0

%global _changelog_trimtime %(date +%s -d "1 year ago")

Name: gtk3
Version: 3.22.10
Release: 4%{?dist}
Summary: The GIMP ToolKit (GTK+), a library for creating GUIs for X

License: LGPLv2+
URL: http://www.gtk.org
Source0: http://download.gnome.org/sources/gtk+/3.22/gtk+-%{version}.tar.xz
source1: ja.po

# Downstream fix to filter out X-RHEL-AliasOf
# https://bugzilla.redhat.com/show_bug.cgi?id=1259292
Patch18: app-chooser-fixes.patch

BuildRequires: pkgconfig(atk) >= %{atk_version}
BuildRequires: pkgconfig(atk-bridge-2.0)
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(cairo) >= %{cairo_version}
BuildRequires: pkgconfig(cairo-gobject) >= %{cairo_version}
BuildRequires: pkgconfig(pango) >= %{pango_version}
BuildRequires: pkgconfig(gdk-pixbuf-2.0) >= %{gdk_pixbuf_version}
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xrandr) >= %{xrandr_version}
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xinerama)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(epoxy)
BuildRequires: gettext
BuildRequires: gtk-doc
BuildRequires: cups-devel
BuildRequires: pkgconfig(rest-0.7)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(colord)
BuildRequires: pkgconfig(avahi-gobject)
BuildRequires: desktop-file-utils
%if 0%{?with_wayland}
BuildRequires: pkgconfig(wayland-client) >= %{wayland_version}
BuildRequires: pkgconfig(wayland-cursor) >= %{wayland_version}
BuildRequires: pkgconfig(wayland-egl) >= %{wayland_version}
BuildRequires: pkgconfig(wayland-protocols) >= %{wayland_protocols_version}
BuildRequires: pkgconfig(xkbcommon)
%endif

# standard icons
Requires: adwaita-icon-theme
# required for icon theme apis to work
Requires: hicolor-icon-theme
# split out in a subpackage
Requires: gtk-update-icon-cache

Requires: atk%{?_isa} >= %{atk_version}
Requires: cairo%{?_isa} >= %{cairo_version}
Requires: cairo-gobject%{?_isa} >= %{cairo_version}
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: libepoxy%{?_isa} >= %{epoxy_version}
Requires: libXrandr%{?_isa} >= %{xrandr_version}
Requires: pango%{?_isa} >= %{pango_version}
%if 0%{?with_wayland}
Requires: libwayland-client%{?_isa} >= %{wayland_version}
Requires: libwayland-cursor%{?_isa} >= %{wayland_version}
%endif

# make sure we have a reasonable gsettings backend
%if 0%{?fedora}
Recommends: dconf%{?_isa}
%else
Requires: dconf%{?_isa}
%endif

# gtk3 itself includes the Adwaita theme now
Obsoletes: adwaita-gtk3-theme < 3.13.3
Provides: adwaita-gtk3-theme = %{version}-%{release}

# gtk3 no longer provides the GtkThemeEngine interface used there
Obsoletes: gtk3-engines <= 2.91.5-5.fc15
Obsoletes: gtk-solidity-engine < 0.4.1-9
Obsoletes: oxygen-gtk3 < 2:1.4.1

%description
GTK+ is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK+ is suitable for
projects ranging from small one-off tools to complete application
suites.

This package contains version 3 of GTK+.

%package -n gtk-update-icon-cache
Summary: Icon theme caching utility
# gtk-update-icon-cache used to be shipped in the gtk2 package
Conflicts: gtk2 < 2.24.29

%description -n gtk-update-icon-cache
GTK+ can use the cache files created by gtk-update-icon-cache to avoid a lot of
system call and disk seek overhead when the application starts. Since the
format of the cache files allows them to be mmap()ed shared between multiple
applications, the overall memory consumption is reduced as well.

%package immodules
Summary: Input methods for GTK+
Requires: gtk3%{?_isa} = %{version}-%{release}
# for im-cedilla.conf
Requires: gtk2-immodules%{?_isa}

%description immodules
The gtk3-immodules package contains standalone input methods that
are shipped as part of GTK+ 3.

%package immodule-xim
Summary: XIM support for GTK+
Requires: gtk3%{?_isa} = %{version}-%{release}

%description immodule-xim
The gtk3-immodule-xim package contains XIM support for GTK+ 3.

%package devel
Summary: Development files for GTK+
Requires: gtk3%{?_isa} = %{version}-%{release}
Obsoletes: gtk3-engines-devel <= 2.91.5-5.fc15

%description devel
This package contains the libraries and header files that are needed
for writing applications with version 3 of the GTK+ widget toolkit. If
you plan to develop applications with GTK+, consider installing the
gtk3-devel-docs package.

%package devel-docs
Summary: Developer documentation for GTK+
Requires: gtk3 = %{version}-%{release}

%description devel-docs
This package contains developer documentation for version 3 of the GTK+
widget toolkit.

%package tests
Summary: Tests for the %{name} package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%setup -q -n gtk+-%{version}
%patch18 -p1

cp %{SOURCE1} po/

%build
export CFLAGS='-fno-strict-aliasing %optflags'
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
        --enable-xkb \
        --enable-xinerama \
        --enable-xrandr \
        --enable-xfixes \
        --enable-xcomposite \
        --enable-xdamage \
        --enable-x11-backend \
%if 0%{?with_wayland}
        --enable-wayland-backend \
%endif
%if 0%{?with_broadway}
        --enable-broadway-backend \
%endif
        --enable-colord \
        --enable-installed-tests
)

# fight unused direct deps
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

make %{?_smp_mflags}

%install
%make_install RUN_QUERY_IMMODULES_TEST=false

%find_lang gtk30
%find_lang gtk30-properties

(cd $RPM_BUILD_ROOT%{_bindir}
 mv gtk-query-immodules-3.0 gtk-query-immodules-3.0-%{__isa_bits}
)

echo ".so man1/gtk-query-immodules-3.0.1" > $RPM_BUILD_ROOT%{_mandir}/man1/gtk-query-immodules-3.0-%{__isa_bits}.1

# Remove unpackaged files
find $RPM_BUILD_ROOT -name '*.la' -delete

%if !0%{?with_broadway}
rm $RPM_BUILD_ROOT%{_mandir}/man1/broadwayd.1*
%endif

touch $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/%{bin_version}/immodules.cache

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-3.0
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/modules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/immodules
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/%{bin_version}/theming-engines

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%post
/sbin/ldconfig
gtk-query-immodules-3.0-%{__isa_bits} --update-cache
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%post devel
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%post immodules
gtk-query-immodules-3.0-%{__isa_bits} --update-cache

%post immodule-xim
gtk-query-immodules-3.0-%{__isa_bits} --update-cache

%postun
/sbin/ldconfig
if [ $1 -gt 0 ]; then
  gtk-query-immodules-3.0-%{__isa_bits} --update-cache
fi
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%postun devel
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%postun immodules
gtk-query-immodules-3.0-%{__isa_bits} --update-cache

%postun immodule-xim
gtk-query-immodules-3.0-%{__isa_bits} --update-cache

%posttrans devel
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f gtk30.lang
%license COPYING
%doc AUTHORS NEWS README
%{_bindir}/gtk-query-immodules-3.0*
%{_bindir}/gtk-launch
%{_libdir}/libgtk-3.so.*
%{_libdir}/libgdk-3.so.*
%{_libdir}/libgailutil-3.so.*
%dir %{_libdir}/gtk-3.0
%dir %{_libdir}/gtk-3.0/%{bin_version}
%dir %{_datadir}/gtk-3.0
%{_libdir}/gtk-3.0/%{bin_version}/theming-engines
%dir %{_libdir}/gtk-3.0/%{bin_version}/immodules
%{_libdir}/gtk-3.0/%{bin_version}/printbackends
%{_libdir}/gtk-3.0/modules
%{_libdir}/gtk-3.0/immodules
%{_datadir}/themes/Default
%{_datadir}/themes/Emacs
%{_libdir}/girepository-1.0
%ghost %{_libdir}/gtk-3.0/%{bin_version}/immodules.cache
%{_mandir}/man1/gtk-query-immodules-3.0*
%{_mandir}/man1/gtk-launch.1*
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.FileChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.ColorChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.Debug.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.exampleapp.gschema.xml
%if 0%{?with_broadway}
%{_bindir}/broadwayd
%{_mandir}/man1/broadwayd.1*
%endif

%files -n gtk-update-icon-cache
%license COPYING
%{_bindir}/gtk-update-icon-cache
%{_mandir}/man1/gtk-update-icon-cache.1*

%files immodules
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-cedilla.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-am-et.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-cyrillic-translit.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-inuktitut.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ipa.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-multipress.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-thai.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ti-er.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ti-et.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-viqr.so
%if 0%{?with_broadway}
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-broadway.so
%endif
%config(noreplace) %{_sysconfdir}/gtk-3.0/im-multipress.conf

%files immodule-xim
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-xim.so

%files devel -f gtk30-properties.lang
%{_libdir}/lib*.so
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{_bindir}/gtk3-demo
%{_bindir}/gtk3-icon-browser
%{_bindir}/gtk-builder-tool
%{_bindir}/gtk-encode-symbolic-svg
%{_bindir}/gtk-query-settings
%{_datadir}/applications/gtk3-demo.desktop
%{_datadir}/applications/gtk3-icon-browser.desktop
%{_datadir}/applications/gtk3-widget-factory.desktop
%{_datadir}/icons/hicolor/*/apps/gtk3-demo.png
%{_datadir}/icons/hicolor/*/apps/gtk3-demo-symbolic.symbolic.png
%{_datadir}/icons/hicolor/*/apps/gtk3-widget-factory.png
%{_datadir}/icons/hicolor/*/apps/gtk3-widget-factory-symbolic.symbolic.png
%{_bindir}/gtk3-demo-application
%{_bindir}/gtk3-widget-factory
%{_datadir}/gettext/
%{_datadir}/gtk-3.0/gtkbuilder.rng
%{_datadir}/gir-1.0
%{_datadir}/glib-2.0/schemas/org.gtk.Demo.gschema.xml
%{_mandir}/man1/gtk3-demo.1*
%{_mandir}/man1/gtk3-demo-application.1*
%{_mandir}/man1/gtk3-icon-browser.1*
%{_mandir}/man1/gtk3-widget-factory.1*
%{_mandir}/man1/gtk-builder-tool.1*
%{_mandir}/man1/gtk-encode-symbolic-svg.1*
%{_mandir}/man1/gtk-query-settings.1*

%files devel-docs
%{_datadir}/gtk-doc

%files tests
%{_libexecdir}/installed-tests/gtk+
%{_datadir}/installed-tests

%changelog
* Tue May 30 2017 Matthias Clasen <mclasen@redhat.com> - 3.22.10-4
- Update Japanese translations
- Resolves: #1449636

* Thu Apr 20 2017 Kalev Lember <klember@redhat.com> - 3.22.10-3
- Really remove all libtool .la files
- Resolves: #1386980

* Thu Apr 20 2017 Kalev Lember <klember@redhat.com> - 3.22.10-2
- Try harder to remove all libtool .la files
- Resolves: #1386980

* Tue Mar 14 2017 Kalev Lember <klember@redhat.com> - 3.22.10-1
- Update to 3.22.10
- Resolves: #1386980

* Tue Feb 28 2017 Kalev Lember <klember@redhat.com> - 3.22.9-1
- Update to 3.22.9
- Resolves: #1386980

* Tue Feb 14 2017 Kalev Lember <klember@redhat.com> - 3.22.8-2
- Build with xrandr 1.5.0
- Resolves: #1386980

* Mon Feb 13 2017 Kalev Lember <klember@redhat.com> - 3.22.8-1
- Update to 3.22.8
- Resolves: #1386980

* Mon Jan 16 2017 Kalev Lember <klember@redhat.com> - 3.22.7-1
- Update to 3.22.7
- Resolves: #1386980

* Thu Jul  1 2016 Benjamin Otte <otte@redhat.com> 3.14.13-20
- Make sure menus always scroll when too large
Resolves: #1025359

* Thu Jun 30 2016 Matthias Clasen <mclasen@redhat.com> 3.14.13-19
- Fix a problem that causes critical warnings in rhythmbox
Resolves: #1351643

* Wed Jun 29 2016 Matthias Clasen <mclasen@redhat.com> 3.14.13-18
- Update translations
Resolves: #1304264

* Tue Mar 15 2016 Matthias Clasen <mclasen@redhat.com> 3.14.13-17
- Remove an unnecessary warning
Related: #1257794

* Wed Sep 23 2015 Ray Strode <rstrode@redhat.com> 3.14.13-16
- Fix mispelling in previous patch
Related: #1259292

* Wed Sep 23 2015 Ray Strode <rstrode@redhat.com> 3.14.13-15
- Fix up app chooser to deal with duplicate entries
Related: #1259292

* Thu Sep 17 2015 Matthias Clasen <cmlasen@redhat.com> 3.14.13-14
- Fix a possible crash when reordering bookmarks
Resolves: #1207187

* Fri Jul 21 2015 Matthias Clasen <cmlasen@redhat.com> 3.14.13-13
- Fix a possible crash during DND
Related: #1174442

* Fri Jul 17 2015 Matthias Clasen <mclasen@redhat.com> 3.14.13-12
- Coverity fixes
Related: #1174442

* Thu Jul 16 2015 Matthias Clasen <mclasen@redhat.com> 3.14.13-11
- Fix rendering stalls with ssh connections
Resolves: #1243646

* Tue Jul 14 2015 Matthias Clasen <mclasen@redhat.com> 3.14.13-10
- Include a settings.ini file
Resolves: #1241374

* Tue Jul  7 2015 Matthias Clasen <mclasen@redhat.com> 3.14.13-9
- Fix a reentrancy issue in GtkSwitch
Resolves: #1238692

* Thu May 21 2015 Matthias Clasen <mclasen@redhat.com> 3.14.13-8
- Don't emit warnings for 'new' deprecations by default
- Disable GtkMenuButton if the associated action says so
Resolves: #1210747
Resolves: #1223463 

* Fri May 15 2015 Marek Kasik <mkasik@redhat.com> 3.14.13-7
- Check connection to remote CUPS server on correct port
- Resolves: #1221157

* Tue May 12 2015 Richard Hughes <rhughes@redhat.com> 3.14.13-6
- Rebuild against the new colord version
- Related: #1174442

* Thu May 07 2015 Ray Strode <rstrode@redhat.com> 3.14.13-5
- Update adwaita-gtk3-theme provides version to be big enough
  to upgrade gnome-themes-standard
  Related: #1174442

* Thu May 07 2015 Ray Strode <rstrode@redhat.com> 3.14.13-4
- Obsolete adwaita-gtk3-theme
  Related: #1174442

* Fri May  1 2015 Matthias Clasen <mclasen@redhat.com> -3.14.13-3
- Handle the app menu on ssh connections better
- Resolves: #982620

* Wed Apr 29 2015 Matthias Clasen <mclasen@redhat.com> -3.14.13-2
- Depend on adwaita-icon-theme
- Related: #1174442

* Tue Apr 28 2015 Matthias Clasen <mclasen@redhat.com> -3.14.13-1
- Update to 3.14.13
- Resolves: #1174442
- Drop patches that have been upstreamed

* Tue Dec 16 2014 Benjamin Otte <otte@redhat.com> - 3.8.8-10
- Don't accidentally export function
- Resolves: #1168685

* Fri Oct 31 2014 Benjamin Otte <otte@redhat.com> - 3.8.8-9
- Don't crash when alt-tabbing in gedit
- Resolves: #1150290

* Mon Oct 20 2014 Benjamin Otte <otte@redhat.com> - 3.8.8-8
- Fix breakage introduced by patch
- Resolves: #1090126

* Sun Oct 05 2014 Benjamin Otte <otte@redhat.com> - 3.8.8-7
- Fix height request on labels
- Resolves: #1062938

* Fri Oct 03 2014 Benjamin Otte <otte@redhat.com> - 3.8.8-6
- Properly resize toplevel when collapsing GtkExpander
- Add missing man pages
- Allow remapping all keys
- Resolves: #982295, #948432, #1090126

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.8.8-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.8.8-4
- Mass rebuild 2013-12-27

* Mon Dec 16 2013 Benjamin Otte <otte@redhat.com> - 3.8.8-3
- Stop window shaking at startup of firstboot
- Resolves: #1035409

* Wed Dec 11 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.8-2
- Update translations
- Resolves: #1030356

* Wed Dec  4 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.8-1
- Update to 3.8.8
- Resolves: #1031802, #1031089

* Wed Nov 27 2013 Florian Müllner <fmuellner@redhat.com> - 3.8.4-8
- Revert last change - the issue will be addressed in gnome-session instead
  Resolves: #1031117

* Fri Nov 22 2013 Florian Müllner <fmuellner@redhat.com> - 3.8.4-6
- Follow upstream in a GtkBin commit war
  Resolves: #1031117

* Fri Nov  1 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.4-5
- Avoid losing %optflags
- Related: #881175

* Fri Nov  1 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.4-4
- Build with -fno-strict-aliasing
- Related: #881175

* Fri Nov  1 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.4-3
- Include a patch needed to fix multilib
- Related: #881175

* Fri Nov  1 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.4-2
- Rebuild with newer gobject-introspection to fix multilib
- Related: #881175

* Fri Aug 30 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.4-1
- Update to 3.8.4
- This update includes a considerable number of bug fixes,
  including fixes for filechooser behavior, a crash fix for
  gnome-shell, appearance fixes for menu items, etc.

* Wed Jun 19 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.2-2
- Fix icon theme reloading reentrancy issue

* Mon May 13 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Wed May  8 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.1-2
- Make man gtk-query-immodules-3.0-64 work

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Mon Mar 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.14-1
- Update to 3.7.14

* Wed Mar  6 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.12-1
- Update to 3.7.12

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.10-1
- Update to 3.7.10

* Tue Feb 05 2013 Richard Hughes <rhughes@redhat.com> - 3.7.8-1
- Update to 3.7.8

* Mon Jan 28 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.6-4
- Move im-cedilla back to -immodules subpackage to avoid
  a conflict with gtk2-immodules (#797838)

* Thu Jan 24 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.6-3
- Enable the Wayland and Broadway backends

* Thu Jan 24 2013 Cosimo Cecchi <cosimoc@redhat.com> - 3.7.6-2
- Backport two patches from git master to fix window allocations

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.6-1
- Update to 3.7.6

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Thu Nov 08 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.0-1
- Update to 3.7.0

* Fri Oct 19 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.1-2
- Don't pull in imsettings just for a directory

* Tue Oct 16 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.6.1-1
- Update to 3.6.1

* Fri Oct 12 2012 Bastien Nocera <bnocera@redhat.com> 3.6.0-2
- Add upstream patch to make Epiphany less painful to use

* Tue Sep 25 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Tue Sep 18 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.18-1
- Update to 3.5.18

* Thu Sep 06 2012 Richard Hughes <hughsient@gmail.com> - 3.5.16-1
- Update to 3.5.16

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 3.5.14-1
- Update to 3.5.14

* Wed Aug 22 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.5.12-2
- Backport a patch from upstream fixing crashers with app menus

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.12-1
- Update to 3.5.12

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.10-1
- Update to 3.5.10

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.8-1
- Update to 3.5.8

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 3.5.6-1
- Update to 3.5.6

* Wed Jun 06 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.20-1
- Update to 3.3.20

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.18-1
- Update to 3.3.18

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.16-1
- Update to 3.3.16

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.14-1
- Update to 3.3.14

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.10-1
- Update to 3.3.10

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.8-1
- Update to 3.3.8

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.6-2
- Revert a problematic focus handling change

* Mon Dec 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.6-1
- Update to 3.3.6

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Wed Nov  3 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Fri Oct 14 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Fri Sep 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-2
- Fix crashes when turning a11y on and off repeatedly

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Tue Sep 13 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Mon Sep  5 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.18-1
- Update to 3.1.18

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.16-1
- Update to 3.1.16

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.12-1
- Update to 3.1.12

* Sat Jul 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.10-1
- Update to 3.1.10

* Tue Jul  5 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.8-1
- Update to 3.1.8

* Tue Jun 14 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.6-1
- Update to 3.1.6

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Fri Apr 15 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.9-1
- Update to 3.0.9

* Thu Apr 14 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.8-3
- Move im-cedilla back to the main package (#637399)

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.8-2
- Add a missed backport

* Sun Apr  3 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.8-1
- Update to 3.0.8

* Fri Apr  1 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.7-1
- Update to 3.0.7

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.6-1
- Update to 3.0.6

* Wed Mar 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.5-1
- Update to 3.0.5

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.4-1
- Update to 3.0.4

* Mon Mar 14 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.3-1
- Update to 3.0.3

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Sat Feb 26 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-2
- Fix frequent crashes on double-click events

* Mon Feb 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.99.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  1 2011 Matthias Clasen <mclasen@redhat.com> - 2.99.3-1
- Update to 2.99.3

* Mon Jan 24 2011 Dan Williams <dcbw@redhat.com> 2.99.2-2
- Fix bug in gtk_show_uri() which caused crashes when plugging in USB drives

* Wed Jan 12 2011 Matthias Clasen <mclasen@redhat.com> 2.99.2-1
- Update to 2.99.2

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.99.1-1
- Update to 2.99.1

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.99.0-3
- Obsolete gtk3-engines

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> 2.99.0-2
- Provide the right directory for theming engines

* Thu Jan  6 2011 Matthias Clasen <mclasen@redhat.com> 2.99.0-1
- Update to 2.99.0
- Drop gtk-update-icon-cache and gtk-builder-convert to
  avoid conflict with gtk2
- Drop the tooltips-style patch for now

* Thu Dec  2 2010 Matthias Clasen <mclasen@redhat.com> 2.91.5-1
- Update to 2.91.5

* Fri Nov 12 2010 Matthias Clasen <mclasen@redhat.com> 2.91.4-2
- Make gnome-terminal work again

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> 2.91.4-1
- Update to 2.91.4

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> 2.91.3-1
- Update to 2.91.3

* Wed Oct 20 2010 Richard Hughes <richard@hughsie.com> 2.91.1-1
- Update to 2.91.1

* Tue Oct 12 2010 Matthias Clasen <mclasen@redhat.com> 2.91.0-2
- Fix a crash in the tooltip code

* Sat Oct  2 2010 Matthias Clasen <mclasen@redhat.com> 2.91.0-1
- Update to 2.91.0

* Wed Sep 29 2010 jkeating - 2.90.7-3
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclaesn@redhat.com> 2.90.7-2
- Reinstate the tooltip look

* Mon Sep 20 2010 Bastien Nocera <bnocera@redhat.com> 2.90.7-1
- Update to 2.90.7

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.5-5
- Co-own /usr/share/gtk-doc
- gtk3-devel requires gdk-pixbuf2-devel

* Mon Jul 26 2010 Colin Walters <walters@verbum.org> - 2.90.5-4
- gtk3-devel requires gdk-pixbuf-devel

* Thu Jul 22 2010 Colin Walters <walters@verbum.org> - 2.90.5-2
- Rebuild with new gobject-introspection

* Mon Jul 22 2010 Matthias Clasen <mclasen@redhat.com> 2.90.5-1
- Update to 2.90.5

* Fri Jul  9 2010 Colin Walters <walters@verbum.org> - 2.90.4-3
- Update tooltip style patch to remove unused GdkRegion

* Tue Jun 29 2010 Colin Walters <walters@pocket> - 2.90.4-2
- Changes to support rebuilds from snapshots

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> 2.90.4-1
- Update to 2.90.4

* Fri Jun 18 2010 Matthias Clasen <mclasen@redhat.com> 2.90.3-1
- Update to 2.90.3

* Sat Jun 12 2010 Matthias Clasen <mclasen@redhat.com> 2.90.2-2
- Copy some tweaks from gtk2

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> 2.90.2-1
- Update to 2.90.2

* Tue May 25 2010 Matthias Clasen <mclasen@redhat.com> 2.90.1-1
- Update to 2.90.1

* Fri May 21 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-5
- Some more package review feedback

* Thu May 20 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-4
- Remove %%check again, it causes trouble

* Mon May 17 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-3
- More review feedback

* Wed May 12 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-2
- Incorporate review feedback

* Wed May 11 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-1
- Update to the 2.90.0 release
- Complete parallel installability

* Mon May 10 2010 Richard Hughes <richard@hughsie.com> 2.90.0-0.0.20100510git
- Update from git
