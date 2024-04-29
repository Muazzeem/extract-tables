import json

from extractor.document_extractor import online_process, get_table_data


def convert_to_json(header_row_values, body_row_values):
    data = []
    for row in body_row_values:
        data.append(dict(zip(header_row_values[0], row)))  # Assumes one header row

    # Convert the list of dictionaries to a JSON string
    json_data = json.dumps(data, indent=4)  # Use indent for readability
    return json_data


def main(file_path):
    document = online_process(
        file_path,
    )

    tables = document.pages[0].tables

    for table in tables:
        header_values = get_table_data(table.header_rows, document.text)
        body_values = get_table_data(table.body_rows, document.text)
        return convert_to_json(header_values, body_values)


if __name__ == "__main__":
    res = main("cleaned3.pdf")
    print(res)
