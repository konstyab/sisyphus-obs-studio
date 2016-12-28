Name: obs-studio
Version: 17.0.0
Release: alt5

%define ffmpeg_libs_suffix -ffmpeg-renamed-libs
%define ffmpeg_libs_upper_suffix -FFMPEG-RENAMED-LIBS

%define repo_p7 0


Summary: Software for video recording and live streaming

License: GPLv2
Group: Video
Url: https://github.com/jp9000/obs-studio

Packager: Sample Maintainer <samplemaintainer@altlinux.org>
BuildPreReq: ffmpeg-renamed-libs-devel
%if %repo_p7
%else
BuildPreReq: libspeexdsp-devel
%endif
BuildPreReq: libspeex-devel
BuildPreReq: libexpat-devel
BuildPreReq: libpcre-devel
%if %repo_p7
%else
BuildPreReq: libpcre2-devel
%endif
BuildPreReq: avconv
BuildPreReq: cmake
BuildPreReq: libpng-devel
BuildPreReq: doxygen
%if %repo_p7
BuildPreReq: gcc-c++
%else
BuildPreReq: gcc5-c++
%endif
BuildPreReq: avplay
BuildPreReq: avprobe
BuildPreReq: libcurl-devel
BuildPreReq: libGL-devel
BuildPreReq: libGLU-devel
BuildPreReq: libGLUT-devel
BuildPreReq: zlib-devel
%if %repo_p7
%else
BuildPreReq: qt5-gstreamer1-devel
BuildPreReq: qt5-serialbus-devel
BuildPreReq: qt5-speech-devel
BuildPreReq: qt5-wayland-devel
BuildPreReq: qt5-webchannel-devel
BuildPreReq: qt5-webengine-devel
BuildPreReq: qt5-3d-devel
%endif
BuildPreReq: qt5-base-devel
BuildPreReq: qt5-connectivity-devel
BuildPreReq: qt5-declarative-devel
BuildPreReq: qt5-location-devel
BuildPreReq: qt5-multimedia-devel
BuildPreReq: qt5-phonon-devel
BuildPreReq: qt5-quick1-devel
%if %repo_p7
BuildPreReq: qt5-quickcontrols
%else
BuildPreReq: qt5-quickcontrols2-devel
%endif
BuildPreReq: qt5-script-devel
BuildPreReq: qt5-sensors-devel
BuildPreReq: qt5-serialport-devel
BuildPreReq: qt5-svg-devel
BuildPreReq: qt5-tools-devel
BuildPreReq: qt5-webkit-devel
BuildPreReq: qt5-websockets-devel
BuildPreReq: qt5-x11extras-devel
BuildPreReq: qt5-xmlpatterns-devel
BuildPreReq: libv4l-devel
BuildPreReq: libpulseaudio-devel
BuildPreReq: libudev-devel
BuildPreReq: libjack-devel
BuildPreReq: libjack
BuildPreReq: libalsa-devel
BuildPreReq: libvlc-devel
BuildPreReq: libvlc-qt-devel
BuildPreReq: libx264-devel

BuildRequires(pre): rpm-macros-cmake
Source: %name-%version.tar
Patch0: obs-studio-libff-circular-queue-include-string-h.patch
Patch1: obs-studio-ffmpeg-mux-alt.patch

Requires: libobs = %version-%release
Requires: obs-plugins = %version-%release
Requires: libvlc


%description
Software for video recording and live streaming.

High performance real time video/audio capturing and mixing,
with unlimited scenes you can switch between seamlessly via custom transitions.

Intuitive audio mixer with filter functionality such as noise
gate, noise suppression, and gain.

Improved and streamlined Settings panel for quickly configuring your
broadcasts and recordings.

Filters for video sources such as image masking, color correction,
chroma/color keying, and more.


Powerful and easy to use configuration options. Add new Sources,
duplicate existing ones, and adjust their properties effortlessly.

Both light and dark themes available to fit your preference


%prep
%setup
%patch0 -p1
%patch1 -p1

%build
var_fflibs="avcodec avdevice avfilter avformat avresample avutil postproc swresample swscale"
var_ff_upperlibs="AVCODEC AVDEVICE AVFILTER AVFORMAT AVRESAMPLE AVUTIL POSTPROC SWRESAMPLE SWSCALE"



var_sed_e=""
for lib in $var_fflibs ; do
  var_sed_e="${var_sed_e} -e \"s/${lib}/${lib}%{ffmpeg_libs_suffix}/g\""
done
find -type f -exec bash -c "case {} in *.h) ;; *.hpp) ;; *.c) ;; *.cpp) ;; *) sed -E -i.bak ${var_sed_e} {} ; rm {}.bak -f ;; esac" \;


var_sed_e=""
for lib in $var_ff_upperlibs ; do
  var_sed_e="${var_sed_e} -e \"s/${lib}/${lib}%{ffmpeg_libs_upper_suffix}/g\""
done
find -type f -exec bash -c "case {} in *.h) ;; *.hpp) ;; *.c) ;; *.cpp) ;; *) sed -E -i.bak ${var_sed_e} {} ; rm {}.bak -f ;; esac" \;

var_sed_e=""
for lib in $var_fflibs ; do
  var_sed_e="${var_sed_e} -e \"s/${lib}%{ffmpeg_libs_suffix}\\\\.h/${lib}\\\\.h/g\""
done
find -type f -exec bash -c "case {} in *.h) ;; *.hpp) ;; *.c) ;; *.cpp) ;; *) sed -E -i.bak ${var_sed_e} {} ; rm {}.bak -f ;; esac" \;

var_sed_e=""
for lib in $var_fflibs ; do
  var_sed_e="${var_sed_e} -e \"s/lib(${lib})/lib\\1%{ffmpeg_libs_suffix}/g\""
done
find -type f -name "*.c" -exec bash -c "sed -E -i.bak ${var_sed_e} {} ; rm {}.bak -f" \;
find -type f -name "*.h" -exec bash -c "sed -E -i.bak ${var_sed_e} {} ; rm {}.bak -f" \;
find -type f -name "*.cpp" -exec bash -c "sed -E -i.bak ${var_sed_e} {} ; rm {}.bak -f" \;
find -type f -name "*.hpp" -exec bash -c "sed -E -i.bak ${var_sed_e} {} ; rm {}.bak -f" \;



# change libvlc.so.5 path to absolute
var_libdir="%_libdir"
var_libdir_escaped=$(echo $var_libdir | sed -e "s/\\//\\\\\\//g")
sed -E -i.bak -e "s/#define\\s+LIBVLC_FILE\\s+\"libvlc.so.5\"/#define LIBVLC_FILE \"${var_libdir_escaped}\\/libvlc.so.5\"/g" plugins/vlc-video/vlc-video-plugin.c
rm plugins/vlc-video/vlc-video-plugin.c.bak -fv


#sed -E -i.bak -e "s/cmake_minimum_required\\s*\\(\\s*VERSION\\s+2\\.8\\.12\\s*\\)/cmake_minimum_required\\(VERSION 2.8.10.2\\)/g" CMakeLists.txt
#rm CMakeLists.txt.bak -fv

%cmake_insource \
  -DOBS_VERSION_OVERRIDE=%{version} \
  -DUNIX_STRUCTURE=1 \
  %ifarch x86_64
    -DOBS_MULTIARCH_SUFFIX=64
  %else
    -DOBS_MULTIARCH_SUFFIX=
  %endif
# -DUNIX_STRUCTURE=1
make clean
%make_build

doxygen

%install

# install will go with error w/o these dirs
%ifarch x86_64
  bits="64"
%else
  bits="32"
%endif
mkdir -p additional_install_files
pushd additional_install_files
mkdir -p misc
mkdir -p data
mkdir -p libs$bits
mkdir -p libs
mkdir -p exec$bits
mkdir -p exec
mkdir -p libs${bits}r
mkdir -p libsr
mkdir -p exec${bits}r
mkdir -p execr
popd


%makeinstall_std

#pushd %%buildroot/usr
#rm lib64/cmake -rf
#popd

mkdir -p %buildroot/usr/libexec/obs/obs-plugins/obs-ffmpeg
mv %buildroot/usr/share/obs/obs-plugins/obs-ffmpeg/ffmpeg-mux %buildroot/usr/libexec/obs/obs-plugins/obs-ffmpeg/

%find_lang %name

RPM_VERIFY_ELF_METHOD="unresolved=relaxed"

sed -E -i.bak -e "s/^\\s*Icon=obs\\s*\$/Icon=\\/usr\\/share\\/icons\\/hicolor\\/256x256\\/apps\\/obs.png/g" %buildroot/usr/share/applications/obs.desktop
rm %buildroot/usr/share/applications/obs.desktop.bak -fv






%files -f %name.lang

%doc CONTRIBUTING COPYING INSTALL README
/usr/bin/*
/usr/share/obs
%exclude /usr/share/obs/obs-plugins
%exclude /usr/share/obs/libobs
/usr/libexec/obs
%exclude /usr/libexec/obs/obs-plugins
/usr/share/icons/hicolor/256x256/apps/obs.png
/usr/share/applications/obs.desktop


%package -n obs-plugins
Requires: obs-studio = %version-%release
Summary: Plugin for obs-studio
Group: Video

%description -n obs-plugins
Plugin for obs-studio

%files -n obs-plugins
%_libdir/obs-plugins
/usr/share/obs/obs-plugins
/usr/libexec/obs


%package -n libobs
Summary: obs-studio library
Group: Video

%description -n libobs
obs-studio library

%files -n libobs
%_libdir/libobs*.so.*
/usr/share/obs/libobs



%package -n libobs-devel
Summary: Development files for obs-studio library
Group: Video

%description -n libobs-devel
Development files for obs-studio library

%files -n libobs-devel
/usr/include/obs
%_libdir/libobs*.so



%changelog
* Wed Dec 28 2016 Konstantin Yablochkin <konstyab@altlinux.org> 17.0.0-alt5
- delete wrong comment
* Thu Dec 15 2016 Sample Maintainer <samplemaintainer@altlinux.org> 17.0.0-alt4
- changed ffmpeg suffix to -ffmpeg, added ffmpeg-libs-devel dependency
  instead of individual list
- change libvlc.so.5 path to absolute
* Sun Dec 11 2016 Sample Maintainer <samplemaintainer@altlinux.org> 0.16.6-alt3
- fixed i586 build
* Sun Dec 04 2016 Sample Maintainer <samplemaintainer@altlinux.org> 0.16.6-alt2
- initial build

