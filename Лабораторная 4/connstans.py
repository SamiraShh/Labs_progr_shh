import math

# Допустимые диапазоны для размеров сечения (мм)
MIN_ZNACH: float = 10.0
MAX_ZNACH: float = 1000.0

# Диапазон для изгиб. момента (кН * м)
M_MIN: float = 0.1
M_MAX: float = 500.0

# Коэффициенты запаса (k = sigma_fact/sigma_dop)
K_SAFE: float = 0.5 #Большой запас
K_LIMIT: float = 1.0 #Допустимо

# Диапазон для допускаемого напряжения (МПа)
MIN_SIGMA_DOP: float = 50.0
MAX_SIGMA_DOP: float =  400.0

# Пи
PI: float = math.pi

# Файл журнала ошибок
LOG_FILE: str = "input_errors.log"