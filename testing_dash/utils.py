# utils.py
def v_grade_to_numeric(v_grade):
    if v_grade.startswith('V'):
        try:
            return int(v_grade[1:])
        except ValueError:
            return 0
    return 0

def count_v6_and_harder(climbed_list):
    return sum(1 for grade in climbed_list if v_grade_to_numeric(grade) >= 6)

def calculate_average_difficulty(climbed_list):
    numeric_grades = [v_grade_to_numeric(grade) for grade in climbed_list]
    if numeric_grades:
        return sum(numeric_grades) / len(numeric_grades)
    return 0