from __future__ import annotations

import os.path
from collections.abc import MutableSequence
from configparser import BasicInterpolation, ConfigParser
from dataclasses import dataclass, field
from enum import Flag
from typing import Any

from . import desktop, paths, platform


class UEMultiEntry(MutableSequence):
    """
    Special entry for lines that are repeated in the ini file using the special
    prefixes.  need something else than 'list' because a list is used by ConfigParser
    to deal with multi-line values.
    """

    @classmethod
    def get(cls, value):
        if isinstance(value, cls):
            # already a UEMultiEntry, but could be from last parse, and its elements are no longer lists
            # convert it back to a list of lists
            if value.entries and not isinstance(value.entries[0], list):
                value.entries = [[e] for e in value.entries]
            return value
        return cls(value)

    def __init__(self, value=None):
        self.entries = []
        self.last = None
        if value is not None:
            self.entries.append(value)
            self.last = 0

    def __repr__(self):
        return f"<UEMultiEntry {self.entries}>"

    def append(self, value):
        # magic, used in parser when adding multi-line content. Get the last list entry added
        return self.entries[self.last]

    def append_item(self, value):
        self.entries.append(value)
        self.last = len(self.entries) - 1

    def __iter__(self):
        return iter(self.entries)

    def remove(self, value):
        self.entries.remove(value)
        self.last = len(self.entries) - 1

    def __getitem__(self, index):
        return self.entries[index]

    def __setitem__(self, index, value):
        self.entries[index] = value
        self.last = index

    def __delitem__(self, index):
        del self.entries[index]
        self.last = len(self.entries) - 1

    def __len__(self):
        return len(self.entries)

    def insert(self, index, value):
        self.entries.insert(index, value)
        self.last = index


class UeConfigDict(dict):
    """A special dictionary which helps with the special unreal option prefixes

    + - Adds a line if that property does not exist yet (from a previous configuration file or earlier in the same configuration file).

    - - Removes a line (but it has to be an exact match).

    . - Adds a new property.

    ! - Removes a property; but you do not have to have an exact match, just the name of the property.
    """

    def append(self, key, value):
        # print(f"Appending {key} to {value}")
        super().append(key, value)

    def __getitem__(self, key):
        # print(f"Getting {key}")
        value = super().__getitem__(key)
        return value
        # too much magic here will confuse everything.  Lets keep this as simple as possible
        # if isinstance(value, UEMultiEntry):
        #    return value.entries
        # return value

    def __setitem__(self, key, value):
        # print(f"Setting {key} to {value}")
        modifier, mkey = key[0], key[1:]
        if modifier not in "+-.!":
            return super().__setitem__(key, value)
        key = mkey
        if modifier in "+.":
            if key not in self:
                super().__setitem__(key, UEMultiEntry(value))
            else:
                me = UEMultiEntry.get(self[key])
                self[key] = me
                if modifier == "." or value not in me:
                    me.append_item(value)
        elif modifier == "-":
            if key in self:
                me = UEMultiEntry.get(self[key])
                self[key] = me
                if value in me:
                    me.remove(value)
        elif modifier == "!":
            if key in self:
                del self[key]
        else:
            assert 0


class UEInterpolation(BasicInterpolation):
    def before_get(self, parser, section, option, value, defaults):
        if isinstance(value, (list, UEMultiEntry)):
            return value
        return super().before_get(parser, section, option, value, defaults)


class UEConfigParser(ConfigParser):
    def __init__(self, *args, **kwargs):
        # override some defaults with the necessary ones.
        kwargs.update(
            {
                "dict_type": UeConfigDict,
                "strict": False,
                "interpolation": UEInterpolation(),
                "empty_lines_in_values": False,
            }
        )
        super().__init__(*args, **kwargs)

    def postprocess(self):
        """Join multi-line entries within UEMultiEntry objects into a single string."""
        for section, options in self.items():
            for option, value in options.items():
                if isinstance(value, UEMultiEntry):
                    for i, e in enumerate(value):
                        if isinstance(e, list):
                            value[i] = "\n".join(item.rstrip() for item in e)

    def read_string(self, *args, **kwargs):
        super().read_string(*args, **kwargs)
        self.postprocess()


class EConfigLayerFlags(Flag):
    Default = 0
    NoExpand = 1
    AllowCommandLineOverride = 2
    RequiresCustomConfig = 4


@dataclass
class ConfigLayer:
    name: str
    path: str
    flags: EConfigLayerFlags = EConfigLayerFlags.Default


"""
/**************************************************
**** CRITICAL NOTES
**** If you change this array, you need to also change EnumerateConfigFileLocations() in ConfigHierarchy.cs!!!
**** And maybe UObject::GetDefaultConfigFilename(), UObject::GetGlobalUserConfigFilename()
**************************************************/
"""
GConfigLayers: list[ConfigLayer] = [
    # Engine/Base.ini
    ConfigLayer("AbsoluteBase", "{ENGINE}/Config/Base.ini"),
    # Engine/Base*.ini
    ConfigLayer("Base", "{ENGINE}/Config/Base{TYPE}.ini"),
    # Engine/Platform/BasePlatform*.ini
    ConfigLayer("BasePlatform", "{ENGINE}/Config/{PLATFORM}/Base{PLATFORM}{TYPE}.ini"),
    # Project/Default*.ini
    ConfigLayer(
        "ProjectDefault",
        "{PROJECT}/Config/Default{TYPE}.ini",
        EConfigLayerFlags.AllowCommandLineOverride,
    ),
    # Project/Generated*.ini Reserved for files generated by build process and should never be checked in
    ConfigLayer("ProjectGenerated", "{PROJECT}/Config/Generated{TYPE}.ini"),
    # Project/Custom/CustomConfig/Default*.ini only if CustomConfig is defined
    ConfigLayer(
        "CustomConfig",
        "{PROJECT}/Config/Custom/{CUSTOMCONFIG}/Default{TYPE}.ini",
        EConfigLayerFlags.RequiresCustomConfig,
    ),
    # Engine/Platform/Platform*.ini
    ConfigLayer("EnginePlatform", "{ENGINE}/Config/{PLATFORM}/{PLATFORM}{TYPE}.ini"),
    # Project/Platform/Platform*.ini
    ConfigLayer("ProjectPlatform", "{PROJECT}/Config/{PLATFORM}/{PLATFORM}{TYPE}.ini"),
    # Project/Platform/GeneratedPlatform*.ini Reserved for files generated by build process and should never be checked in
    ConfigLayer(
        "ProjectPlatformGenerated",
        "{PROJECT}/Config/{PLATFORM}/Generated{PLATFORM}{TYPE}.ini",
    ),
    # Project/Platform/Custom/CustomConfig/Platform*.ini only if CustomConfig is defined
    ConfigLayer(
        "CustomConfigPlatform",
        "{PROJECT}/Config/{PLATFORM}/Custom/{CUSTOMCONFIG}/{PLATFORM}{TYPE}.ini",
        EConfigLayerFlags.RequiresCustomConfig,
    ),
    # UserSettings/.../User*.ini
    ConfigLayer(
        "UserSettingsDir",
        "{USERSETTINGS}Unreal Engine/Engine/Config/User{TYPE}.ini",
        EConfigLayerFlags.NoExpand,
    ),
    # UserDir/.../User*.ini
    ConfigLayer(
        "UserDir",
        "{USER}Unreal Engine/Engine/Config/User{TYPE}.ini",
        EConfigLayerFlags.NoExpand,
    ),
    # Project/User*.ini
    ConfigLayer(
        "GameDirUser", "{PROJECT}/Config/User{TYPE}.ini", EConfigLayerFlags.NoExpand
    ),
]


"""
/// <summary>
/// Plugins don't need to look at the same number of insane layers. Here PROJECT is the Plugin dir
/// </summary>
"""
GPluginLayers: list[ConfigLayer] = [
    # Engine/Base.ini
    ConfigLayer("AbsoluteBase", "{ENGINE}/Config/Base.ini", EConfigLayerFlags.NoExpand),
    # Plugin/Base*.ini
    ConfigLayer("PluginBase", "{PLUGIN}/Config/Base{TYPE}.ini"),
    # Plugin/Default*.ini (we use Base and Default as we can have both depending on Engine or Project plugin, but going forward we should stick with Default)
    ConfigLayer("PluginDefault", "{PLUGIN}/Config/Default{TYPE}.ini"),
    # Plugin/Platform/Platform*.ini
    ConfigLayer("PluginPlatform", "{PLUGIN}/Config/{PLATFORM}/{PLATFORM}{TYPE}.ini"),
    # Project/Default.ini
    ConfigLayer("ProjectDefault", "{PROJECT}/Config/Default{TYPE}.ini"),
    # Project/Platform/.ini
    ConfigLayer("ProjectDefault", "{PROJECT}/Config/{PLATFORM}/{PLATFORM}{TYPE}.ini"),
]


class EConfigExpansionFlags(Flag):
    Default = 0
    ForUncooked = 1 << 0
    ForCooked = 1 << 1
    ForPlugin = 1 << 2
    All = 0xFF


@dataclass
class ConfigLayerExpansion:
    """
    /**
    * This describes extra files per layer, to deal with restricted and NDA covered platform files that can't have the settings
    * be in the Base/Default ini files.
    * Note that we treat DedicatedServer as a "Platform" where it will have it's own directory of files, like a platform
    */
    """

    # a set of replacements from the source file to possible other files
    before1: str | None = None
    after1: str | None = None
    before2: str | None = None
    after2: str | None = None
    flags: EConfigExpansionFlags = EConfigExpansionFlags.Default


GConfigExpansions: list[ConfigLayerExpansion] = [
    # no replacements
    ConfigLayerExpansion(flags=EConfigExpansionFlags.All),
    # Restricted Locations
    ConfigLayerExpansion(
        "{ENGINE}/",
        "{ENGINE}/Restricted/NotForLicensees/",
        "{PROJECT}/Config/",
        "{RESTRICTEDPROJECT_NFL}/",
        EConfigExpansionFlags.ForUncooked | EConfigExpansionFlags.ForCooked,
    ),
    ConfigLayerExpansion(
        "{ENGINE}/",
        "{ENGINE}/Restricted/NoRedist/",
        "{PROJECT}/Config/",
        "{RESTRICTEDPROJECT_NR}/",
        EConfigExpansionFlags.ForUncooked,
    ),
    # Platform Extensions
    ConfigLayerExpansion(
        "{ENGINE}/Config/{PLATFORM}/",
        "{EXTENGINE}/Config/",
        "{PROJECT}/Config/{PLATFORM}/",
        "{EXTPROJECT}/Config/",
        EConfigExpansionFlags.ForUncooked
        | EConfigExpansionFlags.ForCooked
        | EConfigExpansionFlags.ForPlugin,
    ),
    # Platform Extensions in Restricted Locations
    #
    # Regarding the commented EConfigExpansionFlags::ForPlugin expansions: in the interest of keeping plugin ini scanning fast,
    # we disable these expansions for plugins because they are not used by Epic, and are unlikely to be used by licensees. If
    # we can make scanning fast (caching what directories exist, etc), then we could turn this back on to be future-proof.
    ConfigLayerExpansion(
        "{ENGINE}/Config/{PLATFORM}/",
        "{ENGINE}/Restricted/NotForLicensees/Platforms/{PLATFORM}/Config/",
        "{PROJECT}/Config/{PLATFORM}/",
        "{RESTRICTEDPROJECT_NFL}/Platforms/{PLATFORM}/Config/",
        EConfigExpansionFlags.ForUncooked | EConfigExpansionFlags.ForCooked,
    ),
    ConfigLayerExpansion(
        "{ENGINE}/Config/{PLATFORM}/",
        "{ENGINE}/Restricted/NoRedist/Platforms/{PLATFORM}/Config/",
        "{PROJECT}/Config/{PLATFORM}/",
        "{RESTRICTEDPROJECT_NR}/Platforms/{PLATFORM}/Config/",
        EConfigExpansionFlags.ForUncooked,
    ),
]


MAX_PLATFORM_INDEX = 99


class ConfigFileHierarchy(dict[int, str]):
    def __init__(self) -> None:
        self.key_gen = self.get_static_key(
            len(GConfigLayers) - 1, len(GConfigExpansions) - 1, MAX_PLATFORM_INDEX
        )
        self.files: set[str] = set()

    @classmethod
    def get_static_key(
        cls, layer_index: int, replacement_index: int, platform_index: int
    ) -> int:
        return (layer_index * 10000) + (replacement_index * 100) + platform_index

    def generate_dynamic_key(self):
        self.key_gen += 1
        return self.key_gen

    def add_static_layer(
        self, filename, layer_index, expansion_index=0, platform_index=0
    ):
        filename = os.path.normpath(filename)
        if filename in self.files:
            return
        # print(
        #    f"Adding static layer {filename} {layer_index} {expansion_index} {platform_index}"
        # )
        self[
            self.get_static_key(layer_index, expansion_index, platform_index)
        ] = filename
        self.files.add(filename)

    def add_dynamic_layer(self, filename):
        filename = os.path.normpath(filename)
        if filename in self.files:
            return
        self[self.generate_dynamic_key()] = filename
        self.files.add(filename)


class UEConfigFile(UEConfigParser):
    """
    This config parser represents loaded ini files. It has some extra fields to keep track of where the file was loaded from.
    plus hierarchy
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name: str | None = None
        self.platform: str = ""
        self.source_engine_config_dir: str = ""
        self.source_project_config_dir: str = ""
        self.source_ini_hierarchy: ConfigFileHierarchy = ConfigFileHierarchy()
        self.num: int = 0

    def __repr__(self) -> str:
        return f"<UEConfigFile {self.name} {self.platform}, {self.source_ini_hierarchy}, {list(self.keys())}>"


"""
/**
	 * Load an ini file directly into an FConfigFile from the specified config folders, optionally writing to disk. 
	 * The passed in .ini name can be a "base" (Engine, Game) which will be modified by platform and/or commandline override,
	 * or it can be a full ini filename (ie WrangleContent) loaded from the Source config directory
	 *
	 * @param ConfigFile The output object to fill
	 * @param IniName Either a Base ini name (Engine) or a full ini name (WrangleContent). NO PATH OR EXTENSION SHOULD BE USED!
	 * @param EngineConfigDir Engine config directory.
	 * @param SourceConfigDir Game config directory.
	 * @param bIsBaseIniName true if IniName is a Base name, which can be overridden on commandline, etc.
	 * @param Platform The platform to use for Base ini names
	 * @param bForceReload force reload the ini file from disk this is required if you make changes to the ini file not using the config system as the hierarchy cache will not be updated in this case
	 * @param bWriteDestIni write out a destination ini file to the Saved folder, only valid if bIsBaseIniName is true
	 * @param bAllowGeneratedIniWhenCooked If true, the engine will attempt to load the generated/user INI file when loading cooked games
	 * @param GeneratedConfigDir The location where generated config files are made.
	 * @return true if the ini file was loaded successfully
	 */
	static bool LoadExternalIniFile(FConfigFile& ConfigFile, const TCHAR* IniName, const TCHAR* EngineConfigDir, const TCHAR* SourceConfigDir, bool bIsBaseIniName, const TCHAR* Platform=NULL, bool bForceReload=false, bool bWriteDestIni=false, bool bAllowGeneratedIniWhenCooked = true, const TCHAR* GeneratedConfigDir = *FPaths::GeneratedConfigDir());
"""

# we support just a subset of the config cache stuff.


def load_external_ini_file(
    ini_name: str,
    engine_config_dir: str,
    source_config_dir: str,
    is_base_ini_name: bool,
    platform: str = "",
    force_reload: bool = False,
    write_dest_ini: bool = False,
    allow_generated_ini_when_cooked: bool = True,
    generated_config_dir: str = "",
) -> UEConfigFile | None:
    # we don't support all the options
    assert allow_generated_ini_when_cooked
    assert generated_config_dir == ""
    assert not write_dest_ini
    assert platform == ""

    ctx = (
        ConfigContext.read_into_local_file(platform)
        if is_base_ini_name
        else ConfigContext.read_single_into_local_file(platform)
    )
    ctx.engine_config_dir = engine_config_dir
    ctx.project_config_dir = source_config_dir
    ctx.force_reload = force_reload
    ctx.write_dest_ini = write_dest_ini
    ctx.allow_generated_ini_when_cooked = allow_generated_ini_when_cooked
    ctx.generated_config_dir = generated_config_dir
    ctx.load(ini_name)
    return ctx.config_file


@dataclass
class PerPlatformDirs:
    platform_extension_engine_dir: str
    platform_extension_project_dir: str


@dataclass
class ConfigContext:
    config_system: None = None
    config_file: UEConfigFile | None = None
    dest_ini_filename: str = ""
    platform: str = ""
    save_platform: str = ""
    generated_config_dir: str = ""
    base_ini_name: str = ""
    start_skipping_at_filename: str = ""

    engine_config_dir: str = ""
    engine_root_dir: str = ""
    project_config_dir: str = ""
    project_root_dir: str = ""
    plugin_root_dir: str = ""

    # useful strings that are used alot when walking the hierarchy
    promect_not_for_licensees_dir: str = ""
    project_no_redist_dir: str = ""
    per_platforms_dirs: dict[str, PerPlatformDirs] = field(default_factory=dict)

    use_hierarchy_cache: bool = False
    allow_generated_ini_when_cooked: bool = False
    force_reload: bool = False
    allow_remote_config: bool = False
    is_hierarchical_config: bool = False
    write_dest_ini: bool = False
    default_engine_required: bool = False
    is_for_plugin: bool = False

    # if this is non-null, it contains a set of pre-scanned ini files to use to find files, instead of looking on disk
    ini_cache_set: set[str] | None = None

    do_not_reset_config_file: bool = True
    cache_on_next_load: bool = False

    def _init(self) -> None:
        """Additional setup logic"""
        if not self.platform:
            self.platform = platform.ini_platform_name()
            self.platform = platform.platform_name()
        elif self.platform == platform.ini_platform_name():
            self.save_platform = platform.platform_name()
        else:
            self.save_platform = self.platform

    @classmethod
    def read_into_local_file(cls, platform=None) -> ConfigContext:
        result = cls(is_hierarchical_config=True, platform=platform)
        result._init()
        return result

    @classmethod
    def read_single_into_local_file(cls, platform=None) -> ConfigContext:
        result = cls(is_hierarchical_config=False, platform=platform)
        result._init()
        return result

    def load(self, ini_name: str) -> Any:
        return self.load_filename(ini_name)[0]

    def load_filename(
        self, ini_name: str, dest_ini_filename: str | None = None
    ) -> tuple[Any, str]:
        # for single file loads, just return early of the file doesn't exist
        if (
            not self.is_hierarchical_config
            and ini_name.endswith(".ini")
            and not self.does_config_file_exist(ini_name)
        ):
            return (False, "")

        if self.cache_on_next_load or self.base_ini_name != ini_name:
            self.reset_base_ini(ini_name)
            self.cache_paths()
            self.cache_on_next_load = False

        ok, perform_load = self.prepare_for_load()
        if not ok:
            return None, ""

        out_final_filename = ""

        # if we are reloading a known ini file (where OutFinalIniFilename already has a value), then we need to leave the OutFinalFilename alone until we can remove LoadGlobalIniFile completely
        if out_final_filename == self.base_ini_name:
            pass  # do nothing
        else:
            assert not self.write_dest_ini or self.dest_ini_filename
            out_final_filename = self.dest_ini_filename

        # now load if we need (PrepareForLoad may find an existing file and just use it)
        return (self.perform_load() if perform_load else True), out_final_filename

    def does_config_file_exist(self, ini_name: str) -> bool:
        # just look in file system
        return os.path.isfile(ini_name)

    def reset_base_ini(self, ini_name: str) -> None:
        if not self.do_not_reset_config_file:
            self.config_file = None
        self.base_ini_name = ini_name

    def cache_paths(self) -> None:
        if not self.is_hierarchical_config:
            return
        assert self.engine_config_dir.endswith("Config")
        assert self.project_config_dir.endswith("Config")
        self.engine_root_dir = os.path.dirname(self.engine_config_dir)
        self.project_root_dir = os.path.dirname(self.project_config_dir)

        prd = os.path.normcase(os.path.normpath(self.project_root_dir))
        erd = os.path.normcase(os.path.normpath(self.engine_root_dir))
        if prd.startswith(erd):
            # project is under root
            relative_dir = os.path.relpath(self.project_root_dir, self.engine_root_dir)
            self.project_not_for_licensees_dir = os.path.join(
                self.engine_root_dir, "Restricted/NotForLicensees", relative_dir
            )
            self.project_no_redist_dir = os.path.join(
                self.engine_root_dir, "Restricted/NoRedist", relative_dir
            )
        else:
            self.project_not_for_licensees_dir = os.path.join(
                self.project_root_dir, "Restricted/NotForLicensees"
            )
            self.project_no_redist_dir = os.path.join(
                self.project_root_dir, "Restricted/NoRedist"
            )

    def prepare_for_load(self) -> tuple[bool, bool]:
        if not self.config_file:
            self.config_file = UEConfigFile()
        return True, True

    def perform_load(self) -> bool:
        assert self.config_file is not None
        if not self.is_hierarchical_config:
            if self.base_ini_name.endswith(".ini"):
                self.dest_ini_filename = self.base_ini_name
                self.base_ini_name = os.path.basename(self.base_ini_name)
            else:
                # generate path to the .ini file (not a Default ini, IniName is the complete name of the file, without path)
                self.dest_ini_filename = os.path.join(
                    self.project_config_dir, f"{self.base_ini_name}.ini"
                )

            self.load_an_ini_file(self.dest_ini_filename, self.config_file)
            self.config_file.name = self.base_ini_name
            self.config_file.platform = ""
            return True

        else:
            self.add_static_layers_to_hierarchy()

            self.load_ini_file_hieararchy(
                self.config_file.source_ini_hierarchy, self.config_file
            )
            # needs_rewrite = self.generate_dest_ini_file()
            self.config_file.name = self.base_ini_name
            self.config_file.platform = self.platform

        return self.config_file.num > 0

    def add_static_layers_to_hierarchy(self) -> None:
        assert self.config_file is not None
        # remember where this file was loaded from
        self.config_file.source_engine_config_dir = self.engine_config_dir
        self.config_file.source_project_config_dir = self.project_config_dir

        # string that can have a reference to it, lower down
        dedicated_server_string = "DedicatedServer" if False else ""

        # cache some platform extension information that can be used inside the loops
        has_custom_config = (
            False  # = !FConfigCacheIni::GetCustomConfigString().IsEmpty();
        )

        # figure out what layers and expansions we will want
        expansion_mode = EConfigExpansionFlags.ForUncooked
        layers = GConfigLayers
        if False:  # if (FPlatformProperties::RequiresCookedData()
            expansion_mode = EConfigExpansionFlags.ForCooked
        if self.is_for_plugin:
            # this has priority over cooked/uncooked
            expansion_mode = EConfigExpansionFlags.ForPlugin
            layers = GPluginLayers

        for i, layer in enumerate(layers):
            # skip optional layers
            if (
                layer.flags & EConfigLayerFlags.RequiresCustomConfig
                and not has_custom_config
            ):
                continue

            # start replacing basic variables
            layer_path = self.perform_basic_replacements(layer.path, self.base_ini_name)

            has_platform_tag = "{PLATFORM}" in layer_path

            # expand if it it has {ED} or {EF} expansion tags
            if not (layer.flags & EConfigLayerFlags.NoExpand):
                # we assume none of the more special tags in expanded ones
                assert "{USERSETTINGS}" not in layer_path and "{USER}" not in layer_path

                for expansion_index, expansion in enumerate(GConfigExpansions):
                    # does this expansion match our current mode?
                    if not (expansion.flags & expansion_mode):
                        continue

                    expanded_path = self.perform_expansion_replacements(
                        expansion, layer_path
                    )
                    if not expanded_path:
                        continue
                    # allow for override, only on BASE EXPANSION!
                    if (
                        layer.flags & EConfigLayerFlags.AllowCommandLineOverride
                        and expansion_index == 0
                    ):
                        assert not has_custom_config, (
                            "EConfigLayerFlags::AllowCommandLineOverride config %s shouldn't have a PLATFORM in it"
                            % (layer.path,)
                        )
                        expanded_path = self.conditional_override_ini_filename(
                            expanded_path, self.base_ini_name
                        )

                    info = platform.get_info(self.platform)
                    num_platforms = (
                        len(info.ini_parent_chain) + 1 if has_platform_tag else 1
                    )
                    current_platform_index = num_platforms - 1
                    dedicated_server_index = -1
                    if has_platform_tag and False:  # is_running_dedicated_server()
                        num_platforms += 1
                        dedicated_server_index = current_platform_index + 1
                    for platform_index in range(num_platforms):
                        current_platform = (
                            dedicated_server_string
                            if platform_index == dedicated_server_index
                            else self.platform
                        )
                        platform_path = self.perform_final_expansions(
                            expanded_path, current_platform
                        )
                        # @todo restricted - ideally, we would move DedicatedServer files into a directory, like platforms are, but for short term compat,
                        # convert the path back to the original (DedicatedServer/DedicatedServerEngine.ini -> DedicatedServerEngine.ini)
                        if platform_index == dedicated_server_index:
                            platform_path.replace("Config/DedicatedServer/", "Config/")

                        if platform_path == self.start_skipping_at_filename:
                            return
                        self.config_file.source_ini_hierarchy.add_static_layer(
                            platform_path, i, expansion_index, platform_index
                        )
            else:
                # if no expansion, just process the special tags (assume no PLATFORM tags)
                assert not has_platform_tag, (
                    "Non-expanded config %s shouldn't have a PLATFORM in it"
                    % (layer.path,)
                )
                assert (
                    not layer.flags & EConfigLayerFlags.AllowCommandLineOverride
                ), "Non-expanded config can't have a EConfigLayerFlags::AllowCommandLineOverride"
                final_path = self.perform_final_expansions(layer_path, "")
                if final_path == self.start_skipping_at_filename:
                    return
                self.config_file.source_ini_hierarchy.add_static_layer(final_path, i)

    def perform_basic_replacements(self, path: str, base_ini_name: str) -> str:
        # replace the basic tags
        out_string = path.replace("{TYPE}", base_ini_name)
        out_string = out_string.replace(
            "{USERSETTINGS}", desktop.platform.user_settings_dir()
        )
        out_string = out_string.replace("{USER}", desktop.platform.user_dir())
        out_string = out_string.replace(
            "{CUSTOMCONFIG}", get_custom_config_string() if False else ""
        )
        return out_string

    def perform_expansion_replacements(
        self, expansion: ConfigLayerExpansion, in_string: str
    ) -> str:
        if not expansion.before1:
            return in_string
        # if nothing to replace, then skip it entirely
        if expansion.before1 not in in_string and (
            not expansion.before2 or expansion.before2 not in in_string
        ):
            return ""
        # replace the directory bits
        assert expansion.after1 is not None
        out_string = in_string.replace(expansion.before1, expansion.after1)
        if expansion.before2:
            assert expansion.after2 is not None
            out_string = out_string.replace(expansion.before2, expansion.after2)
        return out_string

    def conditional_override_ini_filename(
        self, expanded_path: str, base_ini_name: str
    ) -> str:
        """
        /**
        * Allows overriding the (default) .ini file for a given base (ie Engine, Game, etc)
        */
        """

        if True:  # !UE_BUILD_SHIPPING
            # Figure out what to look for on the commandline for an override. Disabled in shipping builds for security reasons
            # const FString CommandLineSwitch = FString::Printf(TEXT("DEF%sINI="), BaseIniName);
            # FParse::Value(FCommandLine::Get(), *CommandLineSwitch, IniFilename);
            pass
        return expanded_path

    def perform_final_expansions(self, expanded_path: str, platform: str) -> str:
        out_string = expanded_path.replace("{ENGINE}", self.engine_root_dir)
        out_string = out_string.replace("{PROJECT}", self.project_root_dir)
        out_string = out_string.replace(
            "{RESTRICTEDPROJECT_NFL}", self.project_not_for_licensees_dir
        )
        out_string = out_string.replace(
            "{RESTRICTEDPROJECT_NR}", self.project_no_redist_dir
        )

        if self.platform:
            ppd = self.get_per_platform_dirs(platform)
            if ppd:
                out_string = out_string.replace(
                    "{EXTENGINE}", ppd.platform_extension_engine_dir
                )
                out_string = out_string.replace(
                    "{EXTPROJECT}", ppd.platform_extension_project_dir
                )
            out_string = out_string.replace("{PLATFORM}", platform)

        if self.is_for_plugin:
            out_string = out_string.replace("{PLUGIN}", self.plugin_root_dir)
        return out_string

    def get_per_platform_dirs(self, platform_name: str) -> PerPlatformDirs:
        dirs = self.per_platforms_dirs.get(platform_name)
        if not dirs:
            dirs = PerPlatformDirs(
                (paths.engine_patform_extensions_dir() + platform_name).replace(
                    paths.engine_dir(), self.engine_root_dir + "/"
                ),
                (paths.project_patform_extensions_dir() + platform_name).replace(
                    paths.project_dir(), self.project_root_dir + "/"
                ),
            )
            self.per_platforms_dirs[platform_name] = dirs
        return dirs

    def load_an_ini_file(self, filename: str, config_file: UEConfigFile) -> bool:
        # skip non-existant files
        if not os.path.isfile(filename):
            return False
        config_file.read(filename)
        config_file.num += 1
        return True

    def load_ini_file_hieararchy(
        self,
        hierarchy: ConfigFileHierarchy,
        config: UEConfigFile,
        use_cache: bool = False,
        ini_cache_set: set[str] = set(),
    ) -> bool:
        # Traverse ini list back to front, merging along the way.
        processed_files = set()
        # print(f"Loading hierarchy {hierarchy}")
        for key, filename in hierarchy.items():
            # print(f"Loading1 {filename}")
            if filename in processed_files:
                continue
            # do_combine = key != 0
            # skip non-existant files
            if not os.path.isfile(filename):
                continue
            # print(f"Loading {filename}")
            config.read(filename)
            config.num += 1
            processed_files.add(filename)

        # Set this configs files source ini hierarchy to show where it was loaded from.
        config.source_ini_hierarchy = hierarchy
        return True


def get_custom_config_string() -> str:
    # default is empty and there is no way to override it in this program.
    return ""
