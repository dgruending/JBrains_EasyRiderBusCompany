import json

# Stage 1/6: Checking the data type
# For exercise description see "Checking the data type/task.html"


def validate_data(data):
    bus_id_errors = 0
    stop_id_errors = 0
    stop_name_errors = 0
    next_stop_errors = 0
    stop_type_errors = 0
    a_time_errors = 0
    for stop in data:
        # check if bus_id is int and provided (not provided would be ""[string])
        if not isinstance(stop["bus_id"], int):
            bus_id_errors += 1
        # check if stop_id is int and provided (not provided would be ""[string])
        if not isinstance(stop["stop_id"], int):
            stop_id_errors += 1
        # check stop_name
        if not isinstance(stop["stop_name"], str) or stop["stop_name"] == "":
            stop_name_errors += 1
        # check if next_stop is int and provided (not provided would be ""[string])
        if not isinstance(stop["next_stop"], int):
            next_stop_errors += 1
        # check stop_type
        if not isinstance(stop["stop_type"], str) or len(stop["stop_type"]) > 1:
            stop_type_errors += 1
        # check a_time
        if not isinstance(stop["a_time"], str) or stop["a_time"] == "":
            a_time_errors += 1

    print("Type and required field validation: {} errors".format(bus_id_errors + stop_id_errors + stop_name_errors
                                                                 + next_stop_errors + stop_type_errors + a_time_errors))
    print(f"bus_id: {bus_id_errors}")
    print(f"stop_id: {stop_id_errors}")
    print(f"stop_name: {stop_name_errors}")
    print(f"next_stop: {next_stop_errors}")
    print(f"stop_type: {stop_type_errors}")
    print(f"a_time: {a_time_errors}")


# Stage 2/6: Correct syntax
# For exercise description see "Correct syntax/task.html"
def validate_format(data):
    stop_name_errors = 0
    stop_type_errors = 0
    a_time_errors = 0


if __name__ == '__main__':
    json_string = input()
    stop_data = json.loads(json_string)
    # validate_data(stop_data)
    validate_format(stop_data)
