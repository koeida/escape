import pygame
class Choice:
    def __init__(self, text, key, target):
        self.text = text
        self.target = target
        self.key = key
    
    
class C_Text:
    def __init__(self, message, choices = None):
        self.message = message
        self.choices = choices

class C_Switch:
    def __init__(self, new_conv):
        self.new_conv = new_conv
        
class C_Give:
    def __init__(self, object):
        self.object = object
        
        
    
    #
conversation = {
    "advent": [C_Text("great! i've been looking for an adventurer! i'm cold. can you give me a coat?",
                [Choice("yes(y)", pygame.K_y, "yescoat"), Choice("no(n)", pygame.K_n, "nocoat")])],
    "stranger":[C_Text("hello, stranger! may i inquire whether you are here as an adventurer or a tourist?", 
                [Choice("adventurer(y)", pygame.K_y, "advent"), Choice("tourist(n)", pygame.K_n, "tourist")])],
    "tourist":[C_Text("yep. now that the dungeons are being renovated, more and more tourists are coming down here. i haven't seen many humans brave enough to visit though!")],
    "yescoat":[C_Text("thanks"), C_Give("coat"), C_Switch("coated")],
    "nocoat": [C_Text("thats sad :( could you get one?")],
    "coated": [C_Text("Thanks for that coat you gave me earlier")]}