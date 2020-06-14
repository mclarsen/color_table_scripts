import sys
import os
import xml.etree.ElementTree as ET

def getControlPoints(ctrl, pos):
  pt0 = 0
  pt1 = 0
  while pt1 < len(ctrl)-1 and ctrl[pt1] < pos:
    pt1 += 1
  if pt1 != 0:
    pt0 = pt1 - 1
  if pt1 == len(ctrl) - 1:
    pt0 = pt1
  return (pt0,pt1)

def interpolate(positions,colors,x):
  x = max(0.0, min(1.0, x))
  (a,b) = getControlPoints(positions,x)
  delta = positions[b] - positions[a]
  f = 0
  if delta != 0:
    f = (x - positions[a]) / (positions[b] - positions[a])
  print(a,b)
  print(positions[a], " -- ", x, " -- ", positions[b])
  print("diff", f)
  return [colors[a][0] + (colors[b][0] - colors[a][0]) * f,
          colors[a][1] + (colors[b][1] - colors[a][1]) * f,
          colors[a][2] + (colors[b][2] - colors[a][2]) * f]

def interpolate_or_clip(colormap, x):
  if   x < 0.0: return [0.0, 0.0, 0.0]
  elif x > 1.0: return [1.0, 1.0, 1.0]
  else: return interpolate(colormap, x)

## load source xml file
def load_xml(xml):
  try:
    xmldoc = ET.parse(xml)
  except IOError as e:
    print ('The input file is invalid. It must be a colormap xml file. Go to https://sciviscolor.org/home/colormaps/ for some good options')
    print ('Go to https://sciviscolor.org/matlab-matplotlib-pv44/ for an example use of this script.')
    sys.exit()
  data_vals=[]
  color_vals=[]
  for s in xmldoc.getroot().findall('.//Point'):
    data_vals.append(float(s.attrib['x']))
    color_vals.append((float(s.attrib['r']),float(s.attrib['g']),float(s.attrib['b'])))
  return {'color_vals':color_vals, 'data_vals':data_vals}

def point(pos,r,g,b):
  ety = """
    <Object name="ColorControlPoint">
        <Field name="colors" type="unsignedCharArray" length="3">%d %d %d</Field>
        <Field name="position" type="float">%s</Field>
    </Object>
""" % (r*255,g*255,b*255,pos)
  return ety

def to_visit(cmap_file):
    vals = load_xml(cmap_file)
    colors = vals['color_vals']
    position = vals['data_vals']
    txt = """
<?xml version="1.0"?>
<Object name="ColorTable">
    <Field name="Version" type="string">3.0.1</Field>
    <Object name="ColorControlPointList">
"""

    print(len(position))
    print(interpolate(position, colors, -1))
    samples = 256
    for i in range(0,samples):
      pos = float(i) / float(samples)
      color = interpolate(position, colors, pos)
      print(color)
      txt+= point(pos, color[0],color[1], color[2])
#if position[0] != 0:
#      txt+=point(0,colors[0][0], colors[0][1], colors[0][2])
#    for pos, color in zip(position, colors):
#      txt+= point(pos, color[0],color[1], color[2])
#    if position[-1] != 1:
#      txt+=point(1,colors[-1][0], colors[-1][1], colors[-1][2])

    txt+="""
        <Field name="category" type="string">UserDefined</Field>
    </Object>
</Object>
"""
    return txt

r = to_visit("color_tables/gr-insert_80-100.xml")
open("test.ct","w").write(r)

