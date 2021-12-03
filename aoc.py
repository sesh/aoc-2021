def d1(depths, window=3):
    count = 0
    for x in range(1, len(depths) - window + 1):
        count += sum(depths[x : x + window]) > sum(depths[x - 1 : x - 1 + window])
    return count


def d2(course):
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


def d2_with_aim(course):
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
