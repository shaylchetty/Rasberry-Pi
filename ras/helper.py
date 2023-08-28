import math

def distSquaredTopLeft(cord):
    x, y = cord
    return x**2 + y**2

def distSquaredBotRight(cord, frameWidth, frameHeight):
    x, y = cord
    return (frameWidth - x)**2 + (frameHeight - y)**2

# def closest_coordinates(coordinates, frameWidth, frameHeight):
#     if not coordinates:
#         return None, None

#     closest_to_top_left = min(coordinates, key=distSquaredTopLeft)
#     closest_to_bottom_right = min(coordinates, key=lambda cord: distSquaredBotRight(cord, frameWidth, frameHeight))

#     return closest_to_top_left, closest_to_bottom_right

def closest_coordinates(coordinates, frameWidth, frameHeight):
    if not coordinates:
        return (0,0), (0,0)
    
    top=coordinates[0][1]
    bot=coordinates[0][1]
    left=coordinates[0][0]
    right=coordinates[0][0]

    for cord in coordinates:
        if cord[0] < left:
            left = cord[0]
        if cord[0] > right:
            right = cord[0]
        if cord[1] < top:
            top = cord[1]
        if cord[1] > bot:
            bot = cord[1]

    return (left, top), (right, bot)



print(closest_coordinates([(14, 8), (165, 329), (180, 328), (195, 329), (134, 331), (126, 332), (120, 333), (240, 343), (148, 347), (183, 417), (136, 423), (1118, 735), (66, 555), (535, 683), (482, 648), (498, 584), (463, 600), (448, 614)], 1280, 720))