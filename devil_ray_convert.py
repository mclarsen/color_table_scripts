import sys
import os
import xml.etree.ElementTree as ET

## load source xml file
def load_xml(xml):
  try:
    xmldoc = ET.parse(xml)
  except IOError as e:
    print ('The input file is invalid. It must be a colormap xml file. Go to https://sciviscolor.org/home/colormaps/ for some good options')
    sys.exit()
  data_vals=[]
  color_vals=[]
  for s in xmldoc.getroot().findall('.//Point'):
    data_vals.append(float(s.attrib['x']))
    color_vals.append((float(s.attrib['r']),float(s.attrib['g']),float(s.attrib['b'])))
  return {'color_vals':color_vals, 'data_vals':data_vals}

def point(pos,r,g,b):
  ety = '      %s, %s, %s, %s,\n' % (pos, r, g, b)
  return ety

def point_last(pos,r,g,b):
  ety = '      %s, %s, %s, %s\n' % (pos, r, g, b)
  ety +='    }\n'
  return ety

def to_devil_ray(cmap_file):
    vals = load_xml(cmap_file)
    colors = vals['color_vals']
    position = vals['data_vals']
    name = os.path.basename(cmap_file).split('.')[0]
    txt = '  {\"' + name + '\",\n'
    txt += '    {\n'
    if position[0] != 0:
      txt+=point(0,colors[0][0], colors[0][1], colors[0][2])

    has_last = position[-1] == 1

    for i, (pos, color) in enumerate(zip(position, colors)):
      if i == len(colors) -1 and has_last:
        txt+= point_last(pos, color[0],color[1], color[2])
      else:
        txt+= point(pos, color[0],color[1], color[2])

    if position[-1] != 1:
      txt+=point_last(1,colors[-1][0], colors[-1][1], colors[-1][2])

    txt += '  },\n'

    return txt

r = to_devil_ray("color_tables/5-wave-yellow-to-blue.xml")
print(r)
#open("import.txt","w").write(r)

