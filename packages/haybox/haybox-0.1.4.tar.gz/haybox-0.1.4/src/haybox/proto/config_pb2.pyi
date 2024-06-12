from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Command(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CMD_UNSPECIFIED: _ClassVar[Command]
    CMD_GET_DEVICE_INFO: _ClassVar[Command]
    CMD_SET_DEVICE_INFO: _ClassVar[Command]
    CMD_GET_CONFIG: _ClassVar[Command]
    CMD_SET_CONFIG: _ClassVar[Command]
    CMD_ERROR: _ClassVar[Command]
    CMD_SUCCESS: _ClassVar[Command]
    CMD_REBOOT_FIRMWARE: _ClassVar[Command]
    CMD_REBOOT_BOOTLOADER: _ClassVar[Command]

class Button(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BTN_UNSPECIFIED: _ClassVar[Button]
    BTN_LF1: _ClassVar[Button]
    BTN_LF2: _ClassVar[Button]
    BTN_LF3: _ClassVar[Button]
    BTN_LF4: _ClassVar[Button]
    BTN_LF5: _ClassVar[Button]
    BTN_LF6: _ClassVar[Button]
    BTN_LF7: _ClassVar[Button]
    BTN_LF8: _ClassVar[Button]
    BTN_LF9: _ClassVar[Button]
    BTN_LF10: _ClassVar[Button]
    BTN_LF11: _ClassVar[Button]
    BTN_LF12: _ClassVar[Button]
    BTN_LF13: _ClassVar[Button]
    BTN_LF14: _ClassVar[Button]
    BTN_LF15: _ClassVar[Button]
    BTN_LF16: _ClassVar[Button]
    BTN_RF1: _ClassVar[Button]
    BTN_RF2: _ClassVar[Button]
    BTN_RF3: _ClassVar[Button]
    BTN_RF4: _ClassVar[Button]
    BTN_RF5: _ClassVar[Button]
    BTN_RF6: _ClassVar[Button]
    BTN_RF7: _ClassVar[Button]
    BTN_RF8: _ClassVar[Button]
    BTN_RF9: _ClassVar[Button]
    BTN_RF10: _ClassVar[Button]
    BTN_RF11: _ClassVar[Button]
    BTN_RF12: _ClassVar[Button]
    BTN_RF13: _ClassVar[Button]
    BTN_RF14: _ClassVar[Button]
    BTN_RF15: _ClassVar[Button]
    BTN_RF16: _ClassVar[Button]
    BTN_LT1: _ClassVar[Button]
    BTN_LT2: _ClassVar[Button]
    BTN_LT3: _ClassVar[Button]
    BTN_LT4: _ClassVar[Button]
    BTN_LT5: _ClassVar[Button]
    BTN_LT6: _ClassVar[Button]
    BTN_LT7: _ClassVar[Button]
    BTN_LT8: _ClassVar[Button]
    BTN_RT1: _ClassVar[Button]
    BTN_RT2: _ClassVar[Button]
    BTN_RT3: _ClassVar[Button]
    BTN_RT4: _ClassVar[Button]
    BTN_RT5: _ClassVar[Button]
    BTN_RT6: _ClassVar[Button]
    BTN_RT7: _ClassVar[Button]
    BTN_RT8: _ClassVar[Button]
    BTN_MB1: _ClassVar[Button]
    BTN_MB2: _ClassVar[Button]
    BTN_MB3: _ClassVar[Button]
    BTN_MB4: _ClassVar[Button]
    BTN_MB5: _ClassVar[Button]
    BTN_MB6: _ClassVar[Button]
    BTN_MB7: _ClassVar[Button]
    BTN_MB8: _ClassVar[Button]
    BTN_MB9: _ClassVar[Button]
    BTN_MB10: _ClassVar[Button]
    BTN_MB11: _ClassVar[Button]
    BTN_MB12: _ClassVar[Button]

class SocdType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOCD_UNSPECIFIED: _ClassVar[SocdType]
    SOCD_NEUTRAL: _ClassVar[SocdType]
    SOCD_2IP: _ClassVar[SocdType]
    SOCD_2IP_NO_REAC: _ClassVar[SocdType]
    SOCD_DIR1_PRIORITY: _ClassVar[SocdType]
    SOCD_DIR2_PRIORITY: _ClassVar[SocdType]

class GameModeId(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODE_UNSPECIFIED: _ClassVar[GameModeId]
    MODE_MELEE: _ClassVar[GameModeId]
    MODE_PROJECT_M: _ClassVar[GameModeId]
    MODE_ULTIMATE: _ClassVar[GameModeId]
    MODE_FGC: _ClassVar[GameModeId]
    MODE_RIVALS_OF_AETHER: _ClassVar[GameModeId]
    MODE_KEYBOARD: _ClassVar[GameModeId]
    MODE_CUSTOM: _ClassVar[GameModeId]

class CommunicationBackendId(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMMS_BACKEND_UNSPECIFIED: _ClassVar[CommunicationBackendId]
    COMMS_BACKEND_DINPUT: _ClassVar[CommunicationBackendId]
    COMMS_BACKEND_XINPUT: _ClassVar[CommunicationBackendId]
    COMMS_BACKEND_GAMECUBE: _ClassVar[CommunicationBackendId]
    COMMS_BACKEND_N64: _ClassVar[CommunicationBackendId]
    COMMS_BACKEND_NES: _ClassVar[CommunicationBackendId]
    COMMS_BACKEND_SNES: _ClassVar[CommunicationBackendId]
    COMMS_BACKEND_NINTENDO_SWITCH: _ClassVar[CommunicationBackendId]
    COMMS_BACKEND_CONFIGURATOR: _ClassVar[CommunicationBackendId]

class RgbAnimationId(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RGB_ANIM_UNSPECIFIED: _ClassVar[RgbAnimationId]
    RGB_ANIM_STATIC: _ClassVar[RgbAnimationId]
    RGB_ANIM_BREATHE: _ClassVar[RgbAnimationId]
    RGB_ANIM_REACTIVE_SIMPLE: _ClassVar[RgbAnimationId]

class DigitalOutput(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GP_UNSPECIFIED: _ClassVar[DigitalOutput]
    GP_A: _ClassVar[DigitalOutput]
    GP_B: _ClassVar[DigitalOutput]
    GP_X: _ClassVar[DigitalOutput]
    GP_Y: _ClassVar[DigitalOutput]
    GP_LB: _ClassVar[DigitalOutput]
    GP_RB: _ClassVar[DigitalOutput]
    GP_LT: _ClassVar[DigitalOutput]
    GP_RT: _ClassVar[DigitalOutput]
    GP_START: _ClassVar[DigitalOutput]
    GP_SELECT: _ClassVar[DigitalOutput]
    GP_HOME: _ClassVar[DigitalOutput]
    GP_CAPTURE: _ClassVar[DigitalOutput]
    GP_DPAD_UP: _ClassVar[DigitalOutput]
    GP_DPAD_DOWN: _ClassVar[DigitalOutput]
    GP_DPAD_LEFT: _ClassVar[DigitalOutput]
    GP_DPAD_RIGHT: _ClassVar[DigitalOutput]
    GP_LSTICK_CLICK: _ClassVar[DigitalOutput]
    GP_RSTICK_CLICK: _ClassVar[DigitalOutput]

class StickDirectionButton(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SD_UNSPECIFIED: _ClassVar[StickDirectionButton]
    SD_LSTICK_UP: _ClassVar[StickDirectionButton]
    SD_LSTICK_DOWN: _ClassVar[StickDirectionButton]
    SD_LSTICK_LEFT: _ClassVar[StickDirectionButton]
    SD_LSTICK_RIGHT: _ClassVar[StickDirectionButton]
    SD_RSTICK_UP: _ClassVar[StickDirectionButton]
    SD_RSTICK_DOWN: _ClassVar[StickDirectionButton]
    SD_RSTICK_LEFT: _ClassVar[StickDirectionButton]
    SD_RSTICK_RIGHT: _ClassVar[StickDirectionButton]

class AnalogAxis(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AXIS_UNSPECIFIED: _ClassVar[AnalogAxis]
    AXIS_LSTICK_X: _ClassVar[AnalogAxis]
    AXIS_LSTICK_Y: _ClassVar[AnalogAxis]
    AXIS_RSTICK_X: _ClassVar[AnalogAxis]
    AXIS_RSTICK_Y: _ClassVar[AnalogAxis]
    AXIS_LTRIGGER: _ClassVar[AnalogAxis]
    AXIS_RTRIGGER: _ClassVar[AnalogAxis]

class AnalogTrigger(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRIGGER_UNSPECIFIED: _ClassVar[AnalogTrigger]
    TRIGGER_LT: _ClassVar[AnalogTrigger]
    TRIGGER_RT: _ClassVar[AnalogTrigger]

class ModifierCombinationMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMBINATION_MODE_UNSPECIFIED: _ClassVar[ModifierCombinationMode]
    COMBINATION_MODE_COMPOUND: _ClassVar[ModifierCombinationMode]
    COMBINATION_MODE_OVERRIDE: _ClassVar[ModifierCombinationMode]
CMD_UNSPECIFIED: Command
CMD_GET_DEVICE_INFO: Command
CMD_SET_DEVICE_INFO: Command
CMD_GET_CONFIG: Command
CMD_SET_CONFIG: Command
CMD_ERROR: Command
CMD_SUCCESS: Command
CMD_REBOOT_FIRMWARE: Command
CMD_REBOOT_BOOTLOADER: Command
BTN_UNSPECIFIED: Button
BTN_LF1: Button
BTN_LF2: Button
BTN_LF3: Button
BTN_LF4: Button
BTN_LF5: Button
BTN_LF6: Button
BTN_LF7: Button
BTN_LF8: Button
BTN_LF9: Button
BTN_LF10: Button
BTN_LF11: Button
BTN_LF12: Button
BTN_LF13: Button
BTN_LF14: Button
BTN_LF15: Button
BTN_LF16: Button
BTN_RF1: Button
BTN_RF2: Button
BTN_RF3: Button
BTN_RF4: Button
BTN_RF5: Button
BTN_RF6: Button
BTN_RF7: Button
BTN_RF8: Button
BTN_RF9: Button
BTN_RF10: Button
BTN_RF11: Button
BTN_RF12: Button
BTN_RF13: Button
BTN_RF14: Button
BTN_RF15: Button
BTN_RF16: Button
BTN_LT1: Button
BTN_LT2: Button
BTN_LT3: Button
BTN_LT4: Button
BTN_LT5: Button
BTN_LT6: Button
BTN_LT7: Button
BTN_LT8: Button
BTN_RT1: Button
BTN_RT2: Button
BTN_RT3: Button
BTN_RT4: Button
BTN_RT5: Button
BTN_RT6: Button
BTN_RT7: Button
BTN_RT8: Button
BTN_MB1: Button
BTN_MB2: Button
BTN_MB3: Button
BTN_MB4: Button
BTN_MB5: Button
BTN_MB6: Button
BTN_MB7: Button
BTN_MB8: Button
BTN_MB9: Button
BTN_MB10: Button
BTN_MB11: Button
BTN_MB12: Button
SOCD_UNSPECIFIED: SocdType
SOCD_NEUTRAL: SocdType
SOCD_2IP: SocdType
SOCD_2IP_NO_REAC: SocdType
SOCD_DIR1_PRIORITY: SocdType
SOCD_DIR2_PRIORITY: SocdType
MODE_UNSPECIFIED: GameModeId
MODE_MELEE: GameModeId
MODE_PROJECT_M: GameModeId
MODE_ULTIMATE: GameModeId
MODE_FGC: GameModeId
MODE_RIVALS_OF_AETHER: GameModeId
MODE_KEYBOARD: GameModeId
MODE_CUSTOM: GameModeId
COMMS_BACKEND_UNSPECIFIED: CommunicationBackendId
COMMS_BACKEND_DINPUT: CommunicationBackendId
COMMS_BACKEND_XINPUT: CommunicationBackendId
COMMS_BACKEND_GAMECUBE: CommunicationBackendId
COMMS_BACKEND_N64: CommunicationBackendId
COMMS_BACKEND_NES: CommunicationBackendId
COMMS_BACKEND_SNES: CommunicationBackendId
COMMS_BACKEND_NINTENDO_SWITCH: CommunicationBackendId
COMMS_BACKEND_CONFIGURATOR: CommunicationBackendId
RGB_ANIM_UNSPECIFIED: RgbAnimationId
RGB_ANIM_STATIC: RgbAnimationId
RGB_ANIM_BREATHE: RgbAnimationId
RGB_ANIM_REACTIVE_SIMPLE: RgbAnimationId
GP_UNSPECIFIED: DigitalOutput
GP_A: DigitalOutput
GP_B: DigitalOutput
GP_X: DigitalOutput
GP_Y: DigitalOutput
GP_LB: DigitalOutput
GP_RB: DigitalOutput
GP_LT: DigitalOutput
GP_RT: DigitalOutput
GP_START: DigitalOutput
GP_SELECT: DigitalOutput
GP_HOME: DigitalOutput
GP_CAPTURE: DigitalOutput
GP_DPAD_UP: DigitalOutput
GP_DPAD_DOWN: DigitalOutput
GP_DPAD_LEFT: DigitalOutput
GP_DPAD_RIGHT: DigitalOutput
GP_LSTICK_CLICK: DigitalOutput
GP_RSTICK_CLICK: DigitalOutput
SD_UNSPECIFIED: StickDirectionButton
SD_LSTICK_UP: StickDirectionButton
SD_LSTICK_DOWN: StickDirectionButton
SD_LSTICK_LEFT: StickDirectionButton
SD_LSTICK_RIGHT: StickDirectionButton
SD_RSTICK_UP: StickDirectionButton
SD_RSTICK_DOWN: StickDirectionButton
SD_RSTICK_LEFT: StickDirectionButton
SD_RSTICK_RIGHT: StickDirectionButton
AXIS_UNSPECIFIED: AnalogAxis
AXIS_LSTICK_X: AnalogAxis
AXIS_LSTICK_Y: AnalogAxis
AXIS_RSTICK_X: AnalogAxis
AXIS_RSTICK_Y: AnalogAxis
AXIS_LTRIGGER: AnalogAxis
AXIS_RTRIGGER: AnalogAxis
TRIGGER_UNSPECIFIED: AnalogTrigger
TRIGGER_LT: AnalogTrigger
TRIGGER_RT: AnalogTrigger
COMBINATION_MODE_UNSPECIFIED: ModifierCombinationMode
COMBINATION_MODE_COMPOUND: ModifierCombinationMode
COMBINATION_MODE_OVERRIDE: ModifierCombinationMode

class ButtonRemap(_message.Message):
    __slots__ = ("physical_button", "activates")
    PHYSICAL_BUTTON_FIELD_NUMBER: _ClassVar[int]
    ACTIVATES_FIELD_NUMBER: _ClassVar[int]
    physical_button: Button
    activates: Button
    def __init__(self, physical_button: _Optional[_Union[Button, str]] = ..., activates: _Optional[_Union[Button, str]] = ...) -> None: ...

class SocdPair(_message.Message):
    __slots__ = ("button_dir1", "button_dir2", "socd_type")
    BUTTON_DIR1_FIELD_NUMBER: _ClassVar[int]
    BUTTON_DIR2_FIELD_NUMBER: _ClassVar[int]
    SOCD_TYPE_FIELD_NUMBER: _ClassVar[int]
    button_dir1: Button
    button_dir2: Button
    socd_type: SocdType
    def __init__(self, button_dir1: _Optional[_Union[Button, str]] = ..., button_dir2: _Optional[_Union[Button, str]] = ..., socd_type: _Optional[_Union[SocdType, str]] = ...) -> None: ...

class AnalogTriggerMapping(_message.Message):
    __slots__ = ("button", "trigger", "value")
    BUTTON_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    button: Button
    trigger: AnalogTrigger
    value: int
    def __init__(self, button: _Optional[_Union[Button, str]] = ..., trigger: _Optional[_Union[AnalogTrigger, str]] = ..., value: _Optional[int] = ...) -> None: ...

class AnalogModifier(_message.Message):
    __slots__ = ("buttons", "axis", "multiplier", "combination_mode")
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    AXIS_FIELD_NUMBER: _ClassVar[int]
    MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    COMBINATION_MODE_FIELD_NUMBER: _ClassVar[int]
    buttons: _containers.RepeatedScalarFieldContainer[Button]
    axis: AnalogAxis
    multiplier: float
    combination_mode: ModifierCombinationMode
    def __init__(self, buttons: _Optional[_Iterable[_Union[Button, str]]] = ..., axis: _Optional[_Union[AnalogAxis, str]] = ..., multiplier: _Optional[float] = ..., combination_mode: _Optional[_Union[ModifierCombinationMode, str]] = ...) -> None: ...

class ButtonComboMapping(_message.Message):
    __slots__ = ("buttons", "digital_output")
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    buttons: _containers.RepeatedScalarFieldContainer[Button]
    digital_output: DigitalOutput
    def __init__(self, buttons: _Optional[_Iterable[_Union[Button, str]]] = ..., digital_output: _Optional[_Union[DigitalOutput, str]] = ...) -> None: ...

class Coords(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class ButtonToKeycodeMapping(_message.Message):
    __slots__ = ("button", "keycode")
    BUTTON_FIELD_NUMBER: _ClassVar[int]
    KEYCODE_FIELD_NUMBER: _ClassVar[int]
    button: Button
    keycode: int
    def __init__(self, button: _Optional[_Union[Button, str]] = ..., keycode: _Optional[int] = ...) -> None: ...

class ButtonToColorMapping(_message.Message):
    __slots__ = ("button", "color")
    BUTTON_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    button: Button
    color: int
    def __init__(self, button: _Optional[_Union[Button, str]] = ..., color: _Optional[int] = ...) -> None: ...

class CustomModeConfig(_message.Message):
    __slots__ = ("id", "digital_button_mappings", "stick_direction_mappings", "analog_trigger_mappings", "modifiers", "stick_range", "button_combo_mappings")
    ID_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_BUTTON_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    STICK_DIRECTION_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    ANALOG_TRIGGER_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    MODIFIERS_FIELD_NUMBER: _ClassVar[int]
    STICK_RANGE_FIELD_NUMBER: _ClassVar[int]
    BUTTON_COMBO_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    id: int
    digital_button_mappings: _containers.RepeatedScalarFieldContainer[Button]
    stick_direction_mappings: _containers.RepeatedScalarFieldContainer[Button]
    analog_trigger_mappings: _containers.RepeatedCompositeFieldContainer[AnalogTriggerMapping]
    modifiers: _containers.RepeatedCompositeFieldContainer[AnalogModifier]
    stick_range: int
    button_combo_mappings: _containers.RepeatedCompositeFieldContainer[ButtonComboMapping]
    def __init__(self, id: _Optional[int] = ..., digital_button_mappings: _Optional[_Iterable[_Union[Button, str]]] = ..., stick_direction_mappings: _Optional[_Iterable[_Union[Button, str]]] = ..., analog_trigger_mappings: _Optional[_Iterable[_Union[AnalogTriggerMapping, _Mapping]]] = ..., modifiers: _Optional[_Iterable[_Union[AnalogModifier, _Mapping]]] = ..., stick_range: _Optional[int] = ..., button_combo_mappings: _Optional[_Iterable[_Union[ButtonComboMapping, _Mapping]]] = ...) -> None: ...

class KeyboardModeConfig(_message.Message):
    __slots__ = ("id", "buttons_to_keycodes")
    ID_FIELD_NUMBER: _ClassVar[int]
    BUTTONS_TO_KEYCODES_FIELD_NUMBER: _ClassVar[int]
    id: int
    buttons_to_keycodes: _containers.RepeatedCompositeFieldContainer[ButtonToKeycodeMapping]
    def __init__(self, id: _Optional[int] = ..., buttons_to_keycodes: _Optional[_Iterable[_Union[ButtonToKeycodeMapping, _Mapping]]] = ...) -> None: ...

class GameModeConfig(_message.Message):
    __slots__ = ("mode_id", "name", "socd_pairs", "button_remapping", "activation_binding", "custom_mode_config", "keyboard_mode_config", "rgb_config")
    MODE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SOCD_PAIRS_FIELD_NUMBER: _ClassVar[int]
    BUTTON_REMAPPING_FIELD_NUMBER: _ClassVar[int]
    ACTIVATION_BINDING_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MODE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    KEYBOARD_MODE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    RGB_CONFIG_FIELD_NUMBER: _ClassVar[int]
    mode_id: GameModeId
    name: str
    socd_pairs: _containers.RepeatedCompositeFieldContainer[SocdPair]
    button_remapping: _containers.RepeatedCompositeFieldContainer[ButtonRemap]
    activation_binding: _containers.RepeatedScalarFieldContainer[Button]
    custom_mode_config: int
    keyboard_mode_config: int
    rgb_config: int
    def __init__(self, mode_id: _Optional[_Union[GameModeId, str]] = ..., name: _Optional[str] = ..., socd_pairs: _Optional[_Iterable[_Union[SocdPair, _Mapping]]] = ..., button_remapping: _Optional[_Iterable[_Union[ButtonRemap, _Mapping]]] = ..., activation_binding: _Optional[_Iterable[_Union[Button, str]]] = ..., custom_mode_config: _Optional[int] = ..., keyboard_mode_config: _Optional[int] = ..., rgb_config: _Optional[int] = ...) -> None: ...

class CommunicationBackendConfig(_message.Message):
    __slots__ = ("backend_id", "default_mode_config", "activation_binding", "secondary_backends")
    BACKEND_ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_MODE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ACTIVATION_BINDING_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_BACKENDS_FIELD_NUMBER: _ClassVar[int]
    backend_id: CommunicationBackendId
    default_mode_config: int
    activation_binding: _containers.RepeatedScalarFieldContainer[Button]
    secondary_backends: _containers.RepeatedScalarFieldContainer[CommunicationBackendId]
    def __init__(self, backend_id: _Optional[_Union[CommunicationBackendId, str]] = ..., default_mode_config: _Optional[int] = ..., activation_binding: _Optional[_Iterable[_Union[Button, str]]] = ..., secondary_backends: _Optional[_Iterable[_Union[CommunicationBackendId, str]]] = ...) -> None: ...

class RgbConfig(_message.Message):
    __slots__ = ("button_colors", "default_color", "animation", "speed")
    BUTTON_COLORS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_COLOR_FIELD_NUMBER: _ClassVar[int]
    ANIMATION_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    button_colors: _containers.RepeatedCompositeFieldContainer[ButtonToColorMapping]
    default_color: int
    animation: RgbAnimationId
    speed: int
    def __init__(self, button_colors: _Optional[_Iterable[_Union[ButtonToColorMapping, _Mapping]]] = ..., default_color: _Optional[int] = ..., animation: _Optional[_Union[RgbAnimationId, str]] = ..., speed: _Optional[int] = ...) -> None: ...

class MeleeOptions(_message.Message):
    __slots__ = ("crouch_walk_os", "disable_ledgedash_socd_override", "custom_airdodge")
    CROUCH_WALK_OS_FIELD_NUMBER: _ClassVar[int]
    DISABLE_LEDGEDASH_SOCD_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_AIRDODGE_FIELD_NUMBER: _ClassVar[int]
    crouch_walk_os: bool
    disable_ledgedash_socd_override: bool
    custom_airdodge: Coords
    def __init__(self, crouch_walk_os: bool = ..., disable_ledgedash_socd_override: bool = ..., custom_airdodge: _Optional[_Union[Coords, _Mapping]] = ...) -> None: ...

class ProjectMOptions(_message.Message):
    __slots__ = ("true_z_press", "disable_ledgedash_socd_override", "custom_airdodge")
    TRUE_Z_PRESS_FIELD_NUMBER: _ClassVar[int]
    DISABLE_LEDGEDASH_SOCD_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_AIRDODGE_FIELD_NUMBER: _ClassVar[int]
    true_z_press: bool
    disable_ledgedash_socd_override: bool
    custom_airdodge: Coords
    def __init__(self, true_z_press: bool = ..., disable_ledgedash_socd_override: bool = ..., custom_airdodge: _Optional[_Union[Coords, _Mapping]] = ...) -> None: ...

class Config(_message.Message):
    __slots__ = ("game_mode_configs", "communication_backend_configs", "custom_modes", "keyboard_modes", "rgb_configs", "default_backend_config", "default_usb_backend_config", "rgb_brightness", "melee_options", "project_m_options")
    GAME_MODE_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    COMMUNICATION_BACKEND_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MODES_FIELD_NUMBER: _ClassVar[int]
    KEYBOARD_MODES_FIELD_NUMBER: _ClassVar[int]
    RGB_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_BACKEND_CONFIG_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_USB_BACKEND_CONFIG_FIELD_NUMBER: _ClassVar[int]
    RGB_BRIGHTNESS_FIELD_NUMBER: _ClassVar[int]
    MELEE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PROJECT_M_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    game_mode_configs: _containers.RepeatedCompositeFieldContainer[GameModeConfig]
    communication_backend_configs: _containers.RepeatedCompositeFieldContainer[CommunicationBackendConfig]
    custom_modes: _containers.RepeatedCompositeFieldContainer[CustomModeConfig]
    keyboard_modes: _containers.RepeatedCompositeFieldContainer[KeyboardModeConfig]
    rgb_configs: _containers.RepeatedCompositeFieldContainer[RgbConfig]
    default_backend_config: int
    default_usb_backend_config: int
    rgb_brightness: int
    melee_options: MeleeOptions
    project_m_options: ProjectMOptions
    def __init__(self, game_mode_configs: _Optional[_Iterable[_Union[GameModeConfig, _Mapping]]] = ..., communication_backend_configs: _Optional[_Iterable[_Union[CommunicationBackendConfig, _Mapping]]] = ..., custom_modes: _Optional[_Iterable[_Union[CustomModeConfig, _Mapping]]] = ..., keyboard_modes: _Optional[_Iterable[_Union[KeyboardModeConfig, _Mapping]]] = ..., rgb_configs: _Optional[_Iterable[_Union[RgbConfig, _Mapping]]] = ..., default_backend_config: _Optional[int] = ..., default_usb_backend_config: _Optional[int] = ..., rgb_brightness: _Optional[int] = ..., melee_options: _Optional[_Union[MeleeOptions, _Mapping]] = ..., project_m_options: _Optional[_Union[ProjectMOptions, _Mapping]] = ...) -> None: ...

class DeviceInfo(_message.Message):
    __slots__ = ("firmware_name", "firmware_version", "device_name")
    FIRMWARE_NAME_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    firmware_name: str
    firmware_version: str
    device_name: str
    def __init__(self, firmware_name: _Optional[str] = ..., firmware_version: _Optional[str] = ..., device_name: _Optional[str] = ...) -> None: ...
