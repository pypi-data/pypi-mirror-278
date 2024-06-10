import argparse
import requests
import json

class Annobee:
    def __init__(self, endpoint='http://localhost:5000/api/interpret'):
        self.endpoint = endpoint
    
    def get_criteria(self, variant, criteria=None):
        """ Sends a POST request to the Flask API with the variant details and optional criteria. """
        print("Inside of get_critera")
        payload = {
            'variant': variant,
            'genome_build': 'hg38',  # default genome build
            'adjustments': {}        # default adjustments if any
        }
        if criteria:
            payload['criteria'] = criteria
        try:
            response = requests.post(self.endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    def interpret_single_file(self, filepath):
        try:
            with open(filepath, 'rb') as file:
                response = requests.post(self.endpoint, files={'file': file})
                response.raise_for_status()
                return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def interpret_multi_file(self, filepath):
        """ Sends a POST request to the Flask API with the file to interpret multi file. """
        try:
            with open(filepath, 'rb') as file:
                response = requests.post(self.endpoint, files={'file': file})
                response.raise_for_status()
                return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}    
    

def main():
    parser = argparse.ArgumentParser(description='Genetic Variant Analysis CLI')
#    parser.add_argument('variant', type=str, help='Variant in the format chr-pos-ref-alt, e.g., 1-12345-A-G')
    parser.add_argument('variant', type=str, nargs='?', default="", help='Variant in the format chr-pos-ref-alt, e.g., 1-12345-A-G')
    parser.add_argument('--endpoint', type=str, default='http://localhost:5000/api/interpret', help='API endpoint to use')
    parser.add_argument('--file', type=str, help='Path to the VCF file for single file interpretation')
    parser.add_argument('--multi-file', type=str, help='Path to the VCF file for multi file interpretation')

    
    # Add arguments for all individual criteria
    criteria = [
        'functional_consequence', 'hgvsp', 'aa_change', 'transcript_id', 'ucsc_trans_id',
        'exon_number', 'start', 'end', 'rmsk', 'clinvar_clnsig', 'clinvar_clnrevstat',
        'af_esp', 'af_exac', 'af_tgp', 'dbscsnv_rf_score', 'dbscsnv_ada_score', 'gerp_rs_score',
        'metasvm_score', 'sift_score', 'af_vep', 'va_pathogenicity', 'interpro_domain',
        'gene', 'ensembl_gene_id', 'vep_gene_id', 'max_af', 'hgnc_id', 'hgnc_src',
        'pvs1', 'ba1', 'ps', 'pm', 'pp', 'bs', 'bp', "all", "ps_sum", "pm_sum", "pp_sum", "bs_sum", "bp_sum"
    ]
    for crit in criteria:
        parser.add_argument(f'-{crit}', action='store_true', help=f'Return {crit.replace("_", " ").upper()} information')
    args = parser.parse_args()
    
    annobee = Annobee(endpoint=args.endpoint)
    
    if args.file:
        response = annobee.interpret_single_file(args.file)
        print(json.dumps(response, indent=4))
        return

    if args.multi_file:
        response = annobee.interpret_multi_file(args.multi_file)
        print(json.dumps(response, indent=4))
        return
    
    if args.variant:
        try:
            chrom, pos, ref, alt = args.variant.split('-')
            variant = {
                'CHROM': str(chrom),
                'POS': int(pos),
                'REF': ref,
                'ALT': alt
            }
        except ValueError:
            print("Error: Variant must be in the format 'chr-pos-ref-alt'. Example: chr1-12345-A-G")
            return
        results = {}
        info_requested = False
        for crit in criteria:
            if getattr(args, crit):
                info_requested = True
                response = annobee.get_criteria(variant, crit)
                results[crit] = response.get('INFO', {}).get(crit, 'Not available')
        if not info_requested:
            response = annobee.get_criteria(variant)  # Get all info if no specific criteria requested
            results = response
        print(json.dumps(results, indent=4))
    else:
        print("Error: Please provide a variant or a file for interpretation")


if __name__ == '__main__':
    main()