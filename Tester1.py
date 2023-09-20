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

for seed in range(100):
    colors = EC.gen_dark_color_set_monochromatic(EC.random_soft_color("HEX", seed), "HEX")

    """print(colors["textLight"])
    print(colors["textDark"])
    print(colors["primary"])
    print(colors["secondary"])
    print(colors["accent"])
    print(colors["background"])
    print()"""

    print(EC.random_soft_color("HEX", seed))
    print(EC.get_realtimecolors_site_link(colors, True))

    #print(ECMath.random(0, 360, seed))