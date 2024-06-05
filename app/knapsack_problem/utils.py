from pyomo.core import Constraint
import numpy as np

np_true = np.bool_(True)


def constraints_from_dict(
        model,
        cons_dict: dict,
        name: str
) -> Constraint:
    """
    Создание pyomo ограничения на основе словаря с ограничениями. Ключ словаря - ключ ограничения,
    значение словаря - ограничение, задаваемое с помощью expression.
    """

    def c_rule(self, *k):
        """
        Извлечение ограничения из словаря и передача его как результат выполнения функции
        """

        # Если ключ ограничения состоит из одного элемента, то необходима конвертация из tuple
        if len(k) == 1:
            k = k[0]
        ret = cons_dict[k]
        # Проверка: Если ограничение изначально выполняется всегда, то возврат константы, иначе pyomo ошибка
        if ret is True or ret is np_true:
            return Constraint.Skip
        return ret

    if cons_dict:
        result = Constraint(cons_dict.keys(), rule=c_rule)
        setattr(model, name, result)
        return result