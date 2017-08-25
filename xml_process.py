#!/usr/bin/env python

#########################################################################
#file name:xml.py
#file description:this file will include xml document parsing and writing
#                 for variety xml formats
#author:joneww
#start date:20170817
#########################################################################

import xml.etree.ElementTree as ET
import string
from xml.dom import minidom
import numpy as np


#########################################################################
#func name:modify_xml_encode
#func description:this function is aimed for modify xml encode from gb2312
#                 to utf-8,because xml.etree.ElementTree can't parse gb2312
#date:20170818
#########################################################################
def modify_xml_encode(file):
    '''

    :param file:the absolute path of input file
    :return:origin file but has been modified
    '''
    #modify string
    file_xml = open(file,"r")
    xml_str = file_xml.read()
    xml_str = unicode(xml_str, encoding='gb2312').encode('utf - 8')
    xml_str = xml_str.replace('<?xml version="1.0" encoding="gb2312"?>', '<?xml version="1.0" encoding="utf-8"?>')
    file_xml.close()

    #modify xml file
    file_xml = open(file, "w")
    file_xml.write(xml_str)
    file_xml.close()

    return file


#########################################################################
#func name:prettify
#func description:input a rough string, and return a pretty format string
#date:20170821
#########################################################################
def prettify(rough_string):
    '''

    :param rough_string:orig xml string
    :return:the pretty string
    '''
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


#########################################################################
#func name:parse_kfb_xml
#func description:parse kfb xml file,
# file structure: <Slide>                            top
#                     <Annotations>                  child
#                         <Regions>                  annotations
#                             <Region ...>           regions
#                                 <Vertices>         vertices
#                                     <Vertice X Y>
#                                     <Vertice X Y>
#                                 </Vertices>
#                             </Region>
#                         </Regions>
#                      </Annotations>
#                  </Slide>
#date:20170818
#########################################################################
def parse_kfb_xml(file, group_name):
    '''

    :param file:kfb annotation xml file for the stand-alone software
    :param group_name:all group name, use for find the group name id
    :return:annos_of_groups, all cor_regions of each group
    '''
    #init group name and group num
    max_group_num = len(group_name)
    annos_of_groups = [[] for i in range(max_group_num)]

    #modify kfb xml encode from gb2312 to utf-8
    file = modify_xml_encode(file)

    #parse xml tree
    tree = ET.parse(file)
    top = tree.getroot() #top = slide

    for child in top:
        if(child.tag == "Annotations"):
            for annotations in child:
                if(annotations.tag == "Regions"):
                    for regions in annotations:
                        g_name = regions.get("Detail")
                        g_name_num = group_name.index(g_name.lower())
                        for vertices in regions:
                            cor_region = []
                            if(vertices.tag == "Vertices"):
                                for vertice in vertices:
                                    x = string.atof(vertice.get("X"))
                                    y = string.atof(vertice.get("Y"))
                                    cor = (x, y)
                                    cor_region.append(cor)
                            annos_of_groups[g_name_num].append(cor_region)
    return annos_of_groups


#########################################################################
#func name:write_coords_inxml_kfb
#func description:write coords in kfb xml format,region info and current
#                 scale is fixed,use ellipse,and 20X
#date:20170821
#########################################################################
def write_coords_inxml_kfb(coords, file, tile_size):
    '''

    :param coords:top left corner coordinate of a rectangle
    :param file:the out xml file path
    :param tile_size:the rectangle's size
    :return:None
    '''
    root = ET.Element("Slide")
    Annotations = ET.SubElement(root, "Annotations")
    Regions = ET.SubElement(Annotations, "Regions")

    end = tile_size-1
    for i in range(len(coords)):
        region = ET.SubElement(Regions,
                                 "Region",
                                 Guid="Ellipse20170728150121",
                                 Name="ASC-US",
                                 Detail="ASC-US",
                                 FontSize="12",
                                 FontItalic="False",
                                 FontBold="False",
                                 Size="2",
                                 FigureType="Ellipse",
                                 Hidden="Visible",
                                 Zoom="20.0",
                                 Visible="Collapsed",
                                 MsVisble="False",
                                 Color="4278190335",
                                 PinType="images/pin_1.png")
        x0,y0 = coords[i]
        x1,y1 = x0+end,y0+end
        Vertices = ET.SubElement(region, "Vertices")
        ET.SubElement(Vertices, "Vertice", X=str(x0/20), Y=str(y0/20))
        ET.SubElement(Vertices, "Vertice", X=str(x1/20), Y=str(y1/20))

    rough_string = ET.tostring(root, 'utf-8')
    f = open(file, "w")
    f.write(rough_string)
    f.close()


#########################################################################
#func name:write_coord_inxml_asap
#func description:write coordinates in xml, support multi-group or specific
#                 group
#date:20170821
#########################################################################
def write_coords_inxml_asap(coords, file, tile_size, group_id):
    '''

    :param coords:top left corner coordinate of a rectangle with multi-group
    :param file:the out xml file path
    :param tile_size:the rectangle's size
    :param group_id:id:the specific group wante to write,None:write the all groups
    :return:None
    '''
    root = ET.Element("ASAP_Annotations")
    annos = ET.SubElement(root, "Annotations")
    annogrps = ET.SubElement(root, "AnnotationGroups")

    group_num = np.shape(coords)[0]
    if(group_id != None):
        group_id_start = group_id
        group_id_end = group_id + 1
    else:
        group_id_start = 1
        group_id_end = group_num + 1

    for group_id in range(group_id_start, group_id_end):
        color = "#00aa00"
        grp_name = 'Group %d' % group_id
        prob_grp = ET.SubElement(annogrps, "Group", Name=grp_name, PartOfGroup="None", Color=color)
        patches = coords[group_id-1]
        end = tile_size - 1
        for i in range(len(patches)):
            patch_head = 'patches'
            x0, y0 = patches[i]
            x1, y1 = x0 + end, y0 + end
            anno = ET.SubElement(annos, "Annotation", Name=patch_head + str(i), \
                                 Type="Polygon", PartOfGroup=grp_name, Color=color)
            coors = ET.SubElement(anno, "Coordinates")
            ET.SubElement(coors, "Coordinate", Order="0", X=str(x0), Y=str(y0))
            ET.SubElement(coors, "Coordinate", Order="1", X=str(x1), Y=str(y0))
            ET.SubElement(coors, "Coordinate", Order="2", X=str(x1), Y=str(y1))
            ET.SubElement(coors, "Coordinate", Order="3", X=str(x0), Y=str(y1))

    rough_string = ET.tostring(root, 'utf-8')
    f = open(file, "w")
    f.write(prettify(rough_string))
    f.close()


##############################test lib func###########################################################
if __name__ == "__main__":
    file = "/home1/zengwx/2017-07-24_16_45_46.kfb.Ano"
    group_name = ["asc-us", "lsil", "hsil", "scc", "ec", "mc"]
    coords = [[[2345,4534],[7896,6757]],[[234,5678]]]
    # modify_xml_encode(file)
    # parse_kfb_xml(file, group_name)
    write_coords_inxml_asap(coords, "kfb.Ano", 128, 2)



