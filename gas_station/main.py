"""
Главный модуль системы управления АЗС
"""
import os
from operations import AZSOperations

class AZSConsole:
    def __init__(self):
        self.azs = AZSOperations()
        self.running = True
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Вывод заголовка"""
        print("=" * 50)
        print("АЗС <<СеверНефть>>")
        print("Система управления заправочной станцией")
        print("=" * 50)
        print()
        
        # Проверка и вывод предупреждений
        disabled_cisterns = self.azs.check_low_levels()
        if disabled_cisterns:
            print("ВНИМАНИЕ!")
            print("Обнаружены отключённые цистерны:")
            for cistern in disabled_cisterns:
                reason = "(низкий уровень топлива)" if cistern.current_volume < cistern.min_level else ""
                print(f" - {cistern.id} {reason}")
            print()
    
    def print_menu(self):
        """Вывод главного меню (Раздел 4)"""
        print("Выберите действие:")
        print("1) Обслужить клиента (касса)")
        print("2) Проверить состояние цистерн")
        print("3) Оформить пополнение топлива")
        print("4) Баланс и статистика")
        print("5) История операций")
        print("6) Перекачка топлива")
        print("7) Управление цистернами")
        print("8) Состояние колонок")
        print("9) EMERGENCY - аварийная ситуация")
        if self.azs.emergency_mode:
            print("10) Отключить аварийный режим")
        print("0) Выход")
        print("-" * 40)
    
    def serve_customer(self):
        """5.1 Обслуживание клиента"""
        print("\n--- Обслуживание клиента ---\n")
        
        # Выбор колонки
        print("Доступные колонки:")
        for i in range(1, 9):
            print(f"{i}) Колонка {i}")
        print()
        
        try:
            column_id = int(input("Выберите колонку: "))
            if column_id < 1 or column_id > 8:
                print("ОШИБКА: Неверный номер колонки")
                return
        except ValueError:
            print("ОШИБКА: Введите число")
            return
        
        print(f"\nКолонка {column_id}\n")
        
        # Выбор типа топлива
        column = self.azs.columns[column_id - 1]
        fuels = list(column.available_fuels.keys())
        
        print("Доступные виды топлива:")
        for i, fuel_type in enumerate(fuels, 1):
            cistern_id = column.available_fuels[fuel_type]
            price = self.azs.fuel_prices.get(fuel_type, 0)
            print(f"{i}) {fuel_type} ({cistern_id}) - {price:.2f} ₽/л")
        print()
        
        try:
            fuel_choice = int(input("Выберите тип топлива: "))
            if fuel_choice < 1 or fuel_choice > len(fuels):
                print("ОШИБКА: Неверный выбор")
                return
            fuel_type = fuels[fuel_choice - 1]
        except ValueError:
            print("ОШИБКА: Введите число")
            return
        
        # Ввод количества литров
        try:
            liters = float(input("Введите количество литров: "))
            if liters <= 0:
                print("ОШИБКА: Количество должно быть положительным")
                return
        except ValueError:
            print("ОШИБКА: Введите число")
            return
        
        # Подтверждение
        price = self.azs.fuel_prices.get(fuel_type, 0)
        total = liters * price
        print(f"\nСтоимость: {liters} л × {price:.2f} ₽ = {total:.2f} ₽")
        
        confirm = input("Подтвердить оплату? (да/нет): ").lower()
        if confirm != 'да':
            print("Операция отменена")
            return
        
        # Выполнение операции
        success, message = self.azs.serve_customer(column_id, fuel_type, liters)
        print(f"\n{message}")
    
    def check_cisterns(self):
        """5.2 Проверка состояния цистерн"""
        print("\n--- Состояние цистерн ---\n")
        
        status_list = self.azs.get_cistern_status()
        for status in status_list:
            print(status)
    
    def refuel_cistern_menu(self):
        """5.3 Оформление пополнения топлива"""
        print("\n--- Оформление пополнения топлива ---\n")
        
        # Выбор цистерны
        print("Доступные цистерны:")
        for i, cistern in enumerate(self.azs.cisterns, 1):
            print(f"{i}) {cistern.id} - {cistern.fuel_type} ({cistern.current_volume:.0f}/{cistern.max_volume:.0f} л)")
        print()
        
        try:
            choice = int(input("Выберите цистерну: "))
            if choice < 1 or choice > len(self.azs.cisterns):
                print("ОШИБКА: Неверный выбор")
                return
            cistern = self.azs.cisterns[choice - 1]
        except ValueError:
            print("ОШИБКА: Введите число")
            return
        
        # Ввод количества
        try:
            liters = float(input(f"Введите количество литров для доливки (до {cistern.max_volume - cistern.current_volume:.0f} л): "))
            if liters <= 0:
                print("ОШИБКА: Количество должно быть положительным")
                return
        except ValueError:
            print("ОШИБКА: Введите число")
            return
        
        # Выполнение операции
        success, message = self.azs.refuel_cistern(cistern.id, liters)
        print(f"\n{message}")
    
    def show_statistics(self):
        """5.4 Баланс и статистика"""
        print("\n--- Баланс и статистика ---\n")
        
        stats = self.azs.get_statistics()
        print(f"Обслужено автомобилей: {stats['total_cars']}")
        print(f"Общий доход: {stats['total_income']:,.2f} ₽")
        print("\nПродано топлива:")
        
        for fuel_type, data in stats['fuel_stats'].items():
            print(f"{fuel_type} — {data['liters']} л ({data['income']:,.0f} ₽)")
    
    def show_history(self):
        """5.5 История операций"""
        print("\n--- История операций ---\n")
        
        history = self.azs.get_history(limit=10)
        if not history:
            print("История операций пуста")
            return
        
        for op in reversed(history):  # Последние операции сначала
            print(f"[{op.timestamp}] {op.description}")
            if op.operation_type == 'sale':
                details = op.details
                print(f"  Колонка: {details['column_id']}, Тип: {details['fuel_type']}")
                print(f"  Количество: {details['liters']} л, Сумма: {details['total_price']:.2f} ₽")
            print()
    
    def transfer_fuel_menu(self):
        """5.6 Перекачка топлива"""
        print("\n--- Перекачка топлива ---\n")
        
        # Выбор исходной цистерны
        print("Исходные цистерны (доступные для перекачки):")
        available_sources = [c for c in self.azs.cisterns if c.is_active and c.current_volume > 0]
        
        for i, cistern in enumerate(available_sources, 1):
            print(f"{i}) {cistern.id} - {cistern.current_volume:.0f} л")
        print()
        
        try:
            source_choice = int(input("Выберите исходную цистерну: "))
            if source_choice < 1 or source_choice > len(available_sources):
                print("ОШИБКА: Неверный выбор")
                return
            source = available_sources[source_choice - 1]
        except ValueError:
            print("ОШИБКА: Введите число")
            return
        
        # Выбор целевой цистерны
        print(f"\nЦелевые цистерны (тип: {source.fuel_type}):")
        available_targets = [c for c in self.azs.cisterns 
                           if c.id != source.id and c.fuel_type == source.fuel_type]
        
        for i, cistern in enumerate(available_targets, 1):
            available_space = cistern.max_volume - cistern.current_volume
            print(f"{i}) {cistern.id} - доступно {available_space:.0f} л")
        print()
        
        try:
            target_choice = int(input("Выберите целевую цистерну: "))
            if target_choice < 1 or target_choice > len(available_targets):
                print("ОШИБКА: Неверный выбор")
                return
            target = available_targets[target_choice - 1]
        except ValueError:
            print("ОШИБКА: Введите число")
            return
        
        # Ввод количества
        try:
            max_liters = min(source.current_volume, target.max_volume - target.current_volume)
            liters = float(input(f"Введите количество литров (до {max_liters:.0f} л): "))
            if liters <= 0 or liters > max_liters:
                print(f"ОШИБКА: Количество должно быть от 0 до {max_liters:.0f}")
                return
        except ValueError:
            print("ОШИБКА: Введите число")
            return
        
        # Подтверждение
        print(f"\nПерекачать {liters} л из {source.id} в {target.id}?")
        confirm = input("Подтвердить? (да/нет): ").lower()
        if confirm != 'да':
            print("Операция отменена")
            return
        
        # Выполнение операции
        success, message = self.azs.transfer_fuel(source.id, target.id, liters)
        print(f"\n{message}")
    
    def manage_cisterns(self):
        """5.7 Управление цистернами"""
        print("\n--- Управление цистернами ---\n")
        
        print("Доступные действия:")
        print("1) Включить цистерну")
        print("2) Выключить цистерну")
        print()
        
        try:
            action = int(input("Выберите действие: "))
            if action not in [1, 2]:
                print("ОШИБКА: Неверный выбор")
                return
        except ValueError:
            print("ОШИБКА: Введите число")
            return
        
        enable = (action == 1)
        
        if enable:
            print("\nЦистерны, доступные для включения:")
            available = [c for c in self.azs.cisterns 
                        if not c.is_active and c.current_volume >= c.min_level]
        else:
            print("\nЦистерны, доступные для выключения:")
            available = [c for c in self.azs.cisterns if c.is_active]
        
        if not available:
            print("Нет доступных цистерн для этого действия")
            return
        
        for i, cistern in enumerate(available, 1):
            status = "ВКЛ" if cistern.is_active else "ВЫКЛ"
            print(f"{i}) {cistern.id} | {cistern.current_volume:.0f} / {cistern.max_volume:.0f} л | {status}")
        print()
        
        try:
            choice = int(input("Выберите цистерну: "))
            if choice < 1 or choice > len(available):
                print("ОШИБКА: Неверный выбор")
                return
            cistern = available[choice - 1]
        except ValueError:
            print("ОШИБКА: Введите число")
            return
        
        # Выполнение операции
        success, message = self.azs.toggle_cistern(cistern.id, enable)
        print(f"\n{message}")
    
    def show_columns(self):
        """5.8 Состояние колонок"""
        print("\n--- Состояние колонок ---\n")
        
        status_list = self.azs.get_column_status()
        for status in status_list:
            print(status)
    
    def emergency_menu(self):
        """5.9 Аварийная ситуация"""
        if self.azs.emergency_mode:
            print("\n--- Отключение аварийного режима ---\n")
            print("ВНИМАНИЕ: Аварийный режим активен!")
            confirm = input("Отключить аварийный режим? (да/нет): ").lower()
            if confirm == 'да':
                success, message = self.azs.disable_emergency()
                print(f"\n{message}")
        else:
            print("\n--- EMERGENCY - аварийная ситуация ---\n")
            print("ВНИМАНИЕ: Это приведет к блокировке ВСЕХ систем!")
            print("Будут выполнены:")
            print("1. Все цистерны будут отключены")
            print("2. Заправка прекратит работу")
            print("3. Будут вызваны аварийные службы")
            print("4. Выход из аварийного режима только вручную")
            print()
            
            confirm = input("АКТИВИРОВАТЬ АВАРИЙНЫЙ РЕЖИМ? (ДА/нет): ").upper()
            if confirm == 'ДА':
                success, message = self.azs.trigger_emergency()
                print(f"\n{message}")
                print("Аварийные службы вызваны!")
            else:
                print("Аварийный режим не активирован")
    
    def run(self):
        """Главный цикл программы"""
        while self.running:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            try:
                choice = input("> ")
                
                if choice == '0':
                    print("\nСохранение данных...")
                    self.azs.save_all()
                    print("Выход из системы. До свидания!")
                    self.running = False
                
                elif choice == '1':
                    self.serve_customer()
                
                elif choice == '2':
                    self.check_cisterns()
                
                elif choice == '3':
                    self.refuel_cistern_menu()
                
                elif choice == '4':
                    self.show_statistics()
                
                elif choice == '5':
                    self.show_history()
                
                elif choice == '6':
                    self.transfer_fuel_menu()
                
                elif choice == '7':
                    self.manage_cisterns()
                
                elif choice == '8':
                    self.show_columns()
                
                elif choice == '9':
                    self.emergency_menu()
                
                elif choice == '10' and self.azs.emergency_mode:
                    self.emergency_menu()
                
                else:
                    print("\nОШИБКА: Неверный выбор")
                
                if self.running and choice != '0':
                    input("\nНажмите Enter для возврата в меню...")
            
            except KeyboardInterrupt:
                print("\n\nПрервано пользователем")
                self.azs.save_all()
                self.running = False
            except Exception as e:
                print(f"\nОШИБКА: {e}")
                input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    app = AZSConsole()
    app.run()