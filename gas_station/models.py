"""
Модели данных для системы управления АЗС
"""
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class Cistern:
    """5.2 Модель цистерны"""
    id: str
    fuel_type: str
    max_volume: float
    current_volume: float
    min_level: float
    is_active: bool
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class Column:
    """5.8 Модель колонки"""
    id: int
    available_fuels: Dict[str, str]  # тип топлива -> id цистерны
    is_active: bool = True
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class Transaction:
    """5.1 Модель транзакции продажи"""
    id: int
    timestamp: str
    column_id: int
    fuel_type: str
    liters: float
    price_per_liter: float
    total_price: float
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class Operation:
    """5.5 Модель операции (история)"""
    id: int
    timestamp: str
    operation_type: str  # 'sale', 'refuel', 'transfer', 'toggle_cistern', 'emergency'
    description: str
    details: Dict
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class Statistics:
    """5.4 Модель статистики"""
    total_cars_served: int
    total_income: float
    fuel_stats: Dict[str, Dict]  # по типам топлива
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)