from storage.DBProxy import DBProxy
from storage.DBPublisher import DBPublisher

def main():
    proxy = DBProxy()
    db = DBPublisher(proxy)


if __name__ == "__main__":
    main()