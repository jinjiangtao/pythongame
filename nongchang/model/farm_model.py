from enum import Enum
from config import CROPS, INITIAL_GOLD


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

    def update_growth(self, current_day):
        if self.state in (CropState.PLANTED, CropState.GROWING) and self.crop_type:
            growth_days = CROPS[self.crop_type]["growth_days"]
            days_since_planted = current_day - self.planted_day
            if days_since_planted >= growth_days:
                self.state = CropState.MATURE
            elif days_since_planted > 0:
                self.state = CropState.GROWING

    def harvest(self):
        if self.state == CropState.MATURE and self.crop_type:
            value = CROPS[self.crop_type]["value"]
            self.state = CropState.EMPTY
            self.crop_type = None
            self.planted_day = None
            return value
        return 0


class FarmModel:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        self.gold = INITIAL_GOLD
        self.current_day = 1
        self.selected_crop = "wheat"

    def get_cell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row][col]
        return None

    def plant_crop(self, row, col):
        cell = self.get_cell(row, col)
        if cell and cell.state == CropState.EMPTY:
            cell.plant(self.selected_crop, self.current_day)
            return True
        return False

    def harvest_crop(self, row, col):
        cell = self.get_cell(row, col)
        if cell:
            value = cell.harvest()
            if value > 0:
                self.gold += value
                return value
        return 0

    def update_day(self):
        self.current_day += 1
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].update_growth(self.current_day)

    def set_selected_crop(self, crop_type):
        if crop_type in CROPS:
            self.selected_crop = crop_type
