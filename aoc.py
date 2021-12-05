def d1(depths: list[str], window: int = 3) -> int:
    count = 0
    for x in range(1, len(depths) - window + 1):
        count += sum(depths[x : x + window]) > sum(depths[x - 1 : x - 1 + window])
    return count


def d2(course: list[str]) -> int:
    course = [(x.split()[0], int(x.split()[1])) for x in course]
    depth, distance = 0, 0

    for instruction, x in course:
        if instruction == "forward":
            distance += x
        elif instruction == "down":
            depth += x
        else:
            depth -= x

    return depth * distance


def d2_with_aim(course: list[str]) -> int:
    course = [(x.split()[0], int(x.split()[1])) for x in course]
    aim, depth, distance = 0, 0, 0

    for instruction in course:
        match instruction:
            case "forward", x:
                distance += x
                depth += x * aim
            case "down", x:
                aim += x
            case "up", x:
                aim -= x

    return depth * distance


def d3_frequencies(readings):
    frequencies = [0 for _ in readings[0]]

    for reading in readings:
        reading = reading.strip()
        for i, x in enumerate(reading):
            if x == "1":
                frequencies[i] += 1
            else:
                frequencies[i] -= 1

    return frequencies


def d3_get_reading_by_bit_criteria(readings, bit_criteria):
    for i in range(len(readings[0])):
        frequencies = d3_frequencies(readings)
        f = frequencies[i]

        bit = bit_criteria(f)
        readings = [x for x in readings if x[i] == bit]

        if len(readings) == 1:
            return int(readings[0], 2)


def d3(readings):
    frequencies = d3_frequencies(readings)

    gamma = int("".join(["1" if x >= 0 else "0" for x in frequencies]), 2)
    epsilon = int("".join(["0" if x >= 0 else "1" for x in frequencies]), 2)

    return gamma * epsilon


def d3_life_support(readings):
    o2_generator = d3_get_reading_by_bit_criteria(
        readings, lambda f: "1" if f >= 0 else "0"
    )
    co2_scrubber = d3_get_reading_by_bit_criteria(
        readings, lambda f: "1" if f < 0 else "0"
    )
    return o2_generator * co2_scrubber


def d4_load_boards(input):
    boards = []
    board = []

    for l in input[2:]:
        if not l:
            boards.append(board)
            board = []
        else:
            board.append([x.strip() for x in l.split()])
    boards.append(board)
    return boards


def d4_check_if_winner(board):
    for row in board:
        if len([x for x in row if x.endswith("*")]) == len(row):
            return True

    for i in range(len(board[0])):
        if len([row[i] for row in board if row[i].endswith("*")]) == len(board[0]):
            return True

    return False


def d4_mark_draw_on_board(draw, board):
    for row in board:
        for i, n in enumerate(row):
            if n == draw:
                row[i] = n + "*"


def d4_tally_board(board):
    total = 0
    for row in board:
        for x in row:
            if not x.endswith("*"):
                total += int(x)
    return total


def d4_bingo(input):
    draws = input[0].split(",")
    boards = d4_load_boards(input)

    for draw in draws:
        for board in boards:
            d4_mark_draw_on_board(draw, board)
            winner = d4_check_if_winner(board)

            if winner:
                total = d4_tally_board(board)
                return total * int(draw)


def d4_bingo_last(input):
    draws = input[0].split(",")
    boards = d4_load_boards(input)

    completed_boards = []
    for draw in draws:
        for board_id, board in enumerate(boards):
            if board_id in completed_boards:
                continue

            d4_mark_draw_on_board(draw, board)
            winner = d4_check_if_winner(board)

            if winner:
                completed_boards.append(board_id)

                if len(completed_boards) == len(boards):
                    total = d4_tally_board(board)
                    return total * int(draw)


def d5_load_grid(input):
    lines = []
    rows = 0
    cols = 0

    for l in input:
        start, end = l.split(" -> ", 1)
        start = [int(x) for x in start.split(",")]
        end = [int(x) for x in end.split(",")]
        lines.append((start, end))

        cols = max([cols, start[0], end[0]])
        rows = max([rows, start[1], end[1]])

    grid = [["."] * (cols + 1) for _ in range(rows + 1)]
    return lines, grid


def d5_set_point(grid, x1, y1):
    if grid[y1][x1] == ".":
        grid[y1][x1] = "1"
    else:
        grid[y1][x1] = str(int(grid[y1][x1]) + 1)


def d5_draw_line(grid, x1, y1, x2, y2):
    d5_set_point(grid, x2, y2)  # bit of a hack
    while x1 != x2 or y1 != y2:
        d5_set_point(grid, x1, y1)
        if x1 < x2:
            x1 += 1
        if x1 > x2:
            x1 -= 1
        if y1 < y2:
            y1 += 1
        if y1 > y2:
            y1 -= 1


def d5_total_grid(grid):
    total = 0
    for row in grid:
        for point in row:
            if point not in [".", "1"]:
                total += 1
    return total


def d5(input):
    lines, grid = d5_load_grid(input)

    for (x1, y1), (x2, y2) in lines:
        if x1 == x2 or y1 == y2:
            d5_draw_line(grid, x1, y1, x2, y2)

    total = d5_total_grid(grid)
    return total


def d5_diagonals(input):
    lines, grid = d5_load_grid(input)

    for (x1, y1), (x2, y2) in lines:
        d5_draw_line(grid, x1, y1, x2, y2)

    total = d5_total_grid(grid)
    return total


if __name__ == "__main__":
    d1_1 = d1([int(x) for x in open("inputs/d1.txt").readlines() if x], 1)
    print("1.1:", d1_1)  # 1553
    assert d1_1 == 1553

    d1_2 = d1([int(x) for x in open("inputs/d1.txt").readlines() if x], 3)
    print("1.2:", d1_2)  # 1597
    assert d1_2 == 1597

    d2_1 = d2(open("inputs/d2.txt").readlines())
    print("2.1:", d2_1)  # 1840243
    assert d2_1 == 1840243

    d2_2 = d2_with_aim(open("inputs/d2.txt").readlines())
    print("2.2:", d2_2)  # 1727785422
    assert d2_2 == 1727785422

    d3_1 = d3([x.strip() for x in open("inputs/d3.txt").readlines()])
    print("3.1:", d3_1)  # 1307354
    assert d3_1 == 1307354

    d3_2 = d3_life_support([x.strip() for x in open("inputs/d3.txt").readlines()])
    print("3.2:", d3_2)  # 1307354
    assert d3_2 == 482500

    d4_1 = d4_bingo([x.strip() for x in open("inputs/d4.txt").readlines()])
    print("4.1:", d4_1)
    assert d4_1 == 39984

    d4_2 = d4_bingo_last([x.strip() for x in open("inputs/d4.txt").readlines()])
    print("4.2:", d4_2)
    assert d4_2 == 8468

    d5_1 = d5([x.strip() for x in open("inputs/d5.txt").readlines() if x.strip()])
    print("5.1:", d5_1)
    assert d5_1 == 6113

    d5_2 = d5_diagonals(
        [x.strip() for x in open("inputs/d5.txt").readlines() if x.strip()]
    )
    print("5.2:", d5_2)
    assert d5_2 == 20373
