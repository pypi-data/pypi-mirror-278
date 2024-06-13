import bpy
import blf
from bpy.app.handlers import persistent
from bpy.app.translations import contexts as i18n_contexts

original_filepath = bpy.path.abspath(bpy.data.filepath)
original_draw_func = bpy.types.TOPBAR_MT_file.draw

def is_original_filepath():
    print(original_filepath, bpy.path.abspath(bpy.data.filepath))
    print((len(original_filepath) > 0
            and bpy.path.abspath(bpy.data.filepath) == original_filepath))
    return (len(original_filepath) > 0
            and bpy.path.abspath(bpy.data.filepath) == original_filepath)

WARNING_TEXT = "Warning: save disabled."
INSTRUCTION_TEXT = "Press Esc to hide this message."

handle = None


def file_menu_draw(self, context):
    layout = self.layout

    layout.operator_context = 'INVOKE_AREA'
    layout.menu("TOPBAR_MT_file_new", text="New", text_ctxt=i18n_contexts.id_windowmanager, icon='FILE_NEW')
    layout.operator("wm.open_mainfile", text="Open...", icon='FILE_FOLDER')
    layout.menu("TOPBAR_MT_file_open_recent")
    layout.operator("wm.revert_mainfile")
    layout.menu("TOPBAR_MT_file_recover")

    layout.separator()

    row = layout.row()
    row.enabled = False
    row.operator_context = 'INVOKE_AREA'
    row.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')

#    row = layout.row()
#    row.enabled = False
#    row.operator("wm.save_mainfile", text="Save Incremental").incremental = True

    layout.operator_context = 'INVOKE_AREA'
    layout.operator("wm.save_as_mainfile", text="Save As...")
    layout.operator_context = 'INVOKE_AREA'
    layout.operator("wm.save_as_mainfile", text="Save Copy...").copy = True

    layout.separator()

    layout.operator_context = 'INVOKE_AREA'
    layout.operator("wm.link", text="Link...", icon='LINK_BLEND')
    layout.operator("wm.append", text="Append...", icon='APPEND_BLEND')
    layout.menu("TOPBAR_MT_file_previews")

    layout.separator()

    layout.menu("TOPBAR_MT_file_import", icon='IMPORT')
    layout.menu("TOPBAR_MT_file_export", icon='EXPORT')

    layout.separator()

    layout.menu("TOPBAR_MT_file_external_data")
    layout.menu("TOPBAR_MT_file_cleanup")

    layout.separator()

    layout.menu("TOPBAR_MT_file_defaults")

    layout.separator()

    layout.operator("wm.quit_blender", text="Quit", icon='QUIT')


def warning_draw(self, context):
    if is_original_filepath():
        row = self.layout.row(align=True)
        row.alert = True
        row.operator("lfs.status_warning", text=WARNING_TEXT)
        row.operator("lfs.status_warning", text="", icon='ERROR')


def set_save_keymaps(do_enable=False):
    """Disable save if this is the file we opened, otherwise enable it."""
    for kc in bpy.context.window_manager.keyconfigs:
        # for km in kc.keymaps:
        if "Window" in kc.keymaps:
            km = kc.keymaps["Window"]
            if not do_enable:
                km.keymap_items.new("lfs.big_warning", type="S", value="PRESS", ctrl=True)
            for kmi in km.keymap_items:
                if kmi.idname == "wm.save_mainfile":
                    # print(kc, km, kmi)
                    kmi.active = do_enable
                elif kmi.idname == "wm.save_mainfile" and not do_enable:
                    km.keymap_items.remove(kmi)


def draw_callback_px(self, context):
    font_id = 0  # XXX, need to find out how best to get this.

    blf.size(font_id, 32)
    blf.color(font_id, 1.0, 0.0, 0.0, 1.0)
    blf.position(font_id, 30, 75, 0)
    blf.draw(font_id, WARNING_TEXT)
    blf.position(font_id, 30, 30, 0)
    blf.draw(font_id, INSTRUCTION_TEXT)

class LFS_OT_BigWarning(bpy.types.Operator):
    """Display a big warning in the viewport"""
    bl_idname = "lfs.big_warning"
    bl_label = "Big Warning"

    def modal(self, context, event):
        for area in context.screen.areas:
            area.tag_redraw()

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            global handle
            try:
                bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')
            except ValueError:
                pass
            handle = None
            return {'CANCELLED'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        global handle
        if handle is not None:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')
            except ValueError:
                pass
        args = (self, context)
        handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class LFS_OT_StatusWarning(bpy.types.Operator):
    """Report issues related to the conformation system.

    This operator is used to get details when clicking the big red warning
    button in the topbar header.
    """
    bl_idname = "lfs.status_warning"
    bl_label = "Warning"

    @classmethod
    def poll(cls, context):
        return is_original_filepath()

    @classmethod
    def description(cls, _context, _properties):
        return "This file comes from a published version. \nYou will not be able to save it."

    def execute(self, context):
        self.report({"WARNING"}, self.description(context, None))
        return {'FINISHED'}


@persistent
def set_save_kms_on_file_load(filepath):
    """Run handler when loading file, decide whether to enable save."""
    if is_original_filepath():
        do_enable = False
        bpy.types.TOPBAR_MT_file.draw = file_menu_draw
        bpy.ops.lfs.big_warning()
    else:
        do_enable = True
        bpy.types.TOPBAR_MT_file.draw = original_draw_func
    set_save_keymaps(do_enable)


def register():
    bpy.types.STATUSBAR_HT_header.append(warning_draw)
    bpy.types.TOPBAR_MT_file.draw = file_menu_draw
    set_save_keymaps(False)

    bpy.utils.register_class(LFS_OT_BigWarning)
    bpy.utils.register_class(LFS_OT_StatusWarning)

    bpy.app.handlers.load_post.append(set_save_kms_on_file_load)

    if is_original_filepath():
        bpy.ops.lfs.big_warning()


if __name__ == "__main__":
    register()
