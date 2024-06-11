import argparse


def main(args):
    input_csv = args.input_csv
    res = final_func(input_csv,**kwargs)
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weight prediction")
    parser.add_argument("--input_csv", help="Input CSV file")
    parser.add_argument("--output_csv", help="Output CSV file")
    args = parser.parse_args()
    main(args)
    
