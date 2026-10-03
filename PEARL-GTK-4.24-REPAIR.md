# Pearl GTK 4.24 background effect repair

Implement the repair in Pearl so it starts normally with GTK 4.24, retains its blur behavior, and continues to work on the supported GTK 4.22 runtime. The failure is caused by GTK and Pearl creating separate background-effect objects for the same Wayland surface. The repair must give that object one owner throughout the surface's lifetime.

This is an implementation handoff for the Pearl maintainer, prepared on 2026-10-03. The source-level repair has not been implemented or tested. The two experimental Devario ISO service overrides were removed in favor of this repair plan. No rebuilt ISO or fixed Pearl package has been produced.

## Confirmed failure and evidence

The failing live session reported:

```text
wl_display#1.error(ext_background_effect_manager_v1#57, 0,
                  "surface already has a background effect")
```

It also reported `VK_ERROR_SURFACE_LOST_KHR` and `Error 71 (Protocol error) dispatching to Wayland display`. Aqueous remained running. The duplicate-effect error explains the client disconnect; the Vulkan message is a downstream symptom of losing that connection.

The locally staged live image contains `pearl 1:0.2.0-1` and `gtk4 1:4.24.0-2`. The development workstation reports GTK 4.22.5. That runtime difference explains how the same Pearl code can work in one installation and fail in another. GTK versions on all other working machines were not collected, so their exact difference remains unverified.

The relevant source establishes this sequence:

1. GTK 4.24 binds `ext_background_effect_manager_v1` when Aqueous advertises it.
2. In `gdk/wayland/gdksurface-wayland.c`, GTK requests a background-effect object when it creates the Wayland surface. It does this when the manager is present, without requiring the application to request a blur region first.
3. Pearl's `src/platform/wayland/effects.zig`, in `Surface.refresh`, calls `getBackgroundEffect(surface)` when Pearl's blur becomes active. `self.effect == null` only establishes that **Pearl** has not created an object; it says nothing about GTK's object.
4. Aqueous's `compositor/aqueous/BackgroundEffectManager.zig`, in `managerRequest`, finds the existing object and posts `background_effect_exists`.

The protocol explicitly permits only one background-effect object per surface. Aqueous's rejection is correct. Creating another manager binding does not provide a separate ownership domain. A client-side `catch` around the request cannot recover from the asynchronous fatal protocol error.

Sources: [GTK 4.24 surface implementation](https://github.com/GNOME/gtk/blob/4.24.0/gdk/wayland/gdksurface-wayland.c), [GTK 4.24 display implementation](https://github.com/GNOME/gtk/blob/4.24.0/gdk/wayland/gdkdisplay-wayland.c), and Pearl's vendored `bindings/protocols/ext-background-effect-v1.xml`.

## Required repair

Give GTK ownership of background-effect objects on the modern GTK path. Express Pearl's blur request through GTK's rendering and styling facilities. Keep Pearl's direct protocol implementation only for supported older GTK runtimes that do not claim these objects themselves.

The durable fix must work when launching Pearl normally, without `GDK_WAYLAND_DISABLE`, an ISO-specific service override, or a renderer override. Moving the environment workaround into Pearl's startup code would still be the same workaround and is outside this plan.

GTK 4.24 registers the CSS `backdrop-filter` property. Its Wayland surface code computes a background-blur region from the rendered content and sends that region using GTK's existing effect object. This provides a concrete migration path, but the precise selectors, clipping, and visual results still need to be implemented and verified against Pearl's widgets. See [GTK 4.24 CSS property registration](https://github.com/GNOME/gtk/blob/4.24.0/gtk/gtkcssstylepropertyimpl.c) and `gdk_wayland_surface_update_content` in the surface implementation above.

### Select ownership using the runtime

Introduce an explicit internal choice such as `gtk`, `native`, or `none`. Make the choice before any Pearl surface requests an effect object, and keep it stable for that surface's lifetime.

| Supported runtime or condition | Intended behavior |
| --- | --- |
| GTK 4.22.5 with compositor blur support | Preserve Pearl's existing native protocol path. |
| GTK 4.24 with compositor blur support | Let GTK own the effect and request blur through GTK. Pearl must not call `getBackgroundEffect` for that surface. |
| Blur unavailable or disabled | Keep a usable surface without an active blur region. Do not switch to native ownership merely because GTK is not applying blur. |

Use the loaded GTK runtime version, not only build-time headers or the Zig bindings version. A binary built with the older supported GTK may later run against GTK 4.24 after a system upgrade. Verify the first affected release before choosing a version boundary; the source inspection confirms GTK 4.24.0, not every development release or downstream backport.

If supporting both runtimes proves impractical, raising Pearl's GTK minimum and removing the native path is an alternative release decision. It would require updating build checks, package dependencies, release metadata, and the workstation runtime together. Do not silently drop the currently declared GTK 4.22.5 support.

### Preserve Pearl surface behavior

Refactor `Effects` and `Surface` without removing their unrelated responsibilities. In particular:

- Retain the native registry and `aqueous_shell_manager_v1` identity handling needed to verify the display session.
- Retain compositor capability tracking and the public blur-availability status. Binding a manager to observe capabilities is distinct from creating a per-surface effect.
- Retain rounded input regions, click-through behavior, panel geometry, and geometry-change callbacks. These are used even by surfaces that do not request blur.
- On the GTK path, never create, destroy, or modify a private GTK protocol object. Do not inspect GTK's private structure layout or use an inferred Wayland object ID.
- Keep GTK as the sole reader and dispatcher of its display connection. Continue asking GTK to draw and commit rather than attaching or committing its `wl_surface` directly.

The existing lifecycle helpers `mapped`, `unmapped`, `detach`, and `clearEffect` must respect the chosen owner. A null native effect pointer is normal on the GTK path. Clearing a Pearl blur request must clear the GTK styling or rendering request while leaving GTK responsible for its own object.

### Migrate blur regions and styling

Current `resources/style.css` uses `.pearl-blur` to select translucent backgrounds. That class does not itself request compositor blur; today the native Wayland code provides the region separately.

For GTK 4.24, add a runtime-specific built-in style provider or equivalent rendering support that requests backdrop blur on the actual panels. Load this only when supported, so GTK 4.22 does not parse an unknown CSS property. Keep this application-controlled behavior separate from the custom-theme CSS allowlist.

Preserve these existing details:

- Bar islands blur their individual rounded shapes. Empty gaps between islands must remain clear and click-through.
- The dock, popup panels, notifications, OSD, and window switcher use their intended bounds, rather than blurring a whole transparent window.
- `Surface.refresh` currently stops applying blur when window opacity drops below `0.72`; preserve the intended fade behavior and clear stale regions.
- Capability changes, theme reloads, custom opacity, resizing, scaling, remapping, and output removal must update or clear regions without acquiring a second object.
- Aqueous's blur policy and layer-rule veto must continue to take effect. Validate how the GTK CSS request maps to the compositor's effect; do not assume a CSS blur radius sets Aqueous's configured radius.

## Files to inspect and change

Paths below are relative to the Pearl checkout at `/home/zoey/Pearl`. The inspected checkout was `25805901726d7ae7000bb8ab8df42ee611954929`; find functions by name if line numbers change.

| File | Work |
| --- | --- |
| `src/platform/wayland/effects.zig` | Add runtime ownership selection; separate input and geometry handling from effect creation; retain the older GTK implementation. |
| `src/ui/surfaces/manager.zig` | Check ownership propagation, capability changes, bar islands, popup lifecycle, and reported blur availability. |
| `src/desktop/dock.zig` | Preserve dock blur bounds and geometry callbacks. |
| `src/plugins/overlay.zig` | Preserve input-region behavior; this also uses `Surface` even when its blur argument is false. |
| `resources/style.css` and `src/core/application.zig` | Add conditional GTK blur styling or rendering support and integrate provider loading without old-runtime CSS errors. |
| `tests/integration/test_surfaces.py` | Extend the existing real-compositor tests with GTK 4.24 ownership and region assertions. |
| `build.zig`, `packaging/release.json`, and Pearl package recipes | Keep runtime support, bindings, build checks, and release validation consistent with the chosen implementation. |

Aqueous's `compositor/aqueous/BackgroundEffectManager.zig` is useful for observing and validating the protocol behavior. Keep its duplicate-object rejection intact.

## Reproduce before changing the code

Use an isolated Aqueous session with blur enabled, then repeat on the failing live system. Ensure the actual Pearl process loads GTK 4.24; a build container using newer headers is not sufficient. Record the runtime library path and package version. Clear the experimental `GDK_WAYLAND_DISABLE` setting and verify that no service or session file injects it.

In an existing test Aqueous session with no other Pearl instance running:

```bash
env -u GDK_WAYLAND_DISABLE WAYLAND_DEBUG=client \
  aqueous-activity-launch /usr/bin/pearl 2>/tmp/pearl-background-effects.log

grep -n -E 'get_background_effect|set_blur_region|wl_display.*error|Error 71' \
  /tmp/pearl-background-effects.log
```

Use the appropriate launcher and binary path for the isolated checkout if they differ from the packaged paths above. Record the two `get_background_effect` requests naming the same `wl_surface`, followed by the protocol error. Match object lifetimes as well as numeric IDs: Wayland can reuse an ID after destruction.

The old ISO override locations were:

```text
usr/lib/systemd/user/aqueous-pearl.service.d/60-devario-background-effects.conf
usr/lib/systemd/user/pearl.service.d/60-devario-background-effects.conf
```

Those files have been removed from the local Devario ISO source. If a separate test installation has a manually created copy, remove that specific workaround there before validating the source repair.

## Validation and acceptance

Start with the existing `zig build test-surfaces` entry point, using the repository's required Zig and dependency setup. Its `blur()` test already starts a private Vulkan Aqueous session with blur enabled, tests visual differences under a compositor rule veto, and inspects Wayland traces. Extend that test rather than relying on a startup-only smoke test. The `basic()` case expects blur to be unavailable, so it alone cannot establish this repair.

Run the following matrix with protocol-disable workarounds absent:

| Scenario | Required result |
| --- | --- |
| Supported GTK 4.22.5 runtime | Native Pearl blur continues to work without new CSS parsing errors. |
| GTK 4.24 runtime | Pearl starts, blur is visible, and each surface has at most one live background-effect object. |
| Binary built against older supported GTK, then run on GTK 4.24 | Ownership follows the runtime, and startup succeeds after the library upgrade. |
| Blur capability absent or toggled off and on | Pearl remains usable, updates styling and status, and avoids stale regions or duplicate objects. |
| Popup cycles, dock visibility, notifications, OSD, and switcher | Repeated mapping and destruction remain correct; input behavior and blur bounds are preserved. |
| Islands, mixed scaling, rotation, resize, output removal and return | No blur across empty gaps, incorrect input regions, stale effects, or protocol disconnects. |
| Default launch and explicit Vulkan rendering | No renderer override is needed to start Pearl. |

For protocol assertions, track the association between each surface and its live effect object. Allow a new object only after the previous object or its surface has been destroyed. GTK may create an object with an empty blur region; that is valid and should not fail a test. Absence of a crash is insufficient: assert that a nonempty region appears when blur is enabled and clears when appropriate, and retain visual comparisons proving that blur is actually rendered.

The release is ready when the affected live machine starts Pearl normally, the older supported runtime still passes, the lifecycle and visual checks pass, and no environment or service workaround is required. Rebuild and test the Pearl package and then the live ISO. Record the GTK runtime, Pearl package version, launch method, protocol trace, and test results with the repair.

The four Devario desktop integration tests previously run during investigation checked packaging and session integration. They did not execute Pearl under GTK 4.24 and are not evidence that this source repair works.
