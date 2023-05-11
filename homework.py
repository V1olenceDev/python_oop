from dataclasses import dataclass, asdict


@dataclass()
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE_TEMPLATE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        message_data = asdict(self)
        return self.MESSAGE_TEMPLATE.format(**message_data)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # длина шага в метрах
    M_IN_KM: int = 1000  # количество метров в километре
    MIN_IN_H: int = 60  # кол-во минут в часе

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        ...

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18  # множитель в формуле
    # расчета калорий
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79  # сдвиг в формуле расчета калорий

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * super().get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / Training.M_IN_KM
                * (self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIE_RATIO: float = 0.035  # Коэффициент для подсчета калорий.
    CALORIE_RATIO_2: float = 0.029  # Коэффициент для подсчета калорий.
    CONVERT_TO_MS: float = 0.278  # Константа для перевода в м/с
    S_IN_M: int = 100  # См в метре

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIE_RATIO * self.weight
                 + ((super().get_mean_speed() * self.CONVERT_TO_MS) ** 2
                    / (self.height / self.S_IN_M)) * self.CALORIE_RATIO_2
                 * self.weight)
                * (self.duration * Training.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    K_SWIM: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / Training.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.K_SWIM * self.weight * self.duration)


TRAINING_CLASSES: dict = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAINING_CLASSES:
        raise ValueError(f"Неизвестный тип тренировки: {workout_type}")

    workout_class = TRAINING_CLASSES[workout_type]
    return workout_class(*data)


def main(training: Training) -> None:
    info = training.show_training_info()
    message = info.get_message()
    return print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
