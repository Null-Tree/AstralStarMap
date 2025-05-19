from SpecRend import SpecRend
import matplotlib.pyplot as plt
import numpy as np

def color_conversion(icol, DeColour = True): 
    # Assuming icol is a list of temperatures and cc is a list of colors to be populated
    cc = [None] * len(icol)

    for i in range(len(icol)): 
        teff = icol[i]

        # Convert spectrum to XYZ coordinates
        x, y, z = SpecRend.spectrum_to_xyz(SpecRend.bb_spectrum, teff)

        # Convert XYZ to RGB
        r, g, b = SpecRend.xyz_to_rgb(SpecRend.Rec709system, x, y, z)

        # Create color (assuming alpha is not needed, or you can add a 4th component)
        cc[i] = (r, g, b)  # Or use a Color class if you have one defined

        if DeColour:
            # Manual implementation of Color.Lerp (linear interpolation)
            def lerp_color(a, b, t):
                return (
                    a[0] + (b[0] - a[0]) * t,
                    a[1] + (b[1] - a[1]) * t,
                    a[2] + (b[2] - a[2]) * t
                )
            
            # Lerp between calculated color and white (50% mix)
            cc[i] = lerp_color(cc[i], (1.0, 1.0, 1.0), 0.5)
        
        
    def normalize_rgb(color):
        return tuple(max(0, min(1, c)) for c in color)
    cc = [normalize_rgb(c) for c in cc]
    return cc

def display_colors(colors):
    n = len(colors)  # Number of colors
    fig, ax = plt.subplots(1, n, figsize=(n, 1))  # Create subplots
    
    if n == 1:
        ax = [ax]  # Ensure ax is iterable for a single color
    
    for i in range(n):
        img = np.zeros((100, 100, 3))  # Create a 100x100 pixel image
        img[:, :] = colors[i]  # Fill with the color
        ax[i].imshow(img)
        ax[i].axis("off")  # Hide axes

    plt.show()

if __name__ == '__main__': 
    # Example values
    icol = [2000,6000,20000]
    DeColour = False
    cc = color_conversion(icol=icol, 
                          DeColour=DeColour)
    print(cc)

    color_list = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (0, 1, 1)]
    display_colors(cc)