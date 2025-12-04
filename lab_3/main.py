from checksum import calculate_checksum, serialize_result
from file_handler import read_json, read_csv, validate


def main():
    settings = read_json("settings.json")
    regex = read_json("regex.json")
    df = read_csv(settings["input_file_path"])
    result = validate(df, regex)
    checksum = calculate_checksum(result)
    serialize_result(settings["variant"],
                     checksum,
                     str(settings["result"]))


if __name__ == "__main__":
    main()