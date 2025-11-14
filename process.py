import nmrglue as ng
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
# Data Section

# Metadatas
metadatas = {
    "TITLE": "2-Pentanone",
    "AUTHOR": "Jeff Hansen",
    "JCAMP-CS": "3.7",
    "ORGIN": "DePauw Department of Chemistry"
}

peak_list = [[1,3, [1,2]], [10, 0.5, [3,4]]]

### Add more error handling when file is invalid format, file is empty
# expect struc file when received spec file, failed merge etc, etc

def build_metadata(metadatas: dict, num_blocks:int | None = None) -> str:
    lines = [
        "##DATA_TYPE=LINK",
        f"##BLOCKS={num_blocks if num_blocks is not None else ''}",
    ]
    
    lines.extend(f"##{k}={v}" for k, v in metadatas.items())

    return "\n".join(lines)

print(build_metadata(metadatas))

def build_jcamp_blocks(jcamp: str, block_id: int | None = None, metadatas: dict | None = None) -> str:
    if metadatas is None:
        metadatas = {}

    lines = jcamp.splitlines()
    insert_lines = [f"##BLOCK_ID={block_id if block_id is not None else ''}"]
    insert_lines += [f"##{k}={v}" for k, v in metadatas.items()]

    insert_pos = 1 if len(lines) >= 1 else 0
    new_lines = lines[:insert_pos] + insert_lines + lines[insert_pos:]

    return "\n".join(new_lines)

# def build_peak_table(peaks: list, metadata: dict | None = None) -> str:
#     if metadata is None:
#         metadata = {}

#     lines = ["##BLOCK_ID=2", "##PEAK TABLE=(XY..XY)"]

#     for k, v in metadata.items():
#         lines.insert(0, f"##{k}={v}")

#     for entry in peaks:
#         if len(entry) >= 2:
#             x, y = entry[:2]
#             lines.append(f"{x}, {y}")

#     lines.append("##END=$$ End of the peaks block")
#     return "\n".join(lines)

# print(build_peak_table(peak_list))

# Add an condition to return an empty string "" or None if the assignment is empty
def build_assignment_table(assignments: list, metadata: dict | None = None) -> str:
    if metadata is None:
        metadata = {}

    lines = ["##BLOCK_ID=3", "##PEAK ASSIGNMENTS=(XYMA)"]

    for k, v in metadata.items():
        lines.insert(0, f"##{k}={v}")

    for x, y, atoms in assignments:
        for atom in atoms:
            lines.append(f"({x}, {y}, , <{atom}>)")

    lines.append("##END=$$ End of the assignment block")
    return "\n".join(lines)

# Add conditions if assignments = None / ""
def build_jcamp(metadatas:str, structure: str, spectrum: str, assignments: str) -> str:
    return "\n\n".join([metadatas, structure, assignments, spectrum])

# testing
# struc_path = input("Enter the struc filename: ")
# with open(struc_path + ".jdx", "r") as f:
#     struc = f.read()

# spec_path = input("Enter the spec filename: ")
# with open(spec_path + ".jdx", "r") as f:
#     spec = f.read()

# spec_bloc = build_jcamp_blocks(spec, 4)
# struc_bloc = build_jcamp_blocks(struc, 1)

# metadata = build_metadata(metadatas)
# # peaks_table = build_peak_table(peak_list)
# assign_table = build_assignment_table(peak_list)
# merged = build_jcamp(metadata, struc_bloc, spec_bloc, assign_table)

# out_path = input("Enter output filename: ")
# with open(out_path + "MS.jdx", "w") as f:
#     f.write(merged)

# print(f"Merged file saved as {out_path}")

# Peak Auto Identification
# dic, data = ng.jcampdx.read("2-PentanoneHNMR.jdx")

# peaks, _ = find_peaks(data, prominence=0.2) # 10000 for CNMR, 0.1 fpr HNMR

# plt.plot(data)
# # print(peaks)

# plt.scatter(peaks, data[peaks], color="red", s=50, zorder=5, label="peaks")
# plt.savefig("plot_1d.png") 

