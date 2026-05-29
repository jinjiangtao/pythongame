from datetime import datetime

class FeeCalculator:
    def __init__(self, config):
        self.config = config
    
    def calculate_duration(self, entry_time_str):
        entry_time = datetime.strptime(entry_time_str, '%Y-%m-%d %H:%M:%S')
        exit_time = datetime.now()
        duration = (exit_time - entry_time).total_seconds() / 60
        return round(duration)
    
    def calculate_fee(self, vehicle_type, entry_time_str):
        duration = self.calculate_duration(entry_time_str)
        
        if duration <= self.config['free_duration']:
            return 0.0, duration
        
        chargeable_duration = duration - self.config['free_duration']
        hours = chargeable_duration / 60
        
        rate = self.config['rates'].get(vehicle_type, 5.0)
        fee = hours * rate
        
        if self.config['daily_cap'] > 0 and fee > self.config['daily_cap']:
            fee = self.config['daily_cap']
        
        return round(fee, 2), duration
    
    def format_duration(self, minutes):
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        if hours > 0:
            return f'{hours}小时{mins}分钟'
        return f'{mins}分钟'