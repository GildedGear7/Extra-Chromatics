class ECMath():

    def avg(*argv):
        totalSum = 0
        for arg in argv:
            totalSum += arg

        return totalSum / len(argv)

    def lerp(a: float, b: float, shift: float):
        return (1 - shift) * a + shift * b
    
    def lpos(a: float, b: float, point: float):
        return (point - min(a, b)) / (max(a , b) - min(a, b))

    def random(minVal, maxVal, seed):
        seed = ((seed * 5656678211) % 44571) ^ 3
        return minVal + (seed % (maxVal - minVal + 1))


def get_RGB(inputVal, inputType: str):
    """
    Value ranges are : \n
    red   = <0 , 255> \n
    green = <0 , 255> \n
    blue  = <0 , 255> \n
    """
    # detect input color type

    # HEX value
    if inputType == "HEX":
        inputVal = inputVal.strip("#")

        rgb = []
        for i in (0, 2, 4):
            decimal = int(inputVal[i:i+2], 16)
            rgb.append(decimal)
        return tuple(rgb)

    # RGB value
    elif inputType == "RGB":
        return inputVal

    #HSV value
    elif inputType == "HSV":
        hue        = inputVal[0] * 6
        saturation = inputVal[1] / 255
        value      = inputVal[2] / 255


        sliceIndex = int(hue)
        sliceIndex = sliceIndex % 6
        hueInSlice = hue - sliceIndex

        p = value * (1 - saturation)
        q = value * (1 - saturation * hueInSlice)
        t = value * (1 - saturation * (1 - hueInSlice))

        p *= 255
        q *= 255
        t *= 255
        value *=255 

        match sliceIndex:
            case 0:
                return (value, t, p)
            case 1:
                return (q, value, p)
            case 2:
                return (p, value, t)
            case 3:
                return (p, q, value)
            case 4:
                return (t, p, value)
            case 5:
                return (value, p, q)

    #invalid value
    else:
        print("ERROR get_RGB() Invalid input type : " + inputType)
        return inputVal

def get_HSV(inputVal, inputType: str):
    """
    Value ranges are : \n
    hue        = <0 , 1> \n
    saturation = <0 , 255> \n
    value      = <0 , 255> \n
    """
    if inputType == "HSV":
        return inputVal
    
    rgb = get_RGB(inputVal, inputType)


    maxOfRgb = max(rgb[0], rgb[1], rgb[2])
    minOfRgb = min(rgb[0], rgb[1], rgb[2])

    rangeOfRgb = maxOfRgb - minOfRgb
    if rangeOfRgb == 0:
        correctedRangeOfRgb = 1
    else:
        correctedRangeOfRgb = 255 / rangeOfRgb
    # calculate value of this color
    value = maxOfRgb

    # calculate saturation of this color
    if maxOfRgb == 0:
        corrector = 255 / maxOfRgb
    else:
        corrector = 255 / maxOfRgb
    saturation = (maxOfRgb - minOfRgb) * corrector

    # calculate hue of this color
    if rgb[0] == maxOfRgb:
        hue = (rgb[1] - rgb[2]) * correctedRangeOfRgb
        hue = (hue / 255)

        if hue < 0:
            hue += 6
    elif rgb[1] == maxOfRgb:
        hue = (rgb[2] - rgb[0]) * correctedRangeOfRgb
        hue = (hue / 255) + 2
    else:
        hue = (rgb[0] - rgb[1]) * correctedRangeOfRgb
        hue = (hue / 255) + 4

    hue = (hue / 6) % 1
    
    return (hue, saturation, value)

def get_HEX(inputVal, inputType: str):
    """
    Value ranges are : \n
    red   = <00 , FF> \n
    green = <00 , FF> \n
    blue  = <00 , FF> \n
    """
    if inputType == "HEX":
        return inputVal

    rgb = get_RGB(inputVal, inputType)
    return '#{:02x}{:02x}{:02x}'.format(
        round(rgb[0]), round(rgb[1]), round(rgb[2])
        )

def get_universal(outputType: str, inputVal, inputType: str):
    if outputType == inputType:
        return inputVal
    
    match outputType:
        case "RGB":
            return get_RGB(inputVal, inputType)
        case "HEX":
            return get_HEX(inputVal, inputType)
        case "HSV":
            return get_HSV(inputVal, inputType)
        case _:
            print("ERROR get_universal() Invalid output type : " + outputType)
            return inputVal


def get_luminance(inputColor, inputType: str):
    inputColor = get_RGB(inputColor, inputType)
    #Calculate relative luminance (Y) for a given RGB color.
    inputColor = [x / 255.0 for x in inputColor]  # Normalize RGB values to the range [0, 1]
    r = inputColor[0]
    g = inputColor[1]
    b = inputColor[2]

    r = r if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def get_contrast(color1, color2, inputType: str):
    #"""Calculate the contrast ratio between two colors."""
    luminance1 = get_luminance(color1, inputType)
    luminance2 = get_luminance(color2, inputType)
    brighter = max(luminance1, luminance2)
    darker = min(luminance1, luminance2)
    contrast = (brighter + 0.05) / (darker + 0.05)
    return contrast

def get_realtimecolors_site_link(color_set: dict, darkMode : bool) -> str:
    output = "https://realtimecolors.com/?colors="
    if darkMode:
        output += color_set["textLight"].strip("#") + "-"
    else :
        output += color_set["textDark"].strip("#") + "-"
    output += color_set["background"].strip("#") + "-"
    output += color_set["primary"].strip("#") + "-"
    output += color_set["secondary"].strip("#") + "-"
    output += color_set["accent"].strip("#")
    return output

def random_true_color(outputType: str, seed: int):
    """Returns truly random color, without taking into consideration its visibility."""
    return get_universal(outputType,
        (
            ECMath.random(0, 255, seed + 0),
            ECMath.random(0, 255, seed + 1),
            ECMath.random(0, 255, seed + 2)
        ),"RGB")

def random_soft_color(outputType:str, seed: int):
    """Returns somewhat random color, taking into consideration its visibility."""
    return get_universal(outputType,
        (
            ECMath.random(0, 360, seed + 0) / 360,
            ECMath.random(40, 255, seed + 1),
            ECMath.random(40, 255, seed + 2)
        ), "HSV")


def hue_shift(inputColor, inputType: str, shift: float):
    inputColor = get_HSV(inputColor, inputType)

    return get_universal(
        inputType,
        ((inputColor[0] + shift) % 1, inputColor[1], inputColor[2]),
        "HSV"
        )


def gen_light_color_set_analogous(color, inColorType: str, strength: float):
    """returns a dictionary containing a whole color scheme \n
    {\n
    "primary", "secondary", "accent", "background", "textLight","textDark"\n
    } keys."""        

    color = get_HSV(color, inColorType)

    textLightColor = ((color[0] + strength) % 1, 70, 255)
    textDarkColor = ((color[0] + strength) % 1, 70, 50)

    primaryColor = (
        color[0],
        ECMath.lerp(color[1], 128, 0.5),
        ECMath.lerp(color[2], 255, 0.8)
        )

    while get_contrast(primaryColor, textDarkColor, "HSV") < 7:
        #print("correction from : " + str(get_contrast(primaryColor, textDarkColor, "HSV")))
        primaryColor = (
            primaryColor[0],
            ECMath.lerp(primaryColor[1], 0, 0.2),
            ECMath.lerp(primaryColor[2], 255, 0.2)
            )
        
    secondaryColor = (
        (color[0] + strength * 0.5) % 1,
        ECMath.lerp(color[1], 20, 0.8),
        ECMath.lerp(color[2], 255, 0.9)
        )
    
    accentColor = (
        (color[0] + strength) % 1,
        ECMath.lerp(color[1], 255, 0.8),
        ECMath.lerp(color[2], 0, 0.3)
        )
    
    if get_contrast(accentColor, textLightColor, "HSV") < 4.5:
        accentColor = (
            accentColor[0],
            accentColor[1],
            ECMath.lerp(accentColor[2], 0, 0.5)
                        )
    
    backgroundColor = (
        color[0],
        ECMath.lerp(color[1], 0, 0.9),
        ECMath.lerp(color[2], 255, 0.95)
        )
    

    primaryColor = get_universal(inColorType, primaryColor, "HSV")
    secondaryColor = get_universal(inColorType, secondaryColor, "HSV")
    accentColor = get_universal(inColorType, accentColor, "HSV")
    backgroundColor = get_universal(inColorType, backgroundColor, "HSV")
    textLightColor = get_universal(inColorType, textLightColor, "HSV")
    textDarkColor = get_universal(inColorType, textDarkColor, "HSV")

    return{
        "primary" : primaryColor,
        "secondary" : secondaryColor,
        "accent" : accentColor,
        "background" : backgroundColor,
        "textLight" : textLightColor,
        "textDark" : textDarkColor
    }

def gen_light_color_set_complementary(color, inColorType: str):
    """returns a dictionary containing a whole color scheme \n
    {\n
    "primary", "secondary", "accent", "background", "textLight","textDark"\n
    } keys."""        

    color = get_HSV(color, inColorType)

    textLightColor = ((color[0] + 0.5) % 1, 70, 255)
    textDarkColor = ((color[0] + 0.5) % 1, 70, 50)

    primaryColor = (
        color[0],
        ECMath.lerp(color[1], 128, 0.5),
        ECMath.lerp(color[2], 255, 0.8)
        )

    while get_contrast(primaryColor, textDarkColor, "HSV") < 7:
        #print("correction from : " + str(get_contrast(primaryColor, textDarkColor, "HSV")))
        primaryColor = (
            primaryColor[0],
            ECMath.lerp(primaryColor[1], 0, 0.2),
            ECMath.lerp(primaryColor[2], 255, 0.2)
            )
        
    secondaryColor = (
        (color[0] + 0.05) % 1,
        ECMath.lerp(color[1], 20, 0.8),
        ECMath.lerp(color[2], 255, 0.9)
        )
    
    accentColor = (
        (color[0] + 0.5) % 1,
        ECMath.lerp(color[1], 255, 0.8),
        ECMath.lerp(color[2], 0, 0.3)
        )
    
    if get_contrast(accentColor, textLightColor, "HSV") < 4.5:
        accentColor = (
            accentColor[0],
            accentColor[1],
            ECMath.lerp(accentColor[2], 0, 0.5)
                        )
    
    backgroundColor = (
        color[0],
        ECMath.lerp(color[1], 0, 0.9),
        ECMath.lerp(color[2], 255, 0.95)
        )
    

    primaryColor = get_universal(inColorType, primaryColor, "HSV")
    secondaryColor = get_universal(inColorType, secondaryColor, "HSV")
    accentColor = get_universal(inColorType, accentColor, "HSV")
    backgroundColor = get_universal(inColorType, backgroundColor, "HSV")
    textLightColor = get_universal(inColorType, textLightColor, "HSV")
    textDarkColor = get_universal(inColorType, textDarkColor, "HSV")

    return{
        "primary" : primaryColor,
        "secondary" : secondaryColor,
        "accent" : accentColor,
        "background" : backgroundColor,
        "textLight" : textLightColor,
        "textDark" : textDarkColor
    }

def gen_dark_color_set_analogous(color, inColorType: str, strength: float):
    """returns a dictionary containing a whole color scheme \n
    {\n
    "primary", "secondary", "accent", "background", "textLight","textDark"\n
    } keys."""        

    color = get_HSV(color, inColorType)

    textLightColor = ((color[0] + strength) % 1, 20, 255)
    textDarkColor = ((color[0] + strength) % 1, 70, 50)

    primaryColor = (
        color[0],
        ECMath.lerp(color[1], 255, 0.5),
        ECMath.lerp(color[2], 255, 0.8)
        )

    while get_contrast(primaryColor, textDarkColor, "HSV") < 7:
        print("primary correction from : " + str(get_contrast(primaryColor, textDarkColor, "HSV")))
        primaryColor = (
            primaryColor[0],
            ECMath.lerp(primaryColor[1], 0, 0.2),
            ECMath.lerp(primaryColor[2], 255, 0.2)
            )
        
    secondaryColor = (
        (color[0] + strength * 0.5) % 1,
        ECMath.lerp(color[1], 255, 0.8),
        ECMath.lerp(color[2], 50, 0.9)
        )

    backgroundColor = (
        color[0],
        ECMath.lerp(color[1], 128, 0.3),
        ECMath.lerp(color[2], 0, 0.95)
        )

    accentColor = (
        (color[0] + strength) % 1,
        ECMath.lerp(color[1], 255, 0.8),
        ECMath.lerp(color[2], 255, 0.3)
        )
    
    while get_contrast(accentColor, backgroundColor, "HSV") < 4.5:
        print("accent correction from : " + str(get_contrast(accentColor, backgroundColor, "HSV")))
        accentColor = (
            accentColor[0],
            ECMath.lerp(accentColor[1], 0, 0.3),
            ECMath.lerp(accentColor[2], 255, 0.5)
                        )
    

    

    primaryColor = get_universal(inColorType, primaryColor, "HSV")
    secondaryColor = get_universal(inColorType, secondaryColor, "HSV")
    accentColor = get_universal(inColorType, accentColor, "HSV")
    backgroundColor = get_universal(inColorType, backgroundColor, "HSV")
    textLightColor = get_universal(inColorType, textLightColor, "HSV")
    textDarkColor = get_universal(inColorType, textDarkColor, "HSV")

    return{
        "primary" : primaryColor,
        "secondary" : secondaryColor,
        "accent" : accentColor,
        "background" : backgroundColor,
        "textLight" : textLightColor,
        "textDark" : textDarkColor
    }