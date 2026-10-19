/* SPDX-License-Identifier: GPL-2.0-or-later */
#include <pk-backend.h>
#include <pk-backend-spawn.h>

static PkBackendSpawn *spawn;
static const gchar *helper = "shellyBackend.py";

const gchar *pk_backend_get_description(PkBackend *backend)
{
    return "Shelly native repository packages";
}

const gchar *pk_backend_get_author(PkBackend *backend)
{
    return "Devario";
}

gboolean pk_backend_supports_parallelization(PkBackend *backend)
{
    return FALSE;
}

void pk_backend_initialize(GKeyFile *conf, PkBackend *backend)
{
    spawn = pk_backend_spawn_new(conf);
    pk_backend_spawn_set_name(spawn, "shelly");
    /* Never kill a running native package transaction. */
    pk_backend_spawn_set_allow_sigkill(spawn, FALSE);
}

void pk_backend_destroy(PkBackend *backend)
{
    g_clear_object(&spawn);
}

void pk_backend_start_job(PkBackend *backend, PkBackendJob *job)
{
    pk_backend_job_set_allow_cancel(job, FALSE);
    pk_backend_job_set_percentage(job, PK_BACKEND_PERCENTAGE_INVALID);
}

PkBitfield pk_backend_get_groups(PkBackend *backend)
{
    return pk_bitfield_from_enums(PK_GROUP_ENUM_OTHER, -1);
}

PkBitfield pk_backend_get_filters(PkBackend *backend)
{
    return pk_bitfield_from_enums(PK_FILTER_ENUM_INSTALLED, -1);
}

PkBitfield pk_backend_get_roles(PkBackend *backend)
{
    return pk_bitfield_from_enums(
        PK_ROLE_ENUM_GET_PACKAGES, PK_ROLE_ENUM_SEARCH_NAME,
        PK_ROLE_ENUM_SEARCH_DETAILS, PK_ROLE_ENUM_RESOLVE,
        PK_ROLE_ENUM_GET_DETAILS, PK_ROLE_ENUM_GET_UPDATES,
        PK_ROLE_ENUM_GET_REPO_LIST, PK_ROLE_ENUM_REFRESH_CACHE,
        PK_ROLE_ENUM_INSTALL_PACKAGES, PK_ROLE_ENUM_REMOVE_PACKAGES,
        PK_ROLE_ENUM_UPDATE_PACKAGES, -1);
}

static void query(PkBackendJob *job, const gchar *command, PkBitfield filters, gchar **values)
{
    g_autofree gchar *filter_text = pk_filter_bitfield_to_string(filters);
    g_autofree gchar *joined = values ? g_strjoinv("&", values) : g_strdup("");
    pk_backend_spawn_helper(spawn, job, helper, command, filter_text, joined, NULL);
}

void pk_backend_get_packages(PkBackend *backend, PkBackendJob *job, PkBitfield filters)
{
    query(job, "get-packages", filters, NULL);
}

void pk_backend_search_names(PkBackend *backend, PkBackendJob *job, PkBitfield filters, gchar **values)
{
    query(job, "search-name", filters, values);
}

void pk_backend_search_details(PkBackend *backend, PkBackendJob *job, PkBitfield filters, gchar **values)
{
    query(job, "search-details", filters, values);
}

void pk_backend_resolve(PkBackend *backend, PkBackendJob *job, PkBitfield filters, gchar **values)
{
    query(job, "resolve", filters, values);
}

void pk_backend_get_updates(PkBackend *backend, PkBackendJob *job, PkBitfield filters)
{
    query(job, "get-updates", filters, NULL);
}

void pk_backend_get_repo_list(PkBackend *backend, PkBackendJob *job, PkBitfield filters)
{
    query(job, "get-repo-list", filters, NULL);
}

void pk_backend_get_details(PkBackend *backend, PkBackendJob *job, gchar **ids)
{
    g_autofree gchar *joined = pk_package_ids_to_string(ids);
    pk_backend_spawn_helper(spawn, job, helper, "get-details", joined, NULL);
}

void pk_backend_refresh_cache(PkBackend *backend, PkBackendJob *job, gboolean force)
{
    pk_backend_spawn_helper(spawn, job, helper, "refresh-cache", pk_backend_bool_to_string(force), NULL);
}

static void transaction(PkBackendJob *job, const gchar *command, PkBitfield flags, gchar **ids)
{
    g_autofree gchar *flag_text = pk_transaction_flag_bitfield_to_string(flags);
    g_autofree gchar *joined = pk_package_ids_to_string(ids);
    pk_backend_spawn_helper(spawn, job, helper, command, flag_text, joined, NULL);
}

void pk_backend_install_packages(PkBackend *backend, PkBackendJob *job, PkBitfield flags, gchar **ids)
{
    transaction(job, "install-packages", flags, ids);
}

void pk_backend_update_packages(PkBackend *backend, PkBackendJob *job, PkBitfield flags, gchar **ids)
{
    transaction(job, "update-packages", flags, ids);
}

void pk_backend_remove_packages(PkBackend *backend, PkBackendJob *job, PkBitfield flags,
                                gchar **ids, gboolean allow_deps, gboolean autoremove)
{
    g_autofree gchar *flag_text = pk_transaction_flag_bitfield_to_string(flags);
    g_autofree gchar *joined = pk_package_ids_to_string(ids);
    pk_backend_spawn_helper(spawn, job, helper, "remove-packages", flag_text, joined,
                            pk_backend_bool_to_string(allow_deps),
                            pk_backend_bool_to_string(autoremove), NULL);
}
