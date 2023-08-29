import re
import sys


def main():
    print(convert(input("Hours: ")))


def convert(s):
    if s := re.search(r"(\d?\d)(?::(\d\d))? (\w\w)+ to (\d?\d)(?::(\d\d))? (\w\w)+", s):
        # print(s.groups())
        first_time = [int(s.group(1)), s.group(2)]
        second_time = [int(s.group(4)), s.group(5)]

        def am_pm_to_24(hour, merid):
            if merid == "AM":
                if hour[0] == 12:
                    hour[0] = 0
            else:
                if hour[0] == 12:
                    pass
                else:
                    hour[0] += 12
                    
        am_pm_to_24(first_time, s.group(3))
        am_pm_to_24(second_time, s.group(6))

        def test_hours(hour):
            if hour < 0 or hour > 24:
                raise ValueError

        test_hours(first_time[0])
        test_hours(second_time[0])

        if first_time[1] is None:
            first_time[1] = 0
        if second_time[1] is None:
            second_time[1] = 0

        def test_minutes(mins):
            if mins < 0 or mins > 59:
                raise ValueError

        test_minutes(int(first_time[1]))
        test_minutes(int(second_time[1]))

        return f"{first_time[0]:02}:{first_time[1]:02} to {second_time[0]:02}:{second_time[1]:02}"
    raise ValueError


if __name__ == "__main__":
    main()