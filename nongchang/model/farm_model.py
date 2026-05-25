from enum import Enum
from config import CROPS, INITIAL_GOLD, INITIAL_STAMINA, MAX_STAMINA, PLANT_COST, HARVEST_COST


class CropState(Enum):
    EMPTY = 0
    PLANTED = 1
    GROWING = 2
    MATURE = 3


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = CropState.EMPTY
        self.crop_type = None
        self.planted_day = None

    def plant(self, crop_type, current_day):
        self.state = CropState.PLANTED
        self.crop_type = crop_type
        self.planted_day = current_day

    def update_growth(self, current_day, difficulty_multiplier=1.0):
        if self.state in (CropState.PLANTED, CropState.GROWING) and self.crop_type:
            growth_days = int(CROPS[self.crop_type]["growth_days"] * difficulty_multiplier)
            days_since_planted = current_day - self.planted_day
            if days_since_planted >= growth_days:
                self.state = CropState.MATURE
            elif days_since_planted > 0:
                self.state = CropState.GROWING

    def harvest(self):
        if self.state == CropState.MATURE and self.crop_type:
            crop_info = CROPS[self.crop_type]
            self.state = CropState.EMPTY
            self.crop_type = None
            self.planted_day = None
            return crop_info
        return None

    def get_growth_progress(self, current_day, difficulty_multiplier=1.0):
        if self.state in (CropState.PLANTED, CropState.GROWING) and self.crop_type:
            growth_days = int(CROPS[self.crop_type]["growth_days"] * difficulty_multiplier)
            days_since_planted = current_day - self.planted_day
            return min(days_since_planted / growth_days * 100, 100)
        return 0


class FarmModel:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        self.gold = INITIAL_GOLD
        self.current_day = 1
        self.selected_crop = "wheat"
        self.stamina = INITIAL_STAMINA
        self.max_stamina = MAX_STAMINA
        self.backpack = {crop_id: 0 for crop_id in CROPS.keys()}

    def get_cell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row][col]
        return None

    def plant_crop(self, row, col):
        if self.stamina < PLANT_COST:
            return False, "体力不足"
        
        cell = self.get_cell(row, col)
        if cell and cell.state == CropState.EMPTY:
            cell.plant(self.selected_crop, self.current_day)
            self.stamina -= PLANT_COST
            return True, f"已播种 {CROPS[self.selected_crop]['name']}"
        return False, "无法播种"

    def harvest_crop(self, row, col):
        if self.stamina < HARVEST_COST:
            return 0, "体力不足"
        
        cell = self.get_cell(row, col)
        if cell:
            crop_id = cell.crop_type
            crop_info = cell.harvest()
            if crop_info:
                self.stamina -= HARVEST_COST
                self.backpack[crop_id] = self.backpack.get(crop_id, 0) + 1
                return crop_info["sell_price"], f"收获成功！获得 {crop_info['name']} x1"
        return 0, "无法收获"

    def update_day(self):
        self.current_day += 1
        difficulty_multiplier = 1.0 + (self.current_day - 1) * 0.05
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].update_growth(self.current_day, difficulty_multiplier)

    def recover_stamina(self, amount=10):
        self.stamina = min(self.stamina + amount, self.max_stamina)

    def set_selected_crop(self, crop_type):
        if crop_type in CROPS:
            self.selected_crop = crop_type
            return True, f"已选择 {CROPS[crop_type]['name']}"
        return False, "无效作物"

    def sell_crop(self, crop_id, amount):
        if self.backpack.get(crop_id, 0) >= amount:
            crop_info = CROPS[crop_id]
            total_value = crop_info["sell_price"] * amount
            self.backpack[crop_id] -= amount
            self.gold += total_value
            return True, f"出售成功！获得 {total_value} 金币"
        return False, "库存不足"

    def buy_seed(self, crop_type):
        crop_info = CROPS.get(crop_type)
        if not crop_info:
            return False, "无效作物"
        
        if self.gold >= crop_info["buy_price"]:
            self.gold -= crop_info["buy_price"]
            return True, f"购买成功！获得 {crop_info['name']}种子"
        return False, "金币不足"

    def get_total_crops(self):
        return sum(self.backpack.values())
