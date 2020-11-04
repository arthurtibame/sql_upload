def extract_jpg_details(filename: str):
    details = filename.split("-")
    jpgtimestamp = details[0]
    jpg_no =details[1][:-4]
    return {
        "jpgtimestamp": jpgtimestamp, "jpg_no":jpg_no
    }