import json
import re

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

    stop_name_pattern = re.compile(r"^([A-Z][a-z]*\s?)+ (Road|Avenue|Boulevard|Street)$")
    stop_type_pattern = re.compile("^[SOF]?$")
    a_time_pattern = re.compile(r"^([01]\d|[2][0-3]):([0-5]\d)$")

    for stop in data:
        if not stop_name_pattern.match(stop["stop_name"]):
            stop_name_errors += 1
        if not stop_type_pattern.match(stop["stop_type"]):
            stop_type_errors += 1
        if not a_time_pattern.match(stop["a_time"]):
            a_time_errors += 1

    print("Format validation: {} errors".format(stop_type_errors + stop_name_errors + a_time_errors))
    print(f"stop_name: {stop_name_errors}")
    print(f"stop_type: {stop_type_errors}")
    print(f"a_time: {a_time_errors}")


# stage 3/6: Bus line info
# For exercise description see "Bus line info/task.html"
def count_line_stops(data):
    lines = dict()
    for stop in data:
        lines[stop["bus_id"]] = lines.get(stop["bus_id"], 0) + 1

    for key in sorted(lines.keys()):
        print(f"bus_id: {key}, stops: {lines[key]}")


# stage 4/6: Special stops
# For exercise description see "Special stops/task.html"
def validate_count_stops(data):
    start_stops = set()
    transfer_stops = set()
    finish_stops = set()
    lines = dict()

    # Gather stops by their stop types
    for stop in data:
        stop_type = stop["stop_type"]
        bus_id = stop["bus_id"]
        if stop_type in ["S", "F"]:
            # Make sure there are no two start or end points for each end line
            if stop_type in lines.get(bus_id, (set(), set()))[0]:
                print(f"There are two start or end stops for the line: {bus_id}.")
                return
            else:
                lines[bus_id] = lines.get(bus_id, (set(), set()))
                lines[bus_id][0].add(stop_type)
                if stop_type == "S":
                    start_stops.add(stop["stop_name"])
                else:
                    finish_stops.add(stop["stop_name"])
        else:
            # in case of bus lines with only non end stops
            if bus_id not in lines.keys():
                lines[bus_id] = (set(), set())
        lines[bus_id][1].add(stop["stop_name"])

    # check if each bus line has a start and end point
    for line, (endpoints, stops) in lines.items():
        if len(endpoints) != 2:
            print(f"There is no start or end stop for the line: {line}.")
            return
        for bus_id in lines.keys():
            if bus_id != line:
                transfer_stops |= (stops & lines[bus_id][1])

    print("Start stops: {0} {1}".format(len(start_stops), sorted(start_stops)))
    print("Transfer stops: {0} {1}".format(len(transfer_stops), sorted(transfer_stops)))
    print("Finish stops: {0} {1}".format(len(finish_stops), sorted(finish_stops)))


# stage 5/6: Unlost in time
# For exercise description see "Unlost in time/task.html"
def validate_a_time(data):
    lines = dict()
    stops = dict()

    # congregate information
    for stop in data:
        # store id -> name relation of stops
        if stop["stop_id"] not in stops.keys():
            stops[stop["stop_id"]] = (stop["stop_name"], dict())
        # store (arrival time, stop type, next stop) of each bus line at each stop
        stops[stop["stop_id"]][1][stop["bus_id"]] = (stop["a_time"], stop["stop_type"], stop["next_stop"])
        # store start points for each bus line
        if stop["stop_type"] == "S":
            lines[stop["bus_id"]] = stop["stop_id"]

    print("Arrival time test:")
    error = False
    for line in sorted(lines.keys()):
        stop_id = lines[line]
        last_a_time = None
        while True:
            stop = stops[stop_id][1][line]
            # check time
            if last_a_time is None:
                last_a_time = stop[0]
            elif last_a_time >= stop[0]:
                print(f"bus_id line {line}: wrong time on station {stops[stop_id][0]}")
                error = True
                break

            # update data for next iteration
            if stop[1] == "F":
                break
            last_a_time = stop[0]
            stop_id = stop[2]

    if not error:
        print("OK")


# stage 6/6: On-demand
# For exercise description see "On-demand/task.html"
def check_on_demand(data):
    print("On demand stops test:")
    on_demand = set()
    start = set()
    end = set()
    transfer = set()
    lines = dict()

    # get data
    for stop in data:
        if stop["stop_type"] == "S":
            start.add((stop["stop_id"], stop["stop_name"]))
            lines[stop["bus_id"]] = lines.get(stop["bus_id"], set()) | {(stop["stop_id"], stop["stop_name"])}
        elif stop["stop_type"] == "S":
            end.add((stop["stop_id"], stop["stop_name"]))
            lines[stop["bus_id"]] = lines.get(stop["bus_id"], set()) | {(stop["stop_id"], stop["stop_name"])}
        elif stop["stop_type"] == "O":
            on_demand.add((stop["stop_id"], stop["stop_name"]))
            lines[stop["bus_id"]] = lines.get(stop["bus_id"], set()) | {(stop["stop_id"], stop["stop_name"])}
        else:
            lines[stop["bus_id"]] = lines.get(stop["bus_id"], set()) | {(stop["stop_id"], stop["stop_name"])}

    # get transfer stops
    for line, stop in lines.items():
        for bus_id in lines.keys():
            if bus_id != line:
                transfer |= (stop & lines[bus_id])

    # get wrong stops
    wrong_stops = []
    for stop in on_demand:
        if stop in (start | end | transfer):
            wrong_stops.append(stop[1])

    if len(wrong_stops) == 0:
        print("OK")
    else:
        print("Wrong stop type:", wrong_stops)


if __name__ == '__main__':
    json_string = input()
    stop_data = json.loads(json_string)

    # stage 1 function
    # validate_data(stop_data)

    # stage 2 function
    # validate_format(stop_data)

    # stage 3 function
    # count_line_stops(stop_data)

    # stage 4 function
    # validate_count_stops(stop_data)

    # stage 5 function
    # validate_a_time(stop_data)

    # stage 6 function
    check_on_demand(stop_data)
