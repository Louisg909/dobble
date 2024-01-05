import random
from icon_dict import icon_dict
from PIL import Image

# 55 cards but can have 57
# 57 icons


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
        asset = Image.open(f"icons/{icon_type}.png")

        # resize asset
        if (old_width := asset.width) >= (old_height := asset.height):
            new_width = background_radius * self.radius_factor
            asset = asset.resize((new_width, old_height * old_width / new_width))
        else:
            new_height = background_radius * self.radius_factor
            asset = asset.resize((old_width * old_height / new_height, new_height))
        
        # rotate asset
        asset = asset.rotate(self.rotation)
        
        return asset
        

def print_grid(grid):
    string = "\t"
    for n in grid:
        string += str(n) + "\n\t"
    print(string)

class Card:
    def __init__(self, icons=None):
        if icons == None:
            self.icons = []
        else:
            self.icons = [icon_dict[icon] for icon in icons]
        #self.icons = [] if icons == None else icons
    def add_icon(self, *icons):
        self.icons += [icon_dict[icon] for icon in icons]
    def __repr__(self):
        return "C" + str(self.icons)

length = 3 # number of rows - total cards = length**2 + length + 1

# initialising grid
grid = [[Card() for _ in range(length)] for _ in range(length)]

# flat horizontal and vertical lines:
for n in range(length):
    for m in range(len(grid[n])):
        grid[n][m].add_icon(n+1,length + m+1)

# initialising vanish points for the cards on the horizontal and vertical vanishing points
vanish1_icons = [n+1 for n in range(length)]
vanish2_icons = [length + n + 1 for n in range(length)]
vanishing_points = [Card(vanish1_icons) , Card(vanish2_icons)]

# The angled lines:
icon_no = 2 * length + 1 # the number that needs to be added
for row_no in range(len(grid)-1):
    # get ratio, down 1, across:
    across_step = length - row_no - 1
    vanishing_card_icons = []
    for across in range(length):
        vanishing_card_icons.append(icon_no)
        for row in grid:
            row[across].add_icon(icon_no)
            across = across + across_step if across + across_step < length else across + across_step - length
        icon_no += 1
    vanishing_points.append(Card(vanishing_card_icons))

# connect all the vanishing point cards togetheCard(vanish1_icons) , Card(vanish2_icons)]
[n.add_icon(icon_no) for n in vanishing_points]

# Add all cards to the deck:
deck = [m for n in grid for m in n] + vanishing_points

print(deck)
