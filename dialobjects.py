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
        
conversation = {
    "stranger":[C_Text("i'm cold. can you give me a coat?", [Choice("yes(y)", pygame.K_y, "yescoat"), Choice("no(n)", pygame.K_n, "nocoat")])],
    "yescoat":[C_Text("thanks"), C_Give("coat"), C_Switch("coated")],
    "nocoat": [C_Text("thats sad :( could you get one?")],
    "coated": [C_Text("Thanks for that coat you gave me earlier")]}