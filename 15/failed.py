def is_move_possible_large(grid, x, y, direction):
    moving = grid[x][y]
    dx, dy = DIRECTIONS[direction]
    nx, ny = x + dx, y + dy
    new_val = grid[nx][ny]

    if direction in ["<", ">"]:
        return is_move_possible(grid, x, y, direction)
    elif new_val == "#":
        return False
    elif moving == "@" and new_val == ".":
        return True
    elif moving == "@" and new_val == "[":
        left = is_move_possible_large(grid, nx, ny, direction)
        if not left:
            return False
        else:
            return is_move_possible_large(grid, nx, ny + 1, direction)
    elif moving == "@" and new_val == "]":
        right = is_move_possible_large(grid, nx, ny, direction)
        if not right:
            return False
        else:
            return is_move_possible_large(grid, nx, ny - 1, direction)
    elif moving == "[" and (new_val == "#" or grid[nx][ny + 1] == "#"):
        return False
    elif moving == "]" and (new_val == "#" or grid[nx][ny - 1] == "#"):
        return False
    elif moving == "[" and new_val == "." and grid[nx][ny + 1] == ".":
        return True
    elif moving == "]" and new_val == "." and grid[nx][ny - 1] == ".":
        return True
    elif moving == "[":
        left = is_move_possible_large(grid, nx, ny, direction)
        if not left:
            return False
        else:
            return is_move_possible_large(grid, nx, ny + 1, direction)
    elif moving == "]":
        right = is_move_possible_large(grid, nx, ny, direction)
        if not right:
            return False
        else:
            return is_move_possible_large(grid, nx, ny - 1, direction)

    print(
        f"This should not be possible. Moving {x, y} in direction {direction}. Object moved is {moving} and the new space has {new_val}."
    )


def move_large(grid, x, y, direction):
    print(f"Attempting to move {x, y, direction}")
    if not is_move_possible_large(grid, x, y, direction):
        return grid

    if direction in ["<", ">"]:
        return move(grid, x, y, direction)

    moving = grid[x][y]
    dx, dy = DIRECTIONS[direction]
    nx, ny = x + dx, y + dy

    if moving == ".":
        return grid
    elif direction in ["<", ">"]:
        return move(grid, x, y, direction)
    elif moving == "@" and grid[nx][ny] == ".":
        grid[x][y] = "."
        grid[nx][ny] = moving
    elif moving == "[" and grid[nx][ny] == "." and grid[nx][ny + 1] == ".":
        grid[x][y] = "."
        grid[x][y + 1] = "."
        grid[nx][ny] = "["
        grid[nx][ny + 1] = "]"
    elif moving == "]" and grid[nx][ny] == "." and grid[nx][ny - 1] == ".":
        grid[x][y] = "."
        grid[x][y - 1] = "."
        grid[nx][ny] = "]"
        grid[nx][ny - 1] = "["
    elif moving == "[":
        grid = move_large(grid, nx, ny, direction)
        grid = move_large(grid, nx, ny + 1, direction)
        grid = move_large(grid, x, y, direction)
    elif moving == "]":
        grid = move_large(grid, nx, ny, direction)
        grid = move_large(grid, nx, ny - 1, direction)
        grid = move_large(grid, x, y, direction)
    elif moving == "@":
        grid = move_large(grid, nx, ny, direction)
        grid = move_large(grid, x, y, direction)
    else:
        print(f"This should not happen. Moving ({x,y}) in direction {direction}")

    return grid


def simulate_large(grid, instructions):
    grid = deepcopy(grid)
    for i, ins in enumerate(instructions):
        # print(f"Running instruction {i} - {ins}")
        x, y = find_robot(grid)
        grid = move_large(grid, x, y, ins)
        display_grid(grid)
    return grid
