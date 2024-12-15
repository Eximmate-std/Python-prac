from fractions import Fraction


def evaluate_polynomial(coefficients, x):
    result = 0
    for degree, coeff in enumerate(coefficients):
        result += coeff * (x ** degree)
    return result

def check_solution(s, w, degree_A, coeffs_A, degree_B, coeffs_B):
    s = Fraction(s)
    w = Fraction(w)
    A_s = evaluate_polynomial(coeffs_A, s)
    B_s = evaluate_polynomial(coeffs_B, s)

    if B_s == 0:
        return False
    return A_s == w * B_s


input_data = input()
input_values = input_data.split(", ")

s = input_values[0]
w = input_values[1]
degree_A = int(input_values[2])
coeffs_A = [Fraction(c) for c in input_values[3:3 + degree_A + 1]]
degree_B = int(input_values[3 + degree_A + 1])
coeffs_B = [Fraction(c) for c in input_values[4 + degree_A + 1: 4 + degree_A + 1 + degree_B + 1]]

print(check_solution(s, w, degree_A, coeffs_A, degree_B, coeffs_B))
