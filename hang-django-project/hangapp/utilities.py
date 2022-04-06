from .models import Homie


def extract_user(data: dict):
    data.pop('hangoutId')
    homie_id = data.pop('homieId')
    if homie_id is not None:
        return Homie.objects.get(pk=homie_id)
    else:
        raise Exception("Homie ID sent in request not found in database")
