
from dataclasses import dataclass, field
from typing import Literal

from gmdkit.models.prop.color import Color as KitColor
from gmdkit.models.prop.hsv import HSV


@dataclass
class Color:
    red: int = 0
    green: int = 0
    blue: int = 0  
    player: Literal[-1,0,1,2] = -1
    blending: bool = False
    channel: int = 0
    opacity: float = 0.0
    copy_id: int = 0
    hsv: HSV = field(default_factory=HSV)
    copy_opacity: bool = False
    disable_legacy_hsv: bool = False
    
    @classmethod
    def from_kit_color(cls, kit_color: KitColor) -> "Color":
        return cls(
            red=kit_color.red,
            green=kit_color.green,
            blue=kit_color.blue, 
            player=kit_color.player,
            blending=kit_color.blending,
            channel=kit_color.channel,
            opacity=kit_color.opacity,
            copy_id=kit_color.copy_id,
            hsv=kit_color.hsv,
            copy_opacity=kit_color.copy_opacity,
            disable_legacy_hsv=kit_color.disable_legacy_hsv
        )
    
    def to_kit_color(self) -> KitColor:
        return KitColor(
            red=self.red,
            green=self.green,
            blue=self.blue, 
            player=self.player,
            blending=self.blending,
            channel=self.channel,
            opacity=self.opacity,
            copy_id=self.copy_id,
            hsv=self.hsv,
            copy_opacity=self.copy_opacity,
            disable_legacy_hsv=self.disable_legacy_hsv,
        )
    
    def map_to_kit_color(self, kitcolor: KitColor) -> None:
        if kitcolor.channel != self.channel:
            raise ValueError("kitcolor's channel does not match color's channel.")
        
        kitcolor.red = self.red
        kitcolor.green = self.green
        kitcolor.blue = self.blue
        kitcolor.player = self.player
        kitcolor.blending = self.blending
        kitcolor.opacity = self.opacity
        kitcolor.copy_id = self.copy_id
        kitcolor.hsv = self.hsv
        kitcolor.copy_opacity = self.copy_opacity
        kitcolor.disable_legacy_hsv = self.disable_legacy_hsv
    
    def set_rgba(self, red: int, green: int, blue: int, alpha: float = 1.0):
        self.red = red
        self.green = green
        self.blue = blue
        self.opacity = alpha
    
    def get_rgba(self):
        return (self.red, self.green, self.blue, self.opacity)
        
    def set_hex(self, hex_string: str):
        hex_string = hex_string.lstrip("#")
        if len(hex_string) != 6:
            raise ValueError("Invalid hex string.")
        
        r = int(hex_string[0:2], 16)
        g = int(hex_string[2:4], 16)
        b = int(hex_string[4:6], 16)
        self.set_rgba(r, g, b)
    
    def get_hex(self):
        r, g, b, _ = self.get_rgba()
        return "#{:02X}{:02X}{:02X}".format(r, g, b)
