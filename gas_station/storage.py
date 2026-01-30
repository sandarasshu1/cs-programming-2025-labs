"""
Хранение и загрузка данных (Требование 6)
"""
import json
import os
from typing import List, Dict, Any
from models import Cistern, Column, Statistics, Operation, Transaction

class Storage:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Файлы данных
        self.cisterns_file = os.path.join(data_dir, "cisterns.json")
        self.columns_file = os.path.join(data_dir, "columns.json")
        self.stats_file = os.path.join(data_dir, "stats.json")
        self.history_file = os.path.join(data_dir, "history.json")
        self.transactions_file = os.path.join(data_dir, "transactions.json")
        
        # Инициализация файлов, если их нет
        self._init_files()
    
    def _init_files(self):
        """Создание файлов с начальными данными, если они не существуют"""
        default_files = {
            self.cisterns_file: self._get_default_cisterns(),
            self.columns_file: self._get_default_columns(),
            self.stats_file: self._get_default_stats(),
            self.history_file: [],
            self.transactions_file: []
        }
        
        for file_path, default_data in default_files.items():
            if not os.path.exists(file_path):
                self._save_data(file_path, default_data)
    
    def _get_default_cisterns(self):
        """Создание начальных цистерн (Раздел 2.2)"""
        return [
            {
                "id": "АИ-92 №1",
                "fuel_type": "АИ-92",
                "max_volume": 20000,
                "current_volume": 12400,
                "min_level": 1000,
                "is_active": True
            },
            {
                "id": "АИ-95 №1",
                "fuel_type": "АИ-95",
                "max_volume": 20000,
                "current_volume": 9800,
                "min_level": 1000,
                "is_active": True
            },
            {
                "id": "АИ-95 №2",
                "fuel_type": "АИ-95",
                "max_volume": 20000,
                "current_volume": 1200,
                "min_level": 1000,
                "is_active": False
            },
            {
                "id": "АИ-98 №1",
                "fuel_type": "АИ-98",
                "max_volume": 15000,
                "current_volume": 10000,
                "min_level": 800,
                "is_active": False
            },
            {
                "id": "ДТ №1",
                "fuel_type": "ДТ",
                "max_volume": 25000,
                "current_volume": 15600,
                "min_level": 1200,
                "is_active": True
            }
        ]
    
    def _get_default_columns(self):
        """Создание начальных колонок (Раздел 3.1, 3.2)"""
        columns = []
        for i in range(1, 9):
            fuels = {}
            
            # АИ-95
            if i <= 4:
                fuels["АИ-95"] = "АИ-95 №1"
            elif i >= 5:
                fuels["АИ-95"] = "АИ-95 №2"
            
            # АИ-92
            if i <= 6:
                fuels["АИ-92"] = "АИ-92 №1"
            
            # АИ-98
            if 3 <= i <= 6:
                fuels["АИ-98"] = "АИ-98 №1"
            
            # ДТ
            if 3 <= i <= 8:
                fuels["ДТ"] = "ДТ №1"
            
            columns.append({
                "id": i,
                "available_fuels": fuels,
                "is_active": True
            })
        
        return columns
    
    def _get_default_stats(self):
        """Начальная статистика"""
        return {
            "total_cars_served": 0,
            "total_income": 0.0,
            "fuel_stats": {
                "АИ-92": {"liters": 0, "income": 0},
                "АИ-95": {"liters": 0, "income": 0},
                "АИ-98": {"liters": 0, "income": 0},
                "ДТ": {"liters": 0, "income": 0}
            }
        }
    
    def _load_data(self, file_path):
        """Загрузка данных из файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_data(self, file_path, data):
        """Сохранение данных в файл"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_cisterns(self) -> List[Cistern]:
        """Загрузка цистерн"""
        data = self._load_data(self.cisterns_file)
        return [Cistern.from_dict(item) for item in data]
    
    def save_cisterns(self, cisterns: List[Cistern]):
        """Сохранение цистерн"""
        data = [cistern.to_dict() for cistern in cisterns]
        self._save_data(self.cisterns_file, data)
    
    def load_columns(self) -> List[Column]:
        """Загрузка колонок"""
        data = self._load_data(self.columns_file)
        return [Column.from_dict(item) for item in data]
    
    def save_columns(self, columns: List[Column]):
        """Сохранение колонок"""
        data = [column.to_dict() for column in columns]
        self._save_data(self.columns_file, data)
    
    def load_statistics(self) -> Statistics:
        """Загрузка статистики"""
        data = self._load_data(self.stats_file)
        return Statistics.from_dict(data)
    
    def save_statistics(self, stats: Statistics):
        """Сохранение статистики"""
        self._save_data(self.stats_file, stats.to_dict())
    
    def load_history(self) -> List[Operation]:
        """Загрузка истории операций"""
        data = self._load_data(self.history_file)
        return [Operation.from_dict(item) for item in data]
    
    def save_history(self, history: List[Operation]):
        """Сохранение истории операций"""
        data = [op.to_dict() for op in history]
        self._save_data(self.history_file, data)
    
    def load_transactions(self) -> List[Transaction]:
        """Загрузка транзакций"""
        data = self._load_data(self.transactions_file)
        return [Transaction.from_dict(item) for item in data]
    
    def save_transactions(self, transactions: List[Transaction]):
        """Сохранение транзакций"""
        data = [t.to_dict() for t in transactions]
        self._save_data(self.transactions_file, data)
    
    def add_operation(self, operation: Operation):
        """Добавление операции в историю"""
        history = self.load_history()
        history.append(operation)
        self.save_history(history)
    
    def add_transaction(self, transaction: Transaction):
        """Добавление транзакции"""
        transactions = self.load_transactions()
        transactions.append(transaction)
        self.save_transactions(transactions)