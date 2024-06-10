class Variant:
    def __init__(self, chr, pos, ref, alt):
        self.chr = chr
        self.pos = pos
        self.ref = ref
        self.alt = alt
        self.functional_consequence = None 
        self.hgvsp = None
        self.aa_change = None
        self.transcript_id = None
        self.ucsc_trans_id = None
        self.exon_number = None
        self.start = None
        self.end = None
        self.rmsk = None
        self.clinvar_clnsig = None # clinvar clinical significance
        self.clinvar_clnrevstat = None # clinvar_clinical_review_status
        self.af_esp = None # ESP allele frequency 
        self.af_exac = None # EXAC allele frequency 
        self.af_tgp = None # TGP allele frequency 
        self.dbscsnv_rf_score = None
        self.dbscsnv_ada_score = None
        self.gerp_rs_score = None # conservation score of gerp 
        self.metasvm_score = None 
        self.sift_score = None 
        self.af_vep = None 
        self.va_pathogenicity = None
        self.interpro_domain = "."
        self.gene = None
        self.ensembl_gene_id = None
        self.vep_gene_id = None
        self.max_af = None 
        self.hgnc_id = None 
        self.hgnc_src = None 
        self.PVS1 = 0

        self.PS = [0, 0, 0, 0]
        self.PM = [0, 0, 0, 0]
        self.PP = [0, 0, 0, 0]
        self.BA1 = 0 
        self.BS = [0, 0, 0, 0]
        self.BP = [0, 0, 0, 0]
        
    def to_dict(self):
        variant_dict = {
            'CHROM':self.chr,
            'POS':self.pos,
            'REF':self.ref,
            'ALT':self.alt,
            'INFO': {
                'VA_PATHOGENICITY': self.va_pathogenicity,
            }
        }

        variant_dict["INFO"]["PVS1"] = self.PVS1
        variant_dict["INFO"]["PS"] = self.PS
        variant_dict["INFO"]["PP"] = self.PP
        variant_dict["INFO"]["PM"] = self.PM
        variant_dict["INFO"]["BA1"] = self.BA1
        variant_dict["INFO"]["BS"] = self.BS
        variant_dict["INFO"]["BP"] = self.BP

        return variant_dict
