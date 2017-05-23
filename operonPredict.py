#! /usr/bin/env python

import MySQLdb as mariadb
import re
from scipy.stats import gaussian_kde as gkde

def findOperons():

        lines = open('OperonSet.txt','r+').readlines()

        genesData=[]

        for line in lines:

                if re.match(r'.+\s+',line):

                        data = re.match(r'.+\[.+\]\s+(.+)',line)


                        if data is not None:

                                if data.group(1) == 'Strong' or data.group(1) == 'Confirmed':

                                        #print(data.group(1))
                                        fields = line.replace('\n','').split('\t')
                                        operon = fields[0]
                                        genesList = fields[5]

                                        operonData = (operon,genesList);
                                        genesData.append(operonData)

                                        #print('{}\t{}'.format(operon,name))


        return genesData

def findGenes(genesData):


        for operon in genesData:

                operonName = operon[0]
                genesList = operon[1]

                findLocus(operonName,genesList)

                #print('{}\t{}'.format(operonName,genesList))


def findLocus(operon,genesList):

        genes = genesList.split(',')

        locus =''


        for gene in genes:

                line = findLine(gene)

                lineData = line.split('\t')

                if len(lineData) >= 2:

                        locus = lineData[2]

                        if locus.replace(' ','') == '':

                                if gene != "3'ETS<sup><i>leuZ</i></sup>":
                                        locus = findSynonym(gene)

                        #print('{}\t{}\t{}'.format(operon,gene,locus))

                if gene != "3'ETS<sup><i>leuZ</i></sup>":

                        getData(operon,gene,locus)

def findLine(gene):

        search = r'.+({})'.format(gene)

        for line in GeneProduct:

                if line[0][0] != '#':

                        find = re.match(search,line)

                        if find is not None:

                                return line

def findSynonym(gene):

        locus =''

        cur.execute("select locus_tag from genes inner join synonyms where genes.gene_id = synonyms.gene_id and synonym='{}';".format(gene))

        for row in cur.fetchall():

                locus = row[0]
        else:
                locus = queryGenes(gene)

        return locus

def queryGenes(gene):

        cur.execute("select locus_tag from genes where name='{}';".format(gene))

        for row in cur.fetchall():

                return row[0]

def getData(operon,gene,locus):

        global genes

        cur.execute("select strand,left_position,right_position from exons inner join genes where exons.gene_id=genes.gene_id and genes.locus_tag='{}'".format(locus))

        for row in cur.fetchall():
                #pass
                #print('{}\t{}\t{}\t{}\t{}\t{}'.format(operon,gene,locus,row[0],row[1],row[2]))

                geneData = (operon,gene,locus,row[0],row[1],row[2]);

                genes.append(geneData)

def sortGenes():

        global genes

        genes  = sorted(genes,key=lambda x: x[4])

        #for gene in genes:

                #print('\t'.join(str(i) for i in gene))

def calcDistances():

        global genes

        operonName = genes[0][0]

        i = 0

        while i < len(genes):

                operon = []

                try:
                        while genes[i][0] == operonName:

                                operon.append(genes[i])

                                i = i+1

                        findIntragenicDistance(operon)

                        operonName  = genes[i][0]
                except IndexError:
                        pass

def findIntragenicDistance(operon):

        global intragenic

        i = 1

        if(len(operon)>1):


                while i< len(operon):

                        distance = operon[i][4]-operon[i-1][5] + 1


                        intragenic.append(distance)

                        i = i+1


def findDirectomes():

        global genes
        global interOperon

        operon = genes[0][0]

        strand = genes[0][3]

        i = 1

        try:

                while i < len(genes):

                        if genes[i][0] == operon:

                                i = i +1

                        else:

                                if genes[i][3] == strand:

                                        distance = genes[i][5]-genes[i][4]+1

                                        interOperon.append(distance)


                                operon = genes[i][0]

                                strand = genes[i][3]
        except IndexError:

                pass


def generateLikelihoods():

        global h0
        global h1

        h0 = gkde(intragenic)

        h1 = gkde(interOperon)

def getPrior(x):

        global prior
        global h1
        global h0

        prior = (h1(x)*0.6)/((h1(x)*0.6)+(h0(x)*0.4))


if __name__ == "__main__":



        global operons
        global cur
        global GeneProduct
        global genes

        global intragenic
        global interOperon

        global h1
        global h0
        global prior

        genes =[]

        intragenic = []

        interOperon = []

        #Open the SQL connect
        db = mariadb.connect(host="bm185s-mysql.ucsd.edu",
                             user="bm185sac",
                             passwd="p@Let97",
                             db ="bm185sac_db",
                             port=3306)

        cur = db.cursor()


        #Open GeneProducts file
        GeneProduct = open('GeneProductSet.txt','r+').readlines()

        genesData = findOperons()

        findGenes(genesData)

        sortGenes()

        calcDistances()

        findDirectomes()

        print(interOperon)

        generateLikelihoods()

        getPrior(10)
