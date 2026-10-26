# Sourced by UWSM for Aqueous sessions. Select egl-wayland2 for EGL clients
# only while the NVIDIA 580 driver is loaded; Aqueous itself uses Vulkan.
# Preserve explicit user selections, including an explicitly empty value.
if [ "${__EGL_EXTERNAL_PLATFORM_CONFIG_FILENAMES+x}" != x ] &&
   [ -r /sys/module/nvidia/version ] &&
   [ -r /usr/share/egl/egl_external_platform.d/09_nvidia_wayland2.json ]; then
    case "$(cat /sys/module/nvidia/version)" in
        580.*)
            export __EGL_EXTERNAL_PLATFORM_CONFIG_FILENAMES="/usr/share/egl/egl_external_platform.d/09_nvidia_wayland2.json:/usr/share/egl/egl_external_platform.d/15_nvidia_gbm.json:/usr/share/egl/egl_external_platform.d/20_nvidia_xcb.json:/usr/share/egl/egl_external_platform.d/20_nvidia_xlib.json"
            ;;
    esac
fi
