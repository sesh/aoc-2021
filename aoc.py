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
