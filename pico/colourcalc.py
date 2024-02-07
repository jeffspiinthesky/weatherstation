class ColourCalc:
    def __init__(self):
        temperature = 0
        self.red = 0
        self.green = 255
        self.blue = 255

    def calc_colour(self,temperature):
        # -10- Blue
        # -9-0 Blue to Cyan R0 G0-255 B255
        # 1-10 Cyan to Green R0 G255 B255-0
        # 11-20 Green to Yellow R0-255 G255 B0
        # 20-30 Yellow to Red R255 G255-0 B0
        # 30+ Red
        if temperature <= -10:
            self.red = 0
            self.green = 0
            self.blue = 255
        elif temperature in range(-10,0):
            self.red = 0
            self.green = ((255/10) * (-10 - temperature))
            self.blue = 255
        elif temperature in range(0, 10):
            self.red = 0
            self.green = 255
            self.blue = ((255/10) * (10-temperature) )
        elif temperature in range(10,20):
            self.red = ((255/10) * (temperature - 10) )
            self.green = 255
            self.blue = 0
        elif temperature in range(20,30):
            self.red = 255
            self.green = ((255/10) * (30 - temperature) )
            self.blue = 0
        elif temperature >= 30:
            self.red = 255
            self.green = 0
            self.blue = 0
        return self.get_colour()

    def get_colour(self):
        return (int(self.red), int(self.green), int(self.blue))
