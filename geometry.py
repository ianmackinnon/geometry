#!/usr/bin/env python
#-*- coding utf-8 -*-

from mako.template import Template
from mako import exceptions

class Geometry(object):

    geo_template = """PGEOMETRY V5
NPoints ${len(geometry.points)} NPrims ${len(geometry.prims)}
NPointGroups 0 NPrimGroups 0
NPointAttrib ${len(geometry.point_attrs)} NVertexAttrib 0 NPrimAttrib ${len(geometry.prim_attrs)} NAttrib ${int(bool(geometry.attr_names))}

%if len(geometry.point_attrs):
PointAttrib
%for name, index in geometry.point_attr_string_dict.items():
${name} 1 index ${len(index)} \\
%for text in index:
${text} \\
%endfor
\\
%endfor
\\
%for p, (name, point_attr) in enumerate(geometry.point_attrs.items()):
%if name in geometry.point_attr_string_dict.keys():
<% continue %>
%endif
${name} 1 int 0
%endfor
%endif

%for p, point in enumerate(geometry.points):
${"%f %f %f %f" % (point[0], point[1], point[2], 1.0)} \\
%if geometry.point_attrs:
[${"\t".join([str(geometry.point_attrs[key][p]) for key in geometry.point_attrs])}]
%endif
%endfor

%if len(geometry.prims):

%if len(geometry.prim_attrs):
PrimitiveAttrib
%for p, (name, prim_attr) in enumerate(geometry.prim_attrs.items()):
${name} 1 int 0
%endfor
%endif

%for p, prim in enumerate(geometry.prims):
Poly ${len(prim)} < ${" ".join([str(v) for v in prim])}
%if geometry.prim_attrs:
[${"\t".join([str(geometry.prim_attrs[key][p]) for key in geometry.prim_attrs])}]
%endif
%endfor

%endif

DetailAttrib
varmap 1 index ${len(geometry.attr_names)} ${" ".join(['"%s -> %s"' % (name, name) for name in geometry.attr_names])}
 (0)

beginExtra
endExtra
"""

    def __init__(self):
        self.points = []
        self.prims = []
        self.point_attrs = {}
        self.prim_attrs = {}
        self.point_attr_string_dict = {}
        self.prim_attr_string_dict = {}
        
    def add_point(self, x, y, z):
        self.points.append((x, y, z))
        return len(self.points) - 1

    def add_prim(self, point_numbers):
        self.prims.append(point_numbers)
        return len(self.prims) - 1
        
    def set_point_attr_int(self, name, index, value):
        assert value == int(value)
        if not name in self.point_attrs:
            self.point_attrs[name] = {}
        self.point_attrs[name][index] = value

    def set_point_attr_string(self, name, point_number, value):
        assert hasattr(name, "strip")
        assert point_number == int(point_number)
        if not name in self.point_attr_string_dict:
            self.point_attr_string_dict[name] = []
        if not value in self.point_attr_string_dict[name]:
            self.point_attr_string_dict[name].append(value)
        index = self.point_attr_string_dict[name].index(value)
        self.set_point_attr_int(name, point_number, index)

    def set_prim_attr_int(self, name, index, value):
        assert value == int(value)
        if not name in self.prim_attrs:
            self.prim_attrs[name] = {}
        self.prim_attrs[name][index] = value


    def get_point_attr(self, name, index):
        assert name in self.point_attrs, 'no such name'
        return self.point_attrs[name].get(index, 0)

    def get_prim_attr(self, name, index):
        assert name in self.prim_attrs, 'no such name'
        return self.prim_attrs[name].get(index, 0)

    @property
    def attr_names(self):
        return self.point_attrs.keys() + self.prim_attrs.keys()

    def render(self):
        try:
            return Template(self.geo_template).render(geometry=self)
        except:
            print exceptions.text_error_template().render()
