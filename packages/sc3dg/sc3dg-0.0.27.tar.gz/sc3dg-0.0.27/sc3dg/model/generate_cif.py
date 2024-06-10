import os
import subprocess
import sys

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        return 0
    return 1

def generate_cif(pairs, name, output, res="50k", max_iter=400):
    os.makedirs(output, exist_ok=True)
    dipc = "./dip-c"
    color_file = "./color/mm10.cpg.20k.txt"

    print("Deleting repeat chromosome pairs...")
    dedup_pairs_path = os.path.join(output, f"{name}_dedup.pairs.gz")
    state = run_command(f"bash dedup_pair.sh {pairs} {dedup_pairs_path}")
    if not state:
        sys.exit(1)
    print("Deleted repeat chromosome pairs done!")

    contacts_pairs_path = os.path.join(output, f"{name}_contacts.pairs.gz")
    state = run_command(f"hickit -i {dedup_pairs_path} -n 10 -u -o - | bgzip > {contacts_pairs_path}")
    if not state:
        sys.exit(1)

    if res == "1m":
        print("Resolution is 1m")
        state = run_command(f"./hickit/hickit -s 1 -M -i {contacts_pairs_path} -n {max_iter} -Sr1m -c1 -r10m -c2 -b4m -b1m -O {output}/{name}_1m.3dg")
        if not state:
            sys.exit(1)
        state = run_command(f"scripts/hickit_3dg_to_3dg_rescale_unit.sh {output}/{name}_1m.3dg")
        if not state:
            sys.exit(1)
        state = run_command(f"{dipc} color -n {color_file} {output}/{name}_1m.dip-c.3dg | {dipc} vis -c /dev/stdin {output}/{name}_1m.dip-c.3dg > {output}/{name}_1m.3dg.cif")
        if not state:
            sys.exit(1)

    elif res == "200k":
        print("Resolution is 200k")
        state = run_command(f"./hickit/hickit -s 1 -M -i {contacts_pairs_path} -n {max_iter} -Sr1m -c1 -r10m -c2 -b4m -b200k -O {output}/{name}_200k.3dg")
        if not state:
            sys.exit(1)
        state = run_command(f"scripts/hickit_3dg_to_3dg_rescale_unit.sh {output}/{name}_200k.3dg")
        if not state:
            sys.exit(1)
        state = run_command(f"{dipc} color -n {color_file} {output}/{name}_200k.dip-c.3dg | {dipc} vis -c /dev/stdin {output}/{name}_200k.dip-c.3dg > {output}/{name}_200k.3dg.cif")
        if not state:
            sys.exit(1)
    elif res == "50k":
        print("Resolution is 50k")
        state = run_command(f"./hickit/hickit -s 1 -M -i {contacts_pairs_path} -n {max_iter} -Sr1m -c1 -r10m -c2 -b4m -b50k -O {output}/{name}_50k.3dg")
        if not state:
            sys.exit(1)
        state = run_command(f"scripts/hickit_3dg_to_3dg_rescale_unit.sh {output}/{name}_50k.3dg")

        if not state:
            sys.exit(1)
        state = run_command(f"{dipc} color -n {color_file} {output}/{name}_50k.dip-c.3dg | {dipc} vis -c /dev/stdin {output}/{name}_50k.dip-c.3dg > {output}/{name}_50k.3dg.cif")
        if not state:
            sys.exit(1)
    elif res == "20k":
        print("Resolution is 20k")
        state = run_command(f"./hickit/hickit -s 1 -M -i {contacts_pairs_path} -n {max_iter} -Sr1m -c1 -r10m -c2 -b4m -b20k -O {output}/{name}_20k.3dg")
        if not state:
            sys.exit(1)
        state = run_command(f"scripts/hickit_3dg_to_3dg_rescale_unit.sh {output}/{name}_20k.3dg")
        if not state:
            sys.exit(1)
        state = run_command(f"{dipc} color -n {color_file} {output}/{name}_20k.dip-c.3dg | {dipc} vis -c /dev/stdin {output}/{name}_20k.dip-c.3dg > {output}/{name}_20k.3dg.cif")
        if not state:
            sys.exit(1)
    else:
        print("Resolution is not 1m, 200k, 50k, 20k")

    # os.remove(dedup_pairs_path)


# generate_cif("path/to/pairs", "sample_name", "path/to/output", res="50k")
