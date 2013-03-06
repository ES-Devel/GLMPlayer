# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

from xml.dom.minidom import Document

from xml.dom import minidom

class xml_parser():      
    
    def __init__(self,xfile,root):
        self.xml_file = xfile
        self.dom = minidom.parse(self.xml_file)
        self.root_element = self.dom.getElementsByTagName(root)
    
    def get_node(self,tag):
        return self.dom.getElementsByTagName(tag)
        
    def get_root(self):
        return self.root_element[0] 
       
    def create_node_value(self,node,value,parent):
        new_node=self.dom.createElement(node)
		parent.appendChild(new_node)
		content=self.dom.createTextNode(value)
		new_node.appendChild(content)
		
	def create_node(self,node,parent):
	    new_node=self.dom.createElement(node)
	    parent.appendChild(new_node)
	    return new_node
		
	def update_xml(self):
	    xmldocument=open(self.xml_file,"w")
		self.dom.writexml(xmldocument)
		xmldocument.close()
        
    def get_list_of_elements(self,tag):
        return self.dom.getElementsByTagName(tag)
        
    def search_value_by_pos(self,tag,index):
        return self.dom.getElementsByTagName(tag)[index].firstChild.data
        
    def delete_by_terms(self,p_tag,c_tag,search_term):
        found = -1
		for i in range(0,len(self.dom.getElementsByTagName(c_tag))):
			if search_term.find(self.dom.getElementsByTagName(c_tag)[i].firstChild.data) >= 0:
				found=i
		self.get_root().removeChild(self.dom.getElementsByTagName(p_tag)[found])
		
	def reset_but_keep_root(self,root_tag):
	    doc=open(self.xml_file,"w")
		doc.write('<?xml version="1.0" ?><'+root_tag+'></'+root_tag+'>')
		doc.close()
		
	def get_value_by_terms(self,p_tag,c_tag,search_term,num):
        value = ''
		for i in range(0,num):
			if search_term.find(self.dom.getElementsByTagName(p_tag)[i].firstChild.data) >= 0:
			    value = self.dom.getElementsByTagName(c_tag)[i].firstChild.data
	    return value
	    
	def set_value_by_terms(self,p_tag,c_tag,search_term,num,value):
		for i in range(0,num):
			if search_term.find(self.dom.getElementsByTagName(p_tag)[i].firstChild.data) >= 0:
			    self.dom.getElementsByTagName(c_tag)[i].firstChild.data = value
