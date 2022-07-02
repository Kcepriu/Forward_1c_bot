from .buttons import Buttons
from ..configs import Roles


class Acl:
    BUTTONS = {
        Buttons.FIND_PARTNERS: (Roles.FIND_PARTNERS,),
        Buttons.QR_DOCUMENTS: (Roles.QR_DOCUMENTS,),
        Buttons.FIND_PRODUCT: (),
        Buttons.SEND_ADMIN: ()
    }
