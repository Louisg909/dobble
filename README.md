# Dobble
Custom dobble game creator
Really enjoyed playing the [original dobble](https://www.dobblegame.com/en/homepage/) with my family, and we decided it would be fun to make a custom game. Rather than painstakingly making it by and, I wanted to make a program that could automate it.
---
## Logic behind the card creation:
The cards are designed so that every card has one icon in common with every single other card. The logic of how this works is explained in a very intuitive way in the video by Matt Parker [How does Dobble (Spot It) work?](https://www.youtube.com/watch?v=VTDKqW_GLkw).

Bellow is a simple explination of it:
*explination of the logic with diagrams*

## Coding the cards
### Idea 1
One idea I have, is to simulate the grid, basically create a load of empty card objects in a 2D, 7x7 array with a load of empty `Card` objects, and then add items to the cards on each "line" through the array (in addition to the ones that are at the vanishing points, lastly adding an item to all of the vanishing point cards)

For example, Pseudo-code for a simplifed 13-icon version of dobble, a 3x3 grid would be used:

![13-icon-dobble-diagram]("readme_assets\13_icon_dobble.png")

So an empty `Card` class would be initiated in each of these spots:

```python
class Card:
    def __init__(self):
        self.icons = []
    def add_icon(self, icon):
        self.icons.append(icon)

grid = [[Card() for _ in range(3)] for _ in range(3)]
vanishing_points = [Card() for _ in range(4)]
```

After this, the items just need to be added to the list. The number of lines in the grid is the number of rows + 1, or `len(grid) + 1`. The plus 1 is just the columns though so can be done seperately as it is always the same. All the rest is just connecting the top index with the column at the end, one down each time. Basically, I can work out the gradient and pick the indecies that fit that gradient each time, and move down by one once I hit the end. (I am using numbers to signify the icons, but one line will be added to the `.add_icon()` method to attatch the actual icon according to a dictionary - or the specification of the icon designs might be added later all together.)

> The number of cards is determined by the variable `length` which signifies the number of rows in the table. The number of cards is calculated from the length as: `length**2 + length + 1`, and the length can be found from the total number of cards by doing the quadratic formula, but the length has to be a whole number, and not all number of cards would give this length as a whole number.
> The samllest, valid card numbers are: 7, 13, 21, 31, 43, 57, 73, and 91. Some cards can be removed like in real dobble, but I don't see much point in that.

```python
# First, the grid with empty cards is initialised
grid = [[Card() for _ in range(length)] for _ in range(length)]


# The flat horizontal and vertical lines can be given their values sepertely
for n in range(length):
    for m in range(len(grid[n])):
        grid[n][m].add_icon(n+1,length + m+1)

# initialising vanish points for the cards on the horizontal and vertical vanishing points
vanish1_icons = [n+1 for n in range(length)]
vanish2_icons = [length + n + 1 for n in range(length)]
vanishing_points = [Card(vanish1_icons) , Card(vanish2_icons)]

# All of the angled lines:
icon_no = 2 * length + 1 # The first number - basically worked out what numbers would have been used so far and added one
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

```





## Adding variety to the icons on the card
- Addng some positional jitter
- Adding some rotation
- Randomising size
- Ensuring no overlap of icons 


---
## Rendering cards to a printable set





