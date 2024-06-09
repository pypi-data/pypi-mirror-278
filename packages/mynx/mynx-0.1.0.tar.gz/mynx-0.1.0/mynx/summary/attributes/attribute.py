from abc import ABC

class Attribute(ABC):
    attribute_name = ...
    end_attribute_name = ...
    line_lenght = ...
    attribute_compute = ...
    end_attribute_compute = ...
    def __init__(self):
        att_name = self.attribute_name != ...
        self._att_name = att_name
        end_att_name = self.end_attribute_name != ...
        self._end_att_name = end_att_name
        l_lenght = self.line_lenght != ...
        att_fn = self.attribute_compute != ...
        self._att_fn = att_fn
        end_att_fn = self.end_attribute_compute != ...

        if att_name or l_lenght:
            if not att_name:
                raise TypeError(f"Can't instantiate abstract class {self.__class__.__name__} with abstract attribute attribute_name")
            else:
                assert isinstance(self.attribute_name, str)
            if not l_lenght:
                raise TypeError(f"Can't instantiate abstract class {self.__class__.__name__} with abstract attribute line_lenght")
            else:
                assert isinstance(self.line_lenght, int)
            if not att_fn:
                raise TypeError(f"Can't instantiate abstract class {self.__class__.__name__} with abstract attribute function attribute_compute")
            else:
                assert callable(self.attribute_compute)

        if end_att_name or end_att_fn:
            if not end_att_name:
                raise TypeError(f"Can't instantiate abstract class {self.__class__.__name__} with abstract attribute end_attribute_name")
            else:
                assert isinstance(self.end_attribute_name, str)
            if not end_att_fn:
                raise TypeError(f"Can't instantiate abstract class {self.__class__.__name__} with abstract attribute function end_attribute_compute")
            else:
                assert callable(self.end_attribute_compute)