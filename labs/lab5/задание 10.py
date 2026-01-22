students = []
n = int(input("Сколько студентов? "))
for i in range(n):
    name = input("Имя студента: ")
    grades = list(map(int, input("Оценки через пробел: ").split()))
    students.append((name, grades))
averages = {name: sum(grades)/len(grades) for name, grades in students}
best_student = max(averages, key=averages.get)
print(f"У {best_student} самый высокий средний балл: {averages[best_student]:.1f}")