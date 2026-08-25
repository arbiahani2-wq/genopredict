import requests
import gzip
import io
import csv
import sys

# Define target RSIDs
TARGET_RSIDS = [
    "rs429358",
    "rs7412",
    "rs744373", 
    "rs11136000",
    "rs3851179",
    "rs6656401"
]

# Correct VCF URLs for GIAB v4.2.1 GRCh38
VCF_URLS = {
    "HG002_Son": "https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/NISTv4.2.1/GRCh38/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz",
    "HG003_Father": "https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG003_NA24149_father/NISTv4.2.1/GRCh38/HG003_GRCh38_1_22_v4.2.1_benchmark.vcf.gz",
    "HG004_Mother": "https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG004_NA24143_mother/NISTv4.2.1/GRCh38/HG004_GRCh38_1_22_v4.2.1_benchmark.vcf.gz"
}

def get_variant_info(rsid):
    """Fetch chromosome, position (hg38), and ref/alt alleles from MyVariant.info"""
    url = f"https://myvariant.info/v1/variant/{rsid}?assembly=hg38"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            hits = []
            if "chrom" in data:
                hits.append(data)
            elif "hits" in data:
                hits = data["hits"]
            
            for hit in hits:
                if "chrom" in hit and "hg38" in hit:
                    chrom = hit["chrom"]
                    pos = hit["hg38"]["start"]
                    # Try to get Ref/Alt from 'vcf' field if detailed, or 'dbsnp'
                    ref = hit.get("vcf", {}).get("ref", "?")
                    alt = hit.get("vcf", {}).get("alt", "?")
                    # If simplified, check other fields
                    if ref == "?" and "ref" in hit: ref = hit["ref"] # rare
                    # MyVariant often puts ref/alt in 'vcf' object
                    
                    return chrom, pos, ref, alt
    except Exception as e:
        print(f"Error fetching info for {rsid}: {e}")
    return None, None, None, None

def stream_and_extract(sample_name, url, targets, writer):
    """Stream VCF and extract matching positions"""
    print(f"Processing {sample_name}...")
    
    # Organize targets by chrom for faster check
    targets_by_chrom = {}
    last_pos_by_chrom = {}
    
    for rsid, ch, pos, ref, alt in targets:
        ch_norm = str(ch).replace("chr", "")
        if ch_norm not in targets_by_chrom:
            targets_by_chrom[ch_norm] = {}
            last_pos_by_chrom[ch_norm] = 0
        targets_by_chrom[ch_norm][pos] = (rsid, ref, alt)
        if pos > last_pos_by_chrom[ch_norm]:
            last_pos_by_chrom[ch_norm] = pos

    found_variants = {} # rsid -> (chrom, pos, ref, alt, gt)

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with gzip.open(r.raw, mode='rt') as f:
                current_chrom = None
                
                for line_idx, line in enumerate(f):
                    if line.startswith("#"):
                        continue
                    
                    parts = line.split("\t")
                    if len(parts) < 10:
                        continue
                        
                    chrom = parts[0].replace("chr", "")
                    pos = int(parts[1])
                    
                    current_chrom = chrom
                    
                    # Optimization: If we passed the last target on this chromosome, we can skip?
                    # VCF is sorted.
                    # But verifying sorted order for all chrs is risky.
                    # However, within a chrom, it is sorted.
                    if chrom in last_pos_by_chrom and pos > last_pos_by_chrom[chrom]:
                        # Skip this line? Yes.
                        # Can we skip to next chrom? No, stream is sequential.
                        continue
                        
                    if chrom in targets_by_chrom and pos in targets_by_chrom[chrom]:
                        # Match found!
                        rsid, target_ref, target_alt = targets_by_chrom[chrom][pos]
                        
                        vcf_ref = parts[3]
                        vcf_alt = parts[4]
                        genotype_info = parts[9]
                        gt = genotype_info.split(":")[0]
                        
                        print(f"  Found {rsid} (chr{chrom}:{pos}) in {sample_name}: GT={gt} Ref={vcf_ref} Alt={vcf_alt}")
                        found_variants[rsid] = (chrom, pos, vcf_ref, vcf_alt, gt)

        # After processing, check what we missed and assume HomRef (0/0) or NoCall depending
        # Actually usually if not in VCF it is 0/0 (Ref).
        for rsid, ch, pos, ref, alt in targets:
            if rsid in found_variants:
                c, p, r, a, g = found_variants[rsid]
                writer.writerow([sample_name, rsid, c, p, r, a, g])
            else:
                # Not found -> Assume 0/0 (Homozygous Reference)
                # We use the Ref from MyVariant as Ref
                print(f"  {rsid} not found in VCF. Assuming 0/0 (Ref).")
                writer.writerow([sample_name, rsid, ch, pos, ref, alt, "0/0"])

    except Exception as e:
        print(f"Failed to process {sample_name}: {e}")

def main():
    print("Resolving coordinates...")
    resolved_targets = []
    for rs in TARGET_RSIDS:
        chrom, pos, ref, alt = get_variant_info(rs)
        if chrom and pos:
            # Normalize chrom?
            resolved_targets.append((rs, chrom, pos, ref, alt))
            print(f"  {rs} -> chr{chrom}:{pos} ({ref}/{alt})")
        else:
            print(f"  Could not resolve {rs}")

    if not resolved_targets:
        print("No targets resolved. Exiting.")
        return

    output_file = "trio_alzheimer_variants.csv"
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Sample", "rsID", "Chrom", "Pos", "Ref", "Alt", "GT"])
        
        for sample, url in VCF_URLS.items():
            stream_and_extract(sample, url, resolved_targets, writer)

    print(f"\nDone! Results saved to {output_file}")

if __name__ == "__main__":
    main()
