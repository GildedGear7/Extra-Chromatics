import ExtraChromatics as EC
from ExtraChromatics import ECMath

def test_color(color):
    if EC.get_HEX(color, "HEX") == EC.get_HEX(EC.get_HSV(color, "HEX"), "HSV"):
        print("===>>>> SUCCESS <<<<===")
    else:
        print("## FAIL ##")
        
    print(EC.get_HEX(color, "HEX"))
    print(EC.get_HEX(EC.get_HSV(color, "HEX"), "HSV"))

#print("EC MATH TEST")
#print(ECMath.lpos(5, 10, 7.5))
seed = 0
strength = -0.3

for seed in range(1):
    randomColor = EC.random_soft_color("HEX", seed)
    randomColor = "#FFEA00"
    print(randomColor)
    colors = EC.gui_theme_light_var1_analogous(randomColor, "HEX", strength)
    print(EC.get_realtimecolors_site_link(colors))

    colors = EC.gui_theme_light_var1_complementary(randomColor, "HEX")
    print(EC.get_realtimecolors_site_link(colors))

    colors = EC.gui_theme_light_var1_monochromatic(randomColor, "HEX")
    print(EC.get_realtimecolors_site_link(colors))


    colors = EC.gui_theme_dark_var1_analogous(randomColor, "HEX", strength)
    print(EC.get_realtimecolors_site_link(colors))

    colors = EC.gui_theme_dark_var1_complementary(randomColor, "HEX")
    print(EC.get_realtimecolors_site_link(colors))

    colors = EC.gui_theme_dark_var1_monochromatic(randomColor, "HEX")
    print(EC.get_realtimecolors_site_link(colors))

    #print(ECMath.random(0, 360, seed))

"""
    var1 = EC.get_HSV(EC.random_true_color("HEX", seed), "HEX")
    print(var1)
    print(EC.get_RGB(var1, "HSV"))
    print(EC.get_HEX(var1, "HSV"))
    print()


colors = EC.gen_light_color_set_analogous(EC.random_soft_color("HEX", seed), "HEX", 0.3)
print(EC.random_soft_color("HEX", seed))
print(EC.get_realtimecolors_site_link(colors))



"""