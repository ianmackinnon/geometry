#!/usr/bin/env python
#-*- coding utf-8 -*-

from mako.template import Template
from mako import exceptions

class Geometry(object):

    geo_template = """PGEOMETRY V5
NPoints ${len(geometry.points)} NPrims ${len(geometry.prims)}
NPointGroups 0 NPrimGroups 0
NPointAttrib ${len(geometry.pointattrs)} NVertexAttrib 0 NPrimAttrib ${len(geometry.primattrs)} NAttrib ${int(bool(geometry.attr_names))}

%if len(geometry.pointattrs):
PointAttrib
%for name, index in geometry.point_attr_string_dict.items():
${name} 1 index ${len(index)} \\
%for text in index:
${text} \\
%endfor

%endfor

%for p, (name, pointattr) in enumerate(geometry.pointattrs.items()):
${name} 1 int 0
%endfor
%endif

%for p, point in enumerate(geometry.points):
${"%f %f %f %f" % (point[0], point[1], point[2], 1.0)} \\
%if geometry.pointattrs:
[${"\t".join([str(geometry.pointattrs[key][p]) for key in geometry.pointattrs])}]
%endif
%endfor

%if len(geometry.prims):

%if len(geometry.primattrs):
PrimitiveAttrib
%for p, (name, primattr) in enumerate(geometry.primattrs.items()):
${name} 1 int 0
%endfor
%endif

%for p, prim in enumerate(geometry.prims):
Poly ${len(prim)} < ${" ".join([str(v) for v in prim])}
%if geometry.primattrs:
[${"\t".join([str(geometry.primattrs[key][p]) for key in geometry.primattrs])}]
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
        self.pointattrs = {}
        self.primattrs = {}
        self.point_attr_string_dict = {}
        
    def add_point(self, x, y, z):
        self.points.append((x, y, z))
        return len(self.points) - 1

    def add_prim(self, point_numbers):
        self.prims.append(point_numbers)
        return len(self.prims) - 1
        
    def set_pointattr_int(self, name, index, value):
        assert value == int(value)
        if not name in self.pointattrs:
            self.pointattrs[name] = {}
        self.pointattrs[name][index] = value

    def set_point_attr_string(self, name, point_number, value):
        assert hasattr(name, "strip")
        assert point_number == int(point_number)
        if not name in self.point_attr_string_dict:
            self.point_attr_string_dict[name] = []
        if not value in self.point_attr_string_dict[name]:
            self.point_attr_string_dict[name].append(value)
        index = self.point_attr_string_dict[name].index(value)
        self.set_pointattr_int(name, point_number, index)

    def get_pointattr(self, name, index):
        assert name in self.pointattrs, 'no such name'
        return self.pointattrs[name].get(index, 0)

    def set_primattr(self, name, index, value):
        assert value == int(value)
        if not name in self.primattrs:
            self.primattrs[name] = {}
        self.primattrs[name][index] = value

    def get_primattr(self, name, index):
        assert name in self.primattrs, 'no such name'
        return self.primattrs[name].get(index, 0)

    @property
    def attr_names(self):
        return self.pointattrs.keys() + self.primattrs.keys()

    def render(self):
        try:
            return Template(self.geo_template).render(geometry=self)
        except:
            print exceptions.text_error_template().render()
