import math


def format_seconds_to_hms(time_in_seconds):
    if time_in_seconds is None:
        return "NULL"
    horas = int(math.floor(time_in_seconds / (60 * 60)))
    minutos = int(math.floor(time_in_seconds / 60) - horas * 60)
    segundos = int(time_in_seconds) % 60
    formatted = ""
    if horas > 24:
        dias = int(math.floor(horas/24))
        horas = horas % 24
        formatted += f"{dias}d, "
    return formatted + "{}:{}:{}".format(str(horas).zfill(2), str(minutos).zfill(2), str(segundos).zfill(2))
