from PIL import Image

def silhouette(iname, oname):
	i = Image.open(iname)

	pix = i.load()
	for y in range(i.size[1]):
		for x in range(i.size[0]):
			a = pix[x, y][3]		
			pix[x, y] = (255,255,255,255) if a == 255 else (0, 0, 0, 0)

	i.save(oname)

silhouette("images/bab0.png", "images/babs.png")
silhouette("images/bug10.png", "images/bugs0.png")
silhouette("images/bug11.png", "images/bugs1.png")
silhouette("images/bug12.png", "images/bugs2.png")
silhouette("images/bug13.png", "images/bugs3.png")

i = Image.new("RGBA", (2048, 2048), (0,0,0,128))
i.save("images/dark.png")
