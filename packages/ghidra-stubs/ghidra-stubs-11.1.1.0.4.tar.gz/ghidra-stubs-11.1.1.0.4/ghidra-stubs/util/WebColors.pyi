from typing import overload
import java.awt
import java.lang


class WebColors(object):
    """
    Class for web color support. This class defines many of the colors used by html. This class
     includes methods for converting a color to a string (name or hex value) and for converting
     those strings back to a color.
 
     Usage Note: Java's HTML rendering engine supports colors in hex form ('#aabb11').  Also, the
     engine supports many web color names ('silver').  However, not all web color names defined in
     this file are supported.  Thus, when specifying HTML colors, do not rely on these web color
     names.
    """

    ALICE_BLUE: java.awt.Color
    ANTIQUE_WHITE: java.awt.Color
    AQUA: java.awt.Color
    AQUAMARINE: java.awt.Color
    AZURE: java.awt.Color
    BEIGE: java.awt.Color
    BISQUE: java.awt.Color
    BLACK: java.awt.Color
    BLANCHED_ALMOND: java.awt.Color
    BLUE: java.awt.Color
    BLUE_VIOLET: java.awt.Color
    BROWN: java.awt.Color
    BURLYWOOD: java.awt.Color
    CADET_BLUE: java.awt.Color
    CHARTREUSE: java.awt.Color
    CHOCOLATE: java.awt.Color
    CORAL: java.awt.Color
    CORNFLOWER_BLUE: java.awt.Color
    CORNSILK: java.awt.Color
    CRIMSON: java.awt.Color
    CYAN: java.awt.Color
    DARK_BLUE: java.awt.Color
    DARK_CYAN: java.awt.Color
    DARK_GOLDENROD: java.awt.Color
    DARK_GRAY: java.awt.Color
    DARK_GREEN: java.awt.Color
    DARK_KHAKI: java.awt.Color
    DARK_MAGENTA: java.awt.Color
    DARK_OLIVE_GREEN: java.awt.Color
    DARK_ORANGE: java.awt.Color
    DARK_ORCHID: java.awt.Color
    DARK_RED: java.awt.Color
    DARK_SALMON: java.awt.Color
    DARK_SEA_GREEN: java.awt.Color
    DARK_SLATE_BLUE: java.awt.Color
    DARK_SLATE_GRAY: java.awt.Color
    DARK_TURQUOSE: java.awt.Color
    DARK_VIOLET: java.awt.Color
    DEEP_PINK: java.awt.Color
    DEEP_SKY_BLUE: java.awt.Color
    DIM_GRAY: java.awt.Color
    DOGER_BLUE: java.awt.Color
    FIRE_BRICK: java.awt.Color
    FLORAL_WHITE: java.awt.Color
    FOREST_GREEN: java.awt.Color
    FUCHSIA: java.awt.Color
    GAINSBORO: java.awt.Color
    GHOST_WHITE: java.awt.Color
    GOLD: java.awt.Color
    GOLDEN_ROD: java.awt.Color
    GRAY: java.awt.Color
    GREEN: java.awt.Color
    GREEN_YELLOW: java.awt.Color
    HONEY_DEW: java.awt.Color
    HOT_PINK: java.awt.Color
    INDIAN_RED: java.awt.Color
    INDIGO: java.awt.Color
    IVORY: java.awt.Color
    KHAKE: java.awt.Color
    LAVENDER: java.awt.Color
    LAVENDER_BLUSH: java.awt.Color
    LAWN_GREEN: java.awt.Color
    LEMON_CHIFFON: java.awt.Color
    LIGHT_BLUE: java.awt.Color
    LIGHT_CORAL: java.awt.Color
    LIGHT_CYAN: java.awt.Color
    LIGHT_GOLDENROD: java.awt.Color
    LIGHT_GRAY: java.awt.Color
    LIGHT_GREEN: java.awt.Color
    LIGHT_PINK: java.awt.Color
    LIGHT_SALMON: java.awt.Color
    LIGHT_SEA_GREEN: java.awt.Color
    LIGHT_SKY_BLUE: java.awt.Color
    LIGHT_SLATE_GRAY: java.awt.Color
    LIGHT_STEEL_BLUE: java.awt.Color
    LIGHT_YELLOW: java.awt.Color
    LIME: java.awt.Color
    LIME_GREEN: java.awt.Color
    LINEN: java.awt.Color
    MAGENTA: java.awt.Color
    MAROON: java.awt.Color
    MEDIUM_BLUE: java.awt.Color
    MEDIUM_ORCHID: java.awt.Color
    MEDIUM_PURPLE: java.awt.Color
    MEDIUM_SEA_GREEN: java.awt.Color
    MEDIUM_SLATE_BLUE: java.awt.Color
    MEDIUM_SPRING_GREEN: java.awt.Color
    MEDIUM_TURQOISE: java.awt.Color
    MEDIUM_VIOLET_RED: java.awt.Color
    MEDUM_AQUA_MARINE: java.awt.Color
    MIDNIGHT_BLUE: java.awt.Color
    MINT_CREAM: java.awt.Color
    MISTY_ROSE: java.awt.Color
    MOCCASIN: java.awt.Color
    NAVAJO_WHITE: java.awt.Color
    NAVY: java.awt.Color
    OLDLACE: java.awt.Color
    OLIVE: java.awt.Color
    OLIVE_DRAB: java.awt.Color
    ORANGE: java.awt.Color
    ORANGE_RED: java.awt.Color
    ORCHID: java.awt.Color
    PALE_GOLDENROD: java.awt.Color
    PALE_GREEN: java.awt.Color
    PALE_TURQUOISE: java.awt.Color
    PALE_VIOLET_RED: java.awt.Color
    PAPAYA_WHIP: java.awt.Color
    PEACH_PUFF: java.awt.Color
    PERU: java.awt.Color
    PINK: java.awt.Color
    PLUM: java.awt.Color
    POWDER_BLUE: java.awt.Color
    PURPLE: java.awt.Color
    REBECCA_PURPLE: java.awt.Color
    RED: java.awt.Color
    ROSY_BROWN: java.awt.Color
    ROYAL_BLUE: java.awt.Color
    SADDLE_BROWN: java.awt.Color
    SALMON: java.awt.Color
    SANDY_BROWN: java.awt.Color
    SEASHELL: java.awt.Color
    SEA_GREEN: java.awt.Color
    SIENNA: java.awt.Color
    SILVER: java.awt.Color
    SLATE_BLUE: java.awt.Color
    SLATE_GRAY: java.awt.Color
    SNOW: java.awt.Color
    SPRING_GREEN: java.awt.Color
    STEEL_BLUE: java.awt.Color
    SYY_BLUE: java.awt.Color
    TAN: java.awt.Color
    TEAL: java.awt.Color
    THISTLE: java.awt.Color
    TOMATO: java.awt.Color
    TURQUOISE: java.awt.Color
    VIOLET: java.awt.Color
    WHEAT: java.awt.Color
    WHITE: java.awt.Color
    WHITE_SMOKE: java.awt.Color
    YELLOW: java.awt.Color
    YELLOW_GREEN: java.awt.Color







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getColor(colorString: unicode) -> java.awt.Color:
        """
        Attempts to convert the given string into a color in a most flexible manner. It first checks
         if the given string matches the name of a known web color as defined above. If so it
         returns that color. Otherwise it tries to parse the string in any one of the following
         formats:
         <pre>
         #rrggbb
         #rrggbbaa
         0xrrggbb
         0xrrggbbaa
         rgb(red, green, blue)
         rgba(red, green, alpha)
         </pre>
         In the hex digit formats, the hex digits "rr", "gg", "bb", "aa" represent the values for red,
         green, blue, and alpha, respectively. In the "rgb" and "rgba" formats the red, green, and
         blue values are all integers between 0-255, while the alpha value is a float value from 0.0 to
         1.0.
         <BR><BR>
        @param colorString the color name
        @return a color for the given string or null
        """
        ...

    @staticmethod
    def getColorOrDefault(value: unicode, defaultColor: java.awt.Color) -> java.awt.Color:
        """
        Tries to find a color for the given String value. The String value can either be
         a hex string (see {@link Color#decode(String)}) or a web color name as defined
         above
        @param value the string value to interpret as a color
        @param defaultColor a default color to return if the string can't be converted to a color
        @return a color for the given string value or the default color if the string can't be translated
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def toColorName(color: java.awt.Color) -> unicode: ...

    @staticmethod
    def toHexString(color: java.awt.Color) -> unicode:
        """
        Returns the hex value string for the given color
        @param color the color
        @return the string
        """
        ...

    @staticmethod
    def toRgbString(color: java.awt.Color) -> unicode:
        """
        Returns the rgb value string for the given color
        @param color the color
        @return the string
        """
        ...

    @overload
    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def toString(color: java.awt.Color) -> unicode:
        """
        Converts a color to a string value. If there is a defined color for the given color value,
         the color name will be returned. Otherwise, it will return a hex string for the color as
         follows. If the color has an non-opaque alpha value, it will be of the form #rrggbb. If
         it has an alpha value,then the format will be #rrggbbaa.
        @param color the color to convert to a string.
        @return the string representation for the given color.
        """
        ...

    @overload
    @staticmethod
    def toString(color: java.awt.Color, useNameIfPossible: bool) -> unicode:
        """
        Converts a color to a string value.  If the color is a WebColor and the useNameIfPossible
         is true, the name of the color will be returned. OOtherwise, it will return a hex string for the color as
         follows. If the color has an non-opaque alpha value, it will be of the form #rrggbb. If
         it has an alpha value ,then the format will be #rrggbbaa.
        @param color the color to convert to a string.
        @param useNameIfPossible if true, the name of the color will be returned if the color is
         a WebColor
        @return the string representation for the given color.
        """
        ...

    @staticmethod
    def toWebColorName(color: java.awt.Color) -> unicode:
        """
        Returns the WebColor name for the given color. Returns null if the color is not a WebColor
        @param color the color to lookup a WebColor name.
        @return the WebColor name for the given color. Returns null if the color is not a WebColor
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

