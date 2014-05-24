#!/usr/bin/env python
#-*- coding utf-8 -*-

import re
import sys

from mako.template import Template
from mako import exceptions

class Geometry(object):

    geo_template = """PGEOMETRY V5
NPoints ${len(geometry.points)} NPrims ${len(geometry.prims)}
NPointGroups 0 NPrimGroups 0
NPointAttrib ${len(geometry.point_attrs)} NVertexAttrib 0 NPrimAttrib ${len(geometry.prim_attrs)} NAttrib ${int(bool(geometry.attr_names))}

%if len(geometry.point_attrs):
PointAttrib

%for p, (name, point_attr) in enumerate(geometry.point_attrs.items()):
%if name in geometry.point_attr_string_dict.keys():
<% index = geometry.point_attr_string_dict[name] %>\
${name} 1 index ${len(index)} \\
%for text in index:
"${text.replace('\\\\', '\\\\\\\\').replace('"', '\\\\"')}" \\
%endfor

%else:
%if point_attr["type"] == int:
${name} 1 int 0
%else:
${name} 1 float 0
%endif
%endif
%endfor
%endif

%for p, point in enumerate(geometry.points):
${"%f %f %f %f" % (point[0], point[1], point[2], 1.0)} \\
%if geometry.point_attrs:
(${"\t".join([str(geometry.point_attrs[key]["values"][p]) for key in geometry.point_attrs])}) \\
%endif

%endfor


%if len(geometry.prims):

%if len(geometry.prim_attrs):
PrimitiveAttrib

%for p, (name, prim_attr) in enumerate(geometry.prim_attrs.items()):
%if name in geometry.prim_attr_string_dict.keys():
<% index = geometry.prim_attr_string_dict[name] %>\
${name} 1 index ${len(index)} \\
%for text in index:
"${text.replace('\\\\', '\\\\\\\\').replace('"', '\\\\"')}" \\
%endfor

%else:
%if prim_attr["type"] == int:
${name} 1 int 0
%else:
${name} 1 float 0
%endif
%endif
%endfor
%endif

%for p, prim in enumerate(geometry.prims):
Poly ${len(prim["points"])} ${"<" if prim["closed"] else ":"} ${" ".join([str(v) for v in prim["points"]])} \\
%if geometry.prim_attrs:
[${"\t".join([str(geometry.prim_attrs[key]["values"][p]) for key in geometry.prim_attrs])}] \\
%endif

%endfor

%endif

%if geometry.attr_names:
DetailAttrib
varmap 1 index ${len(geometry.attr_names)} ${" ".join(['"%s -> %s"' % (name, name) for name in geometry.attr_names])}
 (0)
%endif

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


    def assert_type(self, attrs, name, type_):
        if attrs[name]["type"] != type_:
            raise TypeError("Point attribute '%s' already has type '%s'." % (name, attrs[name]["type"]))
        
        
    def add_point(self, x, y, z):
        self.points.append((x, y, z))
        return len(self.points) - 1

    def add_prim(self, point_numbers, closed=True):
        self.prims.append({"closed": closed, "points": point_numbers})
        return len(self.prims) - 1

        
    def set_point_attr_int(self, name, index, value):
        assert value == int(value)
        if not name in self.point_attrs:
            self.point_attrs[name] = {"type": int, "values": {}}
        else:
            self.assert_type(self.point_attrs, name, int)
        self.point_attrs[name]["values"][index] = value

    def set_point_attr_float(self, name, index, value):
        assert value == float(value)
        if not name in self.point_attrs:
            self.point_attrs[name] = {"type": float, "values": {}}
        else:
            self.assert_type(self.point_attrs, name, float)
        self.point_attrs[name]["values"][index] = value

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
            self.prim_attrs[name] = {"type": int, "values": {}}
        else:
            self.assert_type(self.prim_attrs, name, int)
        self.prim_attrs[name]["values"][index] = value

    def set_prim_attr_float(self, name, index, value):
        assert value == float(value)
        if not name in self.prim_attrs:
            self.prim_attrs[name] = {"type": float, "values": {}}
        else:
            self.assert_type(self.prim_attrs, name, float)
        self.prim_attrs[name]["values"][index] = value

    def set_prim_attr_string(self, name, prim_number, value):
        assert hasattr(name, "strip")
        assert prim_number == int(prim_number)
        if not name in self.prim_attr_string_dict:
            self.prim_attr_string_dict[name] = []
        if not value in self.prim_attr_string_dict[name]:
            self.prim_attr_string_dict[name].append(value)
        index = self.prim_attr_string_dict[name].index(value)
        self.set_prim_attr_int(name, prim_number, index)


    def get_point_attr(self, name, index):
        assert name in self.point_attrs, 'no such name'
        return self.point_attrs[name]["values"].get(index, 0)

    def get_prim_attr(self, name, index):
        assert name in self.prim_attrs, 'no such name'
        return self.prim_attrs[name]["values"].get(index, 0)

    @property
    def attr_names(self):
        return self.point_attrs.keys() + self.prim_attrs.keys()

    def render(self):
        try:
            return Template(self.geo_template).render(geometry=self)
        except:
            print exceptions.text_error_template().render()



def parse_index(text):
    parts = text.split(" \"")
    length = int(parts.pop(0))
    assert len(parts) == length
    for i, part in enumerate(parts):
        assert part[-1] == u"\""
        part = part[:-1]
        part = part.replace("\\\"", "\"")
        part = part.replace("\\\\", "\\")
        parts[i] = part
    return parts



def read(path):
    geo_file = open(path)
    geo = Geometry()
    headlines = [
        ("PGEOMETRY V5", ()),
        ("NPoints (\d+) NPrims (\d+)", ("npoints", "nprims")),
        ("NPointGroups (\d+) NPrimGroups (\d+)", ("npointgroups", "nprimgroups")),
        ("NPointAttrib (\d+) NVertexAttrib (\d+) NPrimAttrib (\d+) NAttrib (\d+)", ("npointattrib", "nvertexattrib", "nprimattrib", "nattrib")),
        ]

    attr = {}
    mode = None
    point_attributes = []
    prim_attributes = []
    points = 0
    prims = 0
    for line in geo_file.readlines():
        line = line.strip()
        if not line:
            continue

        if headlines:
            regex_string, keys = headlines.pop(0)
            regex = re.compile(regex_string)
            match = regex.match(line)
            if not match:
                print "Failed to match '%s' with line '%s'." % (regex_string, line)
                sys.exit(1)
            values = [int(x) for x in match.groups()]
            attr.update(dict(zip(keys, values)))
            continue
        
        if line == "PointAttrib":
            mode = "PointAttrib"
            continue
        if line == "PrimitiveAttrib":
            mode = "PrimitiveAttrib"
            continue
        if line == "DetailAttrib":
            break

        if mode == "PointAttrib":
            regex_string = "(\w+) (\d+) (\w+) (.+)$"
            regex = re.compile(regex_string)
            match = regex.match(line)
            if match:
                name, length, type_, value = match.groups()
                assert length == '1'
                if type_ == "index":
                    value = parse_index(value)
                point_attributes.append((name, type_, value))
                continue
            else:
                mode = "Point"

        if mode == "PrimitiveAttrib":
            regex_string = "(\w+) (\d+) (\w+) (.+)$"
            regex = re.compile(regex_string)
            match = regex.match(line)
            if match:
                name, length, type_, value = match.groups()
                assert length == '1'
                if type_ == "index":
                    value = parse_index(value)
                prim_attributes.append((name, type_, value))
                continue
            elif re.match("Run \d+ Poly$", line):
                continue
            else:
                mode = "Prim"

        if mode == "Point":
            line = line.replace("(", "").replace(")", "")
            parts = re.split("\s+", line)
            x, y, z, w = (float(v) for v in parts[:4])
            attrs = parts[4:]
            geo.add_point(x, y, z)
            assert len(attrs) == len(point_attributes)
            for i, (name, type_, value) in enumerate(point_attributes):
                if type_ == "int":
                    geo.set_point_attr_int(name, points, int(attrs[i]))
                elif type_ == "float":
                    geo.set_point_attr_float(name, points, float(attrs[i]))
                elif type_ == "index":
                    geo.set_point_attr_string(name, points, value[int(attrs[i])])
                else:
                    raise TypeError, "Type '%s' not recognised." % type_
            points += 1

        if mode == "Prim":
            line = line.replace("[", "").replace("]", "")
            parts = re.split("\s+", line)
            length = int(parts.pop(0))
            closed = parts.pop(0) == "<"
            point_list = parts[length:]
            attrs = parts[:length]
            attrs = parts[4:]
            geo.add_prim(point_list, closed=closed)
            assert len(attrs) == len(prim_attributes)
            for i, (name, type_, value) in enumerate(prim_attributes):
                if type_ == "int":
                    geo.set_prim_attr_int(name, prims, int(attrs[i]))
                elif type_ == "float":
                    geo.set_prim_attr_float(name, prims, float(attrs[i]))
                elif type_ == "index":
                    geo.set_prim_attr_string(name, prims, value[int(attrs[i])])
                else:
                    raise TypeError, "Type '%s' not recognised." % type_
            prims += 1

    return geo
