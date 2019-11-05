import csv
import sys

def filter_csv(connections, edges, output):
  connections_list = []
  with open(connections, 'r', newline='') as connections_file:
    reader = csv.reader(connections_file, delimiter=',')

    for row in reader:
      if row[0] not in connections_list:
        connections_list.append(row[0])
  
  with open(edges, 'r', newline='') as edges_file, open(output, 'w', newline='') as output_file:
    reader = csv.DictReader(edges_file, delimiter=',') # ['Source', 'Target']
    writer = csv.writer(output_file)

    writer.writerow(reader.fieldnames)

    for row in reader:
      if row['Source'] in connections_list and row['Target'] in connections_list:
        writer.writerow(row.values())

if __name__ == "__main__":
  if len(sys.argv) == 1:
    print(f'''Filters an edges csv to only users in the connections csv.
    Connections csv MUST have both a "Source" and "Target" column.
    Usage: {sys.argv[0]} <connections csv> <edges csv> <output csv>''')

    exit()

  filter_csv(sys.argv[1], sys.argv[2], sys.argv[3])