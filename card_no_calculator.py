

no_cards = lambda length: length**2 + length + 1

#table_cells = lambda entry1, entry2, entry3: f"| {entry1: ^8} | {entry2: ^8} | {entry3: ^8} |"
#table_lines = "+----------+----------+----------+"
#print(table_lines)
#print("| o. cards | No. icons | 
#print(table_lines)

print("These are the number of cards required to have the equal number of icons. You can remove some cards like the real game of dobble did, but I don't see any point in this.")
for length in range(2,10):
    print(no_cards(length))
