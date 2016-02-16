# -- coding: utf-8 --
import csv, sys, time, datetime, xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

#2015-10-07. Converts gould_books.csv to MODS. Records are for plates only but book records can be derived or use existing MARC records.
# dict[key][0] etc
# add second date for bird ksrl_sc_gould_ng_1_2_002.tif - 1880:01:01
xmlFile = 'newBatch.xml'
xmlData = open(xmlFile, 'w')
# dataFile=sys.argv[1]

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
'C. Hullmandel':'C. Hullmandel, Imp.',
'WALTER':'T. Walter, Imp.',
'W':'T. Walter, Imp.',
'CH, W':'Hullmandel & Walton, Imp.',
'CH, WALTON':'Hullmandel & Walton, Imp.',
'WALTER, COHN':'Walter & Cohn, Imp.',
'TW':'T. Walter, Imp.',
'Hullmandel & Walton':'Hullmandel & Walton, Imp.'}

#title,date,place,publisher, callno, oclcno
# taylor and francis and gould as publisher? printer vs publisher in plate vs book(birds of asia/europe/australia?)
books={'HM':['Century of birds from the Himalaya Mountains','1831','England--London','Gould, John, 1804-1881','Ellis Aves H121','ocm09637074'],
'OD':['Monograph of the Odontophorinae, or partridges of America','1850','England--London','Gould, John, 1804-1881','Ellis Aves H128','ocm04582685'],
'RA':['Monograph of the Ramphastidae, or family of toucans','1834','England--London','Gould, John, 1804-1881;Taylor and Francis','Ellis Aves H17','ocm05898907'],
'TR':['Monograph of the Trogonidae, or family of trogons','1835-1838','England--London','Gould, John, 1804-1881','Ellis Aves H135','ocm15167573'],
'AS':['Birds of Asia','1850-1883','England--London','Gould, John, 1804-1881;Taylor and Francis','Ellis Aves H120','ocm07297872'],
'AU':['Birds of Australia','1848','England--London','Gould, John, 1804-1881;R. and J.E. Taylor','Ellis Aves H141','ocm07752160'],
'EU':['Birds of Europe','1837','England--London','Gould, John, 1804-1881;R. and J.E. Taylor','Ellis Aves H132','ocm04485568'],
'GB':['Birds of Great Britain','1873','England--London','Gould, John, 1804-1881;Taylor and Francis','Ellis Aves H131','ocm04275233'],
'HB':['Monograph of the Trochilidae, or family of hummingbirds','1861-1887','England--London','Gould, John, 1804-1881','Ellis Aves H91','ocm07484123'],
'KR':['Monograph of the Macropodidae, or family of kangaroos','1841-1872','England--London','Gould, John, 1804-1881','Ellis Omnia H80','ocm07528705'],
'MM':['Introduction to the mammals of Australia','1863','England--London','Gould, John, 1804-1881;Taylor and Francis','Ellis Omnia C547','ocm10249957'],
'NG':['The birds of New Guinea and the adjacent Papuan islands, including many new species recently discovered in Australia','1875-1888','England--London','Gould, John, 1804-1881;H. Sotheran & Co.','Ellis Aves H129','ocm07748327'],
'PI':['Monograph of the Pittidae','1880-1881','England--London','Gould, John, 1804-1881','Ellis Aves H142','ocm09638814'],
'AA':['Birds of Australia, and the adjacent islands','1837-1838','England--London','Gould, John, 1804-1881','Ellis Aves H125','ocm31830935'],
'IA':['Icones Avium, or, figures and descriptions of new and interesting species of birds from various part of the globe','1837-1838','England--London','Gould, John, 1804-1881','Ellis Aves H106','ocm38881658']}


with open('gould_books.csv', 'rU',errors='ignore') as csvfile:
    reader = csv.DictReader(csvfile)
    

    for row in reader:

        record = SubElement(root, 'mods:mods')
        record.set('xsi:schemaLocation', 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd')
        # inserts filename as local identifier
        identifier = SubElement(record, 'mods:identifier')
        identifier.set('type', 'local')
        identifier.text = row['FullFileName']

        
        titleInfo = SubElement(record, 'mods:titleInfo')
        title=SubElement(titleInfo,'mods:title')
        partName=SubElement(titleInfo,'mods:partName')
        partName.text='plate'
        partNo=SubElement(titleInfo,'mods:partNumber')
        partNo.text=row['PlateNumber']
        typeImage=SubElement(record,'mods:typeOfResource')
        typeImage.text='still image'

        # first try and take Title from an actual title on the piece
        if len(row['TitleOnPiece'])>0:

            title.text = row['TitleOnPiece']
        # if no title, see if there is a Common Name
        elif len(row['Bird_1_CommonNameOnPiece'])>0:
            title.text = row['Bird_1_CommonNameOnPiece']
        # if still no luck, concatenate the genus and species into a title
        elif len(row['Bird_1_GenusOnPiece'])>0:
            title.text= row['Bird_1_GenusOnPiece'] +' '+ row['Bird_1_SpeciesOnPiece']
        # otherwise call it untitled so it can be flagged and looked at later
        else:
            title.text='Untitled'



        # for each bird in the picture, grab the Genus and Species and turn them into individual subjects
        if len(row['Bird_1_GenusModern'])>0 and len(row['Bird_1_SpeciesModern'])>0:
            subject=SubElement(record,'mods:subject')
            topSubject=SubElement(subject,'mods:topic') 
            topSubject.text=row['Bird_1_GenusModern']+' '+row['Bird_1_SpeciesModern']
        if len(row['Bird_2_GenusModern'])>0 and len(row['Bird_2_SpeciesModern'])>0:
            subject=SubElement(record,'mods:subject')
            topSubject=SubElement(subject,'mods:topic') 
            topSubject.text=row['Bird_2_GenusModern']+' '+row['Bird_2_SpeciesModern']
        if len(row['Bird_3_GenusModern'])>0 and len(row['Bird_3_SpeciesModern'])>0:
            subject=SubElement(record,'mods:subject')
            topSubject=SubElement(subject,'mods:topic') 
            topSubject.text=row['Bird_3_GenusModern']+' '+row['Bird_3_SpeciesModern']

        
        if len(row['Bird_1_DateCreated'])>0 or len(row['Printer'])>0:
            # originInfo requires at least one value. since these are only for plates it made more sense to see what origin information 
            # about the plates could be derived
            originInfo=SubElement(record,'mods:originInfo')
            # some plates have a date attached
            if len(row['Bird_1_DateCreated'])>0:
                dateCreated=SubElement(originInfo,'mods:dateCreated')
                dateCreated.set('encoding','w3cdtf')
                dateCreated.text=row['Bird_1_DateCreated']
            # others have a printer for the plate listed. Gets a little tricky when considering the publisher of the volume as one would think these are the same entities.
            # only used it if we had a printer listed in the spreadsheet.
            if len(row['Printer'])>0:
                printrow=row['Printer']
                pub=SubElement(originInfo,'mods:publisher')
                for x in printrow:
                    if x in printers:
                        pub.text=printers.get(x)
            
            
        # misc notes about the plate
        if len(row['ContentNote'])>0:
            note=SubElement(record,'mods:note')
            note.text=row['ContentNote']

        # adding named artists for each plate
        if len(row['NamedArtists'])>0:
            namerow=row['NamedArtists'].split(',')
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


        
        
        # info about the nature of the resource. not from the spreadsheet
        physDesc=SubElement(record,'mods:physicalDescription')
        digOr=SubElement(physDesc,'mods:digitalOrigin')
        digOr.text='reformatted digital'
        form=SubElement(physDesc,'mods:form')
        form.set('type','material')
        form.set('authorityURI','http://vocab.getty.edu/aat')
        form.set('valueURI','http://vocab.getty.edu/aat/300041379')
        form.text='lithograph'
        interMed=SubElement(physDesc,'mods:internetMediaType')
        interMed.text='image/tiff'
        genre=SubElement(record,'mods:genre')
        
        genre.text='Ornithological illustration'
        accessCond=SubElement(record,'mods:accessCondition')
        accessCond.set('type','use and reproduction')
        accessCond.text='This work is in the public domain and is available for users to copy, use, and redistribute in part or in whole. No known restrictions apply to the work.'

        # related item was used for the host parent of the plate, e.g. the monographic volume
        relatedItem=SubElement(record,'mods:relatedItem')
        relatedItem.set('type','host')
        
        
        
        relOrInfo=SubElement(relatedItem,'mods:originInfo')
        relOrInfo.set('eventType','publication')
        bookRow=row['Book']
        
        if bookRow in books:
            relTitleInfo=SubElement(relatedItem,'mods:titleInfo')
            relTitle=SubElement(relTitleInfo,'mods:title')
            relTitle.text=books.get(bookRow)[0]
            relPart=SubElement(relatedItem,'mods:part')
            relDet=SubElement(relPart,'mods:detail')
            relDet.set('type','volume')
            relNum=SubElement(relDet,'mods:number')
            relNum.text=row['Part']
            if relNum.text=='S':
                relNum.text='Supplement'
            relLoc=SubElement(relatedItem,'mods:location')
            
            relIdentifier=SubElement(relatedItem,'mods:identifier')
            relIdentifier.set('type','oclc')
            relIdentifier.text=books.get(bookRow)[5]
            relLang=SubElement(relatedItem,'mods:language')
            relLangCode=SubElement(relLang,'mods:languageTerm')
            relLangCode.set('type','code')
            relLangCode.set('authority','639-2')
            relLangCode.text='eng'
            relLangText=SubElement(relLang,'mods:languageTerm')
            relLangText.set('type','text')
            relLangText.text='English'
            relGenre=SubElement(relatedItem,'mods:genre')
            relGenre.text='Illustrated ornithological books'
            
            
            pubs=books.get(bookRow)[3].split(';')
            for x in pubs:
                relPub=SubElement(relOrInfo,'mods:publisher')

                relPub.text=x



            # this wasn't in the spreadsheet, but I used London for the place of publication
            relPlace=SubElement(relOrInfo,'mods:place')
            relPlaceTerm=SubElement(relPlace,'mods:placeTerm')
            relPlaceTerm.text=books.get(bookRow)[2]
            
            relphysText=SubElement(relLoc,"mods:physicalLocation")
            relphysText.set('type','text')
            relphysText.text='University of Kansas. Kenneth Spencer Research Library'
            relphysCode=SubElement(relLoc,'mods:physicalLocation')
            relphysCode.set('authority','marcorg')
            relphysCode.text='KFS'
            relShelf=SubElement(relLoc,'mods:shelfLocator')
            relShelf.text=books.get(bookRow)[4]

            relEd=SubElement(relOrInfo,'mods:edition')
            if '-' in books.get(bookRow)[1]:

                relDateStart=SubElement(relOrInfo,'mods:dateIssued')
                relDateStart.set('point','start')
                relDateEnd=SubElement(relOrInfo,'mods:dateIssued')
                relDateEnd.set('point','end')
                
                relDateStart.text=books.get(bookRow)[1][0:4]
                relDateEnd.text=books.get(bookRow)[1][5:10]
            else:
                relDate=SubElement(relOrInfo,'mods:dateIssued') 
                relDate.text=books.get(bookRow)[1]

        
        if row['Edition']=='1S':
            relEd.text='1st'
        else:
            relEd.text=row['Edition']


        # For supplements with same titles as host book or with second editions
        
        if relTitle.text=='Monograph of the Trogonidae, or family of trogons' and relEd.text=='2nd ed.':
            relDate.text='1875'
        if relTitle.text=='Monograph of the Ramphastidae, or family of toucans' and row['Part']=='S':
            relDate.text='1855'
            relTitle.text='Supplement to the first edition of A monograph of the Ramphastidae, : or family of toucans'
            relIdentifier.text='ocm05916002'
            relShelf.text='Ellis Aves H17 item 2'
        if relTitle.text=='Monograph of the Ramphastidae, or family of toucans' and relEd.text=='2nd ed.':
            relDate.text='1854'
            relPub.text='Taylor and Francis'
            relIdentifier.text='ocm11587418'
            relShelf='Ellis Aves H126'
        if relTitle.text=='Monograph of the Trochilidae, or family of hummingbirds' and row['Edition']=='1S':
            relSubTit=SubElement(relTitleInfo,'mods:subTitle')
            relDate.text='1887'
            relSubTit.text='Completed after the author\'s death by R. Bowdler Sharpe'
            relPub.text='H. Sotheran &amp;   Co.'
        if relTitle.text=='Birds of Australia' and row['Edition']=='1S':
            relTitle.text='The birds of Australia, supplement'
            relIdentifier.text='ocm07568143'
            relShelf.text='Ellis Aves H130'


        
        

        

        recordInfo=SubElement(record,'mods:recordInfo')
        recordConSo=SubElement(recordInfo,'mods:recordContentSource')
        recordConSo.set('authority','naf')
        recordConSo.set('authorityURI','http://id.loc.gov/authorities/names')
        recordConSo.set('valueURI','http://id.loc.gov/authorities/names/n82079265.html')
        recordConSo.text='University of Kansas'
        recordID=SubElement(recordInfo,'mods:recordIdentifier')
        recordID.text=row['BaseFileName']
        recordOrigin=SubElement(recordInfo,'mods:recordOrigin')
        recordOrigin.text='Records prepared through a combination of local MARC records and a local database for biological subjects.'
        recordCreDate=SubElement(recordInfo,'mods:recordCreationDate')
        recordCreDate.set('encoding','w3cdtf')
        recordCreDate.text=st


        # print tostring(root)



       
tree.write('newBooks.xml',xml_declaration=True, encoding="UTF-8")
