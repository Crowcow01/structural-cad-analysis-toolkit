def percentage_error(calculated, reference):
    if reference == 0: return abs(calculated-reference)
    return abs(calculated-reference)/abs(reference)*100

def print_benchmark(name, calculated, reference, unit):
    print(f"{name:<10} Calculated={calculated:>12.6f} {unit:<5} Reference={reference:>10.6f} {unit:<5} Error={percentage_error(calculated,reference):.4f}%")
