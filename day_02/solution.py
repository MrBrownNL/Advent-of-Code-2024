from data_processor import get_puzzle_input

def parse_input(content):
    return [list(map(int, line.split())) for line in content.strip().split('\n')]

def is_report_safe(levels):
    return all(1 <= levels[i+1] - levels[i] <= 3 for i in range(len(levels)-1)) or \
        all(1 <= levels[i] - levels[i+1] <= 3 for i in range(len(levels)-1))

def count_safe_reports(reports, dampener=False):
    def is_safe(levels):
        if is_report_safe(levels):
            return True
        if dampener:
            return any(is_report_safe(levels[:i] + levels[i+1:]) for i in range(len(levels)))
        return False

    return sum(1 for report in reports if is_safe(report))


def solve_part_1(input_string):
    reports = parse_input(input_string)
    return count_safe_reports(reports)


def solve_part_2(input_string):
    reports = parse_input(input_string)
    return count_safe_reports(reports, dampener=True)


if __name__ == '__main__':
    content = get_puzzle_input(day=2)
    reports = parse_input(content)

    safe_reports_count = count_safe_reports(reports)
    print(f"Number of safe reports: {safe_reports_count}")

    safe_reports_damped_count = count_safe_reports(reports, dampener=True)
    print(f"Number of safe reports with Problem Dampener: {safe_reports_damped_count}")
