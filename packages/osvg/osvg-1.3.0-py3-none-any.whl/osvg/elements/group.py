"""
Module to define Group class.
"""

import osvg.elements.elementbase
import osvg.helper
import osvg.positions
import osvg.float
import osvg.style


class Group(osvg.elements.elementbase.SVGElement):
    """
    A Group class matches the 'g' tag in SVG.
    It can be customized with:
        - name => tag id
        - rotation: rotate group (all elements within it)
        - style => tag style
        - layer: Manipulate the order in the XML elements
    """

    xml_tag = "g"

    def add_group(
        self,
        position: "Group" = None,
        name: str = None,
        style: osvg.style.Style = None,
        layer: int = 0,
        rotation: int | float | osvg.float.Float = 0,
    ) -> "Group":
        """
        Add a group as a subgroup to this group.
        """
        # pylint: disable=too-many-arguments
        if position is None:
            position = osvg.positions.Position(x=self.position.x, y=self.position.y)
        return Group(
            parent=self,
            position=position,
            name=name,
            style=style,
            layer=layer,
            rotation=rotation,
        )
