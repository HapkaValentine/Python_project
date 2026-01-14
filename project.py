import datetime
class Applicant:
    def __init__(self, last_name, first_name, patronymic, gender, birth_date,
                 specialty, experience, languages, expected_salary):
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.gender = gender
        self.birth_date = birth_date
        self.specialty = specialty
        self.experience = experience
        self.languages = languages
        self.expected_salary = expected_salary
    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"
    def get_age(self):
        today = datetime.date.today()
        year, month, day = self.birth_date
        birth_date = datetime.date(year, month, day)
        age = today.year - birth_date.year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age
    def __str__(self):
        birth_date_str = f"{self.birth_date[2]:02d}.{self.birth_date[1]:02d}.{self.birth_date[0]}"
        languages_str = ""
        if self.languages:
            for i in range(len(self.languages)):
                languages_str += self.languages[i]
                if i != len(self.languages) - 1:
                    languages_str += ", "
        else:
            languages_str = "нет"
        return (f"ФИО: {self.get_full_name()}\n"
                f"Пол: {self.gender}\n"
                f"Дата рождения: {birth_date_str} (Возраст: {self.get_age()})\n"
                f"Специальность: {self.specialty}\n"
                f"Стаж: {self.experience} лет\n"
                f"Иностранные языки: {languages_str}\n"
                f"Ожидаемый оклад: {self.expected_salary} руб.\n")
class EmploymentAgency:
    def __init__(self):
        self.database = []
        self.load_from_file("applicants.txt")
    def load_from_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    if line and not line.startswith("#"):
                        last_name = line
                        first_name = lines[i+1].strip()
                        patronymic = lines[i+2].strip()
                        gender = lines[i+3].strip()
                        birth_date_str = lines[i+4].strip()
                        birth_date_parts = birth_date_str.split('-')
                        year = int(birth_date_parts[0])
                        month = int(birth_date_parts[1])
                        day = int(birth_date_parts[2])
                        birth_date = (year, month, day)
                        specialty = lines[i+5].strip()
                        experience = float(lines[i+6].strip())
                        languages_line = lines[i+7].strip()
                        if languages_line == "нет":
                            languages = []
                        else:
                            languages = languages_line.split(',')
                            for j in range(len(languages)):
                                languages[j] = languages[j].strip()
                        expected_salary = float(lines[i+8].strip())
                        
                        applicant = Applicant(last_name, first_name, patronymic, gender, birth_date,
                                             specialty, experience, languages, expected_salary)
                        self.database.append(applicant)
                        i += 9
                    else:
                        i += 1
            print(f"Загружено {len(self.database)} записей из файла '{filename}'")
        except FileNotFoundError:
            print(f"Файл '{filename}' не найден. Создайте файл с данными.")
            print("Формат файла:")
            print("Фамилия")
            print("Имя")
            print("Отчество")
            print("Пол (м/ж)")
            print("Дата рождения (ГГГГ-ММ-ДД)")
            print("Специальность")
            print("Стаж (лет)")
            print("Языки (через запятую или 'нет')")
            print("Ожидаемый оклад")
            print("---")
            exit(1)
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
            exit(1)
    def shaker_sort(self, arr, key_func, reverse=False):
        n = len(arr)
        if n <= 1:
            return arr
        left = 0
        right = n - 1
        swapped = True
        while swapped:
            swapped = False
            for i in range(left, right):
                compare_result = self.compare_items(arr[i], arr[i + 1], key_func)
                if (not reverse and compare_result > 0) or (reverse and compare_result < 0):
                    temp = arr[i]
                    arr[i] = arr[i + 1]
                    arr[i + 1] = temp
                    swapped = True
            right -= 1
            if not swapped:
                break
            swapped = False
            for i in range(right, left, -1):
                compare_result = self.compare_items(arr[i - 1], arr[i], key_func)
                if (not reverse and compare_result > 0) or (reverse and compare_result < 0):
                    temp = arr[i - 1]
                    arr[i - 1] = arr[i]
                    arr[i] = temp
                    swapped = True
            left += 1
        return arr
    def compare_items(self, item1, item2, key_func):
        keys1 = key_func(item1)
        keys2 = key_func(item2)
        for i in range(len(keys1)):
            if keys1[i] < keys2[i]:
                return -1
            elif keys1[i] > keys2[i]:
                return 1
        return 0
    def report1_specialty_surname(self):
        print("ОТЧЕТ 1: Полный список всех соискателей")
        print("Сортировка: специальность (по возрастанию) + фамилия (по возрастанию)")
        if len(self.database) == 0:
            print("База данных пуста!")
            return
        def key_func_specialty_surname(applicant):
            return (applicant.specialty, applicant.last_name)
        sorted_db = self.database[:]
        sorted_db = self.shaker_sort(sorted_db, key_func_specialty_surname, reverse=False)
        for i in range(len(sorted_db)):
            applicant = sorted_db[i]
            print(f"\n{i+1}. {applicant.get_full_name()}")
            print(f"   Специальность: {applicant.specialty}")
            print(f"   Стаж: {applicant.experience} лет")
            print(f"   Ожидаемый оклад: {applicant.expected_salary} руб.")
        print(f"\nВсего соискателей: {len(sorted_db)}")
    def report2_by_specialty(self):
        print("ОТЧЕТ 2: Список соискателей по специальности")
        print("Сортировка: стаж (по убыванию) + пол (по убыванию) + фамилия (по возрастанию)")
        if len(self.database) == 0:
            print("База данных пуста!")
            return
        specialties = []
        for i in range(len(self.database)):
            specialty = self.database[i].specialty
            found = False
            for j in range(len(specialties)):
                if specialties[j] == specialty:
                    found = True
                    break
            if not found:
                specialties.append(specialty)
        for i in range(len(specialties)):
            for j in range(i + 1, len(specialties)):
                if specialties[i] > specialties[j]:
                    temp = specialties[i]
                    specialties[i] = specialties[j]
                    specialties[j] = temp
        print("\nДоступные специальности:")
        for i in range(len(specialties)):
            print(f"{i+1}. {specialties[i]}")
        try:
            choice = int(input("\nВыберите номер специальности: "))
            if choice < 1 or choice > len(specialties):
                print("Неверный номер специальности!")
                return
            selected_specialty = specialties[choice - 1]
        except ValueError:
            print("Ошибка: введите числовое значение!")
            return
        filtered = []
        for i in range(len(self.database)):
            if self.database[i].specialty == selected_specialty:
                filtered.append(self.database[i])
        if len(filtered) == 0:
            print(f"\nНет соискателей по специальности '{selected_specialty}'")
            return
        def key_func_experience_gender_surname(applicant):
            gender_value = 1 if applicant.gender == "м" else 0
            return (applicant.experience, gender_value, applicant.last_name)
        filtered = self.shaker_sort(filtered, key_func_experience_gender_surname, reverse=True)
        print(f"\nСоискатели по специальности '{selected_specialty}':")
        for i in range(len(filtered)):
            applicant = filtered[i]
            print(f"\n{i+1}. {applicant.get_full_name()}")
            print(f"   Стаж: {applicant.experience} лет")
            print(f"   Пол: {applicant.gender}")
            print(f"   Ожидаемый оклад: {applicant.expected_salary} руб.")
            languages_str = ""
            if applicant.languages:
                for j in range(len(applicant.languages)):
                    languages_str += applicant.languages[j]
                    if j != len(applicant.languages) - 1:
                        languages_str += ", "
            else:
                languages_str = "нет"
            print(f"   Иностранные языки: {languages_str}")
        print(f"\nВсего соискателей по специальности '{selected_specialty}': {len(filtered)}")
    def report3_by_salary_range(self):
        print("ОТЧЕТ 3: Список соискателей по диапазону оклада")
        print("Сортировка: оклад (по убыванию) + фамилия (по возрастанию)")
        if len(self.database) == 0:
            print("База данных пуста!")
            return
        try:
            n1 = float(input("Введите нижнюю границу оклада (N1): "))
            n2 = float(input("Введите верхнюю границу оклада (N2): "))
            if n1 < 0 or n2 < 0:
                print("Оклад не может быть отрицательным!")
                return
            if n1 > n2:
                temp = n1
                n1 = n2
                n2 = temp
                print(f"\nГраницы были автоматически поменяны местами: от {n1} до {n2}")
        except ValueError:
            print("Ошибка: введите числовое значение!")
            return
        filtered = []
        for i in range(len(self.database)):
            salary = self.database[i].expected_salary
            if salary >= n1 and salary <= n2:
                filtered.append(self.database[i])
        if len(filtered) == 0:
            print(f"\nНет соискателей с ожидаемым окладом от {n1} до {n2} руб.")
            return
        def key_func_salary_surname(applicant):
            return (applicant.expected_salary, applicant.last_name)
        filtered = self.shaker_sort(filtered, key_func_salary_surname, reverse=True)
        print(f"\nСоискатели с ожидаемым окладом от {n1} до {n2} руб.:")
        for i in range(len(filtered)):
            applicant = filtered[i]
            print(f"\n{i+1}. {applicant.get_full_name()}")
            print(f"   Специальность: {applicant.specialty}")
            print(f"   Стаж: {applicant.experience} лет")
            print(f"   Ожидаемый оклад: {applicant.expected_salary} руб.")
            languages_str = ""
            if applicant.languages:
                for j in range(len(applicant.languages)):
                    languages_str += applicant.languages[j]
                    if j != len(applicant.languages) - 1:
                        languages_str += ", "
            else:
                languages_str = "нет"
            print(f"   Иностранные языки: {languages_str}")
        print(f"\nВсего соискателей в диапазоне оклада: {len(filtered)}")
    def display_all_applicants(self):
        print("СПИСОК ВСЕХ СОИСКАТЕЛЕЙ")
        if len(self.database) == 0:
            print("База данных пуста!")
            return
        for i in range(len(self.database)):
            applicant = self.database[i]
            print(f"\n{i+1}. {applicant.get_full_name()}")
            print(f"   Специальность: {applicant.specialty}")
            print(f"   Стаж: {applicant.experience} лет")
            print(f"   Ожидаемый оклад: {applicant.expected_salary} руб.")
        print(f"\nВсего соискателей: {len(self.database)}")
    def display_statistics(self):
        print("СТАТИСТИКА БАЗЫ ДАННЫХ")
        if len(self.database) == 0:
            print("База данных пуста!")
            return
        total = len(self.database)
        male_count = 0
        female_count = 0
        for i in range(total):
            if self.database[i].gender == "м":
                male_count += 1
            else:
                female_count += 1
        specialties = {}
        for i in range(total):
            specialty = self.database[i].specialty
            if specialty in specialties:
                specialties[specialty] += 1
            else:
                specialties[specialty] = 1
        total_salary = 0
        total_experience = 0
        for i in range(total):
            total_salary += self.database[i].expected_salary
            total_experience += self.database[i].experience
        avg_salary = total_salary / total if total > 0 else 0
        avg_experience = total_experience / total if total > 0 else 0
        print(f"Общее количество соискателей: {total}")
        print(f"Мужчины: {male_count} ({male_count/total*100:.1f}%)")
        print(f"Женщины: {female_count} ({female_count/total*100:.1f}%)")
        print(f"\nСредний ожидаемый оклад: {avg_salary:.0f} руб.")
        print(f"Средний стаж работы: {avg_experience:.1f} лет")
        print("\nРаспределение по специальностям:")
        specialty_names = []
        for key in specialties:
            specialty_names.append(key)
        for i in range(len(specialty_names)):
            for j in range(i + 1, len(specialty_names)):
                if specialty_names[i] > specialty_names[j]:
                    temp = specialty_names[i]
                    specialty_names[i] = specialty_names[j]
                    specialty_names[j] = temp
        for i in range(len(specialty_names)):
            specialty = specialty_names[i]
            count = specialties[specialty]
            percentage = count / total * 100
            print(f"  {specialty}: {count} чел. ({percentage:.1f}%)")
    def run(self):
        while True:
            print("КАДРОВОЕ АГЕНТСТВО - ГЛАВНОЕ МЕНЮ")
            print("1. Просмотреть всех соискателей")
            print("2. Отчет 1: Все соискатели (специальность + фамилия)")
            print("3. Отчет 2: Соискатели по специальности (стаж + пол + фамилия)")
            print("4. Отчет 3: Соискатели по диапазону оклада (оклад + фамилия)")
            print("5. Статистика базы данных")
            print("0. Выход")           
            choice = input("Выберите действие: ")
            if choice == "1":
                self.display_all_applicants()
            elif choice == "2":
                self.report1_specialty_surname()
            elif choice == "3":
                self.report2_by_specialty()
            elif choice == "4":
                self.report3_by_salary_range()
            elif choice == "5":
                self.display_statistics()
            elif choice == "0":
                print("\nСпасибо за использование программы! До свидания!")
                break
            else:
                print("\nНеверный выбор! Пожалуйста, выберите действие из меню.")
            input("\nНажмите Enter для продолжения...")
def main():
    print("ПРОГРАММА 'КАДРОВОЕ АГЕНТСТВО'")
    print("Разработчик: Система управления базой данных соискателей")
    agency = EmploymentAgency()
    agency.run()
main()