import pygame
import world
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

class C_Global:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        
conversation = {
    "stranger": [
        C_Text("i'm cold. can you give me a coat?", 
        [Choice("yes(y)", pygame.K_y, "yescoat"), Choice("no(n)", pygame.K_n, "nocoat")])],
    "yescoat":[C_Text("thanks"), C_Give("coat"), C_Switch("coated")],
    "nocoat": [C_Text("thats sad :( could you get one?")],
    "coated": [C_Text("Thanks for that coat you gave me earlier")],
    "tortoise":[
        C_Text("There are five golden tortoises in this zone. If you bring me all of them, there will be a reward. Will you try?", 
        [Choice("yes(y)", pygame.K_y, "okay"), Choice("no(n)", pygame.K_n, "bye")])],
    "okay":[
        C_Text("Cool"), 
        C_Global("tortoise_spawn", True), 
        C_Switch("tortiose2")],
    "bye":[C_Text("bye")],
    "tortiose2":[C_Text("Have you gotten those?",
        [Choice("yes(y)", pygame.K_y, "awsome!"),
        Choice("no(n)", pygame.K_n, "bye")])],
    "awsome!":[C_Text("Yay!")]}