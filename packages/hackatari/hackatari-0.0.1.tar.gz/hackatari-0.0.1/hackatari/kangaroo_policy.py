from ocatari.ram.kangaroo import Player, Child, Ladder, Platform


def get_player_position(state):
    for obj in state:
        if isinstance(obj, Player):
            return obj._xy
    return None

def get_child_position(state):
    for obj in state:
        if isinstance(obj, Child):
            return obj._xy
    return None

def get_platforms(state):
    return [obj for obj in state if isinstance(obj, Platform)]

def get_ladders(state):
    return [obj for obj in state if isinstance(obj, Ladder)]

def get_fruits(state):
    return [obj for obj in state if isinstance(obj, Fruit)]

def get_bell(state):
    for obj in state:
        if isinstance(obj, Bell):
            return obj._xy
    return None

def get_closest_ladder(player_pos, ladders):
    closest_ladder = None
    min_distance = float('inf')
    for ladder in ladders:
        ladder_pos = ladder._xy
        distance = abs(player_pos[0] - ladder_pos[0]) + abs(player_pos[1] - ladder_pos[1])
        if distance < min_distance:
            min_distance = distance
            closest_ladder = ladder
    return closest_ladder

def get_next_platform_above(player_pos, platforms):
    next_platform = None
    min_distance = float('inf')
    for platform in platforms:
        platform_pos = platform._xy
        if platform_pos[1] < player_pos[1]:
            distance = player_pos[1] - platform_pos[1]
            if distance < min_distance:
                min_distance = distance
                next_platform = platform
    return next_platform

def is_player_on_platform(player_pos, platforms):
    for platform in platforms:
        platform_pos = platform._xy
        platform_width = platform.wh[0]
        if platform_pos[1] == player_pos[1] and platform_pos[0] <= player_pos[0] <= (platform_pos[0] + platform_width):
            return True
    return False

def is_player_near_ladder(player_pos, ladder_pos):
    return abs(player_pos[0] - ladder_pos[0]) <= 1

def move_towards(target_pos, player_pos):
    if target_pos[0] > player_pos[0]:
        return 'RIGHT'
    elif target_pos[0] < player_pos[0]:
        return 'LEFT'
    elif target_pos[1] > player_pos[1]:
        return 'UP'
    else:
        return 'DOWN'


def kangaroo_policy(state):
    player_pos = get_player_position(state)
    child_pos = get_child_position(state)
    platforms = get_platforms(state)
    ladders = get_ladders(state)
    
    if player_pos is None or child_pos is None:
        return 'NOOP'
    
    # If the player is on the same level as the child and the child is directly reachable
    if player_pos[1] == child_pos[1]:
        return move_towards(child_pos, player_pos)
    
    # If the player is not on the same level as the child
    if player_pos[1] < child_pos[1]:
        # Move up if there is a platform above
        next_platform = get_next_platform_above(player_pos, platforms)
        if next_platform:
            closest_ladder = get_closest_ladder(player_pos, ladders)
            if closest_ladder and is_player_near_ladder(player_pos, closest_ladder._xy):
                return 'UP'
            elif closest_ladder:
                return move_towards(closest_ladder._xy, player_pos)
    else:
        # If the player is above the child, move down
        return 'DOWN'
    
    # Default action if none of the conditions are met
    return 'NOOP'

# def ladder_on_same_floor(player_pos, ladders):


# def on_ladder(player, ladder):
#     if player.x == ladder.x and ladder.y < player.y < ladder.y + ladder.h:
#         print(player, ladder)
#         return True
#     return False

def on_ladder(player, ladder):
    lx, ly = ladder._xy
    lw, lh = ladder.wh
    if lx <= player.x <= lx + lw and ly <= player.y <= ly + lh:
        return True
    return False

def can_climb_up():
    for ladder in ladders:
        lx, ly = ladder._xy
        lw, lh = ladder.wh
        if lx <= player_x <= lx + lw and player_y > ly:
            return True
    return False

def get_next_ladder(player, ladders):
    sorted_ladders = sorted(ladders, key=lambda x: abs(x.y - player.y))
    return sorted_ladders[0]

def quentin_policy(state):
    player = None
    child = None
    ladders = []
    platforms = []
    for obj in state:
        if isinstance(obj, Player):
            player = obj
        elif isinstance(obj, Child):
            child = obj
        elif isinstance(obj, Ladder):
            ladders.append(obj)
        elif isinstance(obj, Platform):
            platforms.append(obj)
    for ladder in ladders:
        if on_ladder(player, ladder):
            if player.y > child.y:
                return 'UP'
            elif player.y < child.y:
                return 'DOWN'
    next_ladder = get_next_ladder(player, ladders)
    if player.x < next_ladder.x:
        return 'RIGHT'
    elif player.x > next_ladder.x:
        return 'LEFT'
    