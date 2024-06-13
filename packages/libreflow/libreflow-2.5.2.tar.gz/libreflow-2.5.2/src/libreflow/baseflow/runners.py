import os
import re
import sys
import platform
import subprocess
import logging
from pathlib import Path
from datetime import datetime

from kabaret import flow
from kabaret.subprocess_manager.runner_factory import Runner
from kabaret.subprocess_manager.flow import RunAction

from ..resources.icons import flow as flow_icons


FILE_EXTENSIONS = ["blend", "kra", "png", "jpg", "txt", "nk", "abc", "mov", "psd", "psb", "aep", "prproj", "zip", "mp4", "mxf", "fbx", "ai", "json", "jsx", "obj", "wav"]
FILE_EXTENSION_ICONS = {
            "blend": ("icons.libreflow", "blender"),
            "kra": ("icons.libreflow", "krita"),
            "png": ("icons.gui", "picture"),
            "jpg": ("icons.gui", "picture"),
            "txt": ('icons.gui', 'text-file-1'),
            "nk": ("icons.libreflow", "nuke"),
            "abc": ("icons.flow", "alembic"),
            "aep": ("icons.libreflow", "afterfx"),
            "psd": ("icons.flow", "photoshop"),
            "psb": ("icons.flow", "photoshop"),
            "prproj": ("icons.libreflow", "premiere-pro"),
            "mov": ("icons.flow", "quicktime"),
            "ai":  ("icons.libreflow", "illustrator"),
            "zip": ("icons.libreflow", "archive"),
            "mp4": ("icons.gui", "youtube-logo"),
            "mxf": ("icons.gui", "youtube-logo"),
            "fbx": ("icons.libreflow", "fbx"),
            "json": ("icons.libreflow", "json"),
            "jsx": ("icons.libreflow", "jsx"),
            "obj": ("icons.libreflow", "3d-object"),
            "wav": ("icons.gui", "youtube-logo"),
        }



# Runners
# -----------------


class DefaultEditor(Runner):
    @classmethod
    def can_edit(cls, filename):
        return True

    def executable(self):
        if platform.system() == "Darwin":
            return "open"
        elif platform.system() == "Linux":
            return "xdg-open"
        return None

    def run(self):
        if platform.system() == "Windows":
            os.startfile(self.argv()[0])
        else:
            super(DefaultEditor, self).run()


class EditFileRunner(Runner):

    ICON = ("icons.flow", "action")

    @classmethod
    def can_edit(cls, filename):
        ext = os.path.splitext(filename)[1]
        supported_exts = cls.supported_extensions()

        return supported_exts is None or ext in supported_exts

    @classmethod
    def supported_extensions(cls):
        """
        Supported file extensions.

        Return None by default to allow any extension.
        """
        return None

    def show_terminal(self):
        return False

    def exec_env_var(self, version=None):
        key = self.__class__.__name__.upper()

        if version is not None:
            key += '_%s' % version.upper().replace('.', '_')
        
        return '%s_EXEC_PATH' % key

    def executable(self):
        try:
            exec_path = os.environ[self.exec_env_var(self.version)]
            logging.getLogger('kabaret').log(logging.INFO, f'[RUNNER] Launch: {exec_path}')
            return exec_path
        except KeyError:
            exec_path = os.environ[self.exec_env_var()]
            logging.getLogger('kabaret').log(logging.INFO, f'[RUNNER] Launch: {exec_path}')
            return exec_path


class ImageMagick(EditFileRunner):

    @classmethod
    def can_edit(cls, filename):
        return True


class Blender(EditFileRunner):

    ICON = ("icons.libreflow", "blender")
    TAGS = [
        "Modeling",
        "Sculpting",
        "Animation",
        "Rigging",
        "3D Drawing",
        "Rendering",
        "Simulation",
        "Video Editing",
        "VFX",
    ]

    @classmethod
    def supported_versions(cls):
        return ["2.83", "2.90", "2.91", "2.92", "2.93"]

    @classmethod
    def supported_extensions(cls):
        return [".blend"]


class Krita(EditFileRunner):

    ICON = ("icons.libreflow", "krita")
    TAGS = ["2D Drawing", "Image Editing"]

    @classmethod
    def supported_versions(cls):
        return ["4.3.0"]

    @classmethod
    def supported_extensions(cls):
        return [".kra", ".png", ".jpg"]


class AfterEffects(EditFileRunner):

    ICON = ("icons.libreflow", "afterfx")

    @classmethod
    def supported_extensions(cls):
        return [".aep", ".png", ".jpg"]


class AfterEffectsRender(EditFileRunner):

    ICON = ("icons.libreflow", "afterfx")

    @classmethod
    def supported_extensions(cls):
        return [".aep"]


class VSCodium(EditFileRunner):

    ICON = ("icons.libreflow", "vscodium")
    TAGS = ["Text editing", "IDE"]

    @classmethod
    def supported_extensions(cls):
        return [".txt"]


class NotepadPP(EditFileRunner):

    ICON = ("icons.flow", "notepad")
    TAGS = ["Text editing"]

    @classmethod
    def supported_extensions(cls):
        return [".txt"]


class Firefox(EditFileRunner):

    ICON = ("icons.flow", "notepad")
    TAGS = ["Browser"]

    @classmethod
    def can_edit(cls, filename):
        return True


class RV(EditFileRunner):

    ICON = ("icons.applications", "rv")
    TAGS = ['Video editing']

    def show_terminal(self):
        return True
    
    def keeps_terminal(self):
        return False


class Nuke(EditFileRunner):

    ICON = ("icons.libreflow", "nuke")
    TAGS = [
        "Compositing",
        "Video Editing",
        "VFX",
    ]

    @classmethod
    def supported_extensions(cls):
        return [".nk"]


class PremierePro(EditFileRunner):

    ICON = ("icons.libreflow", "premiere-pro")
    TAGS = ["Video Editing"]

    @classmethod
    def supported_extensions(cls):
        return [".prproj"]


class Mrviewer(EditFileRunner):

    ICON = ("icons.flow", "quicktime")
    TAGS = ['Video editing']

    def show_terminal(self):
        return True
    
    def keeps_terminal(self):
        return False


class PythonRunner(Runner):

    def executable(self):
        return sys.executable
    
    def show_terminal(self):
        return False

    def keep_terminal(self):
        return False


class MarkSequenceRunner(PythonRunner):
    
    TAGS = ['Mark image sequence']

    def argv(self):
        script_path = "%s/../scripts/mark_sequence.py" % os.path.dirname(__file__)
        return [script_path] + self.extra_argv


class SessionWorker(PythonRunner):

    def argv(self):
        args = [
            "%s/../scripts/session_worker.py" % (
                os.path.dirname(__file__)
            ),
            self.runner_name()
        ]
        args += self.extra_argv
        return args


class LaunchSessionWorker(RunAction):

    def runner_name_and_tags(self):
        return "SessionWorker", []
    
    def launcher_oid(self):
        raise NotImplementedError()

    def launcher_exec_func_name(self):
        raise NotImplementedError()

    def launcher_exec_func_args(self):
        return []

    def launcher_exec_func_kwargs(self):
        return {}
    
    def extra_argv(self):
        return [
            self.launcher_oid(),
            self.launcher_exec_func_name(),
            self.launcher_exec_func_args(),
            self.launcher_exec_func_kwargs()
        ]
    
    def runner_configured(self):
        '''
        Returns None if the type of the runner run by this action is registered in the
        project's runner factory, or a message as a string describing the error.
        '''
        msg = None
        name, tags = self.runner_name_and_tags()
        versions = self.root().session().cmds.SubprocessManager.get_runner_versions(name, tags)
        if versions is None:
            msg = (f'Runner \'{name}\' not found: make sure it is '
                'registered in the project runner factory.\n\n')
        return msg
    
    def run(self, button):
        '''
        Sets the environment variable which contains the runner executable path
        before launching the runner.
        '''
        name, tags = self.runner_name_and_tags()
        
        rid = self.root().session().cmds.SubprocessManager.run(
            runner_name=name,
            tags=tags,
            version=self.get_version(button),
            label=self.get_run_label(),
            extra_argv=self.extra_argv(),
            extra_env=self.extra_env(),
        )
        return self.get_result(runner_id=rid)


class DefaultExtension(flow.values.SessionValue):
    DEFAULT_EDITOR = 'choice'
    _map = flow.Parent(4)

    def choices(self):
        return sorted(set(FILE_EXTENSIONS) - set(self._map.mapped_names()))
    
    def revert_to_default(self):
        exts = self.choices()
        if exts:
            self.set(exts[0])


class SelectFileExtension(flow.Action):
    extension = flow.SessionParam(value_type=DefaultExtension).ui(choice_icons=FILE_EXTENSION_ICONS)
    _value = flow.Parent()

    def needs_dialog(self):
        self.extension.revert_to_default()
        return True
    
    def get_buttons(self):
        return ['Confirm', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        self._value.set(self.extension.get())


class FileExtension(flow.values.SessionValue):
    select = flow.Child(SelectFileExtension)


class RunnerName(flow.values.SessionValue):
    '''
    Lists the names of all runner types registered
    in the project's runner factory compatible with
    the default application extension (`DefaultApp.name()`). # todo: update
    '''
    DEFAULT_EDITOR = 'choice'
    STRICT_CHOICES = False
    _parent = flow.Parent()

    def choices(self):
        runners = self.root().project().get_factory().find_runners(
            f'*.{self._parent.get_file_extension()}')

        return [r[0] for r in runners]
    
    def revert_to_default(self):
        names = self.choices()
        if names:
            self.set(names[0])
        else:
            self.set(None)


class RunnerVersion(flow.values.SessionValue):
    '''
    Lists the available versions of the runner
    selected in the parent action.
    '''
    DEFAULT_EDITOR = 'choice'
    STRICT_CHOICES = False
    _action = flow.Parent()

    def choices(self):
        factory = self.root().project().get_factory()
        versions = [
            v for v in factory.get_runner_versions(
                self._action.runner_name.get())
            if v is not None
        ]
        return ['Default'] + versions
    
    def revert_to_default(self):
        self.set('Default')


class AddDefaultApp(flow.Action):
    '''
    Create a new extension with an associated default
    application.
    '''
    ICON = ("icons.gui", "plus-sign-in-a-black-circle")
    
    file_extension = flow.Param('', value_type=FileExtension).watched()
    runner_name = flow.Param(value_type=RunnerName).ui(label='Application').watched()
    runner_version = flow.Param(value_type=RunnerVersion).ui(label='Version')
    _map = flow.Parent()

    def needs_dialog(self):
        self.file_extension.revert_to_default()
        self.message.set('')
        return True

    def get_buttons(self):
        return ['Add', 'Cancel']
    
    def get_file_extension(self):
        return self.file_extension.get()

    def child_value_changed(self, child_value):
        if child_value is self.runner_name:
            self.runner_version.touch()
        elif child_value is self.file_extension:
            self.runner_name.revert_to_default()

    def run(self, button):
        if button == 'Cancel':
            return
        
        ext = self.file_extension.get()
        if re.fullmatch(r'\w+', ext) is None:
            self.message.set(f"'{ext}' is not a valid file extension.")
            return self.get_result(close=False)

        app = self._map.add(ext)
        app.runner_name.set(self.runner_name.get())
        app.runner_version.set(self.runner_version.get())
        self._map.touch()


class EditDefaultApp(flow.Action):
    '''
    Edit the name and version of a runner associated
    to an extension.
    '''
    ICON = ('icons.libreflow', 'edit-blank')

    runner_name = flow.SessionParam(value_type=RunnerName).ui(label='Application').watched()
    runner_version = flow.SessionParam(value_type=RunnerVersion).ui(label='Version')
    _app = flow.Parent()

    def needs_dialog(self):
        self.runner_name.set_watched(False)
        current_runner = self._app.runner_name.get()
        if current_runner in self.runner_name.choices():
            self.runner_name.set(current_runner)
        else:
            self.runner_name.revert_to_default()
        self.runner_name.set_watched(True)
        
        return True

    def get_buttons(self):
        return ['Save', 'Cancel']
    
    def get_file_extension(self):
        return self._app.name()

    def child_value_changed(self, child_value):
        if child_value is self.runner_name:
            self.runner_version.touch()

    def run(self, button):
        if button == 'Cancel':
            return

        self._app.runner_name.set(self.runner_name.get())
        self._app.runner_version.set(self.runner_version.get())
        self._app.touch()


class RemoveDefaultApp(flow.Action):
    '''
    Remove a default application.
    '''
    ICON = ('icons.gui', 'remove-symbol')

    _app = flow.Parent()
    _map = flow.Parent(2)

    def needs_dialog(self):
        return False
    
    def run(self, button):
        _map = self._map
        _map.remove(self._app.name())
        _map.touch()


class DefaultApp(flow.Object):
    '''
    Mapping between a file extension and a runner type.

    The actual extension is the name of the object
    (`DefaultApp.name()`).
    '''
    runner_name = flow.Param()
    runner_version = flow.Param()
    edit = flow.Child(EditDefaultApp)
    remove = flow.Child(RemoveDefaultApp)


class DefaultApps(flow.Map):
    '''
    Maps a file extension with one of the runner types
    available in the project's runner factory.
    '''
    add_default_app = flow.Child(AddDefaultApp).ui(label='Add default application')

    @classmethod
    def mapped_type(cls):
        return DefaultApp

    def columns(self):
        return ['Extension', 'Application', 'Version']

    def _fill_row_cells(self, row, item):
        row['Extension'] = item.name()
        row['Application'] = item.runner_name.get()
        version = item.runner_version.get()
        row['Version'] = version if version else 'Default'

    def _fill_row_style(self, style, item, row):
        style['activate_oid'] = item.edit.oid()
        style['icon'] = FILE_EXTENSION_ICONS.get(
            item.name(), ('icons.gui', 'cog-wheel-silhouette'))
