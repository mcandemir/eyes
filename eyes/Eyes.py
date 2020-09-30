import cv2
import numpy as np


class Eyes:
    def __init__(self, *images):
        """
        --> creates 2 dicts with given argument, one to store
        original images, the other is for manipulating

        --> when doing operations on specified images,
        image names always comes first in arguments
            ------------------------
            eyes = Eyes(img1, img2)
            eyes.greyscale(0)
            ------------------------
            eyes = Eyes(('car', img1), ('tree', img2))
            eyes.greyscale('car')
            ------------------------
            eyes = Eyes(('car', img1), ('tree', img2))
            eyes.gaussian_blur('car', 'tree', ksize=(5,5), sigma=0)
            ------------------------

        --> if the arguments only includes images, then they
        will be stored as {0: image1, 1: image2..}

        --> if the arguments are a tuple ('image name', image1),
        they will be stored  as {'image name': image1..}

        :param images: images that we want to work on
        """
        self.IMAGES = {}
        if type(images[0]) is not tuple:
            images = enumerate(images)
        for i, img in images:
            self.IMAGES[i] = img
        self.images = self.IMAGES.copy()

    def greyscale(self, *args):
        """
        reduce the image dimension to 2-D
        """
        if not args:
            args = self.images.keys()
        for i in args:
            self.images[i] = cv2.cvtColor(self.images[i], cv2.COLOR_BGR2GRAY)

    def gaussian_blur(self, *args, ksize=(5, 5), sigma=0):
        """
        apply gaussian blur
        """
        if not args:
            args = self.images.keys()
        for i in args:
            self.images[i] = cv2.GaussianBlur(self.images[i], ksize, sigma)

    def grey_blurred(self, *args, ksize=(5, 5), sigma=0):
        """
        reduce the image dimension to 2-D and apply Gaussian blur
        """
        if not args:
            args = self.images.keys()
        for i in args:
            self.images[i] = cv2.cvtColor(self.images[i], cv2.COLOR_BGR2GRAY)
            self.images[i] = cv2.GaussianBlur(self.images[i], ksize, sigma)

    def canny(self, *args, threshold1=50, threshold2=150):
        """
        detect edges
        """
        if not args:
            args = self.images.keys()
        for i in args:
            self.images[i] = cv2.Canny(self.images[i], threshold1, threshold2)

    def set_roi(self, *args, corners):
        """
        creates our region of interest polygon with mask
        :param args: images we want to apply on
        :param corners: list of region of interest coordinates by (x, y)
        """
        if len(corners) < 3:
            raise AttributeError("Minimum number of the given coordinates must be 3")
        if not args:
            args = self.images.keys()

        poly = np.array([corners])

        for i in args:
            mask = np.zeros_like(self.images[i])
            cv2.fillPoly(mask, poly, (255, 255, 255))
            self.images[i] = cv2.bitwise_and(mask, self.images[i])
            # cv2.imshow('test', self.images[i])
            # cv2.waitKey(0)

    def get(self, *args):
        """
        returns the image or images
        """
        # return only the image
        if len(args) == 1:
            key = args[0]
            return np.copy(self.images[key])

        # return multiple images as a dictionary
        if not args:
            return self.images.copy()
        else:
            specified = {}
            for i in args:
                specified[i] = np.copy(self.images[i])
            return specified

    def show(self, *args):
        """
        display the current images
        """
        if not args:
            args = self.images.keys()
        [cv2.imshow(str(i), self.images[i]) for i in args]
        cv2.waitKey(0)

    def info(self, *args):
        """
        print information about added images
        """
        if not args:
            args = self.images.keys()
        for i in args:
            print(f"Image: {i}\t   Shape: {self.images[i].shape}")

    def add(self, *images):
        if type(images[0]) is not tuple:
            images = enumerate(images)
        for i, img in images:
            self.IMAGES[i] = img
            self.images[i] = self.IMAGES[i].copy()

    def reset(self, *args):
        """
        reset the images into their original state
        """
        if not args:
            args = self.images.keys()
        for i in args:
            self.images[i] = np.copy(self.IMAGES[i])
