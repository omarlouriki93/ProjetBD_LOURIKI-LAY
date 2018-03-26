import operator
import csv
import sys, getopt

# sort the table
# tab : list of tuples, each tuple represent a row
# cols : specify the column number to sort
def sortTab(tab, cols):
    for col in reversed(cols):
        tab = sorted(tab, key=operator.itemgetter(col))
    return tab

# read the CSV file
def csvFileRead(filename):	
    csv_file = open(filename, "rU")
    read_row = csv.reader(csv_file, delimiter=";")

    rownum = 0	
    a = []
    l1 = list()
    next(read_row)
    for row in read_row:
        l = list()
        l.append(row[2])
        l.append(row[0])
        if row[11] == '':
           l.append('0')
        else:
           l.append(row[11])
        if row[14] == '':
           l.append('0')
        else:
           l.append(row[14])
        l.append(row[1])
        l.append(row[19])
        l.append(row[21])
        l1.append(l)
        rownum += 1

    csv_file.close()
    return l1

myGlobalList = []

def saveData(codePostal, number_of_year, consoResidentielRef, consoResidentielTotal, consoProfessionelRef, consoProfessionelTotal, commune, consoIndustrielRef, consoIndustrielTotal, consoTertiaireRef, consoTertiaireTotal):
  l1 = list()
  l1.append(codePostal)
  l1.append(consoResidentielTotal - (consoResidentielRef * number_of_year))
  l1.append(consoProfessionelTotal - (consoProfessionelRef * number_of_year))
  l1.append(consoResidentielTotal)
  l1.append(consoProfessionelTotal)
  l1.append(commune)
  l1.append(consoIndustrielTotal - (consoIndustrielRef * number_of_year))
  l1.append(consoIndustrielTotal)
  l1.append(consoTertiaireTotal - (consoTertiaireRef * number_of_year))
  l1.append(consoTertiaireTotal)
  myGlobalList.append(l1)

def ExecuteProg(inputfile, outputfile):
# Extract columns 'Code Postal', 'Annee', 'Conso Total Residentiel', 'Conso Total Professionel' to list
  myList = csvFileRead(inputfile)

  mySortedList = []
  #Sort list on columns 'Code Postal' and 'Annee'
  for row in sortTab(myList, (0,1)):
     mySortedList.append(row)

  codePostal = 0
  consoResidentielRef = 0
  consoProfessionelRef = 0
  consoIndustrielRef = 0
  consoTertiaireRef = 0
  consoResidentielTotal = 0
  consoProfessionelTotal = 0
  consoIndustrielTotal = 0
  consoTertiaireTotal = 0
  number_of_year = 0;
  commune = ""
  for listElem in mySortedList:
     if codePostal != 0 and codePostal != listElem[0]:
        #Store global results
        saveData(codePostal, number_of_year, consoResidentielRef, consoResidentielTotal, consoProfessionelRef, consoProfessionelTotal, commune, consoIndustrielRef, consoIndustrielTotal, consoTertiaireRef, consoTertiaireTotal)

     if codePostal != listElem[0]:
        codePostal = listElem[0]
        consoResidentielRef = float(listElem[2])
        consoProfessionelRef = float(listElem[3])
        commune = listElem[4]
        consoIndustrielRef = float(listElem[5])
        consoTertiaireRef = float(listElem[6])
        consoResidentielTotal = 0
        consoProfessionelTotal = 0
        consoIndustrielTotal = 0
        consoTertiaireTotal = 0
        number_of_year = number_of_year = 0

     number_of_year = number_of_year + 1
     consoResidentielTotal = consoResidentielTotal + float(listElem[2])
     consoProfessionelTotal = consoProfessionelTotal + float(listElem[3])
     consoIndustrielTotal = consoIndustrielTotal + float(listElem[5])
     consoTertiaireTotal = consoTertiaireTotal + float(listElem[6])

  saveData(codePostal, number_of_year, consoResidentielRef, consoResidentielTotal, consoProfessionelRef, consoProfessionelTotal, commune, consoIndustrielRef, consoIndustrielTotal, consoTertiaireRef, consoTertiaireTotal)

  with open (outputfile, "w")as fp:
     fp.write("Code_Postal;Diff_ConsoResidentiel;Diff_ConsoProfessionel;ConsoResidentielTotal;ConsoProfessionelTotal;Commune;Diff_ConsoIndustriel;ConsoIndustrielTotal;Diff_ConsoTertiaire;ConsoTertiaireTotal\n")
     for listElem in myGlobalList:
         fp.write("%s;%f;%f;%f;%f;%s;%f;%f;%f;%f\n" % (listElem[0], listElem[1], listElem[2], listElem[3], listElem[4], listElem[5], listElem[6], listElem[7], listElem[8], listElem[9]))


  print("End of Program. OutputFile: %s" % outputfile)

inputfile = 'consommation-electrique.csv'
outputfile = 'output.csv'
ExecuteProg(inputfile, outputfile)
