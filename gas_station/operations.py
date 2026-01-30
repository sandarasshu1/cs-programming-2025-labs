"""
Бизнес-логика системы управления АЗС
"""
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from models import *
from storage import Storage

class AZSOperations:
    def __init__(self):
        self.storage = Storage()
        self.cisterns = self.storage.load_cisterns()
        self.columns = self.storage.load_columns()
        self.stats = self.storage.load_statistics()
        self.history = self.storage.load_history()
        self.transactions = self.storage.load_transactions()
        
        # Цены на топливо (можно вынести в конфиг)
        self.fuel_prices = {
            "АИ-92": 57.47,
            "АИ-95": 58.30,
            "АИ-98": 64.50,
            "ДТ": 52.00
        }
        
        # Счётчики для ID
        self.next_op_id = len(self.history) + 1
        self.next_transaction_id = len(self.transactions) + 1
        
        # Аварийный режим
        self.emergency_mode = False
    
    def save_all(self):
        """Сохранение всех данных"""
        self.storage.save_cisterns(self.cisterns)
        self.storage.save_columns(self.columns)
        self.storage.save_statistics(self.stats)
    
    def get_disabled_cisterns(self) -> List[Cistern]:
        """Получение отключённых цистерн"""
        return [c for c in self.cisterns if not c.is_active]
    
    def check_low_levels(self):
        """Проверка низкого уровня топлива в цистернах (Раздел 2.2)"""
        disabled_cisterns = []
        for cistern in self.cisterns:
            if cistern.current_volume < cistern.min_level:
                if cistern.is_active:
                    cistern.is_active = False
                    self._add_operation(
                        "toggle_cistern",
                        f"Автоматическое отключение цистерны {cistern.id} (низкий уровень)",
                        {"cistern_id": cistern.id, "action": "auto_disable"}
                    )
                disabled_cisterns.append(cistern)
        return disabled_cisterns
    
    def serve_customer(self, column_id: int, fuel_type: str, liters: float) -> Tuple[bool, str]:
        """5.1 Обслуживание клиента (касса)"""
        if self.emergency_mode:
            return False, "Аварийный режим! Заправка невозможна."
        
        # Проверка колонки
        if column_id < 1 or column_id > len(self.columns):
            return False, "Неверный номер колонки"
        
        column = self.columns[column_id - 1]
        if not column.is_active:
            return False, "Колонка неактивна"
        
        # Проверка типа топлива
        if fuel_type not in column.available_fuels:
            return False, f"Топливо {fuel_type} недоступно на этой колонке"
        
        cistern_id = column.available_fuels[fuel_type]
        cistern = next((c for c in self.cisterns if c.id == cistern_id), None)
        
        if not cistern:
            return False, f"Цистерна {cistern_id} не найдена"
        
        # Проверка состояния цистерны
        if not cistern.is_active:
            return False, f"Цистерна {cistern.id} отключена"
        
        # Проверка достаточности топлива
        if cistern.current_volume < liters:
            return False, f"Недостаточно топлива в цистерне. Доступно: {cistern.current_volume:.1f} л"
        
        # Рассчёт стоимости
        price_per_liter = self.fuel_prices.get(fuel_type, 0)
        total_price = liters * price_per_liter
        
        # Создание транзакции
        transaction = Transaction(
            id=self.next_transaction_id,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            column_id=column_id,
            fuel_type=fuel_type,
            liters=liters,
            price_per_liter=price_per_liter,
            total_price=total_price
        )
        
        # Списание топлива
        cistern.current_volume -= liters
        
        # Обновление статистики
        self.stats.total_cars_served += 1
        self.stats.total_income += total_price
        
        if fuel_type not in self.stats.fuel_stats:
            self.stats.fuel_stats[fuel_type] = {"liters": 0, "income": 0}
        
        self.stats.fuel_stats[fuel_type]["liters"] += liters
        self.stats.fuel_stats[fuel_type]["income"] += total_price
        
        # Сохранение данных
        self.storage.add_transaction(transaction)
        self._add_operation(
            "sale",
            f"Продажа {liters} л {fuel_type} на колонке {column_id}",
            {"column_id": column_id, "fuel_type": fuel_type, "liters": liters, "total_price": total_price}
        )
        self.save_all()
        
        self.next_transaction_id += 1
        return True, f"Успешно! Стоимость: {total_price:.2f} ₽"
    
    def refuel_cistern(self, cistern_id: str, liters: float) -> Tuple[bool, str]:
        """5.3 Оформление пополнения топлива"""
        cistern = next((c for c in self.cisterns if c.id == cistern_id), None)
        
        if not cistern:
            return False, "Цистерна не найдена"
        
        if cistern.current_volume + liters > cistern.max_volume:
            available = cistern.max_volume - cistern.current_volume
            return False, f"Превышен максимальный объем. Доступно для доливки: {available:.1f} л"
        
        cistern.current_volume += liters
        
        self._add_operation(
            "refuel",
            f"Пополнение цистерны {cistern_id} на {liters} л",
            {"cistern_id": cistern_id, "liters": liters}
        )
        
        self.save_all()
        return True, f"Цистерна {cistern_id} успешно пополнена на {liters} л"
    
    def transfer_fuel(self, source_id: str, target_id: str, liters: float) -> Tuple[bool, str]:
        """5.6 Перекачка топлива между цистернами"""
        source = next((c for c in self.cisterns if c.id == source_id), None)
        target = next((c for c in self.cisterns if c.id == target_id), None)
        
        if not source or not target:
            return False, "Одна из цистерн не найдена"
        
        if source.fuel_type != target.fuel_type:
            return False, "Перекачка возможна только между цистернами с одинаковым типом топлива"
        
        if not source.is_active:
            return False, f"Исходная цистерна {source_id} отключена"
        
        if source.current_volume < liters:
            return False, f"Недостаточно топлива в исходной цистерне. Доступно: {source.current_volume:.1f} л"
        
        if target.current_volume + liters > target.max_volume:
            available = target.max_volume - target.current_volume
            return False, f"Целевая цистерна переполнится. Доступно для приема: {available:.1f} л"
        
        # Выполнение перекачки
        source.current_volume -= liters
        target.current_volume += liters
        
        self._add_operation(
            "transfer",
            f"Перекачка {liters} л {source.fuel_type} из {source_id} в {target_id}",
            {"source_id": source_id, "target_id": target_id, "liters": liters, "fuel_type": source.fuel_type}
        )
        
        self.save_all()
        return True, f"Успешно перекачано {liters} л из {source_id} в {target_id}"
    
    def toggle_cistern(self, cistern_id: str, enable: bool) -> Tuple[bool, str]:
        """5.7 Включение/выключение цистерн"""
        cistern = next((c for c in self.cisterns if c.id == cistern_id), None)
        
        if not cistern:
            return False, "Цистерна не найдена"
        
        if enable:
            if cistern.current_volume < cistern.min_level:
                return False, f"Невозможно включить цистерну. Уровень топлива ниже минимального ({cistern.min_level} л)"
            cistern.is_active = True
            action = "включена"
        else:
            cistern.is_active = False
            action = "выключена"
        
        self._add_operation(
            "toggle_cistern",
            f"Ручное управление: цистерна {cistern_id} {action}",
            {"cistern_id": cistern_id, "action": "enable" if enable else "disable"}
        )
        
        self.save_all()
        return True, f"Цистерна {cistern_id} успешно {action}"
    
    def trigger_emergency(self) -> Tuple[bool, str]:
        """5.9 Аварийная ситуация"""
        self.emergency_mode = True
        
        # Отключение всех цистерн
        for cistern in self.cisterns:
            if cistern.is_active:
                cistern.is_active = False
        
        self._add_operation(
            "emergency",
            "АКТИВИРОВАН АВАРИЙНЫЙ РЕЖИМ! Все системы заблокированы.",
            {"action": "emergency_activated"}
        )
        
        self.save_all()
        return True, "АВАРИЙНЫЙ РЕЖИМ! Все цистерны заблокированы. Вызваны аварийные службы."
    
    def disable_emergency(self) -> Tuple[bool, str]:
        """Отключение аварийного режима"""
        self.emergency_mode = False
        
        self._add_operation(
            "emergency",
            "Аварийный режим отключен",
            {"action": "emergency_disabled"}
        )
        
        self.save_all()
        return True, "Аварийный режим отключен. Цистерны остаются заблокированными."
    
    def get_cistern_status(self) -> List[str]:
        """5.2 Получение статуса цистерн"""
        status = []
        for cistern in self.cisterns:
            status_str = f"{cistern.id} | {cistern.current_volume:,.0f} / {cistern.max_volume:,.0f} л | "
            status_str += "ВКЛ" if cistern.is_active else "ВЫКЛ"
            
            if not cistern.is_active and cistern.current_volume < cistern.min_level:
                status_str += " (ниже порога)"
            
            status.append(status_str)
        return status
    
    def get_column_status(self) -> List[str]:
        """5.8 Получение статуса колонок"""
        status = []
        for column in self.columns:
            fuels_info = []
            for fuel_type, cistern_id in column.available_fuels.items():
                cistern = next((c for c in self.cisterns if c.id == cistern_id), None)
                if cistern and cistern.is_active:
                    fuels_info.append(f"{fuel_type} ({cistern_id})")
                else:
                    fuels_info.append(f"{fuel_type} ({cistern_id}) - НЕДОСТУПНО")
            
            status_str = f"Колонка {column.id}: {', '.join(fuels_info)}"
            status.append(status_str)
        return status
    
    def get_statistics(self) -> Dict:
        """5.4 Получение статистики"""
        return {
            "total_cars": self.stats.total_cars_served,
            "total_income": self.stats.total_income,
            "fuel_stats": self.stats.fuel_stats
        }
    
    def get_history(self, limit: int = 10) -> List[Operation]:
        """5.5 Получение истории операций"""
        return self.history[-limit:] if limit > 0 else self.history
    
    def _add_operation(self, op_type: str, description: str, details: Dict):
        """Добавление операции в историю"""
        operation = Operation(
            id=self.next_op_id,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            operation_type=op_type,
            description=description,
            details=details
        )
        self.storage.add_operation(operation)
        self.history.append(operation)
        self.next_op_id += 1