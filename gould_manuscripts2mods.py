# -- coding: utf-8 --
import csv, sys, time, datetime, xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

#2015-10-07. Converts gould_manuscripts_20151110.csv to MODS
# these are not as cleanly 
# dict[key][0] etc
# add second date for bird ksrl_sc_gould_ng_1_2_002.tif - 1880:01:01
xmlFile = 'newBatch.xml'
xmlData = open(xmlFile, 'w')
dataFile=sys.argv[1]

ts=time.time()
st=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

root = Element('mods:modsCollection')
root.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
root.set('xmlns:mods', 'http://www.loc.gov/mods/v3')
root.set('xsi:schemaLocation', 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd')
tree = ET.ElementTree(root)

artists={'JG':'Gould, John, 1804-1881','H':'Hart, William Matthew, 1830-1908', 'R':'Richter, Henry Constantine, 1821-1902','EG':'Gould, Elizabeth, 1804-1841',
'K':'Krefft, Gerard, 1830-1881', 'L':'Lear, Edward, 1812-1888','W':'Wolf, Joseph, 1820-1899','FM':'McCoy, Frederick, 1823-1899','TWW':'Wood, Thomas Waterman, 1823-1903',
'FRS':'Stack, F.R.','GB':'Bedde, George','RBS':'Sing, Raj been','LG':'Gould, Louisa, 1837-','RK':'Kretschmer, Robert, 1812-1872','SG':'Gould, Sarah, 1841-1911',
'WDE':'Erck, W.D.','JHG':'Gould, John Henry'}

printers={'CH':'C. Hullmandel, Imp.',
'WALTER':'T. Walter, Imp.',
'W':'T. Walter, Imp.',
'CH, W':'Hullmandel & Walton, Imp.',
'CH, WALTON':'Hullmandel & Walton, Imp.',
'WALTER, COHN':'Walter & Cohn, Imp.',
'TW':'T. Walter, Imp.',
'Hullmandel & Walton':'Hullmandel & Walton, Imp.'}

#title,date,place,publisher, callno, oclcno

books={'HM':['Century of birds from the Himalaya Mountains','1831','London','Gould, John, 1804-1881','Ellis Aves H121','ocm09637074'],
'OD':['Monograph of the Odontophorinae, or partridges of America','1850','London','Gould, John, 1804-1881','Ellis Aves H128','ocm04582685'],
'RA':['Monograph of the Ramphastidae, or family of toucans','1834','London','Gould, John, 1804-1881','Ellis Aves H17','ocm05898907'],
'TR':['Monograph of the Trogonidae, or family of trogons','1835-1838','London','Gould, John, 1804-1881','Ellis Aves H135','ocm15167573'],
'AS':['Birds of Asia','1850-1883','London','Taylor and Francis','Ellis Aves H120','ocm07297872'],
'AU':['Birds of Australia','1848','London','Printed by R. and J.E. Taylor','Ellis Aves H141','ocm07752160'],
'EU':['Birds of Europe','1837','London','R. and J.E. Taylor','Ellis Aves H132','ocm04485568'],
'GB':['Birds of Great Britain','1873','London','Printed by Taylor and Francis','Ellis Aves H131','ocm04275233'],
'HB':['Monograph of the Trochilidae, or family of hummingbirds','1861-1887','London','Gould, John, 1804-1881','Ellis Aves H91','ocm07484123'],
'KR':['Monograph of the Macropodidae, or family of kangaroos','1841-1872','London','Gould, John, 1804-1881','Ellis Omnia H80','ocm07528705'],
'MM':['Introduction to the mammals of Australia','1863','London','Printed for the author by Taylor and Francis','Ellis Omnia C547','ocm10249957'],
'NG':['The birds of New Guinea and the adjacent Papuan islands, including many new species recently discovered in Australia','1875-1888','London','H. Sotheran & Co.','Ellis Aves H129','ocm07748327'],
'PI':['Monograph of the Pittidae','1880-1881','London','Gould, John, 1804-1881','Ellis Aves H142','ocm09638814'],
'AA':['Birds of Australia, and the adjacent islands','1837-1838','London','Gould, John, 1804-1881','Ellis Aves H125','ocm31830935'],
'PA':['Monograph of the Paradiseidae, or birds of paradise and Ptilonorhynchidae, or bower-birds','1891-1898','London','H. Sotheran','Ellis Aves H127','ocm34087120'],
'IA':['Icones Avium, or, figures and descriptions of new and interesting species of birds from various part of the globe','1837-1838','London','Gould, John, 1804-1881','Ellis Aves H106','ocm38881658']}


with open(dataFile, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    

    for row in reader:

        record = SubElement(root, 'mods:mods')
        record.set('xsi:schemaLocation', 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd')
        # inserts filename as local identifier
        identifier = SubElement(record, 'mods:identifier')
        identifier.set('type', 'local')
        identifier.text = row['FullFileName']

        # titles are less common for these draft images
        titleInfo = SubElement(record, 'mods:titleInfo')
        title=SubElement(titleInfo,'mods:title')
        # first try and take SubjectNote column as title
        if len(row['SubjectNote'])>0:
            title.text = row['SubjectNote']
        # if nothing there, use concatenation of genus and species
        elif len(row['Bird_1_GenusOnPiece'])>0:
            title.text= row['Bird_1_GenusOnPiece'] +' '+ row['Bird_1_SpeciesOnPiece']
        # otherwise, call it untitled and look at it later.
        else: 
            title.text='Untitled'
        
        typeImage=SubElement(record,'mods:typeOfResource')
        typeImage.text='still image'

        # for each bird on piece, make individual subjects using genus and species
        if len(row['Bird_1_GenusOnPiece'])>0 and len(row['Bird_1_SpeciesOnPiece'])>0:
            subject=SubElement(record,'mods:subject')
            topSubject=SubElement(subject,'mods:topic') 
            topSubject.text=row['Bird_1_GenusOnPiece']+' '+row['Bird_1_SpeciesOnPiece']
        if len(row['Bird_2_GenusOnPiece'])>0 and len(row['Bird_2_SpeciesOnPiece'])>0:
            subject=SubElement(record,'mods:subject')
            topSubject=SubElement(subject,'mods:topic') 
            topSubject.text=row['Bird_2_GenusOnPiece']+' '+row['Bird_2_SpeciesOnPiece']
        
        # origin info wants at least some data, so if there is a date we threw that in
        originInfo=SubElement(record,'mods:originInfo')
        if len(row['Bird_1_DateCreated'])==9:
                DateStart=SubElement(originInfo,'mods:dateCreated')
                DateStart.set('encoding','w3cdtf')
                DateStart.set('point','start')
                DateStart.text=row['Bird_1_DateCreated'][0:4]
                DateEnd=SubElement(originInfo,'mods:dateCreated')
                DateEnd.set('encoding','w3cdtf')
                DateEnd.set('point','end')
                DateEnd.text=row['Bird_1_DateCreated'][5:9]
                
        elif len(row['Bird_1_DateCreated'])>0:
                dateCreated=SubElement(originInfo,'mods:dateCreated')
                dateCreated.set('encoding','w3cdtf')
                dateCreated.text=row['Bird_1_DateCreated']
        # since there were many without a date, we used Great Britain as the place it was created to satisfy the requirements
        Place=SubElement(originInfo,'mods:place')
        PlaceTerm=SubElement(Place,'mods:placeTerm')
        PlaceTerm.set('authority','iso3166')
        PlaceTerm.set('type','code')
        PlaceTerm.text='GB'
        placetext=SubElement(Place,'mods:placeTerm')
        placetext.set('type','text')
        placetext.text='Great Britain'
            
            
            
        # these are valuable and were put in as generic notes, concatenated if there were two.
        if len(row['ContentNote'])>0:
            if len(row['PublicationNote'])>0:

                note=SubElement(record,'mods:note')
                note.text=row['PublicationNote']+'. '+row['ContentNote']
        else:
            note=SubElement(record,'mods:note')
            note.text=row['ContentNote']

        # named artists for the images
        if len(row['NamedArtists'])>0:
            namerow=row['NamedArtists'].split(';')
            for initial in namerow:
                name=SubElement(record,'mods:name')
                name.set('type','personal')
                namePart=SubElement(name,'mods:namePart')
                role=SubElement(name,'mods:role')
                roleTermcode=SubElement(role,'mods:roleTerm')
                roleTermcode.set('type','code')
                roleTermcode.text='art'
                roleTermtext=SubElement(role,'mods:roleTerm')
                roleTermtext.set('type','text')
                roleTermtext.text='artist'

                if initial in artists:
                    namePart.text=artists.get(initial)


        
        # medium and form get rather complicated for these as it is quite varied. used the 'medium' column for form, and 'size' for extent
        # this could be reviewed by someone with an art history background for accuracy
        
        physDesc=SubElement(record,'mods:physicalDescription')
        if len(row['Bird_1_Medium'])>0:
            form=SubElement(physDesc,'mods:form')
            form.set('type','material')
            form.text=row['Bird_1_Medium']
        if len(row['Size'])>0:
            extent=SubElement(physDesc,'mods:extent')
            extent.text=row['Size']


        digOr=SubElement(physDesc,'mods:digitalOrigin')
        digOr.text='reformatted digital'
        interMed=SubElement(physDesc,'mods:internetMediaType')
        interMed.text='image/tiff'
        
        
        accessCond=SubElement(record,'mods:accessCondition')
        accessCond.set('type','use and reproduction')
        accessCond.text='This work is in the public domain and is available for users to copy, use, and redistribute in part or in whole. No known restrictions apply to the work.'


        # if there is a final published image the draft refers to, it was listed as a related item with a format of [Book title],[plate]
        bookRow=row['Book']
        SecondBook=row['SecondBook']

        if SecondBook in books:
            relatedItem1=SubElement(record,'mods:relatedItem')
            relatedItem1.set('type','succeeding')
        
        
            relTitleInfo1=SubElement(relatedItem1,'mods:titleInfo')
            relTitle1=SubElement(relTitleInfo1,'mods:title')
            relTitle1.text=books.get(SecondBook)[0]+', '+'vol. '+row['Part']
            if len(row['PlateNumber'])>0:
                
                partName1=SubElement(relTitleInfo1,'mods:partName')
                partName1.text='plate'
                partNo1=SubElement(relTitleInfo1,'mods:partNumber')
                partNo1.text=row['PlateNumber']
            

            relGenre1=SubElement(relatedItem1,'mods:genre')
            relGenre1.text='Illustrated ornithological book'
            relOrInfo1=SubElement(relatedItem1,'mods:originInfo')
            relOrInfo1.set('eventType','publication')
                
               
                
                
            relIdentifier1=SubElement(relatedItem1,'mods:identifier')
            relIdentifier1.set('type','oclc')
            relIdentifier1.text=books.get(SecondBook)[5]
            
            relPub1=SubElement(relOrInfo1,'mods:publisher')
            relPub1.text=books.get(bookRow)[3]
            relPlace1=SubElement(relOrInfo1,'mods:place')
            relPlaceTerm1=SubElement(relPlace1,'mods:placeTerm')
            relPlaceTerm1.text=books.get(SecondBook)[2]
        
            relLoc1=SubElement(relatedItem1,'mods:location')
            relphysText1=SubElement(relLoc1,"mods:physicalLocation")
            relphysText1.set('type','text')
            relphysText1.text='University of Kansas. Kenneth Spencer Research Library'
            relphysCode1=SubElement(relLoc1,'mods:physicalLocation')
            relphysCode1.set('authority','marcorg')
            relphysCode1.text='KFS'

            # second related image
            relatedItem2=SubElement(record,'mods:relatedItem')
            relatedItem2.set('type','succeeding')
        
        
            relTitleInfo2=SubElement(relatedItem2,'mods:titleInfo')
            relTitle2=SubElement(relTitleInfo2,'mods:title')
            relTitle2.text=books.get(bookRow)[0]+','+'vol. '+row['Part']
            partName2=SubElement(relTitleInfo2,'mods:partName')
            partName2.text='plate'
            partNo2=SubElement(relTitleInfo2,'mods:partNumber')
            partNo2.text=row['PlateNumber']
            relGenre2=SubElement(relatedItem2,'mods:genre')
            relGenre2.text='Illustrated ornithological book'
            


            relOrInfo2=SubElement(relatedItem2,'mods:originInfo')
            relOrInfo2.set('eventType','publication')
                
               
                
                
            relIdentifier2=SubElement(relatedItem2,'mods:identifier')
            relIdentifier2.set('type','oclc')
            relIdentifier2.text=books.get(bookRow)[5]
            
            relPub2=SubElement(relOrInfo2,'mods:publisher')
            relPub2.text=books.get(bookRow)[3]
            relPlace2=SubElement(relOrInfo2,'mods:place')
            relPlaceTerm2=SubElement(relPlace2,'mods:placeTerm')
            relPlaceTerm2.text=books.get(bookRow)[2]
        
            relLoc2=SubElement(relatedItem2,'mods:location')
            relphysText2=SubElement(relLoc2,"mods:physicalLocation")
            relphysText2.set('type','text')
            relphysText2.text='University of Kansas. Kenneth Spencer Research Library'
            relphysCode2=SubElement(relLoc2,'mods:physicalLocation')
            relphysCode2.set('authority','marcorg')
            relphysCode2.text='KFS'
        elif len(row['Book'])>0 and len(row['SecondBook'])==0:
            relatedItem1=SubElement(record,'mods:relatedItem')
            relatedItem1.set('type','succeeding')
        
        
            relTitleInfo1=SubElement(relatedItem1,'mods:titleInfo')
            relTitle1=SubElement(relTitleInfo1,'mods:title')
            relTitle1.text=books.get(bookRow)[0]+','+'vol. '+row['Part']
            partName1=SubElement(relTitleInfo1,'mods:partName')
            partName1.text='plate'
            partNo1=SubElement(relTitleInfo1,'mods:partNumber')
            partNo1.text=row['PlateNumber']
            relGenre1=SubElement(relatedItem1,'mods:genre')
            relGenre1.text='Illustrated ornithological book'
            


            relOrInfo1=SubElement(relatedItem1,'mods:originInfo')
            relOrInfo1.set('eventType','publication')
                
               
                
                
            relIdentifier1=SubElement(relatedItem1,'mods:identifier')
            relIdentifier1.set('type','oclc')
            relIdentifier1.text=books.get(bookRow)[5]
            
            relPub1=SubElement(relOrInfo1,'mods:publisher')
            relPub1.text=books.get(bookRow)[3]
            relPlace1=SubElement(relOrInfo1,'mods:place')
            relPlaceTerm1=SubElement(relPlace1,'mods:placeTerm')
            relPlaceTerm1.text=books.get(bookRow)[2]
        
            relLoc1=SubElement(relatedItem1,'mods:location')
            relphysText1=SubElement(relLoc1,"mods:physicalLocation")
            relphysText1.set('type','text')
            relphysText1.text='University of Kansas. Kenneth Spencer Research Library'
            relphysCode1=SubElement(relLoc1,'mods:physicalLocation')
            relphysCode1.set('authority','marcorg')
            relphysCode1.text='KFS'
        else:
            continue


        recordInfo=SubElement(record,'mods:recordInfo')
        recordConSo=SubElement(recordInfo,'mods:recordContentSource')
        recordConSo.set('authority','naf')
        recordConSo.set('authorityURI','http://id.loc.gov/authorities/names')
        recordConSo.set('valueURI','http://id.loc.gov/authorities/names/n82079265.html')
        recordConSo.text='University of Kansas'
        recordID=SubElement(recordInfo,'mods:recordIdentifier')
        recordID.text=row['BaseFilename']
        recordOrigin=SubElement(recordInfo,'mods:recordOrigin')
        recordOrigin.text='Records prepared through a combination of local MARC records and a local database for biological subjects.'
        recordCreDate=SubElement(recordInfo,'mods:recordCreationDate')
        recordCreDate.set('encoding','w3cdtf')
        recordCreDate.text=st


        # print tostring(root)



       
tree.write('newManuscripts.xml',xml_declaration=True, encoding="UTF-8")
