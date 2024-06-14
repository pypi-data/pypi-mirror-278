from __future__ import annotations

import glob
import os.path
from configparser import SectionProxy
from dataclasses import dataclass, field

from . import config_cache, paths

# dummy implementation of the platform module, we only ever use the empty platform.

has_searched_for_files = False
has_searched_for_platforms = False

data_driven_ini_filenames: list[str] = []
platforms: dict[str, DataDrivenPlatformInfo] = {}
platform_name_aliases: dict[str, str] = {}
all_sorted_platforms: list[str] = []
sorted_platforms: list[str] = []
all_sorted_platform_infos: list[DataDrivenPlatformInfo] = []
sorted_platform_infos: list[DataDrivenPlatformInfo] = []


def reset():
    global has_searched_for_files
    global has_searched_for_platforms
    has_searched_for_files = False
    has_searched_for_platforms = False


@dataclass
class DataDrivenPlatformInfo:
    ini_platform_name: str = ""
    ini_parent_chain: list[str] = field(default_factory=list)
    is_fake_platform: bool = False
    is_confidential: bool = False


def get_info(platform: str) -> DataDrivenPlatformInfo:
    if platform:
        return get_platforms().get(platform, DataDrivenPlatformInfo())
    return DataDrivenPlatformInfo()


# hardwired for windows now
def ini_platform_name() -> str:
    return "Windows"


def platform_name() -> str:
    return "Windows"


def get_data_driven_ini_filenames() -> list[str]:
    global has_searched_for_files
    global data_driven_ini_filenames
    if has_searched_for_files:
        return data_driven_ini_filenames

    # look for the special files in any config subdirectories
    patterns = [
        # look for the special files in any config subdirectories
        os.path.join(paths.engine_config_dir(), "**", "DataDrivenPlatformInfo.ini"),
        os.path.join(
            paths.engine_patform_extensions_dir(), "**", "DataDrivenPlatformInfo.ini"
        ),
        os.path.join(
            paths.project_patform_extensions_dir(), "**", "DataDrivenPlatformInfo.ini"
        ),
    ]
    found = []
    for p in patterns:
        found += glob.glob(p, recursive=True)
    data_driven_ini_filenames = found
    has_searched_for_files = True
    return data_driven_ini_filenames


def get_platforms() -> dict[str, DataDrivenPlatformInfo]:
    global has_searched_for_platforms
    global platforms
    if has_searched_for_platforms:
        return platforms

    # get the filenames
    filenames = get_data_driven_ini_filenames()

    # read the files
    platforms = {}
    ini_parents: dict[str, str] = {}
    for filename in filenames:
        platformstring, inifile = load_data_driven_ini_file(filename)

        if "DataDrivenPlatformInfo" not in inifile.sections():
            continue

        if platformstring not in platforms:
            platforms[platformstring] = DataDrivenPlatformInfo()
        info = platforms[platformstring]
        ddpi = inifile["DataDrivenPlatformInfo"]
        load_ddpi_ini_settings(platformstring, info, ddpi)
        info.ini_platform_name = platformstring

        ini_parent = ddpi.get("ParentPlatform", "")
        ini_parents[platformstring] = ini_parent

        aliases = ddpi.get("PlatformNameAliases", "")
        for alias in aliases.split(","):
            alias = alias.strip()
            if alias:
                platform_name_aliases[alias] = platformstring

    # now that all are read in, calculate the ini parent chain, starting with parent-most
    for platform, info in platforms.items():
        # walk up the chain and build up the ini chain of parents
        current_platform = ini_parents.get(platform, "")
        while current_platform:
            info.ini_parent_chain.append(current_platform)
            current_platform = ini_parents.get(current_platform, "")
        info.ini_parent_chain.reverse()

    global all_sorted_platforms
    global sorted_platforms
    global all_sorted_platform_infos
    global sorted_platform_infos
    all_sorted_platforms = list(platforms.keys())
    all_sorted_platforms.sort()
    sorted_platforms = [
        x for x in all_sorted_platforms if not platforms[x].is_fake_platform
    ]
    all_sorted_platform_infos = [platforms[x] for x in all_sorted_platforms]
    sorted_platform_infos = [platforms[x] for x in sorted_platforms]

    has_searched_for_platforms = True
    return platforms


def load_data_driven_ini_file(filename) -> tuple[str, config_cache.UEConfigParser]:
    parser = config_cache.UEConfigParser()
    parser.read(filename)

    if filename.startswith(
        paths.engine_patform_extensions_dir()
    ) or filename.startswith(paths.project_patform_extensions_dir()):
        # platforms/platform/config/DataDrivenPlatformInfo.ini
        platform_name = os.path.basename(os.path.dirname(os.path.dirname(filename)))
    else:
        # config/platform/DatDrivenPlatformInfo.ini
        platform_name = os.path.basename(os.path.dirname(filename))
    return platform_name, parser


def load_ddpi_ini_settings(
    platform_name: str, info: DataDrivenPlatformInfo, ini: SectionProxy
) -> None:
    # don't support command line prefixes

    def get_bool(name, default):
        return ini.getboolean(name, default)

    info.is_confidential = get_bool("bIsConfidential", info.is_confidential)
    info.is_fake_platform = get_bool("bIsFakePlatform", info.is_fake_platform)

    """

	DDPIGetString(IniFile, TEXT("TargetSettingsIniSectionName"), Info.TargetSettingsIniSectionName);
	DDPIGetString(IniFile, TEXT("HardwareCompressionFormat"), Info.HardwareCompressionFormat);
	DDPIGetStringArray(IniFile, TEXT("AdditionalRestrictedFolders"), Info.AdditionalRestrictedFolders);

	DDPIGetBool(IniFile, TEXT("Freezing_b32Bit"), Info.Freezing_b32Bit);
	DDPIGetUInt(IniFile, Info.Freezing_b32Bit ? TEXT("Freezing_MaxFieldAlignment32") : TEXT("Freezing_MaxFieldAlignment64"), Info.Freezing_MaxFieldAlignment);
	DDPIGetBool(IniFile, TEXT("Freezing_bForce64BitMemoryImagePointers"), Info.Freezing_bForce64BitMemoryImagePointers);
	DDPIGetBool(IniFile, TEXT("Freezing_bAlignBases"), Info.Freezing_bAlignBases);

	DDPIGetGuid(IniFile, TEXT("GlobalIdentifier"), Info.GlobalIdentifier);
	checkf(Info.GlobalIdentifier != FGuid(), TEXT("Platform %s didn't have a valid GlobalIdentifier set in DataDrivenPlatformInfo.ini"), *PlatformName.ToString());

	// NOTE: add more settings here!
	DDPIGetBool(IniFile, TEXT("bHasDedicatedGamepad"), Info.bHasDedicatedGamepad);
	DDPIGetBool(IniFile, TEXT("bDefaultInputStandardKeyboard"), Info.bDefaultInputStandardKeyboard);

	DDPIGetBool(IniFile, TEXT("bInputSupportConfigurable"), Info.bInputSupportConfigurable);
	DDPIGetString(IniFile, TEXT("DefaultInputType"), Info.DefaultInputType);
	DDPIGetBool(IniFile, TEXT("bSupportsMouseAndKeyboard"), Info.bSupportsMouseAndKeyboard);
	DDPIGetBool(IniFile, TEXT("bSupportsGamepad"), Info.bSupportsGamepad);
	DDPIGetBool(IniFile, TEXT("bCanChangeGamepadType"), Info.bCanChangeGamepadType);
	DDPIGetBool(IniFile, TEXT("bSupportsTouch"), Info.bSupportsTouch);

#if DDPI_HAS_EXTENDED_PLATFORMINFO_DATA

	DDPIGetString(IniFile, TEXT("AutoSDKPath"), Info.AutoSDKPath);
	DDPIGetString(IniFile, TEXT("TutorialPath"), Info.SDKTutorial);
	DDPIGetName(IniFile, TEXT("PlatformGroupName"), Info.PlatformGroupName);
	DDPIGetName(IniFile, TEXT("PlatformSubMenu"), Info.PlatformSubMenu);


	DDPIGetString(IniFile, TEXT("NormalIconPath"), Info.IconPaths.NormalPath);
	DDPIGetString(IniFile, TEXT("LargeIconPath"), Info.IconPaths.LargePath);
	DDPIGetString(IniFile, TEXT("XLargeIconPath"), Info.IconPaths.XLargePath);
	if (Info.IconPaths.XLargePath == TEXT(""))
	{
		Info.IconPaths.XLargePath = Info.IconPaths.LargePath;
	}

	FString PlatformString = PlatformName.ToString();
	Info.IconPaths.NormalStyleName = *FString::Printf(TEXT("Launcher.Platform_%s"), *PlatformString);
	Info.IconPaths.LargeStyleName = *FString::Printf(TEXT("Launcher.Platform_%s.Large"), *PlatformString);
	Info.IconPaths.XLargeStyleName = *FString::Printf(TEXT("Launcher.Platform_%s.XLarge"), *PlatformString);

	Info.bCanUseCrashReporter = true; // not specified means true, not false
	DDPIGetBool(IniFile, TEXT("bCanUseCrashReporter"), Info.bCanUseCrashReporter);
	DDPIGetBool(IniFile, TEXT("bUsesHostCompiler"), Info.bUsesHostCompiler);
	DDPIGetBool(IniFile, TEXT("bUATClosesAfterLaunch"), Info.bUATClosesAfterLaunch);
	DDPIGetBool(IniFile, TEXT("bIsEnabled"), Info.bEnabledForUse);

	DDPIGetName(IniFile, TEXT("UBTPlatformName"), Info.UBTPlatformName);
	// if unspecified, use the ini platform name (only Win64 breaks this)
	if (Info.UBTPlatformName == NAME_None)
	{
		Info.UBTPlatformName = PlatformName;
	}
	Info.UBTPlatformString = Info.UBTPlatformName.ToString();
		
	GCommandLinePrefix = TEXT("");

	// now that we have all targetplatforms in a single TP module per platform, just look for it (or a ShaderFormat for other tools that may want this)
	// we could look for Platform*, but then platforms that are a substring of another one could return a false positive (Windows* would find Windows31TargetPlatform)
	Info.bHasCompiledTargetSupport = FDataDrivenPlatformInfoRegistry::HasCompiledSupportForPlatform(PlatformName, FDataDrivenPlatformInfoRegistry::EPlatformNameType::TargetPlatform);

	ParsePreviewPlatforms(IniFile);
#endif
}
"""
