from modules.data_processor import get_puzzle_input


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def solve_part_1(input_str: str) -> int:
    def check_solvable(ax, ay, bx, by, px, py):
        x_gcd = gcd(ax, bx)
        if px % x_gcd != 0:
            return None

        y_gcd = gcd(ay, by)
        if py % y_gcd != 0:
            return None

        # Limit to a max of 100 button clicks
        for i in range(101):
            for j in range(101):
                if i * ax + j * bx == px and i * ay + j * by == py:
                    return i * 3 + j  # Cost calculation
        return None

    total_tokens = 0
    for machine in input_str.strip().split('\n\n'):
        lines = machine.strip().split('\n')

        ax = int(lines[0].split('X+')[1].split(',')[0])
        ay = int(lines[0].split('Y+')[1])
        bx = int(lines[1].split('X+')[1].split(',')[0])
        by = int(lines[1].split('Y+')[1])
        px = int(lines[2].split('X=')[1].split(',')[0])
        py = int(lines[2].split('Y=')[1])

        tokens = check_solvable(ax, ay, bx, by, px, py)
        if tokens is not None:
            total_tokens += tokens

    return total_tokens


def solve_part_2(input_str: str) -> int:
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def find_min_tokens(ax, ay, bx, by, px, py):
        # Find solutions using Diophantine equations
        x_gcd, x_m, x_n = extended_gcd(ax, bx)
        if px % x_gcd != 0:
            return None

        y_gcd, y_m, y_n = extended_gcd(ay, by)
        if py % y_gcd != 0:
            return None

        x_t = px // x_gcd

        a_count = x_m * x_t
        b_count = x_n * x_t

        k = (py - (a_count * ay + b_count * by)) // (ay * bx // x_gcd - ax * by // x_gcd)

        a_count += k * (bx // x_gcd)
        b_count -= k * (ax // x_gcd)

        if (a_count * ax + b_count * bx == px and
                a_count * ay + b_count * by == py and
                a_count >= 0 and b_count >= 0):
            return a_count * 3 + b_count

        return None

    total_tokens = 0
    offset = 10000000000000

    for machine in input_str.strip().split('\n\n'):
        lines = machine.strip().split('\n')

        ax = int(lines[0].split('X+')[1].split(',')[0])
        ay = int(lines[0].split('Y+')[1])
        bx = int(lines[1].split('X+')[1].split(',')[0])
        by = int(lines[1].split('Y+')[1])
        px = int(lines[2].split('X=')[1].split(',')[0]) + offset
        py = int(lines[2].split('Y=')[1]) + offset

        tokens = find_min_tokens(ax, ay, bx, by, px, py)
        if tokens is not None:
            total_tokens += tokens

    return total_tokens


if __name__ == '__main__':
    day = 13
    data = get_puzzle_input(day=day)

    result_part_1 = solve_part_1(data)
    print(f"Puzzle result part 1: {result_part_1}")

    result_part_2 = solve_part_2(data)
    print(f"Puzzle result part 2: {result_part_2}")
