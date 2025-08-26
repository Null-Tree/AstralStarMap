
#skybox export
#########################################################################################

#CONFIG



# sizepower=14 #size power for dimensions of expor timage #normal 14 for 16k

# 14 for 16k 

# sizepower=15
# maxradius=  100 #32*2



sizepower=15
maxradius=  80 #32*2


#width power of 2, height half
width=int(2**sizepower)
height=int(width/2)




# 13 for 8k

# sizepower=13
# maxradius= 18

#stars
#min radius of star
minradius=0



#color min intensity of star rgb
colormin=0


#app mag req
appmagreq = 100
#greyshade
#makes color into shade of grey x

draw_cons=True

#color border for ocnstalations
consborderRGB = (80,80,80) 
#line width for constalations
conslinewidth=4

#txtcondif
txtfill = (194, 215, 234)
txtfontsize=32
consLabel=True
antialius=True

#bg
bgcolor=(0,0,0)

star_graphic_original = Image.open(r"graphics\stargraphic.png")


# color system
cs = cs_hdtv

# disable for better stars
basic_render=True

# /"celestial" or "galactic"
cord_mode="galactic"

###############################################################
###################################
