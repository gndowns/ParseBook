import sys
import json

def main(thread_path):
  with open(thread_path) as fp:
    thread = json.load(fp)

  message_count = 0

  # Date format: "Saturday, October 24, 2015 at 8:34pm EDT"
  first_date = thread["messages"][1]["created_at"].split()
  # new Date format: ['Saturday,' 'October', '24', '2015', 'at', '8:34pm', 'EDT']
  month = first_date[1]
  year = first_date[3]

  month_year = " ".join([month, year])
  frequencies = {month_year: 0}

  for msg in thread["messages"]:
    message_count += 1

    this_date = msg["created_at"].split()
    this_month_year = " ".join([ this_date[1], this_date[3] ])

    if this_month_year == month_year:
      frequencies[month_year] += 1
    else:
      frequencies[this_month_year] = 0
      month_year = this_month_year

  print("Total Number of Messages: {}".format(message_count) )
  print(json.dumps(frequencies, indent=2))

 
if not len(sys.argv) == 2:
  print("ERROR: need path to conversation json")
  sys.exit()

main(sys.argv[1])
