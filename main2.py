import random
import tkinter as tk
from tkinter import filedialog as tkfd, filedialog
from PIL import Image, ImageTk, ImageOps


def displayImage(img, image_label):
    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo)
    image_label.photo = photo
    image_label.place(x=0, y=0, width=1000, height=1000)


class App:
    def __init__(self, imagePath):
        self.root = tk.Tk()
        self.root.geometry("1800x1000")
        self.root.maxsize(1800, 1000)
        self.root.minsize(1800, 1000)
        self.root.title('Image Transformer')

        self.info_text = None
        self.img = Image.open(imagePath)
        self.original_img = self.img.copy()
        self.image_label = tk.Label(self.root)

        displayImage(self.img, self.image_label)
        self.displayButtonFrame()
        self.displayTextFrame()

        self.root.mainloop()

    def displayButtonFrame(self):
        buttonFrame = tk.Frame(self.root, bg='darkgrey')
        buttonFrame.place(x=1400, y=0, width=400, height=1000)

        clockwiseBtn = tk.Button(buttonFrame, text='Rotate Clockwise', font=('Arial', 20), command=self.rotateClockwise)
        clockwiseBtn.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

        counterClockBtn = tk.Button(buttonFrame, text='Rotate Counter-Clockwise', font=('Arial', 20), command=self.rotateCounterClockwise)
        counterClockBtn.grid(row=1, column=0, sticky='ew', padx=10, pady=10)

        reflectXBtn = tk.Button(buttonFrame, text='Reflect X-axis', font=('Arial', 20), command=self.reflectX)
        reflectXBtn.grid(row=2, column=0, sticky='ew', padx=10, pady=10)

        reflectYBtn = tk.Button(buttonFrame, text='Reflect Y-axis', font=('Arial', 20), command=self.reflectY)
        reflectYBtn.grid(row=3, column=0, sticky='ew', padx=10, pady=10)

        reflectXYBtn = tk.Button(buttonFrame, text='Reflect Diagonal', font=('Arial', 20), command=self.reflectDiagonal)
        reflectXYBtn.grid(row=4, column=0, sticky='ew', padx=10, pady=10)

        convertToGreyscaleBtn = tk.Button(buttonFrame, text='Greyscale', font=('Arial', 20), command=self.convertToGreyscale)
        convertToGreyscaleBtn.grid(row=5, column=0, sticky='ew', padx=10, pady=10)

        restoreToOriginalBtn = tk.Button(buttonFrame, text='Reset Image', font=('Arial', 20), command=self.restoreToOriginal)
        restoreToOriginalBtn.grid(row=6, column=0, sticky='ew', padx=10, pady=100)

        downloadBtn = tk.Button(buttonFrame, text='Download Image', font=('Arial', 20), command=self.downloadImage)
        downloadBtn.grid(row=7, column=0, sticky='ew', padx=10, pady=10)

    def displayTextFrame(self):
        textFrame = tk.Frame(self.root)
        textFrame.place(x=1000, y=0, width=400, height=1000)

        self.info_text = tk.Text(textFrame, height=15, bg='light grey')
        self.info_text.pack(fill='both', expand=True)
        self.info_text.insert(tk.END, "Operations Explained Here.\n")

    def rotateClockwise(self):
        self.img = self.img.rotate(-90, expand=True)
        displayImage(self.img, self.image_label)
        self.updateTextRotations(-90)

    def rotateCounterClockwise(self):
        self.img = self.img.rotate(90, expand=True)
        displayImage(self.img, self.image_label)
        self.updateTextRotations(90)

    def reflectX(self):
        self.img = ImageOps.flip(self.img)
        displayImage(self.img, self.image_label)
        self.updateTextReflections(0)

    def reflectY(self):
        self.img = ImageOps.mirror(self.img)
        displayImage(self.img, self.image_label)
        self.updateTextReflections(1)

    def reflectDiagonal(self):
        self.img = self.img.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)
        displayImage(self.img, self.image_label)
        self.updateTextReflections(2)

    def convertToGreyscale(self):
        width, height = self.img.size
        randX = random.randint(0, width - 1)
        randY = random.randint(0, height - 1)
        rgbPixel = self.img.getpixel((randX, randY))

        self.img = self.img.convert("L").convert("RGB")
        displayImage(self.img, self.image_label)

        self.updateInfoTextColor(rgbPixel, (randX, randY))

    def restoreToOriginal(self):
        self.img = self.original_img.copy()
        displayImage(self.img, self.image_label)
        self.info_text.delete('1.0', tk.END)
        self.info_text.insert(tk.END, "Image has been reset to its original state.\n")

    def downloadImage(self):
        filePath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if filePath:
            self.img.save(filePath)

    def updateTextRotations(self, angle):
        width, height = self.img.size
        randX = random.randint(0, width - 1)
        randY = random.randint(0, height - 1)

        if angle == -90:
            rotationMatrix = "[0, 1]\n[-1, 0]"
            operationInfo = "90 degrees CW rotation"
            newX = randY
            newY = -randX
        elif angle == 90:
            rotationMatrix = "[0, -1]\n[1, 0]"
            operationInfo = "90 degrees CCW rotation"
            newX = -randY
            newY = randX

        text = f"Transformation: {operationInfo}\n\n" \
                              f"Random Pixel Chosen: {randX, randY}\n\n" \
                              f"Transformation Matrix:\n{rotationMatrix}\n\n" \
                              f"× Pixel Vector:\n[{randX},\n {randY}]\n\n" \
                              f"= Output Vector:\n[{newX},\n {newY}]"

        self.info_text.delete('1.0', tk.END)
        self.info_text.insert(tk.END, text)

    def updateTextReflections(self, refIndex):
        width, height = self.img.size
        randX = random.randint(0, width - 1)
        randY = random.randint(0, height - 1)

        if refIndex == 0:
            rotationMatrix = "[-1, 0]\n[0, 1]"
            operationInfo = "Reflection over the Y-axis"
            newX = width - randX - 1
            newY = randY
        elif refIndex == 1:
            rotationMatrix = "[1, 0]\n[0, -1]"
            operationInfo = "Reflection over the X-axis"
            newX = randX
            newY = height - randY - 1
        elif refIndex == 2:
            rotationMatrix = "[0, 1]\n[1, 0]"
            operationInfo = "Reflection over the diagonal"
            newX = randY
            newY = randX

        text = f"Transformation: {operationInfo}\n\n" \
                              f"Random Pixel Chosen: ({randX}, {randY})\n\n" \
                              f"Transformation Matrix:\n{rotationMatrix}\n\n" \
                              f"× Pixel Vector:\n[{randX},\n {randY}]\n\n" \
                              f"= Output Vector:\n[{newX},\n {newY}]"

        self.info_text.delete('1.0', tk.END)
        self.info_text.insert(tk.END, text)

    def updateInfoTextColor(self, rgbPixel, pixelPos):
        r, g, b = rgbPixel
        greyscaleVal = int(0.2989 * r + 0.5870 * g + 0.1140 * b)

        operationInfo = "Conversion to Grayscale"
        pixelInfo = f"Random Pixel Location: {pixelPos}"
        rgbVector = f"RGB Vector of Random Pixel: [{r}, {g}, {b}]"
        convMatrix = "Conversion Matrix: [0.2989, 0.5870, 0.1140]"
        greyscaleVal = f"Grayscale Value of Random Pixel: [{greyscaleVal}]"

        text = f"Transformation: {operationInfo}\n\n" \
                              f"{pixelInfo}\n\n" \
                              f"{rgbVector}\n\n" \
                              f"{convMatrix}\n\n" \
                              f"Resulting {greyscaleVal}"

        self.info_text.delete('1.0', tk.END)
        self.info_text.insert(tk.END, text)


if __name__ == '__main__':
    chosenImg = tkfd.askopenfilename()
    if chosenImg:
        imgStats = Image.open(chosenImg).size
        if (imgStats[0] / imgStats[1] == 1) and imgStats[0] <= 1080:
            app = App(chosenImg)
        else:
            print("Image Resolution must be square and less than 1080 pixels in width\nExample image can be found here: https://croppola.com/croppola/example-bird2/image.jpg?algorithm=croppola&aspectRatio=1&width=500&thumbnailMaximumWidth=150")
            exit(-1)
    else:
        print("Please Select an Image")
        exit(-1)
