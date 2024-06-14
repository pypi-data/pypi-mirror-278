from .create_group_calls import CreateGroupCall
from .discard_group_calls import DiscardGroupCall
from .get_group_calls import GetGroupCall
from .title_group_calls import EditTitileGroupCall


class Calls(
    CreateGroupCall,
    DiscardGroupCall,
    EditTitileGroupCall,
    GetGroupCall
):
    pass
