
from extract_transform import main as transform_data
from load_to_postgres import main as load_data


def main():
    print("Starting ETL pipeline...")

    print("\nSTEP 1: Data quality and transformation")
    transform_data()

    print("\nSTEP 2: Load to PostgreSQL")
    load_data()

    print("\nETL PIPELINE COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
