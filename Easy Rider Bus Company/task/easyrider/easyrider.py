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
        # check stop_name TODO
        # check if next_stop is int and provided (not provided would be ""[string])
        if not isinstance(stop["next_stop"], int):
            next_stop_errors += 1
        # check stop_type TODO
        # check a_time TODO


if __name__ == '__main__':
    json_string = input()
    stop_data = json.loads(json_string)
    validate_data(stop_data)
