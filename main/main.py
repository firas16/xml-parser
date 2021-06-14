# This is a sample Python script.
import time
from xmlParser import parse_performance, parse_managers_and_performance, parse_managers_iter, parse_managers_from_path

t0 = time.time()
parse_managers_from_path("resources/thematics_morningstarLong.xml")
print("duration managers: ", time.time() - t0)

t0 = time.time()
parse_managers_iter("resources/thematics_morningstarLong.xml")
print("duration managers iter : ", time.time() - t0)

t0 = time.time()
parse_performance("resources/thematics_morningstarLong.xml")
print("duration performance : ", time.time() - t0)

t0 = time.time()
parse_managers_and_performance("resources/thematics_morningstarLong.xml")
print("duration All : ", time.time() - t0)



