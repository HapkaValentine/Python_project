import datetime
import re
class Applicant:
    """Класс для представления соискателя"""
    def __init__(self, last_name, first_name, patronymic, gender, birth_date,
                 specialty, experience, languages, expected_salary):
        """
        Инициализация объекта соискателя
        Параметры:
        last_name - фамилия
        first_name - имя
        patronymic - отчество
        gender - пол ('м' или 'ж')
        birth_date - дата рождения в формате (год, месяц, день)
        specialty - специальность
        experience - стаж работы (в годах)
        languages - список иностранных языков
        expected_salary - ожидаемый оклад
        """
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.gender = gender
        self.birth_date = birth_date
        self.speciality = specialty
        self.experience = experience
        self.languages = languages
        self.expected_salary = expected_salary
    def get_full_name(self):
        """Получить полное имя соискателя"""
        return f"{self.last_name} {self.first_name} {self.patronymic}"
    def get_age(self):
        """Вычислить возраст соискателя"""
        today = datetime.date.today()
        birth_date = datetime.date(*self.birth_date)
        age = today.year - birth_date.year
        # Корректировка, если день рождения еще не наступил в текущем году
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age
    def __str__(self):
        """Строковое представление объекта"""
        languages_str = ', '.join(self.languages) if self.languages else "нет"
        birth_date_str = f"{self.birth_date[2]:02d}.{self.birth_date[1]:02d}.{self.birth_date[0]}"
        return (f"ФИО: {self.get_full_name()}\n"
                f"Пол: {self.gender}\n"
                f"Дата рождения: {birth_date_str} (Возраст: {self.get_age()})\n"
                f"Специальность: {self.speciality}\n"
                f"Стаж: {self.experience} лет\n"
                f"Иностранные языки: {languages_str}\n"
                f"Ожидаемый оклад: {self.expected_salary:,} руб.\n")
class EmploymentAgency:
    """Класс для управления базой данных кадрового агентства"""
    def __init__(self):
        """Инициализация базы данных"""
        self.database = []
        self.initialize_sample_data()
    def initialize_sample_data(self):
        """Инициализация базы тестовыми данными"""
        sample_data = [
            # Программисты
            ("Иванов", "Иван", "Иванович", "м", (1990, 5, 15), "Программист Python", 5, ["Английский"], 150000),
            ("Петрова", "Мария", "Сергеевна", "ж", (1992, 8, 22), "Программист Python", 3, ["Английский", "Немецкий"],
             120000),
            ("Смирнов", "Алексей", "Петрович", "м", (1988, 3, 10), "Программист Java", 8, ["Английский"], 180000),
            ("Кузнецова", "Елена", "Владимировна", "ж", (1995, 11, 30), "Программист Java", 2,
             ["Английский", "Французский"], 100000),
            ("Соколов", "Дмитрий", "Александрович", "м", (1991, 7, 18), "Программист C++", 6, ["Английский"], 160000),
            # Аналитики
            ("Васильев", "Сергей", "Игоревич", "м", (1985, 2, 14), "Аналитик данных", 10, ["Английский"], 200000),
            ("Павлова", "Ольга", "Николаевна", "ж", (1993, 9, 5), "Аналитик данных", 4, ["Английский", "Испанский"],
             130000),
            ("Громов", "Андрей", "Викторович", "м", (1989, 12, 20), "Аналитик данных", 7, ["Английский", "Китайский"],
             170000),
            # Менеджеры
            ("Новиков", "Артем", "Сергеевич", "м", (1987, 6, 25), "Менеджер проектов", 9, ["Английский"], 190000),
            ("Морозова", "Анна", "Дмитриевна", "ж", (1994, 4, 12), "Менеджер проектов", 3,
             ["Английский", "Французский"], 125000),
            ("Федоров", "Максим", "Олегович", "м", (1990, 1, 8), "Менеджер проектов", 5, ["Английский"], 155000),
            # Тестировщики
            ("Волков", "Роман", "Андреевич", "м", (1992, 10, 17), "Тестировщик", 4, ["Английский"], 110000),
            ("Алексеева", "Татьяна", "Валерьевна", "ж", (1996, 3, 3), "Тестировщик", 1, ["Английский"], 90000),
            ("Лебедев", "Игорь", "Павлович", "м", (1988, 8, 28), "Тестировщик", 7, ["Английский", "Немецкий"], 140000),
            # Дизайнеры
            ("Семенов", "Виктор", "Геннадьевич", "м", (1993, 7, 19), "Дизайнер UI/UX", 5, ["Английский"], 135000),
            ("Егорова", "Ксения", "Анатольевна", "ж", (1995, 12, 7), "Дизайнер UI/UX", 2, ["Английский", "Итальянский"],
             105000),
            # DevOps
            ("Козлов", "Николай", "Федорович", "м", (1986, 5, 23), "DevOps инженер", 11, ["Английский"], 220000),
            ("Захарова", "Юлия", "Игоревна", "ж", (1991, 2, 14), "DevOps инженер", 4, ["Английский"], 145000),
            # Системные администраторы
            ("Орлов", "Павел", "Михайлович", "м", (1984, 9, 11), "Системный администратор", 15, ["Английский"], 180000),
            ("Макарова", "Светлана", "Владимировна", "ж", (1990, 6, 30), "Системный администратор", 6, ["Английский"],
             130000),
            # Маркетологи
            ("Борисов", "Константин", "Александрович", "м", (1989, 4, 8), "Маркетолог", 8, ["Английский", "Испанский"],
             160000),
            ("Тихонова", "Екатерина", "Сергеевна", "ж", (1994, 11, 21), "Маркетолог", 3, ["Английский"], 115000),
            # Бухгалтеры
            ("Антонов", "Георгий", "Васильевич", "м", (1983, 12, 5), "Бухгалтер", 12, ["Английский"], 140000),
            ("Филиппова", "Наталья", "Петровна", "ж", (1988, 10, 17), "Бухгалтер", 9, ["Английский", "Немецкий"],
             135000),
            # HR-специалисты
            ("Давыдов", "Михаил", "Олегович", "м", (1992, 7, 4), "HR-специалист", 5, ["Английский"], 120000),
            ("Соболева", "Ирина", "Александровна", "ж", (1993, 3, 28), "HR-специалист", 4,
             ["Английский", "Французский"], 125000),
        ]
        for data in sample_data:
            applicant = Applicant(*data)
            self.database.append(applicant)
    def add_applicant(self):
        """Добавление нового соискателя в базу данных"""
        print("ДОБАВЛЕНИЕ НОВОГО СОИСКАТЕЛЯ")
        try:
            last_name = input("Введите фамилию: ").strip()
            if not last_name:
                raise ValueError("Фамилия не может быть пустой")
            first_name = input("Введите имя: ").strip()
            if not first_name:
                raise ValueError("Имя не может быть пустым")
            patronymic = input("Введите отчество: ").strip()
            gender = input("Введите пол (м/ж): ").strip().lower()
            if gender not in ['м', 'ж']:
                raise ValueError("Пол должен быть 'м' или 'ж'")
            birth_date_input = input("Введите дату рождения (ГГГГ-ММ-ДД): ").strip()
            birth_match = re.match(r'(\d{4})-(\d{1,2})-(\d{1,2})', birth_date_input)
            if not birth_match:
                raise ValueError("Дата должна быть в формате ГГГГ-ММ-ДД")
            year, month, day = map(int, birth_match.groups())
            birth_date = (year, month, day)
            # Проверка корректности даты
            try:
                datetime.date(year, month, day)
            except ValueError:
                raise ValueError("Некорректная дата")
            specialty = input("Введите специальность: ").strip()
            if not specialty:
                raise ValueError("Специальность не может быть пустой")
            experience = float(input("Введите стаж работы (лет): ").strip())
            if experience < 0:
                raise ValueError("Стаж не может быть отрицательным")
            languages_input = input("Введите иностранные языки (через запятую): ").strip()
            languages = [lang.strip() for lang in languages_input.split(',') if lang.strip()]
            expected_salary = float(input("Введите ожидаемый оклад (руб.): ").strip())
            if expected_salary <= 0:
                raise ValueError("Оклад должен быть положительным числом")
            applicant = Applicant(last_name, first_name, patronymic, gender, birth_date,
                                  specialty, experience, languages, expected_salary)
            self.database.append(applicant)
            print(f"\nСоискатель {applicant.get_full_name()} успешно добавлен в базу!")
        except ValueError as e:
            print(f"\nОшибка: {e}")
        except Exception as e:
            print(f"\nНеизвестная ошибка: {e}")
    def remove_applicant(self):
        """Удаление соискателя из базы данных"""
        print("УДАЛЕНИЕ СОИСКАТЕЛЯ")
        if not self.database:
            print("База данных пуста!")
            return
        self.display_all_applicants()
        try:
            index = int(input("\nВведите номер соискателя для удаления (0 для отмены): ").strip())
            if index == 0:
                print("Операция отменена.")
                return
            if 1 <= index <= len(self.database):
                applicant = self.database.pop(index - 1)
                print(f"\nСоискатель {applicant.get_full_name()} успешно удален из базы!")
            else:
                print("\nНеверный номер соискателя!")
        except ValueError:
            print("\nОшибка: введите числовое значение!")
    def edit_applicant(self):
        """Редактирование данных соискателя"""
        print("РЕДАКТИРОВАНИЕ ДАННЫХ СОИСКАТЕЛЯ")
        if not self.database:
            print("База данных пуста!")
            return
        self.display_all_applicants()
        try:
            index = int(input("\nВведите номер соискателя для редактирования (0 для отмены): ").strip())
            if index == 0:
                print("Операция отменена.")
                return
            if not (1 <= index <= len(self.database)):
                print("\nНеверный номер соискателя!")
                return
            applicant = self.database[index - 1]
            print(f"\nТекущие данные соискателя:")
            print(applicant)
            print("\nВведите новые данные (оставьте поле пустым, чтобы оставить текущее значение):")
            last_name = input(f"Фамилия [{applicant.last_name}]: ").strip()
            if last_name:
                applicant.last_name = last_name
            first_name = input(f"Имя [{applicant.first_name}]: ").strip()
            if first_name:
                applicant.first_name = first_name
            patronymic = input(f"Отчество [{applicant.patronymic}]: ").strip()
            if patronymic:
                applicant.patronymic = patronymic
            gender = input(f"Пол [{applicant.gender}]: ").strip().lower()
            if gender in ['м', 'ж']:
                applicant.gender = gender
            elif gender:
                print("Предупреждение: пол должен быть 'м' или 'ж'. Текущее значение сохранено.")
            specialty = input(f"Специальность [{applicant.speciality}]: ").strip()
            if specialty:
                applicant.speciality = specialty
            experience = input(f"Стаж [{applicant.experience}]: ").strip()
            if experience:
                try:
                    applicant.experience = float(experience)
                except ValueError:
                    print("Предупреждение: стаж должен быть числом. Текущее значение сохранено.")
            languages_input = input(
                f"Языки [{', '.join(applicant.languages) if applicant.languages else 'нет'}]: ").strip()
            if languages_input:
                applicant.languages = [lang.strip() for lang in languages_input.split(',') if lang.strip()]
            expected_salary = input(f"Оклад [{applicant.expected_salary}]: ").strip()
            if expected_salary:
                try:
                    applicant.expected_salary = float(expected_salary)
                except ValueError:
                    print("Предупреждение: оклад должен быть числом. Текущее значение сохранено.")
            print(f"\nДанные соискателя {applicant.get_full_name()} успешно обновлены!")
        except ValueError:
            print("\nОшибка: введите числовое значение!")
    def display_all_applicants(self):
        """Отображение всех соискателей"""
        print("СПИСОК ВСЕХ СОИСКАТЕЛЕЙ")
        if not self.database:
            print("База данных пуста!")
            return
        for i, applicant in enumerate(self.database, 1):
            print(f"\n{i}. {applicant.get_full_name()}")
            print(f"   Специальность: {applicant.speciality}")
            print(f"   Стаж: {applicant.experience} лет")
            print(f"   Ожидаемый оклад: {applicant.expected_salary:,} руб.")
    def shaker_sort(self, arr, key_func):
        """
        Реализация шейкерной сортировки (cocktail shaker sort)
        Параметры:
        arr - массив для сортировки
        key_func - функция получения ключа сортировки
        """
        n = len(arr)
        left = 0
        right = n - 1
        while left <= right:
            # Проход слева направо
            for i in range(left, right):
                if key_func(arr[i]) > key_func(arr[i + 1]):
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
            right -= 1
            # Проход справа налево
            for i in range(right, left, -1):
                if key_func(arr[i - 1]) > key_func(arr[i]):
                    arr[i - 1], arr[i] = arr[i], arr[i - 1]
            left += 1
        return arr
    def report1_specialty_surname(self):
        """
        Отчет 1: Полный список всех соискателей,
        отсортированный по специальности (возрастание) + фамилия (возрастание)
        """
        print("ОТЧЕТ 1: Полный список всех соискателей")
        print("Сортировка: специальность (по возрастанию) + фамилия (по возрастанию)")
        if not self.database:
            print("База данных пуста!")
            return
        # Создаем копию базы для сортировки
        sorted_db = self.database.copy()
        # Определяем функцию ключа для сортировки
        def sort_key(applicant):
            return (applicant.speciality, applicant.last_name)
        # Применяем шейкерную сортировку
        sorted_db = self.shaker_sort(sorted_db, sort_key)
        # Выводим результаты
        for i, applicant in enumerate(sorted_db, 1):
            print(f"\n{i}. {applicant.get_full_name()}")
            print(f"   Специальность: {applicant.speciality}")
            print(f"   Стаж: {applicant.experience} лет")
            print(f"   Пол: {applicant.gender}")
            print(f"   Ожидаемый оклад: {applicant.expected_salary:,} руб.")
        print(f"\nВсего соискателей: {len(sorted_db)}")
    def report2_by_specialty(self):
        "Отчет 2: Список всех соискателей заданной специальности,отсортированный по стаж работы (убывание) + пол (убывание) + фамилия (возрастание)"
        print("ОТЧЕТ 2: Список соискателей по специальности")
        print("Сортировка: стаж (по убыванию) + пол (по убыванию) + фамилия (по возрастанию)")
        if not self.database:
            print("База данных пуста!")
            return
        # Получаем список всех специальностей
        specialties = sorted(set(applicant.speciality for applicant in self.database))
        print("\nДоступные специальности:")
        for i, specialty in enumerate(specialties, 1):
            print(f"{i}. {specialty}")
        try:
            choice = int(input("\nВыберите номер специальности: ").strip())
            if 1 <= choice <= len(specialties):
                selected_specialty = specialties[choice - 1]
            else:
                print("\nНеверный номер специальности!")
                return
        except ValueError:
            print("\nОшибка: введите числовое значение!")
            return
        # Фильтруем по специальности
        filtered = [app for app in self.database if app.speciality == selected_specialty]
        if not filtered:
            print(f"\nНет соискателей по специальности '{selected_specialty}'")
            return
        # Определяем функцию ключа для сортировки
        # Для убывающей сортировки используем отрицательные значения
        def sort_key(applicant):
            # Пол: 'м' > 'ж' для убывающей сортировки
            gender_value = 0 if applicant.gender == 'м' else 1
            return (-applicant.experience, -gender_value, applicant.last_name)
        # Применяем шейкерную сортировку
        filtered = self.shaker_sort(filtered, sort_key)
        # Выводим результаты
        print(f"\nСоискатели по специальности '{selected_specialty}':")
        for i, applicant in enumerate(filtered, 1):
            print(f"\n{i}. {applicant.get_full_name()}")
            print(f"   Стаж: {applicant.experience} лет")
            print(f"   Пол: {applicant.gender}")
            print(f"   Ожидаемый оклад: {applicant.expected_salary:,} руб.")
            print(f"   Иностранные языки: {', '.join(applicant.languages) if applicant.languages else 'нет'}")
        print(f"\nВсего соискателей по специальности '{selected_specialty}': {len(filtered)}")
    def report3_by_salary_range(self):
        "Отчет 3: Список всех соискателей, претендующих на оклад в диапазоне от N1 до N2,отсортированный по ожидаемый оклад (убывание) + фамилия (возрастание)"
        print("ОТЧЕТ 3: Список соискателей по диапазону оклада")
        print("Сортировка: оклад (по убыванию) + фамилия (по возрастанию)")
        if not self.database:
            print("База данных пуста!")
            return
        try:
            n1 = float(input("Введите нижнюю границу оклада (N1): ").strip())
            n2 = float(input("Введите верхнюю границу оклада (N2): ").strip())
            if n1 > n2:
                n1, n2 = n2, n1  # Меняем местами, если введено неправильно
                print(f"\nГраницы были автоматически поменяны местами: от {n1} до {n2}")
            if n1 < 0 or n2 < 0:
                raise ValueError("Оклад не может быть отрицательным")
        except ValueError as e:
            print(f"\nОшибка: {e}")
            return
        # Фильтруем по диапазону оклада
        filtered = [app for app in self.database if n1 <= app.expected_salary <= n2]
        if not filtered:
            print(f"\nНет соискателей с ожидаемым окладом от {n1} до {n2} руб.")
            return
        # Определяем функцию ключа для сортировки
        def sort_key(applicant):
            return (-applicant.expected_salary, applicant.last_name)
        # Применяем шейкерную сортировку
        filtered = self.shaker_sort(filtered, sort_key)
        # Выводим результаты
        print(f"\nСоискатели с ожидаемым окладом от {n1:,} до {n2:,} руб.:")
        for i, applicant in enumerate(filtered, 1):
            print(f"\n{i}. {applicant.get_full_name()}")
            print(f"   Специальность: {applicant.speciality}")
            print(f"   Стаж: {applicant.experience} лет")
            print(f"   Ожидаемый оклад: {applicant.expected_salary:,} руб.")
            print(f"   Иностранные языки: {', '.join(applicant.languages) if applicant.languages else 'нет'}")
        print(f"\nВсего соискателей в диапазоне оклада: {len(filtered)}")
    def display_statistics(self):
            "Отображение статистики по базе данных"
            print("\n" + "=" * 50)
            print("СТАТИСТИКА БАЗЫ ДАННЫХ")
            if not self.database:
                print("База данных пуста!")
                return
            total = len(self.database)
        # Статистика по полу
            male_count = sum(1 for app in self.database if app.gender == 'м')
            female_count = total - male_count
        # Статистика по специальностям
            specialties = {}
            for app in self.database:
                specialties[app.speciality] = specialties.get(app.speciality, 0) + 1
        # Средний оклад
            avg_salary = sum(app.expected_salary for app in self.database) / total
        # Средний стаж
            avg_experience = sum(app.experience for app in self.database) / total
            print(f"Общее количество соискателей: {total}")
            print(f"Мужчины: {male_count} ({male_count / total * 100:.1f}%)")
            print(f"Женщины: {female_count} ({female_count / total * 100:.1f}%)")
            print(f"\nСредний ожидаемый оклад: {avg_salary:,.0f} руб.")
            print(f"Средний стаж работы: {avg_experience:.1f} лет")
            print("\nРаспределение по специальностям:")
            for specialty, count in sorted(specialties.items()):
                percentage = count / total * 100
                print(f"  {specialty}: {count} чел. ({percentage:.1f}%)")
    def save_to_file(self):
        "Сохранение базы данных в файл"
        try:
            filename = input("Введите имя файла для сохранения (по умолчанию: database.txt): ").strip()
            if not filename:
                filename = "database.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("БАЗА ДАННЫХ КАДРОВОГО АГЕНТСТВА\n")
                for i, applicant in enumerate(self.database, 1):
                    f.write(f"{i}. {applicant.get_full_name()}\n")
                    f.write(f"   Пол: {applicant.gender}\n")
                    birth_date_str = f"{applicant.birth_date[2]:02d}.{applicant.birth_date[1]:02d}.{applicant.birth_date[0]}"
                    f.write(f"   Дата рождения: {birth_date_str}\n")
                    f.write(f"   Возраст: {applicant.get_age()} лет\n")
                    f.write(f"   Специальность: {applicant.speciality}\n")
                    f.write(f"   Стаж: {applicant.experience} лет\n")
                    f.write(
                        f"   Иностранные языки: {', '.join(applicant.languages) if applicant.languages else 'нет'}\n")
                    f.write(f"   Ожидаемый оклад: {applicant.expected_salary:,} руб.\n")
                    f.write("-" * 50 + "\n")
                f.write(f"\nВсего записей: {len(self.database)}\n")
            print(f"\nБаза данных успешно сохранена в файл '{filename}'!")
        except Exception as e:
            print(f"\nОшибка при сохранении файла: {e}")
    def run(self):
        "Основной цикл программы с меню"
        while True:
            print("КАДРОВОЕ АГЕНТСТВО - ГЛАВНОЕ МЕНЮ")
            print("1. Просмотреть всех соискателей")
            print("2. Добавить нового соискателя")
            print("3. Удалить соискателя")
            print("4. Редактировать данные соискателя")
            print("5. Статистика базы данных")
            print("6. Отчет 1: Все соискатели (специальность + фамилия)")
            print("7. Отчет 2: Соискатели по специальности (стаж + пол + фамилия)")
            print("8. Отчет 3: Соискатели по диапазону оклада (оклад + фамилия)")
            print("9. Сохранить базу в файл")
            print("0. Выход")
            choice = input("Выберите действие: ").strip()
            if choice == "1":
                self.display_all_applicants()
            elif choice == "2":
                self.add_applicant()
            elif choice == "3":
                self.remove_applicant()
            elif choice == "4":
                self.edit_applicant()
            elif choice == "5":
                self.display_statistics()
            elif choice == "6":
                self.report1_specialty_surname()
            elif choice == "7":
                self.report2_by_specialty()
            elif choice == "8":
                self.report3_by_salary_range()
            elif choice == "9":
                self.save_to_file()
            elif choice == "0":
                print("\nСпасибо за использование программы! До свидания!")
                break
            else:
                print("\nНеверный выбор! Пожалуйста, выберите действие из меню.")
            input("\nНажмите Enter для продолжения...")
def main():
    """Основная функция программы"""
    print("ПРОГРАММА 'КАДРОВОЕ АГЕНТСТВО'")
    print("Разработчик: Система управления базой данных соискателей")
    print("Версия: 1.0")
    print("\nИнициализация базы данных...")
    # Создаем экземпляр агентства
    agency = EmploymentAgency()
    print(f"База данных успешно загружена! Записей: {len(agency.database)}")
    # Запускаем основной цикл
    agency.run()
main()