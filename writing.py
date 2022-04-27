class Writing:
    def write_region(self, file_name, list_region):
        f = open(f"{file_name}.csv", "w+", encoding="utf-8")  # create/overwrite file (w+)
        for i in range(len(list_region)):
            f.write(f"{list_region[i]}\n")
        f.close()

    def write(self, file_name, list_name, list_location, list_price, list_url):
        f = open(f"{file_name}.csv", "a+", encoding="utf-8")  # open/create file and then append some item (a+)
        for i in range(len(list_name)):
            f.write(f"{list_name[i]};{list_location[i]};{list_price[i]};{list_url[i]}\n")
        f.close()

    def write_url(self, file_name, list_url):
        f = open(f"{file_name}.csv", "w+", encoding="utf-8")  # create/overwrite file (w+)
        for i in range(len(list_url)):
            f.write(f"{list_url[i]}\n")
        f.close()

    def write_detail(self, file_name, m_title, m_address, m_furnish, m_facilities, m_type, m_bfacilities, m_nearby):
        f = open(f"{file_name}.csv", "a+", encoding="utf-8")  # open/create file and then append some item (a+)
        f.write(f"{m_title};{m_address};{m_furnish};{m_facilities};{m_type};{m_bfacilities};{m_nearby}\n")
        f.close()
