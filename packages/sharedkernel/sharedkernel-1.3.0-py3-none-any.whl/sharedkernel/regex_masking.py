import re
from persian_tools import national_id, phone_number
from persian_tools.bank import card_number, sheba

class RegexMaskingBuilder:
    def __init__(self, message: str):
        self.message = message
    
    def with_card_no(self):
        find_patterns = re.findall(r'(?<!\d)\d{16}(?!\d)', self.message)
        for i in find_patterns:
            if card_number.validate(i):
                self.message = re.sub(i, "*" * 16, self.message)
        return self
    
    def with_national_id(self):
        find_patterns = re.findall(r'(?<!\d)\d{10}(?!\d)', self.message)
        for i in find_patterns:
            if national_id.validate(i):
                self.message = re.sub(i, "*" * 10, self.message)
        return self

    def with_mobile_no(self):
        find_patterns = re.findall(r'(?<!\d)\d{10,12}(?!\d)', self.message)
        for i in find_patterns:
            if phone_number.validate(i):
                self.message = re.sub(i, "*" * len(i), self.message)
        return self
    
    def with_sheba(self):
        find_patterns = re.findall(r'|'.join([r'(?<!\d)\d{24}(?!\d)', r'IR\d{24}(?!\d)']), self.message)
        for i in find_patterns:
            if sheba.validate("IR" + i) or sheba.validate(i):
                self.message = re.sub(i, "*" * len(i), self.message)
        return self
    
    def with_phone_no(self):
        phone_number_pattern1 = r'(?<!\d)^0[0-9]{2,}-[0-9]{8}$(?!\d)'
        phone_number_pattern2 = r'(?<!\d)^0[0-9]{2,}[0-9]{8}$(?!\d)'
        self.message = re.sub(r'|'.join([phone_number_pattern1, phone_number_pattern2]), "*" * 12, self.message)
        return self
    
    def with_cvv2(self):
        self.message = re.sub(r'(?<!\d)\d{3}(?!\d)', "*" * 3, self.message)
        return self

    def with_peigiri_no(self):
        patterns = {
            r'(?<!\d)\d{6}(?!\d)': "*" * 6,
            r'(?<!\d)\d{12}(?!\d)': "*" * 12,
            r'(?<!\d)\d{20}(?!\d)': "*" * 20
        }
        for key, value in patterns.items():
            self.message = re.sub(key, value, self.message)
        return self
    
    def with_account_no(self):
        self.message = re.sub(r'(?<!\d)\d{12,16}(?!\d)', "*" * 16, self.message)
        return self
    
    def build(self):
        return self.message