import sys
import json

def main(threads_path, thread_path, ids):
  ids = ids.split()
  ids.sort()
  ids = " ".join(ids)

  with open(threads_path) as fp:
    threads = json.load(fp)

  thread = threads["threads"][ids]

  with open(thread_path, "w") as fp:
    json.dump(thread, fp, indent=2)


if not len(sys.argv) == 4:
  print("ERROR: need in and out path")
  sys.exit()

main(sys.argv[1], sys.argv[2], sys.argv[3])
