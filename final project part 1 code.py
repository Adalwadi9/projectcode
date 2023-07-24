import csv

class InventoryManager:
    def __init__(self, manufacturer_file, price_file, service_dates_file):
        """
        Initializes the InventoryManager with the provided input files.

        Parameters:
        manufacturer_file (str): The file path of the ManufacturerList.csv
        price_file (str): The file path of the PriceList.csv
        service_dates_file (str): The file path of the ServiceDatesList.csv
        """
        self.manufacturer_file = manufacturer_file
        self.price_file = price_file
        self.service_dates_file = service_dates_file

    def load_inventory(self):
        """
        Loads the inventory data from the input files.

        Returns:
        dict: A dictionary containing the loaded inventory data.
        """
        inventory = {}

        # Load ManufacturerList.csv
        with open(self.manufacturer_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                item_id = row[0]
                manufacturer = row[1]
                item_type = row[2]
                damaged = row[3] if len(row) > 3 else ""
                inventory[item_id] = {
                    'manufacturer': manufacturer,
                    'item_type': item_type,
                    'damaged': damaged
                }

        # Load PriceList.csv
        with open(self.price_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                item_id = row[0]
                price = row[1]
                if item_id in inventory:
                    inventory[item_id]['price'] = price

        # Load ServiceDatesList.csv
        with open(self.service_dates_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                item_id = row[0]
                service_date = row[1]
                if item_id in inventory:
                    inventory[item_id]['service_date'] = service_date

        return inventory

    def generate_full_inventory_report(self, inventory):
        """
        Generates the FullInventory.csv report.

        Parameters:
        inventory (dict): The inventory data.

        Returns:
        str: The report content.
        """
        report = "item ID,manufacturer name,item type,price,service date,damaged\n"

        for item_id, item_data in sorted(inventory.items(), key=lambda x: x[1]['manufacturer']):
            manufacturer = item_data['manufacturer']
            item_type = item_data['item_type']
            price = item_data.get('price', "")
            service_date = item_data.get('service_date', "")
            damaged = item_data['damaged']
            report += f"{item_id},{manufacturer},{item_type},{price},{service_date},{damaged}\n"

        return report

    def generate_item_type_inventory_report(self, inventory):
        """
        Generates the item type inventory reports.

        Parameters:
        inventory (dict): The inventory data.

        Returns:
        dict: A dictionary containing the item type reports.
        """
        item_type_reports = {}

        for item_id, item_data in inventory.items():
            item_type = item_data['item_type']
            if item_type not in item_type_reports:
                item_type_reports[item_type] = ""

            manufacturer = item_data['manufacturer']
            price = item_data.get('price', "")
            service_date = item_data.get('service_date', "")
            damaged = item_data['damaged']
            item_type_reports[item_type] += f"{item_id},{manufacturer},{price},{service_date},{damaged}\n"

        return item_type_reports

    def generate_past_service_date_inventory_report(self, inventory):
        """
        Generates the PastServiceDateInventory.csv report.

        Parameters:
        inventory (dict): The inventory data.

        Returns:
        str: The report content.
        """
        report = "item ID,manufacturer name,item type,price,service date,damaged\n"

        sorted_inventory = sorted(inventory.items(), key=lambda x: x[1].get('service_date', ""))
        for item_id, item_data in sorted_inventory:
            manufacturer = item_data['manufacturer']
            item_type = item_data['item_type']
            price = item_data.get('price', "")
            service_date = item_data.get('service_date', "")
            damaged = item_data['damaged']
            report += f"{item_id},{manufacturer},{item_type},{price},{service_date},{damaged}\n"

        return report

    def generate_damaged_inventory_report(self, inventory):
        """
        Generates the DamagedInventory.csv report.

        Parameters:
        inventory (dict): The inventory data.

        Returns:
        str: The report content.
        """
        report = "item ID,manufacturer name,item type,price,service date\n"

        sorted_inventory = sorted(inventory.items(), key=lambda x: float(x[1].get('price', 0)), reverse=True)
        for item_id, item_data in sorted_inventory:
            manufacturer = item_data['manufacturer']
            item_type = item_data['item_type']
            price = item_data.get('price', "")
            service_date = item_data.get('service_date', "")
            report += f"{item_id},{manufacturer},{item_type},{price},{service_date}\n"

        return report

# Example usage
manager = InventoryManager("ManufacturerList.csv", "PriceList.csv", "ServiceDatesList.csv")
inventory = manager.load_inventory()

full_inventory_report = manager.generate_full_inventory_report(inventory)
with open("FullInventory.csv", "w") as file:
    file.write(full_inventory_report)

item_type_reports = manager.generate_item_type_inventory_report(inventory)
for item_type, report in item_type_reports.items():
    file_name = f"{item_type}Inventory.csv"
    with open(file_name, "w") as file:
        file.write(report)

past_service_date_report = manager.generate_past_service_date_inventory_report(inventory)
with open("PastServiceDateInventory.csv", "w") as file:
    file.write(past_service_date_report)

damaged_inventory_report = manager.generate_damaged_inventory_report(inventory)
with open("DamagedInventory.csv", "w") as file:
    file.write(damaged_inventory_report)