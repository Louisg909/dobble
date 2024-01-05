from PIL import Image
import math
import random

class Icon:
    def __init__(self,icon_type):
        self.icon_type = icon_type
        self.radius_factor = random.uniform(0.15,0.3) # size as a fraction of the radius of the entire card
        self.rotation = random.randint(0,360)
        self.jitter = tuple([random.uniform(-1,1) for _ in range(2)]) # I had this as 3 for ages.. as if I would have 3D jitter lol
    
    def __mul__(self,other): # resizing
        # check if positions are next to eachother
        # check if radius overlap according to predetermined distance between icons, the icon's radiuses and their jitter
        overlap = None
        # if overlap, see how much by - and reduce both of their radises by 0.75*overlap
        self.radius -= 0.75 * overlap
        other.radius -= 0.75 * overlap

    def open_formatted_asset(self,background_radius):
        asset = Image.open(f"icons/{self.icon_type}.png")
        asset = asset.convert("RGBA")

        # resize asset
        if (old_width := asset.width) >= (old_height := asset.height):
            new_width = background_radius * self.radius_factor
            asset = asset.resize((int(round(new_width)), int(round(old_height * old_width / new_width))))
        else:
            new_height = background_radius * self.radius_factor
            asset = asset.resize((int(round(old_width * old_height / new_height)), int(round(new_height))))
        
        # rotate asset
        #asset = asset.rotate(self.rotation)
        
        return asset

class Card:
    def __init__(self, icons=None):
        if icons == None:
            self.icons = []
        else:
            self.icons = [icon for icon in icons]
        #self.icons = [] if icons == None else icons
    def add_icon(self, *icons):
        self.icons += [icon_dict[icon] for icon in icons]
    def __repr__(self):
        return "C" + str(self.icons)

test_card = Card([Icon("cheese"),Icon("poop"),Icon("yellow"),Icon("yank"),Icon("louis")])



# Deck = list(object)
 
# Make way to generate a high resolution PNG of a card, bassed on the positioning, rotation etc of the items in a card object
def card_to_png(card: object, file_name):
    def get_pos(index, background_radius,numb_items):
        # all items are centered at radius 0.5*background radius, and evenly fanned out from 0 deg
        # every 72 deg
        radius = 0.5 * background_radius
        angle = 360/numb_items * index
        # converting from polar to caetesian to find relative positions from centre
        x_rel = math.cos(angle)*radius
        y_rel = math.sin(angle)*radius
        # transforming it to get relative to top left corner
        y_pos = background_radius - y_rel
        x_pos = background_radius + x_rel
        return x_pos, y_pos

    def jitter_and_paste_asset(icon,background, no_items):
        asset = icon.open_formatted_asset(background.width)
        jitter_scale = 0.025
        x_pos, y_pos = get_pos(count, background.width/2, number_of_items)
        x_pos += icon.jitter[0] * jitter_scale
        y_pos += icon.jitter[1] * jitter_scale

        # pasting onto background
        background.paste(asset, (int(x_pos), int(y_pos)), asset)  # The third argument is the mask
        del asset
        return background


    background_name = "dobble_background_lowres_test.png"
    background = Image.open(background_name)
    background = background.convert("RGBA")

    # open assets
    # still need to sort out the positioning
    count = 0
    number_of_items = len(card.icons)
    for icon in card.icons:
        background = jitter_and_paste_asset(icon,background,number_of_items)
        count += 1
    background.save(f"card_outputs/{file_name}.png")

card_to_png(test_card, "test")


# Make something to go through each card in the deck, and save it as a PNG to an output directory
def render_deck(deck):
    for card_no in range(len(deck)):
        # load background here and give the object into the function as then it reduces on reloading the file every single time - leave as is for now though as I am testing the singular function
        file_name = f"card_outputs/card_{card_no}.png"
        # render card
        card_to_png(deck[card_no],file_name)

