from typing import List, Optional, TypeVar
from ai_haley_kg_domain.model.KGFrame import KGFrame
from ai_haley_kg_domain.model.KGSlot import KGSlot
from vital_ai_vitalsigns.collection.graph_collection import GraphCollection
from vital_ai_vitalsigns.model.GraphObject import GraphObject
from vital_ai_vitalsigns.part.graph_part import GraphPart

G = TypeVar('G', bound=Optional[GraphObject])


class KGFramePart(GraphPart):

    def __init__(self, data: List[G] = None, score: float = 1.0, *, graph_collection: GraphCollection | None = None):
        super().__init__(data, score, graph_collection=graph_collection)

    def get_kgslots(self) -> List[KGSlot]:
        kgframe = self.get_kgframe()
        # todo check if frame exists
        # enforce slots connected to this frame

        return [item for item in self if isinstance(item, KGSlot)]

    def get_kgframe(self) -> Optional[KGFrame]:
        kg_frames = [item for item in self if isinstance(item, KGFrame)]
        if len(kg_frames) == 1:
            return kg_frames[0]
        return None



