import types
from loguru import logger
from dataclasses import field, dataclass
from typing import Any, List
from intervaltree import IntervalTree, Interval
import pandas as pd


@dataclass
class BASE:
    chr:str
    start:int
    end:int
    strand:str
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError(f"{name}' cannot be modified.")
        super().__setattr__(name, value)


@dataclass
class EXON(BASE):
    id:str


class TRANSCRIPT:
    """
    """
    def __init__(self, trans_id:str, trans_name:str, chr:str, start:int, end:int, strand:str):
        self.id = trans_id
        self.name = trans_name
        self.chr = chr
        self.start = start
        self.end = end
        self.strand = strand
        self.CDS = [] # List[BASE]
        self.start_codon = [] # List[BASE]
        self.stop_codon = [] # List[BASE]
        self.UTR5 = [] # List[BASE]
        self.UTR3 = [] # List[BASE]
        self.exons = {}
        self.other = [] # List[BASE]


    def add_exon(self, exon:EXON):
        if exon.id == "NONE":
            exon.id = f"exon_{len(self.exons) + 1}"
        self.exons[exon.id] = exon
    

    def add_start_codon(self, start_codon:BASE):
        self.start_codon.append(start_codon)
    
    def add_stop_codon(self, stop_codon:BASE):
        self.stop_codon.append(stop_codon)
    
    def add_UTR5(self, UTR5):
        self.UTR5.append(UTR5)
    
    def add_UTR3(self, UTR3):
        self.UTR3.append(UTR3)
    
    def add_CDS(self, CDS:BASE):
        self.CDS.append(CDS)
    
    def add_other(self, other:BASE):
        self.other.append(other)



class GENE:
    """
    """

    def __init__(self, gene_id:str, gene_name:str, chr:str, start:int, end:int, strand:str):
        self.id = gene_id
        self.name = gene_name
        self.chr = chr
        self.start = start
        self.end = end
        self.strand = strand
        self.trans = {}
        self.trans_map = {}
    

    def add_trans(self, trans:TRANSCRIPT):
        self.trans[trans.id] = trans
        self.trans_map[trans.name] = trans.id

def Bases_dict(bases:str) -> dict:
    bases_dict = {}
    for base in bases.split(";"):
        base_list = base.split('"')
        if len(base_list) > 1:
            name = base_list[0].strip()
            content = base_list[1].strip()
            bases_dict[name] = content
    return bases_dict

def Gtf_block(gtf_file:str) -> types.GeneratorType:

    with open(gtf_file, "r") as f:

        blocks = []
        for line in f:
            if line.startswith("#"):
                continue
            
            line_list = line.strip().split("\t")
            if len(line_list) < 8:
                continue

            anno_type = line_list[2]
            if anno_type == "gene":
                if len(blocks) == 0:
                    pass
                else:
                    yield blocks
                    blocks = []
            blocks.append(line.strip())
        
        if blocks:
            yield blocks


#anno_map = anno_name1,gtf_str2;anno_name2,gtf_str2;...
class GTF:
    """
    """
    def __init__(self, name=None, version=None, URL=None, anno_map=None):
        self.name = name
        self.version = version
        self.URL = URL
        self.genes = {}
        self.genes_map = {}
        self.genes_interval = {}
        self.err = []
        self.anno_map = {"gene":"gene", "trans":"transcript", "exon":"exon",
                         "CDS":"CDS", "start_codon":"start_codon",
                         "stop_codon":"stop_codon", "UTR5":"five_prime_utr",
                         "UTR3":"three_prime_utr", "other":"other"}
        if anno_map:
            for bases in anno_map.split(";"):
                name = bases.split(",")[0]
                gtf_str = bases.split(",")[1]
                if name in self.anno_map:
                    self.anno_map[name] = gtf_str
                else:
                    logger.warning(f"annotation map err: {name}; maby use key words 'other'")


    

    def add_gene(self, gene:GENE):
        self.genes[gene.id] = gene
        self.genes_map[gene.name] = gene.id
    
    def add_err(self, err:str):
        self.err.append(err)
    
    def read(self, gtf, name=None, version=None, URL=None, anno_map=None):

        self.name = name
        self.version = version
        self.URL = URL

        if anno_map:
            for bases in anno_map.split(";"):
                Tname = bases.split(",")[0]
                gtf_str = bases.split(",")[1]
                if Tname in self.anno_map:
                    self.anno_map[Tname] = gtf_str
                else:
                    logger.warning(f"annotation map err: {Tname}; maby use key words 'other'")

        blocks = Gtf_block(gtf)

        for block in blocks:
            for line in block:
                chrn, tmp1, anno_type, start, end, tmp2, strand, tmp3, bases = line.split("\t")
                start = int(start)
                end = int(end)
                bases_dict = Bases_dict(bases)

                if anno_type == self.anno_map["gene"]:
                    # gene name
                    if "gene_name" in bases_dict:
                        gene_name = bases_dict["gene_name"]
                    else:
                        gene_name = bases_dict["gene_id"]
                    
                    gene = GENE(bases_dict["gene_id"], gene_name, chrn, start, end, strand)
                
                elif anno_type == self.anno_map["trans"]:
                    # transcript name
                    if "transcript_name" in bases_dict:
                        trans_name = bases_dict["transcript_name"]
                    else:
                        trans_name = bases_dict["transcript_id"]
                    trans = TRANSCRIPT(bases_dict["transcript_id"], trans_name, 
                                       chrn, start, end, strand)
                    gene.add_trans(trans)
                
                elif anno_type == self.anno_map["exon"]:
                    # exon_id
                    if bases_dict["exon_id"]:
                        exon = EXON(chrn, start, end, strand, bases_dict["exon_id"])
                    else:
                        exon = EXON(chrn, start, end, strand, "NONE")
                    
                    trans_id = bases_dict["transcript_id"]
                    gene.trans[trans_id].add_exon(exon)
                
                elif anno_type == self.anno_map["CDS"]:
                    cds = BASE(chrn, start, end, strand)
                    trans_id = bases_dict["transcript_id"]
                    gene.trans[trans_id].add_CDS(cds)
                
                elif anno_type == self.anno_map["start_codon"]:
                    start_codon = BASE(chrn, start, end, strand)
                    trans_id = bases_dict["transcript_id"]
                    gene.trans[trans_id].add_start_codon(start_codon)
                
                elif anno_type == self.anno_map["stop_codon"]:
                    stop_codon = BASE(chrn, start, end, strand)
                    trans_id = bases_dict["transcript_id"]
                    gene.trans[trans_id].add_stop_codon(stop_codon)
                
                elif anno_type == self.anno_map["UTR5"]:
                    utr5 = BASE(chrn, start, end, strand)
                    trans_id = bases_dict["transcript_id"]
                    gene.trans[trans_id].add_UTR5(utr5)
                
                elif anno_type == self.anno_map["UTR3"]:
                    utr3 = BASE(chrn, start, end, strand)
                    trans_id = bases_dict["transcript_id"]
                    gene.trans[trans_id].add_UTR3(utr3)

                elif anno_type == self.anno_map["other"]:
                    other = BASE(chrn, start, end, strand)
                    trans_id = bases_dict["transcript_id"]
                    gene.trans[trans_id].add_other(other)
                
                else:
                    logger.warning(f"annotation type warning: {anno_type}")
                    self.add_err(line)
            
            self.add_gene(gene)
            # interval
            if gene.chr in self.genes_interval:
                chr_interval = self.genes_interval[gene.chr]
            else:
                chr_interval = IntervalTree()
            chr_interval.addi(gene.start, gene.end, data=gene.id)
            self.genes_interval[gene.chr] = chr_interval

        return
    
    # loc = chr:start:end
    def searchs(self, loc):
        chrn, start, end = loc.split(":")
        start = int(start)
        end = int(end)
        if chrn in self.genes_interval:
            return sorted(self.genes_interval[chrn][start:end])
        elif chrn.split("chr")[1] in self.genes_interval:
            return sorted(self.genes_interval[chrn.split("chr")[1]][start:end])
        elif f"chr{chrn}" in self.genes_interval:
            return sorted(self.genes_interval[f"chr{chrn}"][start:end])
        else:
            logger.warning(f"not found chr {chrn} in gtf")


    # genes = {genename1},{genename2},...,{genenameN}
    def maps(self, genes, mapType="n2i"):
        dict_map = {}
        if mapType == "n2i":
            for name in genes.split(","):
                if name in self.genes_map:
                    dict_map[name] = self.genes_map[name]
                else:
                    logger.warning(f"not found genename {name} in gtf")
                    dict_map[name] = "None"

        elif mapType == "i2n":
            for id in genes.split(","):
                if id in self.genes:
                    dict_map[id] = self.genes[id].name
                else:
                    logger.warning(f"not found geneid {id} in gtf")
                    dict_map[id] = "None"
        else:
            logger.error("params err: please check mapType")
            raise ValueError("params err: please check mapType")
        return dict_map
    

    # genes = {geneid1},{geneid2},...,{geneidN}
    def inquires(self, genes, itype="id", ilevel="gene"):
        
        if genes == "all":
            geneid_list = list(self.genes.keys())
            logger.waring("all genes in gtf will be used with default!!!")
        else:
            if itype == "id":
                geneid_list = genes.split(",")
            elif itype == "name":
                geneid_list = [self.genes_map[name] for name in genes.split(",")]
            else:
                logger.error("params err: please check itype")
                raise ValueError("params err: please check mtype")
        
        list_geneid = []
        list_genename = []
        list_chr = []
        list_start = []
        list_end = []
        list_strand = []
        if ilevel == "gene":
            for geneid in geneid_list:
                if geneid in self.genes:
                    gene = self.genes[geneid]
                    list_geneid.append(gene.id)
                    list_genename.append(gene.name)
                    list_chr.append(gene.chr)
                    list_start.append(gene.start)
                    list_end.append(gene.end)
                    list_strand.append(gene.strand)
                else:
                    logger.warning(f"not found geneid {geneid} in gtf")
                    list_geneid.append(geneid)
                    list_genename.append("-")
                    list_chr.append("-")
                    list_start.append(0)
                    list_end.append(0)
                    list_strand.append("-")
            df = pd.DataFrame({"geneid":list_geneid, "genename":list_genename,
                               "chr":list_chr, "start":list_start,
                               "end":list_end, "strand":list_strand})
        elif ilevel == "trans":
            list_transid = []
            list_transname = []
            list_transstart = []
            list_transend = []
            for geneid in geneid_list:
                if geneid in self.genes:
                    gene = self.genes[geneid]
                    if len(gene.trans) >0:
                        for transid, trans in gene.trans.items():
                            list_geneid.append(gene.id)
                            list_genename.append(gene.name)
                            list_chr.append(gene.chr)
                            list_start.append(gene.start)
                            list_end.append(gene.end)
                            list_strand.append(gene.strand)
                            list_transid.append(trans.id)
                            list_transname.append(trans.name)
                            list_transstart.append(trans.start)
                            list_transend.append(trans.end)
                    else:
                        logger.warning(f"not found transcripts of {geneid} in gtf")
                        list_geneid.append(gene.id)
                        list_genename.append(gene.name)
                        list_chr.append(gene.chr)
                        list_start.append(gene.start)
                        list_end.append(gene.end)
                        list_strand.append(gene.strand)
                        list_transid.append("-")
                        list_transname.append("-")
                        list_transstart.append(0)
                        list_transend.append(0)
                else:
                    logger.warning(f"not found geneid {geneid} in gtf")
                    list_geneid.append(geneid)
                    list_genename.append("-")
                    list_chr.append("-")
                    list_start.append(0)
                    list_end.append(0)
                    list_strand.append("-")
                    list_transid.append("-")
                    list_transname.append("-")
                    list_transstart.append(0)
                    list_transend.append(0)
            df = pd.DataFrame({"geneid":list_geneid, "genename":list_genename,
                               "chr":list_chr, "start":list_start,
                               "end":list_end, "strand":list_strand,
                               "transid":list_transid, "transname":list_transname,
                               "transstart":list_transstart, "transend":list_transend})
        elif ilevel == "exon":
            list_transid = []
            list_transname = []
            list_transstart = []
            list_transend = []
            list_exonid = []
            list_exonstart = []
            list_exonend = []
            for geneid in geneid_list:
                if geneid in self.genes:
                    gene = self.genes[geneid]
                    if len(gene.trans) >0:
                        for transid, trans in gene.trans.items():
                            if len(trans.exons) >0:
                                for exonid, exon in trans.exons.items():
                                    list_geneid.append(gene.id)
                                    list_genename.append(gene.name)
                                    list_chr.append(gene.chr)
                                    list_start.append(gene.start)
                                    list_end.append(gene.end)
                                    list_strand.append(gene.strand)
                                    list_transid.append(trans.id)
                                    list_transname.append(trans.name)
                                    list_transstart.append(trans.start)
                                    list_transend.append(trans.end)
                                    list_exonid.append(exon.id)
                                    list_exonstart.append(exon.start)
                                    list_exonend.append(exon.end)
                            else:
                                logger.warning(f"not found exon of {transid} of {geneid} in gtf")
                                list_geneid.append(gene.id)
                                list_genename.append(gene.name)
                                list_chr.append(gene.chr)
                                list_start.append(gene.start)
                                list_end.append(gene.end)
                                list_strand.append(gene.strand)
                                list_transid.append(trans.id)
                                list_transname.append(trans.name)
                                list_transstart.append(trans.start)
                                list_transend.append(trans.end)
                                list_exonid.append("-")
                                list_exonstart.append(0)
                                list_exonend.append(0)
                    else:
                        logger.warning(f"not found transcripts of {geneid} in gtf")
                        list_geneid.append(gene.id)
                        list_genename.append(gene.name)
                        list_chr.append(gene.chr)
                        list_start.append(gene.start)
                        list_end.append(gene.end)
                        list_strand.append(gene.strand)
                        list_transid.append("-")
                        list_transname.append("-")
                        list_transstart.append(0)
                        list_transend.append(0)
                        list_exonid.append("-")
                        list_exonstart.append(0)
                        list_exonend.append(0)
                else:
                    logger.warning(f"not found geneid {geneid} in gtf")
                    list_geneid.append(geneid)
                    list_genename.append("-")
                    list_chr.append("-")
                    list_start.append(0)
                    list_end.append(0)
                    list_strand.append("-")
                    list_transid.append("-")
                    list_transname.append("-")
                    list_transstart.append(0)
                    list_transend.append(0)
                    list_exonid.append("-")
                    list_exonstart.append(0)
                    list_exonend.append(0)
                        
            df = pd.DataFrame({"geneid":list_geneid, "genename":list_genename,
                               "chr":list_chr, "start":list_start,
                               "end":list_end, "strand":list_strand,
                               "transid":list_transid, "transname":list_transname,
                               "transstart":list_transstart, "transend":list_transend,
                               "exonid":list_exonid, "exonstart":list_exonstart,
                               "exonend":list_exonend})
        else:
            logger.error("params err: please check ilevel")
            raise ValueError("params err: please check ilevel")
        return df 



