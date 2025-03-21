import argparse
import pandas as pd
import xml.etree.ElementTree as ET
import pdg

def main():
    api = pdg.connect()
    print ("PDG edition:", api.edition)
    
    # Output DataFrame
    df = pd.DataFrame()

    # evt.pdl dictionary
    # Particle name : id
    part_dict = {}
    pdlFile = open(evtFile, "r")
    pdlData = pdlFile.readlines()
    for line in pdlData:
        words = line.split()
        if words[0] == "add" and words[2] == "Particle":
            part_dict[words[3]] = int(words[4])
    pdlFile.close()

    # Reference decay file
    tree_ref = ET.parse(refFile)
    root_ref = tree_ref.getroot()
    
    # Input decay file
    tree_dec = ET.parse(decFile)
    root_dec = tree_dec.getroot()    
    # Alias dictionary
    alias_dict = {}
    for alias in root_dec.findall('alias'):
        name = alias.get('name')
        particle = alias.get('particle')
        alias_dict[name] = particle
    # Signal decay
    for decay_dec in root_dec.findall('decay'):
        name_dec = decay_dec.get('name')
        if (name_dec[-3:] != "sig"): continue
        signal = name_dec[:-3]
        print (signal, "signal decay:")
        for child_dec in decay_dec:
            br_dec = '{:.6f}'.format(round(float(child_dec.get('br')), 6))
            pr_dec = child_dec.get('daughters')
            pr_dec_list = pr_dec.split()
            pr_dec_list_id = []
            # Apply alias to list of daughters
            for d in range(len(pr_dec_list)):
                if pr_dec_list[d] in alias_dict:
                    pr_dec_list[d] = alias_dict[pr_dec_list[d]]
                # List of daughter ids
                pr_dec_list_id.append(part_dict[pr_dec_list[d]])
            pr_dec_list_id.sort()

            # Filter based on daughters
            #filter = (len(pr_dec_list_id) > 2) and (211 in pr_dec_list_id or -211 in pr_dec_list_id)
            #if (not filter): continue

            # Reference decay file
            br_ref = '{:.6f}'.format(0)
            for decay_ref in root_ref.findall('decay'):
                name_ref = decay_ref.get('name')
                if (name_ref != signal): continue
                for child_ref in decay_ref:
                    pr_ref = child_ref.get('daughters')
                    pr_ref_list = pr_ref.split()
                    pr_ref_list_id = []
                    for d in range(len(pr_ref_list)):
                        pr_ref_list_id.append(part_dict[pr_ref_list[d]])
                    pr_ref_list_id.sort()
                    if (pr_dec_list_id == pr_ref_list_id):
                        br_ref = '{:.6f}'.format(round(float(child_ref.get('br')), 6))
                    
            # PDG interface
            br_pdg = '{:.6f}'.format(0)
            for exclusive in api.get_particle_by_mcid(part_dict[signal]).exclusive_branching_fractions():
                try:    decay_products = [int(p.item.particle.mcid) for p in exclusive.decay_products if p.item.particle]
                except: pass
                decay_products.sort()
                if (pr_dec_list_id == decay_products):
                    br_pdg = '{:.6f}'.format(round(float(exclusive.value), 6))
                    print (exclusive, ":", br_pdg)
                    break;

            # Concat the DataFrame
            new_row = { 'Products': pr_dec_list, 'DEC': br_dec, 'REF': br_ref, 'PDG': br_pdg }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.at['Sum', 'Products'] = ''
    df.at['Sum', 'DEC'] = '{:.6f}'.format(df['DEC'].astype(float).sum())
    df.at['Sum', 'REF'] = '{:.6f}'.format(df['REF'].astype(float).sum())
    df.at['Sum', 'PDG'] = '{:.6f}'.format(df['PDG'].astype(float).sum())
    print (df.to_string())
            
if __name__ == '__main__':
    # Use evtgen/scripts/convertDecayFile.py to convert a decay file to XML format
    # Use DecFiles/dkfiles/ to select a decay file converted to XML format
    parser = argparse.ArgumentParser(description='Branching fraction table of a decay file with references to DECAY.DEC and PDG')
    parser.add_argument('-d', '--decFile', dest='decFile', default='DecFiles/dkfiles/Bd_D0DX,muX=cocktail,RDstar,TightCut.XML',
                        help='Input decay file in XML format. Default is DecFiles/dkfiles/Bd_D0DX,muX=cocktail,RDstar,TightCut.XML')
    parser.add_argument('-r', '--refFile', dest='refFile', default='DECAY.XML', # from evtgen/DECAY.DEC
                        help='Reference decay file in XML format. Default is DECAY.XML')
    parser.add_argument('-e', '--evtFile', dest='evtFile', default='evt.pdl', # from evtgen/evt.pdl
                        help='EvtGen particle properties file. Default is evt.pdl')
    args    = parser.parse_args()
    decFile = args.decFile
    refFile = args.refFile
    evtFile = args.evtFile
    print(args)
    main()
