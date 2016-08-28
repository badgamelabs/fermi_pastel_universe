#!/usr/bin/python
from PIL import Image, ImageDraw, ImageOps
from Utils.ImageAdjuster import ImageAdjuster

# image adjustment utility
imageAdjuster = ImageAdjuster()


"""
Draws Stars onto a scene
"""
class OpenSpace:

    def drawBackground(self, scene, body, canvas):
        draw = ImageDraw.Draw(scene)
        bgColor = imageAdjuster.adjustHSV(body.baseColor, [.1, 0, 0])
        draw.rectangle(((0, 0), canvas), fill=bgColor)

        # create background gradient
        sceneData = scene.load()
        spaceRangeRate = ((((body.seed.total%4)+1)/10.0)+.1)
        for x in range(0, canvas[0]):
            for y in range(0, canvas[1]):
                sceneData[x,y] = imageAdjuster.adjustHSV(sceneData[x,y],
                    [
                        ((y+(x*body.signMod))/200.0)*spaceRangeRate,
                        0,
                        0])

    def drawStars(self, scene, body, canvas):
        values = body.seed.values

        starField = Image.new("RGBA", canvas, (0, 0, 0, 0))
        draw = ImageDraw.Draw(starField)

        heart = Image.open("art/heart_7_7.png").convert('RGBA')
        burst = Image.open("art/star_burst_7_7.png").convert('RGBA')

        for i in range(0,((body.seed.total+1)*333)%60):
            xSeed = values[i%16]
            ySeed = values[15-(i%16)]

            x = ((((xSeed**xSeed) * (ySeed+1))*3) % (canvas[0]+5)) - 4
            y = ((((ySeed**ySeed) * (xSeed+1))*3) % (canvas[1]+5)) - 4

            heartMod = values[values[11]] + 15
            burstMod = values[values[3]] + 14

            if x%heartMod == y%heartMod:
                starField.paste(heart, (x,y), heart)
            elif x%burstMod == y%burstMod:
                starField.paste(burst, (x,y), burst)
            else:
                size = (((x+y)%2)+1)*2
                draw.rectangle((x,y,x,y+size), fill=(255,255,255,255/(8-size)))
                draw.rectangle((x-(size/2),y+(size/2),x+(size/2),y+(size/2)), fill=(255,255,255,255/(8-size)))

        scene.paste(starField, (0,0), starField)
        return scene
