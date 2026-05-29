import re

class Validators:
    @staticmethod
    def validate_plate_number(plate_number):
        plate_number = plate_number.strip().upper()
        
        if not plate_number:
            return False, '车牌号不能为空'
        
        pattern = r'^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z][A-HJ-NP-Z0-9]{4,5}[A-HJ-NP-Z0-9挂学警港澳]$'
        
        if not re.match(pattern, plate_number):
            return False, '车牌号格式不正确'
        
        return True, ''
    
    @staticmethod
    def validate_positive_number(value):
        try:
            num = float(value)
            if num <= 0:
                return False, '必须输入正数'
            return True, ''
        except ValueError:
            return False, '必须输入数字'