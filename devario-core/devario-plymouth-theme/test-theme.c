// SPDX-License-Identifier: GPL-3.0-or-later
// Runs the actual Plymouth script engine without a display server or root.
#include <assert.h>
#include <png.h>
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ply-utils.h"
#include "ply-pixel-buffer.h"
#include "script.h"
#include "script-execute.h"
#include "script-object.h"
#include "script-parse.h"
#include "script-lib-image.h"
#include "script-lib-math.h"
#include "script-lib-plymouth.h"
#include "script-lib-sprite.h"
#include "script-lib-string.h"

// Redirect only module loading into the supplied, uninstalled build tree.
ply_module_handle_t *ply_open_module(const char *path)
{
    char mapped[4096];
    const char *name = strrchr(path, '/');
    name = name ? name + 1 : path;
    if (!strcmp(name, "label-pango.so")) {
        snprintf(mapped, sizeof mapped, "%s/src/plugins/controls/label-pango/%s",
                 getenv("DEVARIO_PLYMOUTH_BUILD"), name);
        path = mapped;
    }
    void *handle = dlopen(path, RTLD_NODELETE | RTLD_NOW | RTLD_LOCAL);
    if (!handle) fprintf(stderr, "Module load: %s\n", dlerror());
    return handle;
}

static sprite_t *sprite(script_state_t *state, const char *name)
{
    sprite_t *result = script_obj_hash_get_native_of_class_name(state->global, name, "sprite");
    assert(result);
    return result;
}

static void expect_text(script_state_t *state, const char *name, const char *expected)
{
    char *value = script_obj_hash_get_string(state->global, name);
    assert(value && !strcmp(value, expected));
    free(value);
}

static void snapshot(script_state_t *state, int width, int height, const char *filename)
{
    ply_pixel_buffer_t *canvas = ply_pixel_buffer_new(width, height);
    ply_pixel_buffer_fill_with_hex_color(canvas, NULL, 0xff000000);
    const char *names[] = {"logo_sprite", "prompt_sprite", "entry_sprite", "message_sprite"};
    for (unsigned i = 0; i < 4; i++) {
        sprite_t *s = sprite(state, names[i]);
        if (s->image && s->opacity > 0)
            ply_pixel_buffer_fill_with_buffer_at_opacity(canvas, s->image, s->x, s->y, s->opacity);
    }
    png_image output = {.version = PNG_IMAGE_VERSION, .width = width, .height = height,
                        .format = PNG_FORMAT_BGRA};
    assert(png_image_write_to_file(&output, filename, 0,
                                  ply_pixel_buffer_get_argb32_data(canvas), 0, NULL));
    ply_pixel_buffer_free(canvas);
}

int main(int argc, char **argv)
{
    assert(argc == 3 && getenv("DEVARIO_PLYMOUTH_BUILD"));
    script_state_t *state = script_state_new(NULL);
    script_lib_image_setup(state, argv[2]);
    script_lib_sprite_data_t *display = script_lib_sprite_setup(
        state, ply_list_new(), ply_buffer_new(), "Adwaita Mono 12", 0xffffffff, 0xff000000);
    script_lib_plymouth_data_t *ply = script_lib_plymouth_setup(state, PLY_BOOT_SPLASH_MODE_BOOT_UP, 30, NULL);
    script_lib_math_setup(state);
    script_lib_string_setup(state);
    display->max_width = 1280;
    display->max_height = 800;
    script_op_t *program = script_parse_file(argv[1]);
    assert(program);
    script_return_t result = script_execute(state, program);
    script_obj_unref(result.object);
    sprite_t *logo = sprite(state, "logo_sprite");
    assert(logo->image && logo->opacity == 1);
    assert(ply_pixel_buffer_get_width(logo->image) == 420);
    assert(sprite(state, "prompt_sprite")->opacity == 0);
    snapshot(state, 1280, 800, "normal.png");
    ply_pixel_buffer_t *original = logo->image;
    for (int i = 0; i < 120; i++) script_lib_plymouth_on_refresh(state, ply);
    assert(logo->image == original && logo->opacity == 1);

    script_lib_plymouth_on_display_password(state, ply, "Unlock encrypted disk", 5);
    expect_text(state, "entry_text", "*****_");
    assert(sprite(state, "prompt_sprite")->opacity == 1);
    assert(ply_pixel_buffer_get_width(sprite(state, "prompt_sprite")->image) > 10);
    snapshot(state, 1280, 800, "password.png");
    script_lib_plymouth_on_display_prompt(state, ply, "Unlock disk", "secret", true);
    expect_text(state, "entry_text", "******_");
    script_lib_plymouth_on_display_question(state, ply, "Recovery choice", "continue");
    expect_text(state, "entry_text", "continue_");
    script_lib_plymouth_on_display_message(state, ply, "Checking filesystem");
    assert(sprite(state, "message_sprite")->opacity == 1);
    script_lib_plymouth_on_hide_message(state, ply, "Earlier message");
    assert(sprite(state, "message_sprite")->opacity == 1);
    script_lib_plymouth_on_hide_message(state, ply, "Checking filesystem");
    assert(sprite(state, "message_sprite")->opacity == 0);
    script_lib_plymouth_on_display_normal(state, ply);
    assert(sprite(state, "prompt_sprite")->opacity == 0);
    assert(sprite(state, "entry_sprite")->opacity == 0);

    const int sizes[][2] = {{640, 480}, {800, 1280}, {3840, 2160}, {320, 240}};
    for (unsigned i = 0; i < sizeof sizes / sizeof sizes[0]; i++) {
        display->max_width = sizes[i][0];
        display->max_height = sizes[i][1];
        script_lib_plymouth_on_refresh(state, ply);
        assert(logo->x >= 0 && logo->y >= 0);
        assert(logo->x + ply_pixel_buffer_get_width(logo->image) <= display->max_width);
        assert(logo->y + ply_pixel_buffer_get_height(logo->image) <= display->max_height);
        script_lib_plymouth_on_display_password(state, ply, "Unlock encrypted disk", 256);
        sprite_t *entry = sprite(state, "entry_sprite");
        assert(entry->x >= 0 && entry->image);
        assert(entry->x + ply_pixel_buffer_get_width(entry->image) <= display->max_width);
    }
    puts("PASS: static logo, password masking, questions, messages and four display sizes");
    return 0;
}
