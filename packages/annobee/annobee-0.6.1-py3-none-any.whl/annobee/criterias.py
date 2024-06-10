# annobee-sdk/criteria.py

import re
import pandas as pd

# local imports
from annobee.variant import Variant
import annobee.utils as utils
import annobee.config as config

class Criteria:
    def __init__(self):
        pass

    def set_PS1(self, variant):
        PS1 = 0
        PS1_t1 = 0
        PS1_t2 = 0
        PS1_t3 = 0
        dbscSNV_cutoff = 0.6  # either score (ada and rf) > 0.6 as splice altering
        ACGTs = ['A', 'C', 'G', 'T']
        
        try:
            if variant.functional_consequence:
                functional_consequence = variant.functional_consequence

                for function in ["missense", "nonsynony"]:
                    if functional_consequence.find(function) >=0 :
                        PS1_t1 = 1

            aa_changes_dict = pd.read_csv(config.hg38_PS1_AA_change_dict_path, sep="\t")
            aa_changes_dict["key"] = aa_changes_dict.iloc[:,0].astype(str) +"-"+ aa_changes_dict.iloc[:,1].astype(str) +"-"+ aa_changes_dict.iloc[:,3].astype(str) +"-"+ aa_changes_dict.iloc[:,4].astype(str)

            try:
                if variant.aa_change:
                    variant_key = str(variant.chr)+"-"+str(variant.pos)+"-"+str(variant.ref)+"-"+str(variant.alt)
                    if any(aa_changes_dict["key"] == variant_key):
                        PS1_t2 = 0
            except:
                for gen in ACGTs:
                    if gen != str(variant.alt):
                        variant.alt = gen
                        variant_key = str(variant.chr)+"-"+str(variant.pos)+"-"+str(variant.ref)+"-"+str(variant.alt)
                    
                    if gen != str(variant.ref):
                        variant.ref = gen
                        variant_key = str(variant.chr)+"-"+str(variant.pos)+"-"+str(variant.ref)+"-"+str(variant.alt)
                        
                    try:
                        if any(aa_changes_dict["key"] == variant_key):
                            PS1_t2 = 0
                    except:
                        pass
                    else:
                        pass
                      
        except Exception as err:
            utils.err_handler(err)
            
        try:
            if not utils.check_value(variant.dbscsnv_rf_score) or not utils.check_value(variant.dbscsnv_ada_score):
                PS1_t3 = 0
            
            if (utils.check_value(variant.dbscsnv_rf_score) and float(variant.dbscsnv_rf_score) > dbscSNV_cutoff) or (utils.check_value(variant.dbscsnv_ada_score) and float(variant.dbscsnv_ada_score) > dbscSNV_cutoff):
                PS1_t3 = 1
            
        except Exception as err:
            utils.err_handler(err)

        if PS1_t1 != 0 and PS1_t2 != 0:
            PS1 = 1
            if PS1_t3 == 1:
                PS1 = 0

        return PS1

    def set_PM5(self, variant):
        PM5 = 0
        PM5_t1 = 0
        PM5_t2 = 0
        PM5_t3 = 0

        if utils.check_value(variant.functional_consequence):
            functional_consequence = variant.functional_consequence
            
            for function in ["missense", "nonsynony"]:
                if functional_consequence.find(function) >= 0:            
                    PM5_t1 = 1
                    aa_changes_dict = pd.read_csv(config.hg38_PS1_AA_change_dict_path, sep="\t", header=None)
                    aa_changes_dict["key"] = aa_changes_dict.iloc[:,0].astype(str) +"-"+ aa_changes_dict.iloc[:,1].astype(str) +"-"+ aa_changes_dict.iloc[:,3] +"-"+ aa_changes_dict.iloc[:,4]

                    if utils.check_value(variant.aa_change):
                        variant_key = str(variant.chr)+"-"+str(variant.pos)+"-"+str(variant.pos)+"-"+variant.alt
                        
                        df_filter = aa_changes_dict[aa_changes_dict["key"] == variant_key]
                        if len(df_filter) >= 0:
                            PM5_t2 = 0 
                        else:
                            PM5_t2=1
                            PM5_t3=0
                            
                            for nucleotide in ["A","C","G","T"]:
                                if nucleotide != variant.alt and nucleotide != variant.ref:
                                    variant_key2 = variant.chr + "-" + variant.pos + "-" + variant.pos + "-" + nucleotide
                                    df_filter = aa_changes_dict[aa_changes_dict["key"] == variant_key2]
                                    if len(df_filter) > 0:
                                        PM5_t3 = 1
                                    
                                    variant_aa_change = variant.aa_change
                                    if df_filter[7][-1] == variant_aa_change[-1]:
                                        PM5_t2 = 0
                                        
        if PM5_t1 != 0 and PM5_t2 != 0 and PM5_t3 != 0:
            PM5 = 1                    
        
        return PM5

    def set_PVS1(self, variant):
        PVS1 = 0
        PVS1_tmp1 = 0
        PVS1_tmp2 = 0
        PVS1_tmp3 = 0 
        dbscSNV_cutoff = 0.6 

        try:
            for func_conseq in ["nonsense","frameshift","splic","stopgain"]:
                if utils.check_value(variant.functional_consequence):
                    if variant.functional_consequence.find(func_conseq) >= 0 and variant.functional_consequence.find("nonframe") < 0:
                        PVS1_tmp1 = 1
                        break
            
            lof_genes_dict = pd.read_csv(config.hg38_PVS1_LOF_genes_dict_path, header=None)
            df_filter = lof_genes_dict[lof_genes_dict[0] == variant.gene]
            if len(df_filter) > 0:
                PVS1_tmp2 = 1

            if utils.check_value(variant.dbscsnv_rf_score) and variant.dbscsnv_rf_score > dbscSNV_cutoff or utils.check_value(variant.dbscsnv_ada_score) and variant.dbscsnv_ada_score > dbscSNV_cutoff:
                PVS1_tmp3 = 1

            if PVS1_tmp1 != 0 and PVS1_tmp2 != 0 and variant.functional_consequence.find("splic") < 0 or PVS1_tmp3 == 1:
                PVS1 = 1 

            if utils.check_value(variant.aa_change):
                knownGene_dict = pd.read_csv(config.hg38_PVS1_knownGeneCanonical_path, sep=" ")

                df_filter = knownGene_dict[knownGene_dict['Transcript(ucsc/known)'] == variant.ucsc_trans_id]

                if len(df_filter) > 0:
                    last_exon_number = df_filter["exons"]

                    if last_exon_number == variant.exon_number:
                        PVS1 = 0

                    if (float(df_filter["end"]) - float(variant.pos)) < 50:
                        PVS1 = 0

        except Exception as err:
            utils.err_handler(err)

        return PVS1

    def set_BP1(self, variant):
        BP1 = 0

        if utils.check_value(variant.functional_consequence):
            for func_conseq in ["missense", "nonsynony"]:
                if variant.functional_consequence.find(func_conseq) >= 0:
                    BP1_genes = pd.read_csv(config.hg38_BP1_genes_dict_path, header=None)
                    df_filter = BP1_genes[BP1_genes[0] == variant.gene]

                    if len(df_filter) > 0: BP1 = 1

        return BP1

    def set_PP2(self, variant):
        PP2 = 0

        if utils.check_value(variant.functional_consequence):
            for func_conseq in ["missense", "nonsynony"]:
                if variant.functional_consequence.find(func_conseq) >= 0:
                    PP2_genes = pd.read_csv(config.hg38_PP2_genes_dict_path, header=None)
                    df_filter = PP2_genes[PP2_genes[0] == variant.gene]

                    if len(df_filter) > 0: PP2 = 1

        return PP2

    def set_PS4(self, variant):
        PS4 = 0
        variant_key = str(variant.chr)+"_"+str(variant.pos)+"_"+str(variant.pos)+"_"+str(variant.ref)+"_"+variant.alt

        PS4_snps_dict = pd.read_csv(config.hg38_PS4_variants_dict_path, sep="\t")
        PS4_snps_dict["CHR"] = PS4_snps_dict["CHR"].apply(lambda s: re.sub("[Cc][Hh][Rr]","",s))
        PS4_snps_dict["key"] = PS4_snps_dict['CHR'].astype(str) +"_"+ PS4_snps_dict['POS_hg38'].astype(str) +"_"+ PS4_snps_dict['REF'] +"_"+ PS4_snps_dict['ALT']

        result_df = PS4_snps_dict[PS4_snps_dict["key"] == variant_key]
        if len(result_df) > 0:
            PS4 = 1

        return PS4

    def set_BS1(self, variant):
        BS1 = 0
        disorder_cutoff = 0.005

        frequency_keys = ["af_esp", "af_exac", "af_tgp"]

        for key in frequency_keys:
            if utils.check_value(getattr(variant, key)) and float(getattr(variant, key)) >= disorder_cutoff: 
                BS1 = 1

        return BS1

    def set_BS2(self, variant):
        BS2 = 0
        try:
            variant_key = variant.chr+"_"+str(variant.pos)+"_"+str(variant.pos)+"_"+variant.ref+"_"+variant.alt

            mim2gene_dict = utils.read_mim2gene()
            omim_filter1 = mim2gene_dict[mim2gene_dict["ensembl_gene_id"] == variant.ensembl_gene_id]

            if len(omim_filter1) > 0:
                mim_adultonset_dict = pd.read_csv(config.mim_adultonset_dict_path, header=None, names=["mim_number"])
                mim_number = omim_filter1["mim_number"]
                mim_adultonset_dict = mim_adultonset_dict.reset_index()
                adultonset_df = mim_adultonset_dict[mim_adultonset_dict["mim_number"] == int(mim_number.iloc[0])]

                BS2_snps_recessive_dict, BS2_snps_dominant_dict = utils.read_BS2_dict()

                if len(adultonset_df) > 0:
                    BS2 = 0
                else:
                    mim_recessive_dict = pd.read_csv(config.mim_recessive_dict_path, header=None, names=["mim_number"])
                    mim_recessive_dict = mim_recessive_dict.reset_index()
                    recessive_df = mim_recessive_dict[mim_recessive_dict["mim_number"] == int(mim_number.iloc[0])]
                    if len(recessive_df) > 0:
                        if variant_key in BS2_snps_recessive_dict and BS2_snps_recessive_dict[variant_key] == "1":
                            BS2=1

                mim_domin_dict = pd.read_csv(config.mim_domin_dict_path, header=None, names=["mim_number"])
                mim_domin_dict = mim_domin_dict.reset_index()
                dominant_df = mim_domin_dict[mim_domin_dict["mim_number"] == int(mim_number.iloc[0])]

                if len(dominant_df) > 0:
                    BS2 = 0
                    if variant_key in BS2_snps_dominant_dict and BS2_snps_dominant_dict[variant_key] == "1":
                        BS2 = 1
            else:
                BS2 = 0
                
        except Exception as err:
            utils.err_handler(err)

        return BS2

    def set_PM2(self, variant):
        try:
            PM2 = 0
            cutoff_maf = 0.005
            control_flag = 1

            frequency_keys = ["af_esp", "af_exac", "af_tgp"]

            for key in frequency_keys:
                if utils.check_value(getattr(variant, key)):
                    control_flag = 0

            if control_flag == 1:
                PM2 = 1

            if control_flag == 0:
                tt2 = 1

                mim2gene_dict = utils.read_mim2gene()
                mim_num = 0
                omim_filter = mim2gene_dict[(mim2gene_dict["ncbi_entrez_gene_id"] == variant.vep_gene_id) | (mim2gene_dict["ensembl_gene_id"] == variant.ensembl_gene_id)]
                
                if len(omim_filter) > 0:
                    omim_filter.reset_index(drop=True, inplace=True)
                    mim_num_series = omim_filter["mim_number"]
                    mim_num = mim_num_series.iloc[0]
                    
                mim_recessive_dict = pd.read_csv(config.mim_recessive_dict_path, sep="\t", header=None, names=["mim_num"])

                if int(mim_num) > 0:
                    res = mim_recessive_dict[mim_recessive_dict["mim_num"] == int(mim_num)]
                    
                    if len(res) > 0:
                        for key in frequency_keys:
                            if utils.check_value(getattr(variant, key)) and float(getattr(variant, key)) >= cutoff_maf:
                                tt2 = 0

                        if tt2 == 1:
                            PM2 = 1
                        if tt2 == 0:
                            PM2 = 0
                    else:
                        PM2 = 0

                if mim_num == 0:
                    PM2 = 0

        except Exception as err:
            utils.err_handler(err)

        return PM2

    def set_PM1(self, variant):
        PM1 = 0
        PM1_t1 = 0
        PM1_t2 = 0

        if variant.functional_consequence:
            functional_consequence = variant.functional_consequence

            for function in ["missense", "nonsynony"]:
                if functional_consequence.find(function) >=0:
                    PM1_t1 = 1

        domain_benign_dict = pd.read_csv(config.hg38_domain_benign_dict_path, sep="\t")
        domain_benign_dict["key"] = domain_benign_dict['Chr'].astype(str) +"-"+ domain_benign_dict['Gene.refGene'] +"-"+ domain_benign_dict['Interpro_domain']

        if variant.interpro_domain != '.':
            variant_key = str(variant.chr) +"-"+ variant.gene +"-"+ variant.interpro_domain
            res_df = domain_benign_dict[domain_benign_dict["key"] == variant_key]
            if len(res_df) > 0:
                PM1_t2 = 1
            else:
                PM1_t2 = 0

        if PM1_t1 == 1 and PM1_t2 == 1:
            PM1 = 1

        return PM1

    def set_PP5(self, variant):
        PP5 = 0

        if utils.check_value(variant.clinvar_clnsig):
            clinical_significance = ''.join(variant.clinvar_clnsig)

            if clinical_significance.find("athogenic") >= 0 and utils.check_value(variant.clinvar_clnrevstat):
                clinical_review_status = ''.join(variant.clinvar_clnrevstat)
                if clinical_review_status.find("onflicting") < 0:
                    PP5 = 1

        return PP5

    def set_BP6(self, variant):
        BP6 = 0

        if utils.check_value(variant.clinvar_clnsig):
            clinical_significance = ''.join(variant.clinvar_clnsig)
            if clinical_significance.find("enign") >= 0 and utils.check_value(variant.clinvar_clnrevstat):
                clinical_review_status = ''.join(variant.clinvar_clnrevstat)
                if clinical_review_status.find("onflicting") < 0:
                    BP6 = 1

        return BP6

    def set_BA1(self, variant):
        BA1 = 0

        if (utils.check_value(variant.af_esp) and float(variant.af_esp) > 0.05) or (utils.check_value(variant.af_exac) and float(variant.af_exac) > 0.05) or (utils.check_value(variant.af_tgp) and float(variant.af_tgp) > 0.05):
            BA1 = 1
        
        if (utils.check_value(variant.af_vep) and float(variant.af_vep) > 0.05):
            BA1 = 1

        return BA1

    def set_BP7(self, variant):
        BP7 = 0
        BP7_temp_1 = 0
        BP7_temp_2 = 0

        cutoff_conserv = 2

        functional_consequences = ["synon","coding-synon"]
        nonsynonym_label = "nonsynon"

        if utils.check_value(variant.functional_consequence):
            functional_consequence = variant.functional_consequence

            for conseq in functional_consequences:
                if functional_consequence.find(conseq) >= 0 and functional_consequence.find(nonsynonym_label)<0:
                    if not utils.check_value(variant.dbscsnv_rf_score) or not utils.check_value(variant.dbscsnv_ada_score):
                        BP7_temp_1=1
                    elif float(variant.dbscsnv_rf_score) < 0.6 and float(variant.dbscsnv_ada_score) < 0.6:
                        BP7_temp_1=1

        if utils.check_value(variant.gerp_rs_score):
            gerp_cs_score = variant.gerp_rs_score
            if float(gerp_cs_score) <= float(cutoff_conserv) or gerp_cs_score == '.':
                BP7_temp_2 = 1
        else:
            BP7_temp_2 = 1

        BP7 = BP7_temp_1 & BP7_temp_2
        return BP7

    def set_PP3(self, variant):
        PP3 = 0

        PP3_t1 = 0
        PP3_t2 = 0
        PP3_t3 = 0
        metasvm_cutoff = 0.0
        conservation_cutoff = 2
        dbscSNV_cutoff = 0.6

        if utils.check_value(variant.metasvm_score):
            if float(variant.metasvm_score) > metasvm_cutoff: PP3_t1 = 1

            if not utils.check_value(variant.sift_score):
                if utils.check_value(variant.functional_consequence):
                    functional_consequence = variant.functional_consequence

                    for function in ["synon","coding-synon"]:
                        if functional_consequence.find(function) < 0: 
                            PP3_t1 = 1

            if utils.check_value(variant.gerp_rs_score) and float(variant.gerp_rs_score) > conservation_cutoff: PP3_t2 = 1

        if (utils.check_value(variant.dbscsnv_rf_score) and float(variant.dbscsnv_rf_score) > dbscSNV_cutoff) or (utils.check_value(variant.dbscsnv_ada_score) and float(variant.dbscsnv_ada_score) > dbscSNV_cutoff):
            PP3_t3 = 1
        
        if (PP3_t1 + PP3_t2 + PP3_t3) >= 2: PP3 = 1

        return PP3

    def set_BP4(self, variant):
        BP4 = 0

        BP4_t1 = 0
        BP4_t2 = 0
        BP4_t3 = 0
        
        metasvm_cutoff = 0.0
        conservation_cutoff = 2
        dbscSNV_cutoff = 0.6
        
        if utils.check_value(variant.metasvm_score) and float(variant.metasvm_score) < metasvm_cutoff:
            BP4_t1 = 1 

        if not utils.check_value(variant.sift_score):
            if utils.check_value(variant.functional_consequence):
                functional_consequence = variant.functional_consequence

                for function in ["synon","coding-synon"]:
                    if functional_consequence.find(function) >= 0 and functional_consequence.find("nonsynon") < 0:
                        BP4_t1 = 1
                
        if utils.check_value(variant.gerp_rs_score) and float(variant.gerp_rs_score) <= conservation_cutoff:
            BP4_t2 = 1
        elif not utils.check_value(variant.gerp_rs_score):
            BP4_t2 = 1

        if (utils.check_value(variant.dbscsnv_rf_score) and float(variant.dbscsnv_rf_score) <= dbscSNV_cutoff) or (utils.check_value(variant.dbscsnv_ada_score) and float(variant.dbscsnv_ada_score) <= dbscSNV_cutoff):
            BP4_t3 = 1
        elif not utils.check_value(variant.dbscsnv_rf_score) and not utils.check_value(variant.dbscsnv_ada_score):
            BP4_t3 = 1
        
        if (BP4_t1 + BP4_t2 + BP4_t3) == 2: BP4 = 1

        return BP4

    def set_PM4(self, variant):
        PM4 = 0
        PM4_t1 = 0
        PM4_t2 = 0
        is_stoploss = False
        
        if utils.check_value(variant.functional_consequence):
            functional_consequence = variant.functional_consequence
            
            for function in ["nonframeshift insertion","nonframeshift deletion","stoploss"]:
                if functional_consequence.find(function) >= 0:
                    PM4_t1 = 1
                
                    if function == "stoploss":
                        is_stoploss = True

        if utils.check_value(variant.rmsk):
            if variant.rmsk == 0:
                PM4_t2 = 1

            if variant.rmsk == 1 and is_stoploss:
                PM4_t2 = 1

        if PM4_t1 !=0 and PM4_t2 != 0:
            PM4 = 1

        return PM4

    def set_BP3(self, variant):
        BP3 = 0
        BP3_t1 = 0
        BP3_t2 = 0
        
        if utils.check_value(variant.functional_consequence):
            functional_consequence = variant.functional_consequence
            
            for function in ["nonframeshift insertion","nonframeshift deletion","nonframeshift substitution"]:
                if functional_consequence.find(function) >= 0:
                    BP3_t1 = 1
        
        if utils.check_value(variant.rmsk):
            if variant.rmsk == 1 and variant.interpro_domain == '.': 
                BP3_t2 = 1

        if BP3_t1 != 0 and BP3_t2 != 0:
            BP3 = 1

        return BP3

    def classify(self, PVS1, PS, PM, PP, BA1, BS, BP):
        PS_sum = utils.sum_of_list(PS)
        PM_sum = utils.sum_of_list(PM)
        PP_sum = utils.sum_of_list(PP)
        BS_sum = utils.sum_of_list(BS)
        BP_sum = utils.sum_of_list(BP)

        result = "VA: "

        if PVS1 == 1 and (PS_sum >= 1 or PM_sum >= 2 or (PM_sum == 1 and PS_sum == 1) or PP_sum >= 2):
            result = "Pathogenic"

        elif PS_sum >= 2:
            result = "Pathogenic"
        
        elif PS_sum == 1 and (PM_sum >= 3 or (PM_sum == 2 and PP_sum >= 2) or (PM_sum == 1 and PP_sum >= 4)):
            result = "Pathogenic"

        elif (PVS1 == 1 and PM_sum == 1) or (PS_sum == 1 and (PM_sum <= 2 or PP_sum >= 2)) or PM_sum >= 3 or (PM_sum == 2 and PP_sum >= 2) or (PM_sum == 1 and PP_sum >= 4):
            result = "Likely Pathogenic"
        
        elif BA1 == 1 or BS_sum >= 2:
            result = "Benign"

        elif (BS_sum >= 1 and BP_sum >= 1) or BP_sum >= 2:
            result = "Likely Benign"
        
        else:
            result = "Uncertain Significance"

        return result

    def interpret(self, chrom, pos, ref, alt):
        variant = Variant(chr=chrom, pos=pos, ref=ref, alt=alt)
        vep_info = None
        clinvar_info = None
        dbscSNV_info = None
        dbNSFP_info = None
        rmsk_info = None
        pathogenicity = "Uncertain Significance"

        try:
            vep = utils.db_connect("vep")
            vep_col = vep["records"]
            vep_info = vep_col.find_one({"$and": [
                        { "chr": str(variant.chr)}, 
                        { "pos": int(variant.pos)},
                        { "ref": variant.ref},
                        { "alt": variant.alt}
                        ]})
            
            if vep_info:
                if utils.exists('consequence', vep_info):
                    variant.functional_consequence = vep_info["consequence"]
                
                if utils.exists('hgvsp', vep_info):
                    variant.hgvsp = vep_info["hgvsp"]
                    variant.aa_change = utils.extract_aa_change(vep_info["hgvsp"])

                if utils.exists('exon', vep_info):
                    variant.exon_number = vep_info["exon"]
                    
                if utils.exists('max_af', vep_info):
                    variant.af_vep = vep_info["max_af"]
                
                if utils.exists('gene', vep_info):
                    variant.vep_gene_id = vep_info['gene']

                if utils.exists('hgnc_id', vep_info):
                    variant.hgnc_id = vep_info['hgnc_id']

                if utils.exists('symbol_source', vep_info):
                    variant.hgnc_src = vep_info['symbol_source']
                    
            clinvar = utils.db_connect("clinvar")
            clinvar_col = clinvar["records"]
            clinvar_info = clinvar_col.find_one({"$and": [
                        {"chr": str(variant.chr)}, 
                        {"pos": int(variant.pos)},
                        {"ref": variant.ref},
                        {"alt": variant.alt}
                        ]})
            
            if clinvar_info:
                clinvar_info_dict = clinvar_info["INFO"]
                if utils.exists("CLNSIG", clinvar_info_dict):
                    variant.clinvar_clnsig = ''.join(clinvar_info["INFO"]["CLNSIG"])
                
                if utils.exists("CLNREVSTAT", clinvar_info_dict):
                    variant.clinvar_clnrevstat = ''.join(clinvar_info["INFO"]["CLNREVSTAT"])
                
                if utils.exists("AF_ESP", clinvar_info_dict):
                    variant.af_esp = clinvar_info["INFO"]["AF_ESP"]

                if utils.exists("AF_EXAC", clinvar_info_dict):
                    variant.af_exac = clinvar_info["INFO"]["AF_EXAC"]

                if utils.exists("AF_TGP", clinvar_info_dict):
                    variant.af_tgp = clinvar_info["INFO"]["AF_TGP"]

            dbscsnv = utils.db_connect("dbscSNV")
            dbscsnv_col = dbscsnv[f"chr{variant.chr}"]
            dbscSNV_info = dbscsnv_col.find_one({"$and": [
                        {"chr": str(variant.chr)}, 
                        {"pos": int(variant.pos)},
                        {"ref": variant.ref},
                        {"alt": variant.alt}
                        ]})
            
            if dbscSNV_info:
                if utils.exists('rf_score', dbscSNV_info):
                    variant.dbscsnv_rf_score = float(dbscSNV_info["rf_score"])

                if utils.exists('ada_score', dbscSNV_info):
                    variant.dbscsnv_ada_score = float(dbscSNV_info["ada_score"])

                if variant.functional_consequence is None and utils.exists('RefSeq_functional_consequence', dbscSNV_info):
                    variant.functional_consequence = dbscSNV_info["RefSeq_functional_consequence"]

            dbnsfp = utils.db_connect("dbNSFP")
            dbnsfp_col = dbnsfp[f"chr{variant.chr}"]
            dbNSFP_info = dbnsfp_col.find_one({"$and": [
                        {"chr": str(variant.chr)}, 
                        {"pos": int(variant.pos)},
                        {"ref": variant.ref},
                        {"alt": variant.alt}
                        ]})
            
            if dbNSFP_info:
                if utils.exists('genename', dbNSFP_info):
                    variant.gene = dbNSFP_info['genename']

                if utils.exists('Ensembl_geneid', dbNSFP_info):
                    variant.ensembl_gene_id = dbNSFP_info['Ensembl_geneid']

                if utils.exists('GERP++_RS', dbNSFP_info):
                    variant.gerp_rs_score = dbNSFP_info['GERP++_RS']
                
                if utils.exists('MetaSVM_score', dbNSFP_info):
                    variant.metasvm_score = dbNSFP_info['MetaSVM_score']

                if utils.exists('SIFT_score', dbNSFP_info):
                    variant.sift_score = dbNSFP_info['SIFT_score']

                if utils.exists('Interpro_domain', dbNSFP_info):
                    variant.interpro_domain = dbNSFP_info["Interpro_domain"]
                    
            rmsk_db = utils.db_connect("rmsk")
            col = rmsk_db[f"chr{variant.chr}"]
            rmsk_info = col.find_one({"$and": [
                        {"chr": "chr"+str(variant.chr)}, 
                        {"pos": int(variant.pos)},
                        {"ref": variant.ref},
                        {"alt": variant.alt}
                        ]})
            
            if rmsk_info:
                variant.rmsk = rmsk_info["rmsk"]
        
            ucsc_db = utils.db_connect("uscsc")
            col = ucsc_db[f"chr{variant.chr}"]
            ucsc_info = col.find_one({"$and": [
                        {"chr": "chr"+str(variant.chr)}, 
                        {"pos": int(variant.pos)},
                        {"ref": variant.ref},
                        {"alt": variant.alt}
                        ]})
            
            if ucsc_info:
                if utils.exists("name2", ucsc_info):
                    variant.ucsc_trans_id = ucsc_info["name2"]
                if utils.exists("chromStart", ucsc_info):
                    variant.start = ucsc_info["chromStart"]
                if utils.exists("chromEnd", ucsc_info):
                    variant.end = ucsc_info["chromEnd"]
        
        except Exception as err:
            utils.err_handler(err)

        PVS1 = self.set_PVS1(variant)
        PS1 = self.set_PS1(variant)
        PS4 = self.set_PS4(variant)
        PM1 = self.set_PM1(variant)
        PM2 = self.set_PM2(variant)
        PM4 = self.set_PM4(variant)
        PM5 = self.set_PM5(variant)
        PP2 = self.set_PP2(variant)
        PP3 = self.set_PP3(variant)
        PP5 = self.set_PP5(variant)

        BA1 = self.set_BA1(variant)
        BS1 = self.set_BS1(variant)
        BS2 = self.set_BS2(variant)
        BP1 = self.set_BP1(variant)
        BP3 = self.set_BP3(variant)
        BP4 = self.set_BP4(variant)
        BP6 = self.set_BP6(variant)
        BP7 = self.set_BP7(variant)

        PS = [PS1, 0, 0, PS4]
        PP = [0, PP2, PP3, 0, PP5]
        PM = [PM1, PM2, 0, PM4, PM5, 0]

        BS = [BS1, BS2, 0, 0]
        BP = [BP1, 0, BP3, BP4, 0, BP6, BP7]

        pathogenicity = self.classify(PVS1=PVS1, PS=PS, PP=PP, PM=PM, BA1=BA1, BS=BS, BP=BP) 

        variant.PVS1 = PVS1
        variant.PS = PS
        variant.PM = PM
        variant.PP = PP
        variant.BA1 = BA1
        variant.BS = BS
        variant.BP = BP
        variant.va_pathogenicity = pathogenicity
        
        return {
            "PVS1": PVS1,
            "PS1": PS1,
            "PS4": PS4,
            "PM1": PM1,
            "PM2": PM2,
            "PM4": PM4,
            "PM5": PM5,
            "PP2": PP2,
            "PP3": PP3,
            "PP5": PP5,
            "BA1": BA1,
            "BS1": BS1,
            "BS2": BS2,
            "BP1": BP1,
            "BP3": BP3,
            "BP4": BP4,
            "BP6": BP6,
            "BP7": BP7,
            "pathogenicity": pathogenicity
        }
