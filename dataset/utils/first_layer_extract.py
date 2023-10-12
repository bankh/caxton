import csv

def read_second_source(second_source_csv):
    print_limits = {}
    with open(second_source_csv, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            path, part, limit = row
            if limit.isdigit():  # Check if limit is a valid integer
                print_limits[part] = int(limit)
    return print_limits

def filter_first_source(source_csv, target_csv, print_limits):
    with open(source_csv, 'r') as f_source, open(target_csv, 'w', newline='') as f_target:
        reader = csv.reader(f_source)
        writer = csv.writer(f_target)
        
        # Write header
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            img_path = row[0]
            print_id = row[11]
            print_number = f"print{print_id}"
            image_number = int(img_path.split('-')[-1].split('.')[0])
            
            if print_number in print_limits and image_number <= print_limits[print_number]:
                writer.writerow(row)

if __name__ == "__main__":
    source_csv = "/path/to/your/source.csv"
    second_source_csv = "/path/to/your/second_source.csv"
    target_csv = "/path/to/your/target.csv"
    
    print_limits = read_second_source(second_source_csv)
    filter_first_source(source_csv, target_csv, print_limits)
