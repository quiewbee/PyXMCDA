#############################################################################
#
# Copyright 2010 University of Luxembourg    
#
# Contributors :
# Thomas Veneziano
# thomas.veneziano@uni.lu
#
# This software is a package for Python
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software.  You can  use, 
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info". 
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability. 
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security. 
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
##############################################################################


XMCDA_2_0 = "http://sma.uni.lu/d2cms/xmcda/_downloads/XMCDA-2.0.0.xsd"

from lxml import etree


##########################################################################
#                                                                        #
#                         PARSING AND VALIDATING                         #
#                                                                        #
##########################################################################


def parseValidate (xmlfile) :
	
	try :
		# TODO (sbigaret) explain that!
		xmlschema_doc = etree.parse(XMCDA_2_0,
					    etree.XMLParser(no_network=False))
		xmlschema = etree.XMLSchema(xmlschema_doc)
		
		xmltree = etree.parse(open(xmlfile, 'r'))
		
		if xmlschema.validate(xmltree) :
			return xmltree.getroot()
		else:
			return None
			
	except :
		return None
		
		
##########################################################################
#                                                                        #
#                             GET THE VALUES                             #
#                                                                        #
##########################################################################		
		
		
def getValue(xmltree) :

	try :
		xmlvalue = xmltree.find("value")
		if xmlvalue.find("integer") != None :
			val = int(xmlvalue.find("integer").text)
		elif xmlvalue.find("real") != None :
			val = float(xmlvalue.find("real").text)
		elif xmlvalue.find("interval") != None :
			val = "INTERVAL !"
		elif xmlvalue.find("rational") != None :
			val = float(xmlvalue.find("rational/numerator").text)/float(xmlvalue.find("rational/denominator").text)
		elif xmlvalue.find("label") != None :
			val = xmlvalue.find("label").text
		elif xmlvalue.find("rankedlabel") != None :
			val = float(xmlvalue.find("rank").text)
		elif xmlvalue.find("boolean") != None :
			val = xmlvalue.find("boolean").text
		elif xmlvalue.find("NA") != None :
			val = "NA"
		elif xmlvalue.find("image") != None :
			val = "IMAGE !"
		elif xmlvalue.find("imageRef") != None :
			val = "IMAGEREF !"
		else :
			val = None
	except :
		val = None

	return val

	
##########


def getValues(xmltree) :

	try :
		xmlvalues = xmltree.find("values")
		if xmlvalues != None :
			values = []
			for val in xmlvalues.findall("value") :
				values.append(getValue(val))
	except :
		values = None

	return values

	
	
##########


def getNumericValue(xmltree) :

	# Only returns the value if it is numeric
	
	try :
		xmlvalue = xmltree.find("value")
		if xmlvalue.find("integer") != None :
			val = int(xmlvalue.find("integer").text)
		elif xmlvalue.find("real") != None :
			val = float(xmlvalue.find("real").text)
		elif xmlvalue.find("rational") != None :
			val = float(xmlvalue.find("rational/numerator").text)/float(xmlvalue.find("rational/denominator").text)
		elif xmlvalue.find("NA") != None :
			val = "NA"
		else :
			val = None
	except :
		val = None
	
	return val
	
	
##########


def getNumericPerformanceTableValue (xmltree) :
	
	# Cette fonction retourne les valeurs utilisables pour un tableau de performance numerique, et met None pour toute autre valeur

	try :
		xmlvalue = xmltree.find("value")
		if xmlvalue.find("integer") != None :
			val = int(xmlvalue.find("integer").text)
		elif xmlvalue.find("real") != None :
			val = float(xmlvalue.find("real").text)
		elif xmlvalue.find("rational") != None :
			val = float(xmlvalue.find("rational/numerator").text)/float(xmlvalue.find("rational/denominator").text)
		elif xmlvalue.find("rankedLabel") != None :
			val = float(xmlvalue.find("rankedLabel/rank").text)
		elif xmlvalue.find("boolean") != None :
			if xmlvalue.find("boolean").text == "true":
				val = 1
			else:
				val = 0
		else :
			val = None
	except :
		val = None
	
	return val


##########


def getSimpleValue (xmltree) :
	
	# Cette fonction retourne tous les types simples, c'est a dire tous sauf les intervalles, et les images

	try :
		xmlvalue = xmltree.find("value")
		if xmlvalue.find("integer") != None :
			val = int(xmlvalue.find("integer").text)
		elif xmlvalue.find("real") != None :
			val = float(xmlvalue.find("real").text)
		elif xmlvalue.find("rational") != None :
			val = float(xmlvalue.find("rational/numerator").text)/float(xmlvalue.find("rational/denominator").text)
		elif xmlvalue.find("label") != None :
			val = xmlvalue.find("label").text
		elif xmlvalue.find("rankedLabel") != None :
			val = float(xmlvalue.find("rankedLabel/rank").text)
		elif xmlvalue.find("boolean") != None :
			val = xmlvalue.find("boolean").text
		elif xmlvalue.find("NA") != None :
			val = "NA"
		else :
			val = None
	except :
		val = None
	
	return val


##########


def getAlternativeValue (xmltree, alternativesId) :

	values = {}
	
	for alternativeValue in xmltree.findall ("alternativesValues/alternativeValue") :
		alt = alternativeValue.find ("alternativeID").text
		if alternativeId.count(alt) > 0 :
			values[alt] = getValue (alternativeValue)

	return values


##########


def getCriterionValue (xmltree, criteriaId) :

	values = {}
	
	for criterionValue in xmltree.findall ("criteriaValues/criterionValue") :
		crit = criterionValue.find ("criterionID").text
		if criteriaId.count(crit) > 0 :
			values[crit] = getValue (criterionValue)

	return values
	

##########################################################################
#                                                                        #
#                         OBTAINING A LIST OF ID                         #
#                                                                        #
##########################################################################


def getAlternativesID (xmltree, condition="ACTIVE") :

	# Retourne la liste des alternatives, selon la condition suivante : ALL, ACTIVE, INACTIVE
	# Par defaut, uniquement les alternatives ACTIVE
	# On suppose que si rien n'est precise, l'alternative est active
	
	alternativesID = []

	for listAlternatives in xmltree.findall('alternatives'):
		for alternative in listAlternatives.findall('alternative'):
			active = alternative.find('active')
			if condition == "ACTIVE" and (active == None or active.text == "true") :
				alternativesID.append(str(alternative.get('id')))
			elif condition == "INACTIVE" and (active != None and active.text == "false") :
				alternativesID.append(str(alternative.get('id')))
			elif condition == "ALL" :
				alternativesID.append(str(alternative.get('id')))

	return alternativesID


##########


def getCriteriaID (xmltree, condition="ACTIVE") :

	# Retourne la liste des criteres, selon la condition suivante : ALL, ACTIVE, INACTIVE
	# Par defaut, uniquement les criteres ACTIVE
	# On suppose que si rien n'est precise, le critre est actif
	
	criteriaID = []

	for listCriteria in xmltree.findall('criteria'):
		for criterion in listCriteria.findall('criterion'):
			active = criterion.find('active')
			
			if condition == "ACTIVE" and (active == None or active.text == "true") :
				criteriaID.append(str(criterion.get('id')))
			elif condition == "INACTIVE" and (active != None and active.text == "false") :
				criteriaID.append(str(criterion.get('id')))
			elif condition == "ALL" :
				criteriaID.append(str(criterion.get('id')))
				
	return criteriaID


##########


def getAttributesID (xmltree, condition="ACTIVE") :

	# Retourne la liste des attributs, selon la condition suivante : ALL, ACTIVE, INACTIVE
	# Par defaut, uniquement les attributs ACTIVE
	# On suppose que si rien n'est precise, le attributs est actif
	
	attributesID = []

	for listAttributes in xmltree.findall('attributes'):
		for attribute in listAttributes.findall('attribute'):
			active = attribute.find('active')
			
			if condition == "ACTIVE" and (active == None or active.text == "true") :
				attributesID.append(str(attribute.get('id')))
			elif condition == "INACTIVE" and (active != None and active.text == "false") :
				attributesID.append(str(attribute.get('id')))
			elif condition == "ALL" :
				attributesID.append(str(attribute.get('id')))
				
	return attributesID


##########


def getCategoriesID (xmltree) :

	# Retourne la liste des categories
	
	categoriesId = []

	for listCategories in xmltree.findall('categories'):
		for category in listCategories.findall('category'):
			categoriesId.append(str(category.get('id')))
			
	return categoriesId
	
##########

def getCategoriesRank(xmltree, catId):

	categoriesRank = {}
	for cat in catId :
		try :
			xml_dir = xmltree.xpath(".//category[@id='"+cat+"']/rank/integer")[0] #FIXME: Always integer?
			categoriesRank[cat] = int(xml_dir.text)
		except :
			categoriesRank[cat] = -1

	return categoriesRank

##########

def getAlternativesReferences (xmltree, altId) :

	# Returns the list of alternativeID given in xmltree, only if they are all present in altId (if not, it returns an empty list)
	
	listId = []
	
	xmlId =  xmltree.find("alternativeID")
	if xmlId != None :
		if altId.count(xmlId.text) > 0 :
			listId.append(xmlId.text)
	else :
		for xmlId in xmltree.findall("alternativesSet/element/alternativeID") :
			if altId.count(xmlId.text) > 0 :
				listId.append(xmlId.text)
			else :
				listId = []
				break

	return listId
	

##########


def getCriteriaReferences (xmltree, criId) :

	# Returns the list of criterionID given in xmltree, only if they are all present in criId (if not, it returns an empty list)
	
	listId = []
	
	xmlId =  xmltree.find("criterionID")
	if xmlId != None :
		if criId.count(xmlId.text) > 0 :
			listId.append(xmlId.text)
	else :
		for xmlId in xmltree.findall("criteriaSet/element/criterionID") :
			if criId.count(xmlId.text) > 0 :
				listId.append(xmlId.text)
			else :
				listId = []
				break

	return listId


##########################################################################
#                                                                        #
#                        GET THE PERFORMANCE TABLE                       #
#                                                                        #
##########################################################################


def getPerformanceTable (xmltree, alternativesId, criteriaId) :

	perfTable = xmltree.find(".//performanceTable")
	
	Table = {}
	
	if perfTable != None :
	
		allAltPerf = perfTable.findall("alternativePerformances")
		for altPerf in allAltPerf :
			alt = altPerf.find("alternativeID").text
			Table[alt]={}
			allCritPerf = altPerf.findall("performance")
			for critPerf in allCritPerf :
				crit = critPerf.find("criterionID").text
				val = getSimpleValue(critPerf)
				Table[alt][crit] = val
						
	return Table
	

##########


def getNumericPerformanceTable (xmltree, alternativesId, criteriaId) :

	perfTable = xmltree.find(".//performanceTable")
	
	Table = {}
	
	if perfTable != None :
	
		allAltPerf = perfTable.findall("alternativePerformances")
		for altPerf in allAltPerf :
			alt = altPerf.find("alternativeID").text
			Table[alt]={}
			allCritPerf = altPerf.findall("performance")
			for critPerf in allCritPerf :
				crit = critPerf.find("criterionID").text
				val = getNumericPerformanceTableValue(critPerf)
				Table[alt][crit] = val
						
	return Table


##########################################################################
#                                                                        #
#                         GET THE XXX COMPARISONS                        #
#                                                                        #
##########################################################################


def getAlternativesComparisons (xmltree, altId, mcdaConcept=None) :

	#Retourne le premier alternativeComparisons trouve avec le bon MCDAConcept (si precise)
	#Par la suite, retourner une liste ?
	
	if mcdaConcept == None :
		strSearch = ".//alternativesComparisons"
	else :
		strSearch = ".//alternativesComparisons[@mcdaConcept=\'"+mcdaConcept+"\']"

	comparisons = xmltree.xpath(strSearch)[0]

	if comparisons == None :
		return {}
	
	else :
	
		datas = {}
		
		for pair in comparisons.findall ("pairs/pair") :
			init = pair.find("initial/alternativeID").text
			term = pair.find("terminal/alternativeID").text
			val = getNumericValue(pair)
			
			# Only the alternatives concerned
			if altId.count(init) > 0 :
				if altId.count(term) > 0 :
					# We check if init is still an entry in the table
					if not(datas.has_key(init)) :
						datas[init] = {}
					datas[init][term] = val

		return datas


##########


def getCriteriaComparisons (xmltree, criId, mcdaConcept=None) :

	#Retourne le premier criteriaComparisons trouve avec le bon MCDAConcept (si precise)
	#Par la suite, retourner une liste ?
	
	if mcdaConcept == None :
		strSearch = ".//criteriaComparisons"
	else :
		strSearch = ".//criteriaComparisons[@mcdaConcept=\'"+mcdaConcept+"\']"

	comparisons = xmltree.xpath(strSearch)[0]

	if comparisons == None :
		return []
	
	else :
	
		datas = []
		
		for pair in comparisons.findall ("pairs/pair") :
		
			comp = {}
			comp["initial"] = getCriteriaReferences(pair.find("initial"), criId)
			comp["terminal"] = getCriteriaReferences(pair.find("terminal"), criId)
			
			if comp["initial"] != [] and comp["terminal"] != [] :
				comp["val"] = getNumericValue(pair)
				datas.append(comp)
			
		return datas


##########################################################################
#                                                                        #
#                            GET THE THRESHOLDS                          #
#                                                                        #
##########################################################################


def getConstantThresholds (xmltree, critId) :

	thresholds = {}
	
	try:
	
		#On suppose pour le moment que les seuils sont constants
		for criterion in xmltree.findall(".//criterion") :
			criterionID = criterion.get("id")
			xmlthresholds = criterion.find("thresholds")
			if xmlthresholds != None :
				tempThresholds = {}
				for xmlthreshold in xmlthresholds.findall("threshold") :
					xmlVal = xmlthreshold.find("constant/real")
					if xmlVal == None :
						xmlVal = xmlthreshold.find("constant/integer")
					if xmlVal != None :
						if xmlthreshold.get("mcdaConcept") != None :
							tempThresholds[xmlthreshold.get("mcdaConcept")] = float(xmlVal.text)
				thresholds[criterionID] = tempThresholds
			else :
				thresholds[criterionID] = {}

	except :
		return None
		
	return thresholds
	
	
##########################################################################
#                                                                        #
#                      GET CRITERION SCALE INFORMATION                   #
#                                                                        #
##########################################################################


def getCriteriaScalesTypes (xmltree, critId) :
	scalesTypes = {}
	for crit in critId :
		try :
			xml_cri = xmltree.xpath(".//criterion[@id='"+crit+"']")[0]
			if xml_cri.find("scale/qualitative") != None :
				scalesTypes[crit] = "qualitative"
			else :
				scalesTypes[crit] = "quantitative"
		except :
			scalesTypes[crit] = "quantitative"
	return scalesTypes


##########

	
def getCriteriaPreferenceDirections (xmltree, critId) :
	prefDir = {}
	for crit in critId :
		try :
			xml_dir = xmltree.xpath(".//criterion[@id='"+crit+"']/scale/*/preferenceDirection")[0]
			prefDir[crit] = xml_dir.text
		except :
			prefDir[crit] = "max"
	return prefDir


##########


def getCriteriaLowerBounds (xmltree, critId) :
	LB = {}
	for crit in critId :
		try :
			xml_val = xmltree.xpath(".//criterion[@id='"+crit+"']/scale/quantitative/minimum/*")[0]
			LB[crit] = float(xml_val.text)
		except :
			LB[crit] = None
	return LB


##########


def getCriteriaUpperBounds (xmltree, critId) :
	UB = {}
	for crit in critId :
		try :
			xml_val = xmltree.xpath(".//criterion[@id='"+crit+"']/scale/quantitative/maximum/*")[0]
			UB[crit] = float(xml_val.text)
		except :
			UB[crit] = None
	return UB


##########


def getCriteriaRankedLabel (xmltree, critId) :
	RL = {}
	for crit in critId :
		try :
			xml_val = xmltree.xpath(".//criterion[@id='"+crit+"']/scale/qualitative")[0]
			if xml_val == None :
				RL[crit] = None
			else :
				RL[crit] = {}
				for rankedLabel in xml_val.findall("rankedLabel") :
					RL[crit][rankedLabel.find("rank").text] = rankedLabel.find("label").text
		except :
			RL[crit] = None
	
	return RL


##########################################################################
#                                                                        #
#                            GET THE PARAMETERS                          #
#                                                                        #
##########################################################################


def getParameterByName (xmltree, paramName, paramFamilyName = None) :
	try :
		if paramFamilyName == None :
			param = xmltree.xpath(".//parameter[@name='"+paramName+"']")[0]
		else :
			param = xmltree.xpath(".//methodParameters[@name=\'"+paramFamilyName+"\']/parameter[@name=\'"+paramName+"\']")[0]
		if param != None :
			return getValue(param)
		else :
			return None
	except :
		return None


##########


def getParametersByName (xmltree, paramName, paramFamilyName = None) :
	try :
		if paramFamilyName == None :
			params = xmltree.xpath(".//parameters[@name='"+paramName+"']")[0]
		else :
			params = xmltree.xpath(".//methodParameters[@name=\'"+paramFamilyName+"\']/parameters[@name=\'"+paramName+"\']")[0]
		if params != None :
			paramList = []
			for param in params.findall("parameter") :
				paramList.append(getValue(param))
			return paramList
		else :
			return {}
	except :
		return {}
		

##########


def getNamedParametersByName (xmltree, paramName, paramFamilyName = None) :
	try :
		if paramFamilyName == None :
			params = xmltree.xpath(".//parameters[@name='"+paramName+"']")[0]
		else :
			params = xmltree.xpath(".//methodParameters[@name=\'"+paramFamilyName+"\']/parameters[@name=\'"+paramName+"\']")[0]
			
		if params != None :
			paramList = {}
			for param in params.findall("parameter") :
				index = param.get("name")
				if index :
					paramList[index] = getValue(param)
			return paramList
		else :
			return {}
	except :
		return {}
			
##########################################################################
#                                                                        #
#                      GET ALTERNATIVES AFFECTATION                      #
#                                                                        #
##########################################################################

def getAlternativesAffectations(xmltree):
    affectations = xmltree.find(".//alternativesAffectations")
	
    table = {}
    if affectations != None :
        alts_aff = affectations.findall("alternativeAffectation")
        for alt_aff in alts_aff :
            alt = alt_aff.find("alternativeID").text
            aff = alt_aff.find("categoryID").text
            table[alt] = aff

    return table

##########################################################################
#                                                                        #
#                              WRITE IN FILES                            #
#                                                                        #
##########################################################################


def writeHeader (xmlfile) :
	xmlfile.write ("<?xml version='1.0' encoding='UTF-8'?>\n<?xml-stylesheet type='text/xsl' href='xmcdaXSL.xsl'?>\n")
	xmlfile.write("<xmcda:XMCDA xmlns:xmcda='http://www.decision-deck.org/2009/XMCDA-2.0.0' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:schemaLocation='http://www.decision-deck.org/2009/XMCDA-2.0.0 http://sma.uni.lu/d2cms/xmcda/_downloads/XMCDA-2.0.0.xsd'>\n\n")


##########


def writeFooter (xmlfile) :
	xmlfile.write ("\n</xmcda:XMCDA>\n")


##########


def createMessagesFile (fileName, logMess, warnMess, errorMess):
	# Creating a message file
	
	xmlfile = open(fileName, 'w')
	writeHeader (xmlfile)
	
	writeMessages (xmlfile, logMess, warnMess, errorMess)
		
	writeFooter(xmlfile)
	xmlfile.close()


##########


def writeMessages (xmlfile, logMess, warnMess, errorMess) :
	xmlfile.write ("<methodMessages>\n")
	for message in logMess :
		xmlfile.write ("<logMessage><text><![CDATA["+message+"]]></text></logMessage>\n")
	for message in warnMess :
		xmlfile.write ("<message><text>WARNING : <![CDATA["+message+"]]></text></message>\n")
	for message in errorMess :
		xmlfile.write ("<errorMessage><text><![CDATA["+message+"]]></text></errorMessage>\n")
	xmlfile.write ("</methodMessages>\n")


##########


def writeLogMessages (xmlfile, messages) :
	xmlfile.write ("<methodMessages>\n")
	for message in messages :
		xmlfile.write ("<logMessage><text><![CDATA["+message+"]]></text></logMessage>\n")
	xmlfile.write ("</methodMessages>\n")


##########


def writeErrorMessages (xmlfile, messages) :
	xmlfile.write ("<methodMessages>\n")
	for message in messages :
		xmlfile.write ("<errorMessage><text><![CDATA["+message+"]]></text></errorMessage>\n")
	xmlfile.write ("</methodMessages>\n")


##########################################################################
#                                                                        #
#                              MISCELLANEOUS                             #
#                                                                        #
##########################################################################


def getStringPart (string, namePart) :
	return (string.partition("###"+namePart+"###")[2]).partition("@@@")[0]


##########


def getCleanedStringPart (string, namePart) :
	# Retire la liste de cplexamp
	str = (string.partition("###"+namePart+"###")[2]).partition("@@@")[0]
	while str.partition ("cplexamp: ")[1] != "" :
		str = str.partition ("cplexamp: ")[2]
	return str


##########


def getListOnString (stringList, sepBefore, sepAfter, sepBetween) :

	# Write a list of string, putting some separator before and after each element and another separator between each of them
	#Sample : getListOnString (["a","o","i"], "v", "l", " ; ") -> "val ; vol ; vil" 
	
	if len(stringList) == 0 :
		return ""
	else :
		tempString = ""
		tempString += sepBefore + str(stringList[0]) + sepAfter
		for item in xrange (1, len(stringList)) :
			tempString += sepBetween + sepBefore + str(stringList[item]) + sepAfter
		
	return tempString


##########


def scaleValue (val, LB1, UB1, LB2, UB2) :
	
	# Scale a value, from the original scale [LB1, UB1] to [LB2, UB2]
	if LB1 == UB1 :
		# Division by 0
		return None
	else :
		a = (UB2-LB2)/(UB1-LB1)
		b = UB2 - a * UB1
		
		return a * val + b


##########


def scaleIntValue (val, LB1, UB1, nbRank) :

	# Scale a value, from the original scale [LB1, UB1] and return the integer corresponding to the closest rank 
	if LB1 == UB1 :
		# Division by 0
		return 0
	else :
		a = nbRank/(UB1-LB1)
		b = nbRank - a * UB1
		val = a * val + b
		
		ind = 0
		for i in range (nbRank) :
			if abs(val-i) < abs(val-ind) :
				ind = i
	
		return ind
		
		
##########

def getRubisElementaryOutranking (altId, critId, perfTable, thresholds) :
		
	#print perfTable
	#print thresholds
		
	ElemOut = {}
	for alt1 in altId :
		ElemOut[alt1] = {}
		for alt2 in altId :
			ElemOut[alt1][alt2] = {}
			for crit in critId :
				if perfTable[alt1][crit] >= perfTable[alt2][crit] :
					ElemOut[alt1][alt2][crit] = 1.0
				else :
					if not thresholds[crit].has_key('indifference') and not thresholds[crit].has_key('preference') :
						# aucun seuil, indif ou pref, defini
						ElemOut[alt1][alt2][crit] = 0.0
					else :
						if (thresholds[crit].has_key('indifference') != thresholds[crit].has_key('preference')) :
							#un seuil, indif ou pref, est defini
							if thresholds[crit].has_key('indifference') :
								if perfTable[alt1][crit] + thresholds[crit]["indifference"] >= perfTable[alt2][crit] :
									ElemOut[alt1][alt2][crit] = 1.0
								else :
									ElemOut[alt1][alt2][crit] = 0.0
							else :
								if perfTable[alt1][crit] + thresholds[crit]["preference"] >= perfTable[alt2][crit] :
									ElemOut[alt1][alt2][crit] = 1.0
								else :
									ElemOut[alt1][alt2][crit] = 0.0
						else :
							# il y a deux seuils
							if perfTable[alt1][crit] + thresholds[crit]["indifference"] >= perfTable[alt2][crit] :
								ElemOut[alt1][alt2][crit] = 1.0
							elif perfTable[alt1][crit] + thresholds[crit]["preference"] >= perfTable[alt2][crit] :
								ElemOut[alt1][alt2][crit] = 0.5
							else :
								ElemOut[alt1][alt2][crit] = 0.0					
	return ElemOut
	
##########

def getVetos (altId, critId, perfTable, thresholds) :
	# Retourne un tableau qui retourne, pour chaque couple ordonne, l'ensemble des criteres soulevant un veto fort. Si l'ensemble est None, il n'y a pas de veto.
	tabVeto = {}
	for alt1 in altId :
		for alt2 in altId :
			for crit in critId :
				if thresholds[crit].has_key('veto') :
					if perfTable[alt1][crit] + thresholds[crit]["veto"] < perfTable[alt2][crit] :
						if not tabVeto.has_key(alt1) :
							tabVeto[alt1] = {}
						if not tabVeto[alt1].has_key(alt2) :
							tabVeto[alt1][alt2] = {}
						tabVeto[alt1][alt2][crit] = 1
	return tabVeto

	
