# Google API keys

Every browser Devario compiles itself, `firefox` and `chromium`, is built
**keyless**: no recipe bakes in another distributor's Google API key. Removed
2026-10-31. The repack recipes (`firefox-developer-edition`, `helium-browser-bin`,
`waterfox-bin`, `zen-browser-bin`) ship a vendor's own binary carrying that
vendor's own registered keys, which is a different question and compliant.

## Why

The upstream recipes carry Arch Linux's own registered key with the header:

> Note: These are for Arch Linux use ONLY. For your own distribution, please get
> your own set of keys.

Google's [API keys policy](https://www.chromium.org/developers/how-tos/api-keys/)
is explicit that a key is bound to whoever accepted the terms:

> Software distribution with keys acquired for yourself is allowed, but the keys
> themselves cannot be shared with parties outside the legal entity that accepted
> the API ToS.

Shipping Arch's key from repo.seafoam-labs.org would attribute Devario traffic to
Arch's registration and consume Arch's quota, so it is not allowed.

## What was removed

| Recipe | Removed | Notes |
| --- | --- | --- |
| `devario-core/firefox` | `_google_api_key`, the `google-api-key` file write, `--with-google-location-service-api-keyfile`, `--with-google-safebrowsing-api-keyfile` | pkgrel 1 -> 2 |
| `devario-browser/firefox-developer-edition` | same four | superseded by the Mozilla repack, see note below |
| `devario-browser/chromium` | `_google_api_key`, the `google_api_key="..."` gn arg | pkgrel stays 1, never published |

Chromium needed nothing else: upstream stopped baking OAuth2 credentials in at
Chromium 89, and `use-oauth2-client-switches-as-default.patch` already moves
`--oauth2-client-id=`/`--oauth2-client-secret=` to runtime switches.

`firefox-developer-edition` is since a repack of Mozilla's own release payload, so
it no longer has a key of ours to remove: that binary carries the keys Mozilla
registered for itself, which is compliant, and unkeying it would mean editing a
signed payload. The keyless description below covers the two source builds,
`firefox` and `chromium`.

## Functional impact

Firefox substitutes the string `no-google-api-key` for a missing key, which Google
rejects ([Mozilla wiki](https://wiki.mozilla.org/Security/Safe_Browsing/V4_Implementation)).
So in the keyless packages:

- Wi-Fi/cell geolocation via Google's Location Service does not resolve.
- Google Safe Browsing phishing/malware list updates and hash completions fail.
  The Mozilla-operated url-classifier lists are unaffected.
- In Chromium the same key backs the Geolocation, Safe Browsing, Time Zone and
  speech/dictionary services. Google's own doc says that skipping the Geolocation
  API "in which case geolocation features of Chrome will not work".

Nothing fails at build time and no other feature changes. The toggles stay
visible in the browsers' preferences, so users get a feature that no longer
succeeds rather than one that is visibly absent.

## Distributor identity

Same class of problem, fixed 2026-10-31 in `devario-core/firefox`: the recipe
declared Arch as the distributor of Devario's build.

- `ac_add_options --with-distribution-id=` sets `MOZ_DISTRIBUTION_ID`
  (`toolkit/moz.configure`, default `org.mozilla`). On Linux it is a build-time
  identity string; on macOS it also derives the plugin-container bundle id.
  The recipe went from `org.archlinux` to `com.devario`, matching the
  `com.devario.*` prefix Devario's own components already use (`devario-welcome`).
- `distribution/distribution.ini` is read at first run and `[Global] id` is
  compared by Firefox itself, so it is behavioural rather than cosmetic. Its
  `id`, `about`, `app.distributor` and `app.partner.<distributor>` went from the
  `archlinux` tokens to `devario` / "Mozilla Firefox for Devario".

`devario-browser/chromium` has no equivalent to change: it reads no
distribution.ini and takes no distributor id, and its identity comes from the
generated desktop entry and appdata, both templated with `PACKAGE=chromium`. The
`# Maintainer:`/`# Contributor:` headers in every imported recipe keep the Arch
addresses, because those record authorship, not the identity of the product we ship.

## Restoring the features: register a Devario key set

Fedora is the working precedent. Its `firefox.spec` ships three of its own
key files (`mozilla-api-key`, `google-api-key`, `google-loc-api-key`) and passes
`--with-mozilla-api-keyfile`, `--with-google-safebrowsing-api-keyfile` and
`--with-google-location-service-api-keyfile`.

1. Open a Google Cloud project owned by the entity that holds
   seafoam-labs.org, membership in `chromium-dev@chromium.org` first (the
   Chrome-specific APIs are only listed for its members).
2. Enable and accept the terms for: Geolocation API (needs billing enabled, free
   tier), Safe Browsing API, Time Zone API. Check the pricing link for each: APIs
   without one have no purchasable quota, so a mass-market browser can outrun the
   free allowance and start failing.
3. Create one API key, restrict it to the Chrome/Firefox client identities, and
   record the restriction in this file.
4. Register and present the product as Devario everywhere. The consent screen
   product name, `--with-distribution-id=com.devario` and the `distribution.ini`
   tokens already fixed in `devario-core/firefox` must agree with the key's
   registered identity; a Devario key in a build that still calls itself Arch
   reproduces the misattribution this document exists for.
5. Add the key to each recipe the way the keys are already handled there: as a
   committed key file listed in `source=()` with a checksum, not as a bare
   variable, and wire the same options back in. `--with-mozilla-api-keyfile`
   covers the `%MOZILLA_API_KEY%` substitutions (Mozilla Location Service
   geolocation) and needs a Mozilla-side registration, not a Google one.
6. Verify the key landed in the build, not just the recipe: Firefox exposes it as
   `'MOZ_GOOGLE_API_KEY'` in `objdir/config.status`, and Chromium's
   `out/Release/args.gn` must show `google_api_key`.
7. Bump pkgrel once per recipe, regenerate `.SRCINFO`, and rebuild
   `--isolated` on the worker before publishing.

Until step 3 is done, keep the recipes keyless. Do not copy another
distribution's key back in.
