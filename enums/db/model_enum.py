gender_male = 'Male'
gender_female = 'Female'
gender_other = 'Other'


from enum import Enum

class GenderEnum(str, Enum):
    Male = gender_male
    Female = gender_female
    Other = gender_other